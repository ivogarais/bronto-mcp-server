from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import PoliciesToolName


class PoliciesAgentSpec(BaseModel):
    description: str = Field(default="Retrieves policies by resource.")
    tools: list[AgentToolSpec] = Field(default_factory=lambda: [
        AgentToolSpec(name=PoliciesToolName.LIST_POLICIES_BY_RESOURCE.value, handler=PoliciesToolName.LIST_POLICIES_BY_RESOURCE.value, description="List policies by resource."),
    ])
