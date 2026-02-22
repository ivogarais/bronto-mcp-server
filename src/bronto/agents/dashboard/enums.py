from enum import Enum


class DashboardAgentName(str, Enum):
    DASHBOARD = "dashboard"


class DashboardToolName(str, Enum):
    BUILD_DASHBOARD_SPEC = "build_dashboard_spec"
    SERVE_DASHBOARD = "serve_dashboard"
