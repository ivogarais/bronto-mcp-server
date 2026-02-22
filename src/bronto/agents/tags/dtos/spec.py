from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import TagsToolName


class TagsAgentSpec(BaseModel):
    description: str = Field(default="Manages tags.")
    tools: list[AgentToolSpec] = Field(default_factory=lambda: [
        AgentToolSpec(name=TagsToolName.LIST_TAGS.value, handler=TagsToolName.LIST_TAGS.value, description="List tags."),
        AgentToolSpec(name=TagsToolName.CREATE_TAG.value, handler=TagsToolName.CREATE_TAG.value, description="Create a tag."),
        AgentToolSpec(name=TagsToolName.UPDATE_TAG.value, handler=TagsToolName.UPDATE_TAG.value, description="Update a tag by name."),
        AgentToolSpec(name=TagsToolName.DELETE_TAG.value, handler=TagsToolName.DELETE_TAG.value, description="Delete a tag by name."),
    ])
