from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import DashboardsApiToolName


class DashboardsApiAgentSpec(BaseModel):
    description: str = Field(default="Retrieves dashboard resources by log.")
    tools: list[AgentToolSpec] = Field(default_factory=lambda: [
        AgentToolSpec(name=DashboardsApiToolName.LIST_DASHBOARDS_BY_LOG.value, handler=DashboardsApiToolName.LIST_DASHBOARDS_BY_LOG.value, description="List dashboards by log ID."),
    ])
