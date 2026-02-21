from pydantic import Field

from ..base import AgentToolSpec, BrontoAgent
from .dtos import SearchAgentSpec
from .enums import SearchAgentName


def _search_spec() -> SearchAgentSpec:
    return SearchAgentSpec()


class SearchAgent(BrontoAgent):
    """Traceability agent for search and metrics tool contracts."""

    name: str = Field(default=SearchAgentName.SEARCH.value)
    description: str = Field(default_factory=lambda: _search_spec().description)
    tools: list[AgentToolSpec] = Field(default_factory=lambda: _search_spec().tools)
