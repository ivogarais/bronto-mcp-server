import pytest

from bronto.config import Config, MCPTransport


def test_default_transport_is_stdio(monkeypatch):
    monkeypatch.delenv("BRONTO_MCP_TRANSPORT", raising=False)

    config = Config()

    assert config.mcp_transport is MCPTransport.STDIO


def test_transport_accepts_streamable_http(monkeypatch):
    monkeypatch.setenv("BRONTO_MCP_TRANSPORT", "streamable-http")

    config = Config()

    assert config.mcp_transport is MCPTransport.STREAMABLE_HTTP


def test_invalid_transport_raises_value_error(monkeypatch):
    monkeypatch.setenv("BRONTO_MCP_TRANSPORT", "http")

    with pytest.raises(ValueError, match="Unsupported BRONTO_MCP_TRANSPORT"):
        Config()


def test_port_parses_to_int(monkeypatch):
    monkeypatch.setenv("BRONTO_MCP_PORT", "9001")

    config = Config()

    assert config.mcp_port == 9001


def test_invalid_port_raises_value_error(monkeypatch):
    monkeypatch.setenv("BRONTO_MCP_PORT", "port")

    with pytest.raises(ValueError, match="Invalid BRONTO_MCP_PORT"):
        Config()
