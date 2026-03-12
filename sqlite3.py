"""
SQLite compatibility shim backed by PostgreSQL.

This project imports sqlite3 in many modules. To migrate quickly to Railway
PostgreSQL without rewriting every query, this module mirrors the minimal
sqlite3 API used by the app and translates common SQLite SQL patterns.
"""

import os
import re
from urllib.parse import urlparse

import pg8000.dbapi as _pg


# User requested fixed Railway credentials for this college project.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:DlOaWOSCsTSUQhdFdasYYJfyTBZOvThl@postgres.railway.internal:5432/railway",
)

IntegrityError = _pg.IntegrityError
OperationalError = _pg.OperationalError
DatabaseError = _pg.DatabaseError


def _parse_database_url(url):
    parsed = urlparse(url)
    return {
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "database": (parsed.path or "").lstrip("/"),
    }


def _convert_insert_or_replace(query):
    """Convert SQLite INSERT OR REPLACE INTO to PostgreSQL UPSERT."""
    if "INSERT OR REPLACE INTO" not in query.upper():
        return query

    pattern = re.compile(
        r"INSERT\s+OR\s+REPLACE\s+INTO\s+(\w+)\s*\((.*?)\)\s*VALUES\s*\((.*?)\)",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(query)
    if not match:
        return query

    table_name = match.group(1)
    columns_raw = match.group(2)
    values_raw = match.group(3)

    columns = [c.strip() for c in columns_raw.split(",") if c.strip()]
    if not columns:
        return query

    # Default to id conflict when present (works for this project's book imports).
    conflict_column = "id" if "id" in [c.lower() for c in columns] else columns[0]

    update_cols = [c for c in columns if c.lower() != conflict_column.lower()]
    set_clause = ", ".join(f"{c} = EXCLUDED.{c}" for c in update_cols)

    return (
        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values_raw}) "
        f"ON CONFLICT ({conflict_column}) DO UPDATE SET {set_clause}"
    )


def _transform_sql(query):
    q = query

    # Param placeholders
    q = q.replace("?", "%s")

    # Autoincrement syntax
    q = re.sub(
        r"INTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT",
        "SERIAL PRIMARY KEY",
        q,
        flags=re.IGNORECASE,
    )

    # SQLite date/datetime helpers
    q = re.sub(r"date\('now'\)", "CURRENT_DATE", q, flags=re.IGNORECASE)
    q = re.sub(
        r"datetime\('now',\s*'-([0-9]+)\s+days'\)",
        r"(NOW() - INTERVAL '\1 days')",
        q,
        flags=re.IGNORECASE,
    )

    # SQLite GLOB used for A-Z filter in dashboard subject query
    q = q.replace("subject GLOB '*[A-Za-z]*'", "subject ~ '[A-Za-z]'")

    # Insert-or-replace upsert
    q = _convert_insert_or_replace(q)

    return q


class Cursor:
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        sql = _transform_sql(query)
        if params is None:
            return self._cursor.execute(sql)
        return self._cursor.execute(sql, params)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        return self._cursor.close()


class Connection:
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return Cursor(self._conn.cursor())

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()


def connect(_db_name=None):
    """sqlite3.connect compatibility signature."""
    conf = _parse_database_url(DATABASE_URL)
    conn = _pg.connect(
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        database=conf["database"],
    )
    return Connection(conn)
