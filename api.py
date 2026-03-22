"""Backend API for Library App.

This service supports two DB modes:
- Local SQLite (default)
- PostgreSQL via DATABASE_URL (Railway)

Mobile app talks to this API through db_adapter.py.
"""

import hashlib
import os
import re
import sqlite3
from urllib.parse import urlparse

from flask import Flask, jsonify, request

try:
    import pg8000.dbapi as pgdb
except Exception:  # pragma: no cover
    pgdb = None


app = Flask(__name__)

API_KEY = os.getenv("LIBRARY_API_KEY", "collage-project-4217").strip()
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:LaOEWdgPFEnQiGytKyaykfAfHDdaBQGY@caboose.proxy.rlwy.net:24267/railway",
).strip()
USE_POSTGRES = bool(DATABASE_URL)


def hash_password(password):
    return hashlib.sha256((password or "").encode()).hexdigest()


def _parse_database_url(url):
    parsed = urlparse(url)
    return {
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "database": (parsed.path or "").lstrip("/"),
    }


def _transform_sql_for_pg(query):
    """Translate sqlite-flavored SQL to Postgres-safe SQL."""
    q = query

    # Placeholder style: ? -> %s
    q = re.sub(r"\?", "%s", q)

    # SQLite-specific helpers
    q = re.sub(r"\bAUTOINCREMENT\b", "", q, flags=re.IGNORECASE)
    q = re.sub(r"\bINTEGER PRIMARY KEY\b", "SERIAL PRIMARY KEY", q, flags=re.IGNORECASE)

    # INSERT OR IGNORE / INSERT OR REPLACE
    q = re.sub(
        r"INSERT\s+OR\s+IGNORE\s+INTO",
        "INSERT INTO",
        q,
        flags=re.IGNORECASE,
    )
    q = re.sub(
        r"INSERT\s+OR\s+REPLACE\s+INTO",
        "INSERT INTO",
        q,
        flags=re.IGNORECASE,
    )

    # datetime('now') -> CURRENT_TIMESTAMP
    q = re.sub(r"datetime\('now'\)", "CURRENT_TIMESTAMP", q, flags=re.IGNORECASE)

    # datetime('now', '-N days') -> CURRENT_TIMESTAMP - INTERVAL 'N days'
    q = re.sub(
        r"datetime\('now'\s*,\s*'-(\d+)\s+days'\)",
        r"(CURRENT_TIMESTAMP - INTERVAL '\1 days')",
        q,
        flags=re.IGNORECASE,
    )

    # date('now', '-N days') -> CURRENT_DATE - INTERVAL 'N days'
    q = re.sub(
        r"date\('now'\s*,\s*'-(\d+)\s+days'\)",
        r"(CURRENT_DATE - INTERVAL '\1 days')",
        q,
        flags=re.IGNORECASE,
    )

    # date('now') -> CURRENT_DATE
    q = re.sub(r"date\('now'\)", "CURRENT_DATE", q, flags=re.IGNORECASE)

    # SQLite GLOB -> Postgres LIKE fallback
    q = re.sub(r"\bGLOB\b", "LIKE", q, flags=re.IGNORECASE)

    return q


def _as_json_rows(rows):
    # Convert tuples to plain lists for JSON serialization.
    return [list(r) if isinstance(r, (tuple, list)) else r for r in rows]


def _ensure_api_key():
    if not API_KEY:
        return None
    client_key = request.headers.get("X-Api-Key", "")
    if client_key != API_KEY:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    return None


def _sqlite_execute(query, params):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        is_read = (query or "").strip().lower().startswith(("select", "with", "pragma"))
        rows = cur.fetchall() if is_read else []
        conn.commit()
        return {
            "ok": True,
            "rows": _as_json_rows(rows),
            "rowcount": cur.rowcount,
            "lastrowid": cur.lastrowid,
        }
    finally:
        conn.close()


def _postgres_execute(query, params):
    if pgdb is None:
        return {"ok": False, "error": "pg8000 is not installed on server"}

    cfg = _parse_database_url(DATABASE_URL)
    if not cfg["database"]:
        return {"ok": False, "error": "Invalid DATABASE_URL"}

    transformed = _transform_sql_for_pg(query)
    conn = pgdb.connect(
        user=cfg["user"],
        password=cfg["password"],
        host=cfg["host"],
        port=cfg["port"],
        database=cfg["database"],
    )
    cur = conn.cursor()
    try:
        cur.execute(transformed, tuple(params))
        is_read = (query or "").strip().lower().startswith(("select", "with", "pragma"))
        rows = cur.fetchall() if is_read else []
        conn.commit()
        return {
            "ok": True,
            "rows": _as_json_rows(rows),
            "rowcount": cur.rowcount,
            "lastrowid": None,
        }
    except Exception as exc:
        conn.rollback()
        return {"ok": False, "error": str(exc)}
    finally:
        conn.close()


def run_sql(query, params):
    if USE_POSTGRES:
        return _postgres_execute(query, params)
    return _sqlite_execute(query, params)


@app.get("/api/health")
def health():
    return jsonify(
        {
            "ok": True,
            "service": "library-backend",
            "db_mode": "postgres" if USE_POSTGRES else "sqlite",
            "api_version": "2026-03-13-datetime-fix",
        }
    )


@app.post("/api/db/query")
def db_query():
    auth = _ensure_api_key()
    if auth:
        return auth

    payload = request.get_json(silent=True) or {}
    query = payload.get("query", "")
    params = payload.get("params", [])

    if not query:
        return jsonify({"ok": False, "error": "Missing SQL query"}), 400

    result = run_sql(query, params)
    code = 200 if result.get("ok") else 400
    return jsonify(result), code


@app.post("/api/db/execute")
def db_execute():
    # Same handler as /query, split path keeps adapter logic simple.
    return db_query()


@app.post("/api/auth/user-login")
def user_login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    if not username or not password:
        return jsonify({"ok": False, "error": "Username and password required"}), 400

    result = run_sql(
        "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
        [username, hash_password(password)],
    )
    if not result.get("ok"):
        return jsonify(result), 400

    rows = result.get("rows", [])
    if not rows:
        return jsonify({"ok": False, "error": "Invalid credentials"}), 401
    uid, uname = rows[0]
    return jsonify({"ok": True, "user": {"id": uid, "username": uname}})


@app.post("/api/auth/user-signup")
def user_signup():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    email = (payload.get("email") or "").strip() or None
    phone = (payload.get("phone") or "").strip() or None
    password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"ok": False, "error": "Username and password required"}), 400

    result = run_sql(
        "INSERT INTO users (username, password_hash, email, phone) VALUES (?, ?, ?, ?)",
        [username, hash_password(password), email, phone],
    )
    if not result.get("ok"):
        return jsonify(result), 400

    return jsonify({"ok": True, "user_id": result.get("lastrowid")})


@app.post("/api/auth/admin-login")
def admin_login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    if not username or not password:
        return jsonify({"ok": False, "error": "Username and password required"}), 400

    result = run_sql(
        "SELECT id, username FROM admins WHERE username = ? AND password_hash = ?",
        [username, hash_password(password)],
    )
    if not result.get("ok"):
        return jsonify(result), 400

    rows = result.get("rows", [])
    if not rows:
        return jsonify({"ok": False, "error": "Invalid credentials"}), 401
    aid, aname = rows[0]
    return jsonify({"ok": True, "admin": {"id": aid, "username": aname}})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
