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
                name=ExportsToolName.CREATE_EXPORT.value,
                handler=ExportsToolName.CREATE_EXPORT.value,
                description="Create a new export job.",
            ),
            AgentToolSpec(
                name=ExportsToolName.GET_EXPORT.value,
                handler=ExportsToolName.GET_EXPORT.value,
                description="Retrieve export job details by export ID.",
            ),
            AgentToolSpec(
                name=ExportsToolName.DELETE_EXPORT.value,
                handler=ExportsToolName.DELETE_EXPORT.value,
                description="Delete an export job by export ID.",
            ),
        ]
    )
