from pydantic import Field

from ..base import AgentToolSpec, BrontoAgent
from .dtos import SearchAgentSpec
from .enums import SearchAgentName


def search_spec() -> SearchAgentSpec:
    return SearchAgentSpec()


class SearchAgent(BrontoAgent):
    """Traceability agent for search and metrics tool contracts."""

    name: str = Field(default=SearchAgentName.SEARCH.value)
    description: str = Field(default_factory=lambda: search_spec().description)
    tools: list[AgentToolSpec] = Field(default_factory=lambda: search_spec().tools)
