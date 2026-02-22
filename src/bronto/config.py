import os
from enum import Enum


class MCPTransport(str, Enum):
    STDIO = "stdio"
    STREAMABLE_HTTP = "streamable-http"


class Config:
    def __init__(self):
        self.bronto_api_key = self._require_non_empty_env("BRONTO_API_KEY")
        self.bronto_api_endpoint = self._require_non_empty_env("BRONTO_API_ENDPOINT")
        self.mcp_transport = self._parse_transport(
            os.environ.get("BRONTO_MCP_TRANSPORT", MCPTransport.STDIO.value)
        )
        self.mcp_host = os.environ.get("BRONTO_MCP_HOST", "127.0.0.1")
        self.mcp_port = self._parse_port(os.environ.get("BRONTO_MCP_PORT", "8000"))
        self.mcp_streamable_http_path = os.environ.get(
            "BRONTO_MCP_STREAMABLE_HTTP_PATH", "/"
        )

    @staticmethod
    def _parse_transport(raw_transport: str) -> MCPTransport:
        try:
            return MCPTransport(raw_transport.lower())
        except ValueError as e:
            accepted_values = ", ".join(item.value for item in MCPTransport)
            raise ValueError(
                f'Unsupported BRONTO_MCP_TRANSPORT "{raw_transport}". '
                f"Accepted values: {accepted_values}"
            ) from e

    @staticmethod
    def _parse_port(raw_port: str) -> int:
        try:
            port = int(raw_port)
        except ValueError as e:
            raise ValueError(
                f'Invalid BRONTO_MCP_PORT "{raw_port}". Expected an integer.'
            ) from e
        if port < 1 or port > 65535:
            raise ValueError(
                f'Invalid BRONTO_MCP_PORT "{raw_port}". Expected a value between 1 and 65535.'
            )
        return port

    @staticmethod
    def _require_non_empty_env(env_name: str) -> str:
        raw_value = os.environ.get(env_name)
        if raw_value is None or raw_value.strip() == "":
            raise ValueError(f"{env_name} is required and cannot be empty.")
        return raw_value.strip()
