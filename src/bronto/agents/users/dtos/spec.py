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
            ),
            AgentToolSpec(
                name=UsersToolName.CREATE_USER.value,
                handler=UsersToolName.CREATE_USER.value,
                description="Create a new user.",
            ),
            AgentToolSpec(
                name=UsersToolName.GET_USER_BY_ID.value,
                handler=UsersToolName.GET_USER_BY_ID.value,
                description="Retrieve a user by ID.",
            ),
            AgentToolSpec(
                name=UsersToolName.UPDATE_USER.value,
                handler=UsersToolName.UPDATE_USER.value,
                description="Update a user by ID.",
            ),
            AgentToolSpec(
                name=UsersToolName.DELETE_USER.value,
                handler=UsersToolName.DELETE_USER.value,
                description="Delete a user by ID.",
            ),
            AgentToolSpec(
                name=UsersToolName.DEACTIVATE_USER.value,
                handler=UsersToolName.DEACTIVATE_USER.value,
                description="Deactivate a user by ID.",
            ),
            AgentToolSpec(
                name=UsersToolName.REACTIVATE_USER.value,
                handler=UsersToolName.REACTIVATE_USER.value,
                description="Reactivate a user by ID.",
            ),
            AgentToolSpec(
                name=UsersToolName.RESEND_USER_INVITATION.value,
                handler=UsersToolName.RESEND_USER_INVITATION.value,
                description="Resend invitation for a user by ID.",
            ),
            AgentToolSpec(
                name=UsersToolName.GET_USER_PREFERENCES.value,
                handler=UsersToolName.GET_USER_PREFERENCES.value,
                description="Retrieve user preferences by user ID.",
            ),
            AgentToolSpec(
                name=UsersToolName.UPDATE_USER_PREFERENCES.value,
                handler=UsersToolName.UPDATE_USER_PREFERENCES.value,
                description="Update user preferences by user ID.",
            ),
            AgentToolSpec(
                name=UsersToolName.GET_USER_ORGANIZATIONS.value,
                handler=UsersToolName.GET_USER_ORGANIZATIONS.value,
                description="Retrieve organizations for a user by user ID.",
            ),
        ]
    )
