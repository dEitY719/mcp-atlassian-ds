RUNNAME := mcp-atlassian-jira

.PHONY: sync-internal sync-external test-internal test-external sync test run stop build push help

## Dependency Management
## sync-internal: Install dependencies from Artifactory
sync-internal:
	uv sync

## sync-external: Install dependencies from public PyPI
sync-external:
	@echo "Creating external environment (.venv.external)..."
	rm -rf .venv.external
	python3 -m venv .venv.external
	.venv.external/bin/pip install --upgrade pip setuptools wheel
	.venv.external/bin/pip install -e .
	.venv.external/bin/pip install pytest pytest-cov pytest-asyncio

## Testing
## test-internal: Run tests with internal environment
test-internal:
	uv run pytest tests/ -v

## test-external: Run tests with external environment
test-external:
	.venv.external/bin/pytest tests/ -v

## sync: Install dependencies (alias for sync-internal)
sync: sync-internal

## test: Run tests (alias for test-internal)
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
