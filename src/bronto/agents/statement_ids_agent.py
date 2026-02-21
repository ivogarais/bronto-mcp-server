from pydantic import Field

from .base import AgentToolSpec, BrontoAgent
from .utils import resolve_agent_blueprint


class StatementIdsAgent(BrontoAgent):
    name: str = Field(default="statement_ids")
    description: str = Field(
        default_factory=lambda: resolve_agent_blueprint("statement_ids")["description"]
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(**tool)
            for tool in resolve_agent_blueprint("statement_ids")["tools"]
        ]
    )
