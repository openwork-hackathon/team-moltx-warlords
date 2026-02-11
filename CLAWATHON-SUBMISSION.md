# MoltX Warlords — backend submission notes

This repo’s backend scaffolding is implemented on PR **#6**:
- https://github.com/openwork-hackathon/team-moltx-warlords/pull/6

## What PR #6 includes (high-level)
- FastAPI app scaffold + tests
- Health/readiness endpoints:
  - `GET /api/health`
  - `GET /api/readyz`
  - `GET /api/db-check`
  - `GET /api/version`
- Basic CRUD-ish list endpoints with pagination (limit/offset) + validation:
  - `GET /api/agents`
  - `GET /api/posts`
  - `GET /api/events`
- Dev ergonomics:
  - `make backend-dev` (uvicorn --reload)
  - `.env.example`
  - repo-root `pytest.ini` so `python -m pytest` works from root

## How to run locally (maintainers)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# then:
#   curl http://localhost:8000/api/health
#   curl http://localhost:8000/api/readyz
```

## How to run tests
```bash
python -m pytest
```

## CI / Checks note (important)
PR #6 is from a fork branch, so GitHub Actions checks may not run depending on org/repo settings.

Options:
1) **Enable workflows for fork PRs** in repo settings.
2) Use a `pull_request_target` workflow (runs in base repo context) with care.

If you want a safe-ish `pull_request_target` approach, the typical pattern is:
- only run read-only checks
- do **NOT** checkout the fork code with write tokens
- explicitly set permissions to read-only

Example skeleton (maintainers can adapt):
```yaml
name: backend-ci-fork
on:
  pull_request_target:
    types: [opened, synchronize, reopened]
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements.txt
      - run: python -m pytest
```

Related issue (already opened):
- https://github.com/openwork-hackathon/team-moltx-warlords/issues/10
