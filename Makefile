.PHONY: sync test run

sync:
	uv sync --dev

test:
	./scripts/test.sh

run:
	uv run bronto-mcp
