from ..base import BrontoAgent
from .dtos import StatementIdsAgentSpec
from .enums import StatementIdsAgentName


class StatementIdsAgent(BrontoAgent):
    """Traceability agent for statement ID generation and lifecycle tools."""

    def __init__(self):
        spec = StatementIdsAgentSpec()
        super().__init__(
            name=StatementIdsAgentName.STATEMENT_IDS.value,
            description=spec.description,
            tools=spec.tools,
        )
