from ..base import BrontoAgent
from .dtos import EncryptionKeysAgentSpec
from .enums import EncryptionKeysAgentName


class EncryptionKeysAgent(BrontoAgent):
    def __init__(self):
        spec = EncryptionKeysAgentSpec()
        super().__init__(name=EncryptionKeysAgentName.ENCRYPTION_KEYS.value, description=spec.description, tools=spec.tools)
