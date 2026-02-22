from ..base import BrontoAgent
from .dtos import ApiKeysAgentSpec
from .enums import ApiKeysAgentName


class ApiKeysAgent(BrontoAgent):
    """Traceability agent for API key discovery tools."""

    def __init__(self):
        spec = ApiKeysAgentSpec()
        super().__init__(
            name=ApiKeysAgentName.API_KEYS.value,
            description=spec.description,
            tools=spec.tools,
        )
