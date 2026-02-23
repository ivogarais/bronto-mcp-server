from ..base import BrontoAgent
from .dtos import DashboardAgentSpec
from .enums import DashboardAgentName


class DashboardAgent(BrontoAgent):
    """Agent for dashboard spec and serve tools."""

    def __init__(self):
        """Initialize the dashboard agent."""
        spec = DashboardAgentSpec()
        super().__init__(
            name=DashboardAgentName.DASHBOARD.value,
            description=spec.description,
            tools=spec.tools,
        )
