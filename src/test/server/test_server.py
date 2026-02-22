from types import SimpleNamespace
from unittest.mock import Mock

import bronto.server as server
from bronto.config import MCPTransport


def _setup_server_test_doubles(monkeypatch, transport: MCPTransport):
    config = SimpleNamespace(
        bronto_api_key="api-key",
        bronto_api_endpoint="https://api.example.bronto.io",
        mcp_transport=transport,
        mcp_host="127.0.0.1",
        mcp_port=9001,
        mcp_streamable_http_path="/mcp",
    )
    registry = Mock()
    registry.build_instructions.return_value = "agent instructions"

    bootstrap_mock = Mock()
    fast_mcp_instance = Mock()
    fast_mcp_constructor = Mock(return_value=fast_mcp_instance)
    bronto_client_instance = Mock()
    bronto_client_constructor = Mock(return_value=bronto_client_instance)
    runtime_instance = Mock()
    runtime_constructor = Mock(return_value=runtime_instance)
    logger_mock = Mock()

    monkeypatch.setattr(server, "bootstrap_logging", bootstrap_mock)
    monkeypatch.setattr(server, "Config", Mock(return_value=config))
    monkeypatch.setattr(server, "build_agent_registry", Mock(return_value=registry))
    monkeypatch.setattr(server, "FastMCP", fast_mcp_constructor)
    monkeypatch.setattr(server, "BrontoClient", bronto_client_constructor)
    monkeypatch.setattr(server, "BrontoRuntime", runtime_constructor)
    monkeypatch.setattr(server, "logger", logger_mock)

    return (
        config,
        registry,
        bootstrap_mock,
        fast_mcp_constructor,
        fast_mcp_instance,
        bronto_client_constructor,
        bronto_client_instance,
        runtime_constructor,
        runtime_instance,
        logger_mock,
    )


def test_main_bootstraps_runtime_and_runs_stdio(monkeypatch):
    (
        config,
        registry,
        bootstrap_mock,
        fast_mcp_constructor,
        fast_mcp_instance,
        bronto_client_constructor,
        bronto_client_instance,
        runtime_constructor,
        runtime_instance,
        logger_mock,
    ) = _setup_server_test_doubles(monkeypatch, MCPTransport.STDIO)

    server.main()

    bootstrap_mock.assert_called_once_with()
    fast_mcp_constructor.assert_called_once()
    assert fast_mcp_constructor.call_args.args == ("Bronto",)
    assert fast_mcp_constructor.call_args.kwargs["host"] == config.mcp_host
    assert fast_mcp_constructor.call_args.kwargs["port"] == config.mcp_port
    assert fast_mcp_constructor.call_args.kwargs["streamable_http_path"] == "/mcp"
    assert (
        fast_mcp_constructor.call_args.kwargs["instructions"]
        == registry.build_instructions.return_value
    )
    assert fast_mcp_constructor.call_args.kwargs["dependencies"] == ["pydantic"]
    bronto_client_constructor.assert_called_once_with(
        config.bronto_api_key, config.bronto_api_endpoint
    )
    runtime_constructor.assert_called_once_with(bronto_client_instance, registry)
    runtime_instance.register.assert_called_once_with(fast_mcp_instance)
    fast_mcp_instance.run.assert_called_once_with(transport="stdio")
    logger_mock.info.assert_any_call(
        "Starting Bronto MCP server, transport=%s", "stdio"
    )
    logger_mock.info.assert_any_call("Bronto tools registered successfully")


def test_main_logs_http_listener_for_streamable_http_transport(monkeypatch):
    (
        config,
        _registry,
        _bootstrap_mock,
        _fast_mcp_constructor,
        fast_mcp_instance,
        _bronto_client_constructor,
        _bronto_client_instance,
        _runtime_constructor,
        _runtime_instance,
        logger_mock,
    ) = _setup_server_test_doubles(monkeypatch, MCPTransport.STREAMABLE_HTTP)

    server.main()

    fast_mcp_instance.run.assert_called_once_with(transport="streamable-http")
    logger_mock.info.assert_any_call(
        "Listening on http://%s:%s%s",
        config.mcp_host,
        config.mcp_port,
        config.mcp_streamable_http_path,
    )
