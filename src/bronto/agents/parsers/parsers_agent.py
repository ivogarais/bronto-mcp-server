from ..base import BrontoAgent
from .dtos import ParsersAgentSpec
from .enums import ParsersAgentName


class ParsersAgent(BrontoAgent):
    """Agent for parser usage analytics tools."""

    def __init__(self):
        """Initialize the parsers agent."""
        spec = ParsersAgentSpec()
        super().__init__(
            name=ParsersAgentName.PARSERS.value,
            description=spec.description,
            tools=spec.tools,
        )
