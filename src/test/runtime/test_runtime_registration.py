from unittest.mock import Mock

import pytest

from bronto.agents.base import AgentToolSpec, BrontoAgent, BrontoAgentRegistry
from bronto.clients import BrontoClient
from bronto.runtime import BrontoRuntime


class FakeMCP:
    def __init__(self):
        self.registered = {}

    def tool(self, name, description):
        def decorator(handler):
            self.registered[name] = {
                "description": description,
                "handler_name": handler.__name__,
            }
            return handler

        return decorator


def test_runtime_init_requires_non_empty_registry():
    client = Mock(spec=BrontoClient)
    empty_registry = BrontoAgentRegistry(agents=[])

    with pytest.raises(ValueError, match="agent_registry must include at least one agent"):
        BrontoRuntime(client, empty_registry)


def test_runtime_register_registers_all_tools():
    registry = BrontoAgentRegistry(
        agents=[
            BrontoAgent(
                name="datasets",
                description="datasets agent",
                tools=[
                    AgentToolSpec(
                        name="get_datasets",
                        handler="get_datasets",
                        description="gets datasets",
                    )
                ],
            )
        ]
    )
    client = Mock(spec=BrontoClient)
    runtime = BrontoRuntime(client, registry)
    mcp = FakeMCP()

    runtime.register(mcp)

    assert "get_datasets" in mcp.registered
    assert mcp.registered["get_datasets"]["description"] == "gets datasets"
    assert mcp.registered["get_datasets"]["handler_name"] == "get_datasets"


def test_runtime_register_fails_when_handler_missing():
    registry = BrontoAgentRegistry(
        agents=[
            BrontoAgent(
                name="broken",
                description="broken agent",
                tools=[
                    AgentToolSpec(
                        name="missing_tool",
                        handler="missing_handler",
                        description="missing",
                    )
                ],
            )
        ]
    )
    client = Mock(spec=BrontoClient)
    runtime = BrontoRuntime(client, registry)

    with pytest.raises(AttributeError, match="Unknown tool handler"):
        runtime.register(FakeMCP())
