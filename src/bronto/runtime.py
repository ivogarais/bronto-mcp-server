from bronto.agents import BrontoAgentRegistry
from bronto.agents.datasets.tools import DatasetsToolHandlers
from bronto.agents.search.tools import SearchToolHandlers
from bronto.agents.statement_ids.tools import StatementIdsToolHandlers
from bronto.agents.terminal_reports.tools import TerminalReportsToolHandlers
from bronto.clients import BrontoClient


class BrontoRuntime(
    SearchToolHandlers,
    DatasetsToolHandlers,
    StatementIdsToolHandlers,
    TerminalReportsToolHandlers,
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
