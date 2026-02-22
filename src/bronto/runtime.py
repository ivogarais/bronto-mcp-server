from bronto.agents import BrontoAgentRegistry
from bronto.agents.api_keys.tools import ApiKeysToolHandlers
from bronto.agents.context.tools import ContextToolHandlers
from bronto.agents.dashboard.tools import DashboardToolHandlers
from bronto.agents.datasets.tools import DatasetsToolHandlers
from bronto.agents.exports.tools import ExportsToolHandlers
from bronto.agents.forward.tools import ForwardToolHandlers
from bronto.agents.search.tools import SearchToolHandlers
from bronto.agents.statement_ids.tools import StatementIdsToolHandlers
from bronto.agents.usage.tools import UsageToolHandlers
from bronto.agents.users.tools import UsersToolHandlers
from bronto.clients import BrontoClient


class BrontoRuntime(
    SearchToolHandlers,
    DatasetsToolHandlers,
    StatementIdsToolHandlers,
    DashboardToolHandlers,
    ApiKeysToolHandlers,
    UsersToolHandlers,
    ContextToolHandlers,
    ExportsToolHandlers,
    UsageToolHandlers,
    ForwardToolHandlers,
):
    """Registers MCP tools and exposes all Bronto handlers."""

    def __init__(
        self,
        bronto_client: BrontoClient,
        agent_registry: BrontoAgentRegistry,
    ):
        if len(agent_registry.agents) == 0:
            raise ValueError("agent_registry must include at least one agent")

        self.bronto_client = bronto_client
        self.agent_registry = agent_registry

    def register(self, mcp):
        for tool_spec in self.agent_registry.iter_tool_specs():
            handler = getattr(self, tool_spec.handler, None)
            if handler is None:
                raise AttributeError(f"Unknown tool handler: {tool_spec.handler}")
            mcp.tool(name=tool_spec.name, description=tool_spec.description)(handler)
