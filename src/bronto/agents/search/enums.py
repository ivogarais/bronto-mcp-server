from enum import Enum


class SearchAgentName(str, Enum):
    SEARCH = "search"


class SearchToolName(str, Enum):
    SEARCH_LOGS = "search_logs"
    GET_SEARCH_STATUS = "get_search_status"
    CANCEL_SEARCH = "cancel_search"
    COMPUTE_METRICS = "compute_metrics"
    GET_TIMESTAMP_AS_UNIX_EPOCH = "get_timestamp_as_unix_epoch"
    GET_CURRENT_TIME = "get_current_time"
    SEARCH_LOGS_PLAYBOOK = "search_logs_playbook"
    COMPUTE_METRICS_PLAYBOOK = "compute_metrics_playbook"
