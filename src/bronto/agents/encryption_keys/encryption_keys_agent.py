from ..base import BrontoAgent
from .dtos import EncryptionKeysAgentSpec
from .enums import EncryptionKeysAgentName


class EncryptionKeysAgent(BrontoAgent):
    """Agent for encryption key management tools."""

    def __init__(self):
        """Initialize the encryption keys agent."""
        spec = EncryptionKeysAgentSpec()
        super().__init__(
            name=EncryptionKeysAgentName.ENCRYPTION_KEYS.value,
            description=spec.description,
            tools=spec.tools,
        )
