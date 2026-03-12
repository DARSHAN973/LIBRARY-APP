# Backend Connection Guide

This app is now wired to use a backend API for all SQL calls.

## How it works

- App code still runs SQL (`SELECT`, `INSERT`, `UPDATE`) as before.
- `db_adapter.py` intercepts `sqlite3.connect(...)`.
- If `LIBRARY_API_URL` (or `data/app_settings.json -> api_base_url`) is set:
  - SQL is sent to backend over HTTP:
    - `POST /api/db/query`
    - `POST /api/db/execute`
- If no API URL is set:
  - App uses local `library.db` (offline mode).

## Files added/updated

- `db_adapter.py` : local/remote DB adapter used by app modules
- `api.py` : Flask backend API with SQL proxy + auth endpoints
- `requirements.txt` : includes `Flask`, `gunicorn`, `pg8000`
- `data/app_settings.json` : includes `api_base_url` and `api_key`

## Deploy backend on Railway

1. Ensure these files are in repo root:
   - `api.py`
   - `requirements.txt`
   - `Procfile`

2. Create `Procfile`:

```txt
web: gunicorn api:app
```

3. In Railway set env vars:
   - `DATABASE_URL` = Railway Postgres URL (auto provided by Railway Postgres plugin)
   - `LIBRARY_API_KEY` = any strong secret string (optional but recommended)

4. Deploy and copy public URL, for example:
   - `https://your-service.up.railway.app`

## Configure mobile app to use backend

Set in `data/app_settings.json`:

```json
{
  "items_per_page": 10,
  "api_base_url": "https://your-service.up.railway.app",
  "api_key": "your-secret-key"
}
```

or set env vars before app launch:

```bash
export LIBRARY_API_URL="https://your-service.up.railway.app"
export LIBRARY_API_KEY="your-secret-key"
python main.py
```

## API endpoints

- `GET /api/health`
- `POST /api/db/query`
- `POST /api/db/execute`
- `POST /api/auth/user-login`
- `POST /api/auth/user-signup`
- `POST /api/auth/admin-login`

## Quick test

```bash
curl https://your-service.up.railway.app/api/health
```

Expected response includes `"ok": true` and `"db_mode": "postgres"` on Railway.
