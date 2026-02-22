from enum import Enum


class ParsersAgentName(str, Enum):
    PARSERS = "parsers"


class ParsersToolName(str, Enum):
    GET_PARSERS_USAGE_FOR_LOG_ID = "get_parsers_usage_for_log_id"
    GET_PARSERS_USAGE_FOR_USER_PER_LOG_ID = "get_parsers_usage_for_user_per_log_id"
