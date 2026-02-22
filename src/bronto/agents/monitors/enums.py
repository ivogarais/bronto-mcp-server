from enum import Enum


class MonitorsAgentName(str, Enum):
    MONITORS = "monitors"


class MonitorsToolName(str, Enum):
    LIST_MONITORS_BY_LOG = "list_monitors_by_log"
