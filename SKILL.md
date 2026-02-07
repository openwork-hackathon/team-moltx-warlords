# Skill: team-moltx-warlords (Clawathon)

This repo is the Clawathon project **MoltX-Warlords**.

## What to do (quick targets)
- Keep backend clean: **tests + ruff lint/format** passing.
- Ship small, reviewable increments (docs, env validation, endpoints, CI fixes).

## Repo layout
- `backend/` — FastAPI service + tests
- `frontend/` — Next.js app
- `contracts/` — Solidity / Base-related contracts

## Fast local loop (backend)
From repo root:

```bash
make backend-install
make backend-test
make backend-lint
make backend-format
```

## CI-style checks
```bash
make backend-format-check
make backend-lint
make backend-test
```

## Environment
- Start from `.env.example` and create `.env` (do **not** commit secrets).
- If a setting is required for local run/tests, prefer adding it to `.env.example` with a safe placeholder and documenting it here.

## Contribution workflow (recommended)
1. Create a branch: `git checkout -b ty/<topic>`
2. Make a small change set.
3. Run: `make backend-format-check backend-lint backend-test`
4. Commit with a scoped message: `docs: ...`, `backend: ...`, `ci: ...`
5. Push to fork and open PR to upstream.

## PR checklist
- [ ] Tests pass (`make backend-test`)
- [ ] Lint/format pass (`make backend-lint`, `make backend-format-check`)
- [ ] Any new config is reflected in `.env.example`
- [ ] README/SKILL docs updated if behavior changed
