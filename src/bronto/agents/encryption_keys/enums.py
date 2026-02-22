from enum import Enum


class EncryptionKeysAgentName(str, Enum):
    ENCRYPTION_KEYS = "encryption_keys"


class EncryptionKeysToolName(str, Enum):
    LIST_ENCRYPTION_KEYS = "list_encryption_keys"
    CREATE_ENCRYPTION_KEY = "create_encryption_key"
    GET_ENCRYPTION_KEY = "get_encryption_key"
    UPDATE_ENCRYPTION_KEY = "update_encryption_key"
    DELETE_ENCRYPTION_KEY = "delete_encryption_key"
