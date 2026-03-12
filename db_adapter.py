"""Database adapter that can use local SQLite or a remote HTTP backend.

Set `LIBRARY_API_URL` to enable remote mode.
When not set, this falls back to local `library.db`.
"""

import os
import sqlite3 as _sqlite3
from urllib.parse import urljoin
import json
from datetime import datetime, date

import requests


class RemoteDBError(Exception):
    """Raised when remote DB API calls fail."""


class RemoteCursor:
    def __init__(self, base_url, timeout):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._rows = []
        self._index = 0
        self.lastrowid = None
        self.rowcount = -1

    def execute(self, query, params=()):
        payload = {
            "query": query,
            "params": [self._to_json_value(p) for p in (list(params) if params else [])],
        }
        endpoint = "/api/db/query" if self._is_read_query(query) else "/api/db/execute"
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        headers = {"Content-Type": "application/json"}
        api_key = _get_api_key()
        if api_key:
            headers["X-Api-Key"] = api_key

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise RemoteDBError(f"Remote DB request failed: {exc}") from exc

        if not data.get("ok"):
            err = data.get("error", "Unknown remote DB error")
            if "UNIQUE constraint failed" in err or "duplicate key" in err.lower():
                raise _sqlite3.IntegrityError(err)
            raise RemoteDBError(err)

        self._rows = data.get("rows", [])
        self._index = 0
        self.lastrowid = data.get("lastrowid")
        self.rowcount = data.get("rowcount", len(self._rows))
        return self

    def executemany(self, query, seq_of_params):
        for item in seq_of_params:
            self.execute(query, item)
        return self

    def fetchone(self):
        if self._index >= len(self._rows):
            return None
        row = self._rows[self._index]
        self._index += 1
        return tuple(row) if isinstance(row, (list, tuple)) else row

    def fetchall(self):
        if self._index == 0:
            rows = self._rows
        else:
            rows = self._rows[self._index :]
            self._index = len(self._rows)
        return [tuple(r) if isinstance(r, (list, tuple)) else r for r in rows]

    def close(self):
        self._rows = []
        self._index = 0

    @staticmethod
    def _is_read_query(query):
        q = (query or "").strip().lower()
        return q.startswith("select") or q.startswith("with") or q.startswith("pragma")

    @staticmethod
    def _to_json_value(value):
        if isinstance(value, (datetime, date)):
            return value.isoformat(sep=" ") if isinstance(value, datetime) else value.isoformat()
        return value


class RemoteConnection:
    def __init__(self, base_url, timeout=20):
        self.base_url = base_url
        self.timeout = timeout

    def cursor(self):
        return RemoteCursor(self.base_url, self.timeout)

    def commit(self):
        # Remote API applies writes immediately per statement.
        return None

    def close(self):
        return None


def _get_api_key():
    env_key = os.getenv("LIBRARY_API_KEY", "").strip()
    if env_key:
        return env_key
    try:
        with open("data/app_settings.json", "r", encoding="utf-8") as fh:
            settings = json.load(fh)
            return (settings.get("api_key") or "").strip()
    except Exception:
        return ""


def connect(database="library.db", timeout=20):
    """Connect to local sqlite or remote backend based on env config."""
    api_url = os.getenv("LIBRARY_API_URL", "").strip()
    if not api_url:
        try:
            with open("data/app_settings.json", "r", encoding="utf-8") as fh:
                settings = json.load(fh)
                api_url = (settings.get("api_base_url") or "").strip()
        except Exception:
            api_url = ""
    if api_url:
        return RemoteConnection(api_url, timeout=timeout)
    return _sqlite3.connect(database)


class _SQLite3Proxy:
    IntegrityError = _sqlite3.IntegrityError
    OperationalError = _sqlite3.OperationalError
    DatabaseError = _sqlite3.DatabaseError

    @staticmethod
    def connect(database="library.db"):
        return connect(database=database)


sqlite3 = _SQLite3Proxy()
