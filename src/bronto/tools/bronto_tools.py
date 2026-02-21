from .base import BrontoToolContext
from .registry import MCPToolRegistrar
from bronto.agents.datasets.tools import DatasetsToolHandlers
from bronto.agents.search.tools import SearchToolHandlers
from bronto.agents.statement_ids.tools import StatementIdsToolHandlers


class BrontoTools(
    BrontoToolContext,
    MCPToolRegistrar,
    SearchToolHandlers,
    DatasetsToolHandlers,
    StatementIdsToolHandlers,
):
    """Facade exposing all Bronto tool handlers and MCP registration."""
