import os
from enum import Enum


class MCPTransport(str, Enum):
    STDIO = "stdio"
    STREAMABLE_HTTP = "streamable-http"


class Config:
    def __init__(self):
        self.bronto_api_key = os.environ.get("BRONTO_API_KEY")
        self.bronto_api_endpoint = os.environ.get(
            "BRONTO_API_ENDPOINT", "https://api.eu.bronto.io"
        )
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
            return int(raw_port)
        except ValueError as e:
            raise ValueError(
                f'Invalid BRONTO_MCP_PORT "{raw_port}". Expected an integer.'
            ) from e
