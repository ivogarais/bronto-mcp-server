from pydantic import Field

from .base import AgentToolSpec, BrontoAgent
from .utils import resolve_agent_blueprint


class SearchAgent(BrontoAgent):
    name: str = Field(default="search")
    description: str = Field(
        default_factory=lambda: resolve_agent_blueprint("search")["description"]
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(**tool) for tool in resolve_agent_blueprint("search")["tools"]
        ]
    )
