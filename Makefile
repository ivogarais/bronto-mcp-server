.PHONY: sync test run run-stdio run-http

sync:
	uv sync --dev

test:
	./scripts/test.sh

run:
	uv run bronto-mcp

run-stdio:
	BRONTO_MCP_TRANSPORT=stdio uv run bronto-mcp

run-http:
	BRONTO_MCP_TRANSPORT=streamable-http uv run bronto-mcp
