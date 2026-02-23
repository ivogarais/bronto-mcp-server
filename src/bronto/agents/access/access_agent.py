from ..base import BrontoAgent
from .dtos import AccessAgentSpec
from .enums import AccessAgentName


class AccessAgent(BrontoAgent):
    """Agent for access management tools."""

    def __init__(self):
        """Initialize the access agent."""
        spec = AccessAgentSpec()
        super().__init__(
            name=AccessAgentName.ACCESS.value,
            description=spec.description,
            tools=spec.tools,
        )
