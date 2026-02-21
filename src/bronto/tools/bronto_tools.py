from .base import BrontoToolsBase
from .registry import MCPToolRegistrationMixin
from agents.datasets.tools import DatasetToolHandlers
from agents.search.tools import SearchToolHandlers
from agents.statement_ids.tools import StatementIdsToolHandlers


class BrontoTools(
    BrontoToolsBase,
    MCPToolRegistrationMixin,
    SearchToolHandlers,
    DatasetToolHandlers,
    StatementIdsToolHandlers,
):
    """Facade exposing all Bronto tool handlers and MCP registration."""
