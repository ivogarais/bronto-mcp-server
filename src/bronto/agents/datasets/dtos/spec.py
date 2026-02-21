from pydantic import BaseModel, Field

from bronto.schemas import Dataset

from ...base import (
    AgentKind,
    AgentToolSpec,
    ToolExecutionSpec,
    ToolInputSpec,
    ToolOutputSpec,
)
from ..enums import DatasetsToolHandler, DatasetsToolName


class DatasetsAgentSpec(BaseModel):
    description: str = Field(
        default="Discovers datasets and key metadata available in Bronto."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=DatasetsToolName.GET_DATASETS.value,
                handler=DatasetsToolHandler.GET_DATASETS.value,
                kind=AgentKind.TOOL,
                description="Fetch all available dataset details including log IDs and tags.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=list[Dataset]),
                    notes="Use first when selecting datasets for queries.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_DATASETS_BY_NAME.value,
                handler=DatasetsToolHandler.GET_DATASETS_BY_NAME.value,
                kind=AgentKind.TOOL,
                description="Fetch datasets matching an exact dataset name and collection name.",
                execution=ToolExecutionSpec(
                    inputs=[
                        ToolInputSpec(name="dataset_name", value_type=str),
                        ToolInputSpec(name="collection_name", value_type=str),
                    ],
                    output=ToolOutputSpec(value_type=list[Dataset]),
                    notes="Resolves log IDs from human-readable names.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_KEYS.value,
                handler=DatasetsToolHandler.GET_KEYS.value,
                kind=AgentKind.TOOL,
                description="List all keys present in a dataset identified by log ID.",
                execution=ToolExecutionSpec(
                    inputs=[ToolInputSpec(name="log_id", value_type=str)],
                    output=ToolOutputSpec(value_type=list[str]),
                    notes="Use before building filters to avoid invalid key names.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_ALL_DATASETS_KEYS.value,
                handler=DatasetsToolHandler.GET_ALL_DATASETS_KEYS.value,
                kind=AgentKind.TOOL,
                description="List keys for every dataset, grouped by dataset ID.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=dict[str, list[str]]),
                    notes="Helps identify candidate datasets for a given key.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_KEY_VALUES.value,
                handler=DatasetsToolHandler.GET_KEY_VALUES.value,
                kind=AgentKind.TOOL,
                description="Fetch sample values for a key in a specific dataset.",
                execution=ToolExecutionSpec(
                    inputs=[
                        ToolInputSpec(name="key", value_type=str),
                        ToolInputSpec(name="log_id", value_type=str),
                    ],
                    output=ToolOutputSpec(value_type=list[str]),
                    notes="Useful for building valid filter predicates.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.DATASETS_PLAYBOOK.value,
                handler=DatasetsToolHandler.DATASETS_PLAYBOOK.value,
                kind=AgentKind.PROMPT,
                description="Playbook for dataset discovery and key validation.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=str),
                    notes="On-demand guidance to keep global instructions concise.",
                ),
            ),
        ]
    )
