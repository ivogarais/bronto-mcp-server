from ..base import BrontoAgent
from .dtos import DashboardAgentSpec
from .enums import DashboardAgentName


class DashboardAgent(BrontoAgent):
    """Dashboard agent for Bronto TUI spec generation and rendering."""

    def __init__(self):
        spec = DashboardAgentSpec()
        super().__init__(
            name=DashboardAgentName.DASHBOARD.value,
            description=spec.description,
            tools=spec.tools,
        )
