from ..base import BrontoAgent
from .dtos import ForwardAgentSpec
from .enums import ForwardAgentName


class ForwardAgent(BrontoAgent):
    """Agent for forwarding configuration tools."""

    def __init__(self):
        """Initialize the forward agent."""
        spec = ForwardAgentSpec()
        super().__init__(
            name=ForwardAgentName.FORWARD.value,
            description=spec.description,
            tools=spec.tools,
        )
