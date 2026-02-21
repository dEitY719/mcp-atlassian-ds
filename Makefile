.PHONY: sync-internal sync-external test-internal test-external help

help:
	@echo "Available commands:"
	@echo ""
	@echo "  Internal (Samsung DS - Artifactory):"
	@echo "    make sync-internal      - Install dependencies from Artifactory"
	@echo "    make test-internal      - Run tests with internal environment"
	@echo ""
	@echo "  External (Public PyPI):"
	@echo "    make sync-external      - Install dependencies from public PyPI"
	@echo "    make test-external      - Run tests with external environment"
	@echo ""

# Internal environment (Samsung DS Artifactory)
sync-internal:
	uv sync

test-internal:
	uv run pytest tests/ -v

# External environment (Public PyPI)
sync-external:
	uv sync --project pyproject.external.toml

test-external:
	uv run --project pyproject.external.toml pytest tests/ -v
