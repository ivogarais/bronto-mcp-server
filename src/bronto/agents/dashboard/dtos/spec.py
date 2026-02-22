from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import DashboardToolName


class DashboardAgentSpec(BaseModel):
    description: str = Field(
        default=(
            "Builds validated Bronto dashboard specs covering all bronto-cli "
            "chart families and can launch the bronto TUI renderer."
        )
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=DashboardToolName.BUILD_DASHBOARD_SPEC.value,
                handler=DashboardToolName.BUILD_DASHBOARD_SPEC.value,
                description=(
                    "Build a validated Bronto dashboard spec from a structured payload "
                    "supporting all bronto-cli chart families."
                ),
            ),
            AgentToolSpec(
                name=DashboardToolName.SERVE_DASHBOARD.value,
                handler=DashboardToolName.SERVE_DASHBOARD.value,
                description=(
                    "Generate a validated Bronto dashboard spec and return a runnable "
                    "`bronto serve --spec <path>` command. "
                    "Use `launch_mode='blocking'` only when a blocking launch is intended."
                ),
            ),
            AgentToolSpec(
                name=DashboardToolName.DASHBOARD_PLAYBOOK.value,
                handler=DashboardToolName.DASHBOARD_PLAYBOOK.value,
                description=(
                    "Playbook with exact payload contract and examples for "
                    "build_dashboard_spec and serve_dashboard."
                ),
            ),
        ]
    )
