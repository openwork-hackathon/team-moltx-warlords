PY ?= python3
PIP ?= pip3

.PHONY: help backend-install backend-test backend-lint backend-format backend-format-check

help:
	@echo "Targets:"
	@echo "  backend-install       Install backend deps (incl dev)"
	@echo "  backend-test          Run backend tests"
	@echo "  backend-lint          Run ruff lint"
	@echo "  backend-format        Format code with ruff"
	@echo "  backend-format-check  Check formatting (CI-style)"

backend-install:
	$(PY) -m pip install --upgrade pip
	$(PIP) install -r backend/requirements.txt
	$(PIP) install -r backend/requirements-dev.txt

backend-test:
	cd backend && PYTHONPATH=. $(PY) -m pytest -q

backend-lint:
	cd backend && $(PY) -m ruff check .

backend-format:
	cd backend && $(PY) -m ruff format .

backend-format-check:
	cd backend && $(PY) -m ruff format --check .
