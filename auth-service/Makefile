# =======================================
# Auth Service Makefile (UV-based workflow)
# =======================================

.PHONY: start test test-unit test-integration test-e2e test-health coverage lint lint-fix format typecheck precommit

# Start the FastAPI server
start:
	uv run uvicorn app.main:app --reload --port 8001

# Run all tests
test:
	uv run pytest

# Run only unit tests
test-unit:
	uv run pytest app/tests/unit/

# Run only integration tests
test-integration:
	uv run pytest app/tests/integration/

# Run only end-to-end (e2e) tests
test-e2e:
	uv run pytest app/tests/e2e/

# Run only health endpoint test
test-health:
	uv run pytest app/tests/unit/test_health.py

# Run tests with coverage report
coverage:
	uv run pytest --cov=app --cov-report=term-missing

# Lint the code using ruff
lint:
	uv run ruff check app

# Automatically fix lint issues
lint-fix:
	uv run ruff check app --fix

# Format code using black and sort imports with isort
format:
	@uv run black . || (uv add --dev black && uv run black .)
	@uv run isort . || (uv add --dev isort && uv run isort .)

# Type checking with mypy
typecheck:
	uv run mypy app

# Run pre-commit hooks
precommit:
	uv run pre-commit run --all-files
