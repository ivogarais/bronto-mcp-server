from enum import Enum


class ApiKeysAgentName(str, Enum):
    API_KEYS = "api_keys"


class ApiKeysToolName(str, Enum):
    LIST_API_KEYS = "list_api_keys"
    CREATE_API_KEY = "create_api_key"
    UPDATE_API_KEY = "update_api_key"
    DELETE_API_KEY = "delete_api_key"
