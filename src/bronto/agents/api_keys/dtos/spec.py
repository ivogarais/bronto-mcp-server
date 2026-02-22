from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import ApiKeysToolName


class ApiKeysAgentSpec(BaseModel):
    description: str = Field(default="Manages API key metadata and discovery operations.")
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=ApiKeysToolName.LIST_API_KEYS.value,
                handler=ApiKeysToolName.LIST_API_KEYS.value,
                description="Retrieve all API keys visible to the authenticated principal.",
            )
        ]
    )
