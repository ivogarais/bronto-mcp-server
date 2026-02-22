from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import UsageToolName


class UsageAgentSpec(BaseModel):
    description: str = Field(default="Retrieves usage analytics by dataset and by user.")
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=UsageToolName.GET_USAGE_FOR_LOG_ID.value,
                handler=UsageToolName.GET_USAGE_FOR_LOG_ID.value,
                description="Retrieve usage metrics grouped by log ID.",
            ),
            AgentToolSpec(
                name=UsageToolName.GET_USAGE_FOR_USER_PER_LOG_ID.value,
                handler=UsageToolName.GET_USAGE_FOR_USER_PER_LOG_ID.value,
                description="Retrieve usage metrics grouped by user and log ID.",
            ),
        ]
    )
