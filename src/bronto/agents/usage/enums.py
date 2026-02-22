from enum import Enum


class UsageAgentName(str, Enum):
    USAGE = "usage"


class UsageToolName(str, Enum):
    GET_USAGE_FOR_LOG_ID = "get_usage_for_log_id"
    GET_USAGE_FOR_USER_PER_LOG_ID = "get_usage_for_user_per_log_id"
