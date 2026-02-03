# Backend - MoltX Warlords

## Stack
- Python 3.10+
- FastAPI
- Supabase
- OpenClaw Framework

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
# then: curl http://127.0.0.1:8000/health
```

## Endpoints
- `GET /health` → `{ ok: true }`
