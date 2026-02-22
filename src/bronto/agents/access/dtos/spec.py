from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import AccessToolName


class AccessAgentSpec(BaseModel):
    description: str = Field(default="Manages organization access and active organization selection.")
    tools: list[AgentToolSpec] = Field(default_factory=lambda: [
        AgentToolSpec(name=AccessToolName.GRANT_ACCESS.value, handler=AccessToolName.GRANT_ACCESS.value, description="Grant access."),
        AgentToolSpec(name=AccessToolName.REVOKE_ACCESS.value, handler=AccessToolName.REVOKE_ACCESS.value, description="Revoke access."),
        AgentToolSpec(name=AccessToolName.LIST_ACCESS_MEMBERS.value, handler=AccessToolName.LIST_ACCESS_MEMBERS.value, description="List access members."),
        AgentToolSpec(name=AccessToolName.CHECK_ACCESS.value, handler=AccessToolName.CHECK_ACCESS.value, description="Check whether a member has access."),
        AgentToolSpec(name=AccessToolName.SWITCH_ACTIVE_ORGANIZATION.value, handler=AccessToolName.SWITCH_ACTIVE_ORGANIZATION.value, description="Switch active organization."),
    ])
