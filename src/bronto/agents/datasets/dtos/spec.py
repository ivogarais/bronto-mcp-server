from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import DatasetsToolName


class DatasetsAgentSpec(BaseModel):
    description: str = Field(
        default="Discovers datasets and key metadata available in Bronto."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=DatasetsToolName.GET_DATASETS.value,
                handler=DatasetsToolName.GET_DATASETS.value,
                description="Fetch all available dataset details including log IDs and tags.",
            ),
            AgentToolSpec(
                name=DatasetsToolName.CREATE_LOG.value,
                handler=DatasetsToolName.CREATE_LOG.value,
                description="Create a new log (dataset) in a collection.",
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_DATASETS_BY_NAME.value,
                handler=DatasetsToolName.GET_DATASETS_BY_NAME.value,
                description="Fetch datasets matching an exact dataset name and collection name.",
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_KEYS.value,
                handler=DatasetsToolName.GET_KEYS.value,
                description="List all keys present in a dataset identified by log ID.",
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_ALL_DATASETS_KEYS.value,
                handler=DatasetsToolName.GET_ALL_DATASETS_KEYS.value,
                description="List keys for every dataset, grouped by dataset ID.",
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_KEY_VALUES.value,
                handler=DatasetsToolName.GET_KEY_VALUES.value,
                description="Fetch sample values for a key in a specific dataset.",
            ),
            AgentToolSpec(
                name=DatasetsToolName.DATASETS_PLAYBOOK.value,
                handler=DatasetsToolName.DATASETS_PLAYBOOK.value,
                description="Playbook for dataset discovery and key validation.",
            ),
        ]
    )
