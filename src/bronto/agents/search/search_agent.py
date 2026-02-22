from ..base import BrontoAgent
from .dtos import SearchAgentSpec
from .enums import SearchAgentName


class SearchAgent(BrontoAgent):
    """Traceability agent for search and metrics tool contracts."""

    def __init__(self):
        spec = SearchAgentSpec()
        super().__init__(
            name=SearchAgentName.SEARCH.value,
            description=spec.description,
            tools=spec.tools,
        )
