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

uvicorn app.main:app --reload --port 8000
# then: curl http://127.0.0.1:8000/health
```

## Setup (Docker)
```bash
# from repo root
docker build -t moltx-backend ./backend
docker run --rm -p 8000:8000 moltx-backend
# then: curl http://127.0.0.1:8000/health
```

## Endpoints
- `GET /health` → `{ ok: true }`
