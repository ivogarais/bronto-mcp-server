from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import ParsersToolName


class ParsersAgentSpec(BaseModel):
    description: str = Field(default="Retrieves parser usage analytics.")
    tools: list[AgentToolSpec] = Field(default_factory=lambda: [
        AgentToolSpec(name=ParsersToolName.GET_PARSERS_USAGE_FOR_LOG_ID.value, handler=ParsersToolName.GET_PARSERS_USAGE_FOR_LOG_ID.value, description="Get parser usage by log ID."),
        AgentToolSpec(name=ParsersToolName.GET_PARSERS_USAGE_FOR_USER_PER_LOG_ID.value, handler=ParsersToolName.GET_PARSERS_USAGE_FOR_USER_PER_LOG_ID.value, description="Get parser usage by user and log ID."),
    ])
