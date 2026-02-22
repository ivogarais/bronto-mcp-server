import pytest

from bronto.config import Config, MCPTransport


@pytest.fixture(autouse=True)
def base_env(monkeypatch):
    monkeypatch.setenv("BRONTO_API_KEY", "test-api-key")
    monkeypatch.setenv("BRONTO_API_ENDPOINT", "https://api.eu.bronto.io")


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


def test_out_of_range_port_raises_value_error(monkeypatch):
    monkeypatch.setenv("BRONTO_MCP_PORT", "70000")

    with pytest.raises(ValueError, match="between 1 and 65535"):
        Config()


def test_missing_api_key_raises_value_error(monkeypatch):
    monkeypatch.delenv("BRONTO_API_KEY", raising=False)

    with pytest.raises(ValueError, match="BRONTO_API_KEY is required"):
        Config()


def test_missing_endpoint_raises_value_error(monkeypatch):
    monkeypatch.delenv("BRONTO_API_ENDPOINT", raising=False)

    with pytest.raises(ValueError, match="BRONTO_API_ENDPOINT is required"):
        Config()


def test_empty_endpoint_raises_value_error(monkeypatch):
    monkeypatch.setenv("BRONTO_API_ENDPOINT", "   ")

    with pytest.raises(ValueError, match="BRONTO_API_ENDPOINT is required"):
        Config()
