from ..base import BrontoAgent
from .dtos import StatementIdsAgentSpec
from .enums import StatementIdsAgentName


class StatementIdsAgent(BrontoAgent):
    """Agent for statement ID lifecycle tools."""

    def __init__(self):
        """Initialize the statement IDs agent."""
        spec = StatementIdsAgentSpec()
        super().__init__(
            name=StatementIdsAgentName.STATEMENT_IDS.value,
            description=spec.description,
            tools=spec.tools,
        )
