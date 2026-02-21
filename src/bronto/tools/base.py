from bronto.agents import BrontoAgentRegistry
from bronto.clients import BrontoClient


class BrontoToolContext:
    """Shared dependencies for Bronto MCP tool handlers."""

    def __init__(
        self,
        bronto_client: BrontoClient,
        agent_registry: BrontoAgentRegistry,
    ):
        if len(agent_registry.agents) == 0:
            raise ValueError("agent_registry must include at least one agent")

        self.bronto_client = bronto_client
        self.agent_registry = agent_registry
