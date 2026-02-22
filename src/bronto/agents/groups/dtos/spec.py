from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import GroupsToolName


class GroupsAgentSpec(BaseModel):
    description: str = Field(default="Manages group resources and memberships.")
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(name=GroupsToolName.LIST_GROUPS.value, handler=GroupsToolName.LIST_GROUPS.value, description="List groups."),
            AgentToolSpec(name=GroupsToolName.CREATE_GROUP.value, handler=GroupsToolName.CREATE_GROUP.value, description="Create a group."),
            AgentToolSpec(name=GroupsToolName.GET_GROUP.value, handler=GroupsToolName.GET_GROUP.value, description="Get a group by ID."),
            AgentToolSpec(name=GroupsToolName.UPDATE_GROUP.value, handler=GroupsToolName.UPDATE_GROUP.value, description="Update a group by ID."),
            AgentToolSpec(name=GroupsToolName.DELETE_GROUP.value, handler=GroupsToolName.DELETE_GROUP.value, description="Delete a group by ID."),
            AgentToolSpec(name=GroupsToolName.LIST_GROUP_MEMBERS.value, handler=GroupsToolName.LIST_GROUP_MEMBERS.value, description="List members in a group."),
            AgentToolSpec(name=GroupsToolName.ADD_GROUP_MEMBERS.value, handler=GroupsToolName.ADD_GROUP_MEMBERS.value, description="Add members to a group."),
            AgentToolSpec(name=GroupsToolName.REMOVE_GROUP_MEMBERS.value, handler=GroupsToolName.REMOVE_GROUP_MEMBERS.value, description="Remove members from a group."),
            AgentToolSpec(name=GroupsToolName.LIST_MEMBER_GROUPS.value, handler=GroupsToolName.LIST_MEMBER_GROUPS.value, description="List groups for a member."),
        ]
    )
