from ..base import BrontoAgent
from .dtos import ContextAgentSpec
from .enums import ContextAgentName


class ContextAgent(BrontoAgent):
    """Agent for context retrieval tools."""

    def __init__(self):
        """Initialize the context agent."""
        spec = ContextAgentSpec()
        super().__init__(
            name=ContextAgentName.CONTEXT.value,
            description=spec.description,
            tools=spec.tools,
        )
