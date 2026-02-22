from ..base import BrontoAgent
from .dtos import ParsersAgentSpec
from .enums import ParsersAgentName


class ParsersAgent(BrontoAgent):
    def __init__(self):
        spec = ParsersAgentSpec()
        super().__init__(name=ParsersAgentName.PARSERS.value, description=spec.description, tools=spec.tools)
