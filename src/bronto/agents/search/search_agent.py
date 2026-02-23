from ..base import BrontoAgent
from .dtos import SearchAgentSpec
from .enums import SearchAgentName


class SearchAgent(BrontoAgent):
    """Agent for search and metric tools."""

    def __init__(self):
        """Initialize the search agent."""
        spec = SearchAgentSpec()
        super().__init__(
            name=SearchAgentName.SEARCH.value,
            description=spec.description,
            tools=spec.tools,
        )
