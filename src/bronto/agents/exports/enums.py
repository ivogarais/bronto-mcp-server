from enum import Enum


class ExportsAgentName(str, Enum):
    EXPORTS = "exports"


class ExportsToolName(str, Enum):
    LIST_EXPORTS = "list_exports"
    CREATE_EXPORT = "create_export"
    GET_EXPORT = "get_export"
    DELETE_EXPORT = "delete_export"
