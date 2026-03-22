"""Migrate local SQLite data from library.db into Railway PostgreSQL.

Run this where the Railway internal hostname is reachable.
"""

import importlib
import os
import sys
import sysconfig
import socket
from urllib.parse import urlparse

import pg8000.dbapi

from database import Database

RAILWAY_DATABASE_URL = (
    "postgresql://postgres:LaOEWdgPFEnQiGytKyaykfAfHDdaBQGY"
    "@caboose.proxy.rlwy.net:24267/railway"
)

SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")


def get_target_database_url():
    """Prefer env override so local migration can use Railway public URL."""
    return os.getenv("DATABASE_URL", RAILWAY_DATABASE_URL)


def validate_hostname_reachable(db_url):
    parsed = urlparse(db_url)
    host = parsed.hostname
    if not host:
        raise ValueError("Invalid DATABASE_URL: missing host")

    try:
        socket.getaddrinfo(host, parsed.port or 5432)
    except socket.gaierror as exc:
        if host.endswith("railway.internal"):
            raise RuntimeError(
                "Hostname 'postgres.railway.internal' is Railway-private and cannot be used from local PC. "
                "Set DATABASE_URL to your Railway PUBLIC Postgres URL and run again."
            ) from exc
        raise RuntimeError(
            f"Cannot resolve database host '{host}'. Check DATABASE_URL."
        ) from exc


def load_stdlib_sqlite3():
    """Load stdlib sqlite3 even though the project has a local sqlite3.py shim."""
    stdlib_path = sysconfig.get_paths()["stdlib"]
    project_root = os.path.dirname(__file__)

    removed_paths = []
    for path in ("", project_root):
        while path in sys.path:
            sys.path.remove(path)
            removed_paths.append(path)

    existing_sqlite3 = sys.modules.pop("sqlite3", None)

    # Ensure stdlib has priority while importing sqlite3.
    sys.path.insert(0, stdlib_path)

    try:
        module = importlib.import_module("sqlite3")
    finally:
        if stdlib_path in sys.path:
            sys.path.remove(stdlib_path)
        for path in removed_paths:
            sys.path.insert(0, path)
        if existing_sqlite3 is not None:
            sys.modules["sqlite3"] = existing_sqlite3

    return module


def parse_database_url(url):
    parsed = urlparse(url)
    return {
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "database": (parsed.path or "").lstrip("/"),
    }


def get_sqlite_tables(sqlite_conn):
    cursor = sqlite_conn.cursor()
    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )
    return [row[0] for row in cursor.fetchall()]


def get_sqlite_columns(sqlite_conn, table):
    cursor = sqlite_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cursor.fetchall()]


def get_postgres_columns(pg_cursor, table):
    pg_cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table,),
    )
    return [row[0] for row in pg_cursor.fetchall()]


def migrate_table(sqlite_conn, pg_conn, table):
    sqlite_columns = get_sqlite_columns(sqlite_conn, table)

    pg_cursor = pg_conn.cursor()
    postgres_columns = get_postgres_columns(pg_cursor, table)

    if not postgres_columns:
        print(f"- Skipping {table}: table does not exist in PostgreSQL")
        return 0

    common_columns = [col for col in sqlite_columns if col in postgres_columns]
    if not common_columns:
        print(f"- Skipping {table}: no common columns")
        return 0

    cols_sql = ", ".join(common_columns)
    placeholders = ", ".join(["%s"] * len(common_columns))

    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute(f"SELECT {cols_sql} FROM {table}")
    rows = sqlite_cursor.fetchall()

    pg_cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")

    if rows:
        pg_cursor.executemany(
            f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholders})",
            rows,
        )

    pg_conn.commit()
    print(f"- Migrated {table}: {len(rows)} rows")
    return len(rows)


def sync_table_sequence(pg_conn, table):
    """Align SERIAL sequence with max(id) after bulk inserts."""
    pg_cursor = pg_conn.cursor()

    try:
        pg_cursor.execute("SELECT pg_get_serial_sequence(%s, 'id')", (table,))
        sequence_row = pg_cursor.fetchone()
        sequence_name = sequence_row[0] if sequence_row else None
        if not sequence_name:
            return

        pg_cursor.execute(f"SELECT COALESCE(MAX(id), 0) FROM {table}")
        max_id = pg_cursor.fetchone()[0] or 0

        if max_id > 0:
            pg_cursor.execute(
                "SELECT setval(%s::regclass, %s, true)",
                (sequence_name, max_id),
            )
        else:
            pg_cursor.execute(
                "SELECT setval(%s::regclass, 1, false)",
                (sequence_name,),
            )

        pg_conn.commit()
    except Exception:
        pg_conn.rollback()


def main():
    if not os.path.exists(SQLITE_DB_PATH):
        raise FileNotFoundError(f"SQLite file not found: {SQLITE_DB_PATH}")

    sqlite3_std = load_stdlib_sqlite3()
    sqlite_conn = sqlite3_std.connect(SQLITE_DB_PATH)

    database_url = get_target_database_url()
    validate_hostname_reachable(database_url)

    # Keep Database() module and sqlite3 shim aligned to the same target URL.
    os.environ["DATABASE_URL"] = database_url

    # Ensure PostgreSQL schema exists before copying data.
    Database().create_tables()

    conf = parse_database_url(database_url)
    pg_conn = pg8000.dbapi.connect(
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        database=conf["database"],
    )

    total_rows = 0
    tables = get_sqlite_tables(sqlite_conn)
    print(f"Found {len(tables)} SQLite tables")

    for table in tables:
        total_rows += migrate_table(sqlite_conn, pg_conn, table)
        sync_table_sequence(pg_conn, table)

    sqlite_conn.close()
    pg_conn.close()

    print(f"Migration complete. Total rows migrated: {total_rows}")


if __name__ == "__main__":
    main()
