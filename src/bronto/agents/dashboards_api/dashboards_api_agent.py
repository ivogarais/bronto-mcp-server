from ..base import BrontoAgent
from .dtos import DashboardsApiAgentSpec
from .enums import DashboardsApiAgentName


class DashboardsApiAgent(BrontoAgent):
    def __init__(self):
        spec = DashboardsApiAgentSpec()
        super().__init__(name=DashboardsApiAgentName.DASHBOARDS_API.value, description=spec.description, tools=spec.tools)
