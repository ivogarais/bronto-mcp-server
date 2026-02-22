from enum import Enum


class DashboardsApiAgentName(str, Enum):
    DASHBOARDS_API = "dashboards_api"


class DashboardsApiToolName(str, Enum):
    LIST_DASHBOARDS_BY_LOG = "list_dashboards_by_log"
