from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import ForwardToolName


class ForwardAgentSpec(BaseModel):
    description: str = Field(default="Retrieves forwarding configuration metadata.")
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=ForwardToolName.LIST_FORWARD_CONFIGS.value,
                handler=ForwardToolName.LIST_FORWARD_CONFIGS.value,
                description="Retrieve configured forwarding destinations and settings.",
            )
        ]
    )
