from ..base import BrontoAgent
from .dtos import AccessAgentSpec
from .enums import AccessAgentName


class AccessAgent(BrontoAgent):
    def __init__(self):
        spec = AccessAgentSpec()
        super().__init__(name=AccessAgentName.ACCESS.value, description=spec.description, tools=spec.tools)
