# Backend review / merge checklist (PR #6)

This PR adds a small FastAPI backend skeleton with basic endpoints, tests, and local dev tooling.

## Quick local verify (no CI required)

```bash
# from repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python -m pytest
```

## Run the backend (local)

Option A (recommended):

```bash
make backend-dev
# serves on http://localhost:8000
```

Option B:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## Smoke endpoints

```bash
curl -s http://localhost:8000/api/health | jq
curl -s http://localhost:8000/api/readyz | jq
curl -s http://localhost:8000/api/db-check | jq
curl -s http://localhost:8000/api/version | jq
```

## Notes on CI for fork PRs

If GitHub Actions checks don't appear on this PR, it may be due to fork-workflow restrictions.
See Issue #10 for maintainer options to enable/approve Actions runs.
