from pydantic import Field

from .base import AgentToolSpec, BrontoAgent
from .utils import resolve_agent_blueprint


class DatasetsAgent(BrontoAgent):
    name: str = Field(default="datasets")
    description: str = Field(
        default_factory=lambda: resolve_agent_blueprint("datasets")["description"]
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(**tool)
            for tool in resolve_agent_blueprint("datasets")["tools"]
        ]
    )
