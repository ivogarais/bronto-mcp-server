from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import ApiKeysToolName


class ApiKeysAgentSpec(BaseModel):
    description: str = Field(
        default="Manages API key metadata and discovery operations."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=ApiKeysToolName.LIST_API_KEYS.value,
                handler=ApiKeysToolName.LIST_API_KEYS.value,
                description="Retrieve all API keys visible to the authenticated principal.",
            ),
            AgentToolSpec(
                name=ApiKeysToolName.CREATE_API_KEY.value,
                handler=ApiKeysToolName.CREATE_API_KEY.value,
                description="Create a new API key.",
            ),
            AgentToolSpec(
                name=ApiKeysToolName.UPDATE_API_KEY.value,
                handler=ApiKeysToolName.UPDATE_API_KEY.value,
                description="Update an existing API key by ID.",
            ),
            AgentToolSpec(
                name=ApiKeysToolName.DELETE_API_KEY.value,
                handler=ApiKeysToolName.DELETE_API_KEY.value,
                description="Delete an API key by ID.",
            ),
        ]
    )
