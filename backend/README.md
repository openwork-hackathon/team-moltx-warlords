# Backend - MoltX Warlords

## Stack
- Python 3.10+
- FastAPI
- Supabase
- OpenClaw Framework

## Setup (local venv)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

uvicorn app.main:app --reload --port 8000
# then: curl http://127.0.0.1:8000/health
```

### Env vars

- `ENV` (default: `dev`)
- `CORS_ORIGINS` (comma-separated, e.g. `http://localhost:5173,http://127.0.0.1:5173`)

## Setup (Docker)
```bash
# from repo root
docker build -t moltx-backend ./backend
docker run --rm -p 8000:8000 moltx-backend
# then: curl http://127.0.0.1:8000/health
```

## Endpoints
- `GET /` → basic service info + links to `/docs` + `/openapi.json`
- `GET /health` → `{ ok: true }` (stable)
- `GET /healthz` or `GET /api/healthz` → includes env + timestamp
- `GET /api/version`
