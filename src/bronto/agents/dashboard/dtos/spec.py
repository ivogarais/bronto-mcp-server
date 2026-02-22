from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import DashboardToolName


class DashboardAgentSpec(BaseModel):
    description: str = Field(
        default=(
            "Builds validated Bronto dashboard specs with deterministic layout "
            "and can launch the bronto TUI renderer."
        )
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=DashboardToolName.BUILD_DASHBOARD_SPEC.value,
                handler=DashboardToolName.BUILD_DASHBOARD_SPEC.value,
                description=(
                    "Build a validated Bronto dashboard spec from a simplified payload "
                    "(fixed layout, renderer-owned styling)."
                ),
            ),
            AgentToolSpec(
                name=DashboardToolName.SERVE_DASHBOARD.value,
                handler=DashboardToolName.SERVE_DASHBOARD.value,
                description=(
                    "Generate a validated Bronto dashboard spec from payload and run "
                    "`bronto serve --spec <path>` in the current terminal."
                ),
            ),
        ]
    )
