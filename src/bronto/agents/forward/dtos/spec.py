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
            ),
            AgentToolSpec(
                name=ForwardToolName.CREATE_FORWARD_CONFIG.value,
                handler=ForwardToolName.CREATE_FORWARD_CONFIG.value,
                description="Create a forwarding configuration.",
            ),
            AgentToolSpec(
                name=ForwardToolName.UPDATE_FORWARD_CONFIG.value,
                handler=ForwardToolName.UPDATE_FORWARD_CONFIG.value,
                description="Update a forwarding configuration by ID.",
            ),
            AgentToolSpec(
                name=ForwardToolName.DELETE_FORWARD_CONFIG.value,
                handler=ForwardToolName.DELETE_FORWARD_CONFIG.value,
                description="Delete a forwarding configuration by ID.",
            ),
            AgentToolSpec(
                name=ForwardToolName.TEST_FORWARD_DESTINATION.value,
                handler=ForwardToolName.TEST_FORWARD_DESTINATION.value,
                description="Test a forwarding destination payload.",
            ),
        ]
    )
