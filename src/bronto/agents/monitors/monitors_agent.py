from ..base import BrontoAgent
from .dtos import MonitorsAgentSpec
from .enums import MonitorsAgentName


class MonitorsAgent(BrontoAgent):
    def __init__(self):
        spec = MonitorsAgentSpec()
        super().__init__(name=MonitorsAgentName.MONITORS.value, description=spec.description, tools=spec.tools)
