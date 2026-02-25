RUNNAME := mcp-atlassian-jira
SKIP_CONFLUENCE ?= 0
USE_REAL_DATA ?= 0

.PHONY: sync-internal sync-external test-internal test-internal-jira test-external test-external-jira sync test run stop build push help

## Dependency Management
## sync-internal: Install dependencies from Artifactory (사내)
## Note: --native-tls is required for internal SSL certificate verification
## Uses system's native TLS instead of Python's bundled CA certificates
sync-internal:
	UV_EXTRA_INDEX_URL="https://repo.samsungds.net/artifactory/api/pypi/pypi-remote/simple" uv sync --native-tls

## sync-external: Install dependencies from public PyPI
sync-external:
	@echo "Creating external environment (.venv.external)..."
	rm -rf .venv.external
	python3 -m venv .venv.external
	.venv.external/bin/pip install --upgrade pip setuptools wheel
	.venv.external/bin/pip install -e .
	.venv.external/bin/pip install pytest pytest-cov pytest-asyncio

## Testing
## test-internal: Run tests with internal environment (USE_REAL_DATA=1 for API validation)
test-internal:
	uv run pytest tests/ -v \
		$(if $(filter 1,$(SKIP_CONFLUENCE)),--skip-confluence) \
		$(if $(filter 1,$(USE_REAL_DATA)),--use-real-data)

## test-internal-jira: Run Jira tests only (skip Confluence, USE_REAL_DATA=1 for API validation)
test-internal-jira:
	uv run pytest tests/ -v --skip-confluence \
		$(if $(filter 1,$(USE_REAL_DATA)),--use-real-data)

## test-external: Run tests with external environment (USE_REAL_DATA=1 for API validation)
test-external:
	.venv.external/bin/pytest tests/ -v \
		$(if $(filter 1,$(SKIP_CONFLUENCE)),--skip-confluence) \
		$(if $(filter 1,$(USE_REAL_DATA)),--use-real-data)

## test-external-jira: Run Jira tests only (skip Confluence, USE_REAL_DATA=1 for API validation)
test-external-jira:
	.venv.external/bin/pytest tests/ -v --skip-confluence \
		$(if $(filter 1,$(USE_REAL_DATA)),--use-real-data)

## sync: Install dependencies (alias for sync-internal)
sync: sync-internal

## test: Run tests (alias for test-internal). Options: SKIP_CONFLUENCE=1, USE_REAL_DATA=1
## Examples:
##   make test                                 # Run all tests (skip real API validation)
##   make test SKIP_CONFLUENCE=1               # Run Jira tests only
##   make test USE_REAL_DATA=1                 # Run all tests including API validation (requires credentials)
##   make test SKIP_CONFLUENCE=1 USE_REAL_DATA=1  # Run Jira + API validation
test: test-internal

## Docker Container Management
## run: run container
run:
	docker run --rm -p 9000:9000 -d --env-file ./.env --name ${RUNNAME} cr.aidev.samsungds.net/mcp-images/mcp-atlassian-jira:latest --transport streamable-http --port 9000

## stop: stop container
stop:
	docker stop ${RUNNAME}

## build: build container
build:
	docker build --no-cache -f Dockerfile -t cr.aidev.samsungds.net/mcp-images/mcp-atlassian-jira:latest .

## push: push container
push:
	docker push cr.aidev.samsungds.net/mcp-images/mcp-atlassian-jira:latest

## help: show this help info
help: Makefile
	@printf "\n\033[1mUsage: make <TARGETS> ...\033[0m\n\n\033[1mTargets:\033[0m\n\n"
	@sed -n 's/^##//p' $< | awk -F':' '{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort | sed -e 's/^/ /'

.DEFAULT:
	@$(MAKE) --no-print-directory help

.DEFAULT_GOAL := help
