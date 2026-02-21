from enum import Enum


class SearchAgentName(str, Enum):
    SEARCH = "search"


class SearchToolName(str, Enum):
    SEARCH_LOGS = "search_logs"
    COMPUTE_METRICS = "compute_metrics"
    GET_TIMESTAMP_AS_UNIX_EPOCH = "get_timestamp_as_unix_epoch"
    GET_CURRENT_TIME = "get_current_time"


class SearchToolHandler(str, Enum):
    SEARCH_LOGS = "search_logs"
    COMPUTE_METRICS = "compute_metrics"
    GET_TIMESTAMP_AS_UNIX_EPOCH = "get_timestamp_as_unix_epoch"
    GET_CURRENT_TIME = "get_current_time"
