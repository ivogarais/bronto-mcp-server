from enum import Enum


class ContextAgentName(str, Enum):
    CONTEXT = "context"


class ContextToolName(str, Enum):
    GET_CONTEXT = "get_context"
