from pydantic import Field

from ..base import AgentToolSpec, BrontoAgent
from .dtos import StatementIdsAgentSpec
from .enums import StatementIdsAgentName


def _statement_ids_spec() -> StatementIdsAgentSpec:
    return StatementIdsAgentSpec()


class StatementIdsAgent(BrontoAgent):
    """Traceability agent for statement ID generation and lifecycle tools."""

    name: str = Field(default=StatementIdsAgentName.STATEMENT_IDS.value)
    description: str = Field(default_factory=lambda: _statement_ids_spec().description)
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: _statement_ids_spec().tools
    )
