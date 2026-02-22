from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import ExportsToolName


class ExportsAgentSpec(BaseModel):
    description: str = Field(default="Retrieves export jobs and status metadata.")
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=ExportsToolName.LIST_EXPORTS.value,
                handler=ExportsToolName.LIST_EXPORTS.value,
                description="Retrieve export jobs available to the authenticated principal.",
            ),
            AgentToolSpec(
                name=ExportsToolName.GET_EXPORT.value,
                handler=ExportsToolName.GET_EXPORT.value,
                description="Retrieve export job details by export ID.",
            ),
        ]
    )
