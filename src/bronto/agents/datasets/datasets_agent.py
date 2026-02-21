from pydantic import Field

from ..base import AgentToolSpec, BrontoAgent
from .dtos import DatasetsAgentSpec


def _datasets_spec() -> DatasetsAgentSpec:
    return DatasetsAgentSpec()


class DatasetsAgent(BrontoAgent):
    name: str = Field(default="datasets")
    description: str = Field(default_factory=lambda: _datasets_spec().description)
    tools: list[AgentToolSpec] = Field(default_factory=lambda: _datasets_spec().tools)
