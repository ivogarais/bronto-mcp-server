from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import UsersToolName


class UsersAgentSpec(BaseModel):
    description: str = Field(default="Manages user directory discovery operations.")
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=UsersToolName.LIST_USERS.value,
                handler=UsersToolName.LIST_USERS.value,
                description="Retrieve users visible to the authenticated principal.",
            )
        ]
    )
