from .base import BrontoToolsBase
from .datasets import DatasetToolHandlers
from .registry import MCPToolRegistrationMixin
from .search import SearchToolHandlers
from .statement_ids import StatementIdsToolHandlers


class BrontoTools(
    BrontoToolsBase,
    MCPToolRegistrationMixin,
    SearchToolHandlers,
    DatasetToolHandlers,
    StatementIdsToolHandlers,
):
    """Facade exposing all Bronto tool handlers and MCP registration."""
