from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import ContextToolName


class ContextAgentSpec(BaseModel):
    description: str = Field(
        default="Retrieves context events around a focal log event."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=ContextToolName.GET_CONTEXT.value,
                handler=ContextToolName.GET_CONTEXT.value,
                description="Retrieve context events around a log position using sequence/time selectors.",
            )
        ]
    )
