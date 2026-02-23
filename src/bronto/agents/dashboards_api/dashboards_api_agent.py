from ..base import BrontoAgent
from .dtos import DashboardsApiAgentSpec
from .enums import DashboardsApiAgentName


class DashboardsApiAgent(BrontoAgent):
    """Agent for dashboards API lookup tools."""

    def __init__(self):
        """Initialize the dashboards API agent."""
        spec = DashboardsApiAgentSpec()
        super().__init__(
            name=DashboardsApiAgentName.DASHBOARDS_API.value,
            description=spec.description,
            tools=spec.tools,
        )
