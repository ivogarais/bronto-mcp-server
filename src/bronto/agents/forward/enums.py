from enum import Enum


class ForwardAgentName(str, Enum):
    FORWARD = "forward"


class ForwardToolName(str, Enum):
    LIST_FORWARD_CONFIGS = "list_forward_configs"
