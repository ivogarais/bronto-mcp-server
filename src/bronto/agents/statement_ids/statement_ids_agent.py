from pydantic import Field

from ..base import AgentToolSpec, BrontoAgent
from .dtos import StatementIdsAgentSpec


def _statement_ids_spec() -> StatementIdsAgentSpec:
    return StatementIdsAgentSpec()


class StatementIdsAgent(BrontoAgent):
    name: str = Field(default="statement_ids")
    description: str = Field(default_factory=lambda: _statement_ids_spec().description)
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: _statement_ids_spec().tools
    )
