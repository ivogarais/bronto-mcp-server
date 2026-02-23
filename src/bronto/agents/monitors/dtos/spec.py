from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import MonitorsToolName


class MonitorsAgentSpec(BaseModel):
    description: str = Field(default="Retrieves monitor resources by log.")
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=MonitorsToolName.LIST_MONITORS_BY_LOG.value,
                handler=MonitorsToolName.LIST_MONITORS_BY_LOG.value,
                description="List monitors by log ID.",
            ),
        ]
    )
