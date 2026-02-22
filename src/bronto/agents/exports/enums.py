from enum import Enum


class ExportsAgentName(str, Enum):
    EXPORTS = "exports"


class ExportsToolName(str, Enum):
    LIST_EXPORTS = "list_exports"
    GET_EXPORT = "get_export"
