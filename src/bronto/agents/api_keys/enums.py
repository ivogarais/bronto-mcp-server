from enum import Enum


class ApiKeysAgentName(str, Enum):
    API_KEYS = "api_keys"


class ApiKeysToolName(str, Enum):
    LIST_API_KEYS = "list_api_keys"
