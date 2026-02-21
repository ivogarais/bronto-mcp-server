# Bronto MCP Server

This project contains an MCP server for Bronto. 

It currently provides tools for models to access details on Bronto datasets, top-keys as well as event and statistical 
searches. When these tools are provided to an AI agent, they make it possible to answer questions such as

_Can you please provide some log events from datasets in the ingestion collection, except for the ones related to garbage collection? The data should be between "2025-05-10 16:05:45" and "2025-05-10 16:25:05"._


## Installation

Check out this project, then use `uv` to create a project-local virtual environment and install dependencies.

```shell
uv venv .venv
uv sync --dev
```

## Configuration

This MCP server is configured using environment variables:

- `BRONTO_API_KEY`: a Bronto API key
- `BRONTO_API_ENDPOINT`: a Bronto API endpoint, e.g. https://api.eu.staging.bronto.io
- `BRONTO_MCP_TRANSPORT`: MCP transport mode (`stdio` or `streamable-http`). Defaults to `stdio`.
- `BRONTO_MCP_HOST`: host used for HTTP transport. Defaults to `127.0.0.1`.
- `BRONTO_MCP_PORT`: port used for HTTP transport. Defaults to `8000`.
- `BRONTO_MCP_STREAMABLE_HTTP_PATH`: HTTP path used for streamable HTTP mode. Defaults to `/`.


## Usage

To run the MCP server in local `stdio` mode (recommended default for broad client compatibility):
```shell
BRONTO_API_KEY=<API KEY HERE> \
BRONTO_API_ENDPOINT=https://api.eu.bronto.io \
make run
```

To run the MCP server in `streamable-http` mode:
```shell
BRONTO_API_KEY=<API KEY HERE> \
BRONTO_API_ENDPOINT=https://api.eu.bronto.io \
BRONTO_MCP_TRANSPORT=streamable-http \
BRONTO_MCP_HOST=127.0.0.1 \
BRONTO_MCP_PORT=8000 \
BRONTO_MCP_STREAMABLE_HTTP_PATH=/ \
make run-http
```

To run tests and coverage:
```shell
make test
```

This MCP server should work with any agent that supports MCP. However, it has only been tested with Claude Code.

Finally, in order to configure Claude Code so that it uses the Bronto MCP server in HTTP mode, simply run 
```json
claude mcp add --transport http bronto http://localhost:8000
```
Note: this will make the Bronto MCP server available to your current project/folder. If you wish to make the server 
available globally, simply add `--scope user` to the command above. Details on how to manage MCP servers with 
Claude Code can be found at https://docs.anthropic.com/en/docs/claude-code/mcp

Then launch Claude Code and run the `/mcp` command to check that the Bronto MCP server is available and that Claude Code 
was able to connect to it. 
