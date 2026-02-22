from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import EncryptionKeysToolName


class EncryptionKeysAgentSpec(BaseModel):
    description: str = Field(default="Manages encryption key resources.")
    tools: list[AgentToolSpec] = Field(default_factory=lambda: [
        AgentToolSpec(name=EncryptionKeysToolName.LIST_ENCRYPTION_KEYS.value, handler=EncryptionKeysToolName.LIST_ENCRYPTION_KEYS.value, description="List encryption keys."),
        AgentToolSpec(name=EncryptionKeysToolName.CREATE_ENCRYPTION_KEY.value, handler=EncryptionKeysToolName.CREATE_ENCRYPTION_KEY.value, description="Create an encryption key."),
        AgentToolSpec(name=EncryptionKeysToolName.GET_ENCRYPTION_KEY.value, handler=EncryptionKeysToolName.GET_ENCRYPTION_KEY.value, description="Get an encryption key by ID."),
        AgentToolSpec(name=EncryptionKeysToolName.UPDATE_ENCRYPTION_KEY.value, handler=EncryptionKeysToolName.UPDATE_ENCRYPTION_KEY.value, description="Update an encryption key by ID."),
        AgentToolSpec(name=EncryptionKeysToolName.DELETE_ENCRYPTION_KEY.value, handler=EncryptionKeysToolName.DELETE_ENCRYPTION_KEY.value, description="Delete an encryption key by ID."),
    ])
