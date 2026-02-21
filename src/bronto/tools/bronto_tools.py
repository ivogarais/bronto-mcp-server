from .base import BrontoToolContext
from .registry import MCPToolRegistrar
from agents.datasets.tools import DatasetsToolHandlers
from agents.search.tools import SearchToolHandlers
from agents.statement_ids.tools import StatementIdsToolHandlers


class BrontoTools(
    BrontoToolContext,
    MCPToolRegistrar,
    SearchToolHandlers,
    DatasetsToolHandlers,
    StatementIdsToolHandlers,
):
    """Facade exposing all Bronto tool handlers and MCP registration."""
