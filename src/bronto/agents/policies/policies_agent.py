from ..base import BrontoAgent
from .dtos import PoliciesAgentSpec
from .enums import PoliciesAgentName


class PoliciesAgent(BrontoAgent):
    """Agent for policy lookup tools."""

    def __init__(self):
        """Initialize the policies agent."""
        spec = PoliciesAgentSpec()
        super().__init__(
            name=PoliciesAgentName.POLICIES.value,
            description=spec.description,
            tools=spec.tools,
        )
