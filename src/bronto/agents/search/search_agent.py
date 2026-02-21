from pydantic import Field

from ..base import AgentToolSpec, BrontoAgent
from .dtos import SearchAgentSpec


def _search_spec() -> SearchAgentSpec:
    return SearchAgentSpec()


class SearchAgent(BrontoAgent):
    name: str = Field(default="search")
    description: str = Field(default_factory=lambda: _search_spec().description)
    tools: list[AgentToolSpec] = Field(default_factory=lambda: _search_spec().tools)
