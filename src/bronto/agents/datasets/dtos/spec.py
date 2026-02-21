from pydantic import BaseModel, Field

from ...base import AgentKind, AgentToolSpec, ToolExecutionSpec
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
                    required_inputs=[],
                    expected_output="List[Dataset]",
                    notes="Use first when selecting datasets for queries.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_DATASETS_BY_NAME.value,
                handler=DatasetsToolHandler.GET_DATASETS_BY_NAME.value,
                kind=AgentKind.TOOL,
                description="Fetch datasets matching an exact dataset name and collection name.",
                execution=ToolExecutionSpec(
                    required_inputs=["dataset_name", "collection_name"],
                    expected_output="List[Dataset]",
                    notes="Resolves log IDs from human-readable names.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_KEYS.value,
                handler=DatasetsToolHandler.GET_KEYS.value,
                kind=AgentKind.TOOL,
                description="List all keys present in a dataset identified by log ID.",
                execution=ToolExecutionSpec(
                    required_inputs=["log_id"],
                    expected_output="List[str]",
                    notes="Use before building filters to avoid invalid key names.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_ALL_DATASETS_KEYS.value,
                handler=DatasetsToolHandler.GET_ALL_DATASETS_KEYS.value,
                kind=AgentKind.TOOL,
                description="List keys for every dataset, grouped by dataset ID.",
                execution=ToolExecutionSpec(
                    required_inputs=[],
                    expected_output="Dict[str, List[str]]",
                    notes="Helps identify candidate datasets for a given key.",
                ),
            ),
            AgentToolSpec(
                name=DatasetsToolName.GET_KEY_VALUES.value,
                handler=DatasetsToolHandler.GET_KEY_VALUES.value,
                kind=AgentKind.TOOL,
                description="Fetch sample values for a key in a specific dataset.",
                execution=ToolExecutionSpec(
                    required_inputs=["key", "log_id"],
                    expected_output="List[str]",
                    notes="Useful for building valid filter predicates.",
                ),
            ),
        ]
    )
