from ..base import BrontoAgent
from .dtos import MonitorsAgentSpec
from .enums import MonitorsAgentName


class MonitorsAgent(BrontoAgent):
    """Agent for monitor discovery tools."""

    def __init__(self):
        """Initialize the monitors agent."""
        spec = MonitorsAgentSpec()
        super().__init__(
            name=MonitorsAgentName.MONITORS.value,
            description=spec.description,
            tools=spec.tools,
        )
