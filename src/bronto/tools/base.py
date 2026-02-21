from typing import Optional

from agents import BrontoAgentRegistry, build_agent_registry
from clients import BrontoClient


class BrontoToolContext:
    """Shared dependencies for Bronto MCP tool handlers."""

    def __init__(
        self,
        bronto_client: BrontoClient,
        agent_registry: Optional[BrontoAgentRegistry] = None,
    ):
        self.bronto_client = bronto_client
        self.agent_registry = agent_registry or build_agent_registry()
