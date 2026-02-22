from ..base import BrontoAgent
from .dtos import PoliciesAgentSpec
from .enums import PoliciesAgentName


class PoliciesAgent(BrontoAgent):
    def __init__(self):
        spec = PoliciesAgentSpec()
        super().__init__(name=PoliciesAgentName.POLICIES.value, description=spec.description, tools=spec.tools)
