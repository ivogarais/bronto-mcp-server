from ..base import BrontoAgent
from .dtos import ApiKeysAgentSpec
from .enums import ApiKeysAgentName


class ApiKeysAgent(BrontoAgent):
    """Agent for API key management tools."""

    def __init__(self):
        """Initialize the API keys agent."""
        spec = ApiKeysAgentSpec()
        super().__init__(
            name=ApiKeysAgentName.API_KEYS.value,
            description=spec.description,
            tools=spec.tools,
        )
