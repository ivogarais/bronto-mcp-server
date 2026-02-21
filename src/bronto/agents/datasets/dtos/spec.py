from pydantic import BaseModel, Field

from ...base import AgentToolSpec, ToolExecutionSpec


class DatasetsAgentSpec(BaseModel):
    description: str = Field(
        default="Discovers datasets and key metadata available in Bronto."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name="get_datasets",
                handler="get_datasets",
                kind="tool",
                description="Fetch all available dataset details including log IDs and tags.",
                execution=ToolExecutionSpec(
                    required_inputs=[],
                    expected_output="List[Dataset]",
                    notes="Use first when selecting datasets for queries.",
                ),
            ),
            AgentToolSpec(
                name="get_datasets_by_name",
                handler="get_datasets_by_name",
                kind="tool",
                description="Fetch datasets matching an exact dataset name and collection name.",
                execution=ToolExecutionSpec(
                    required_inputs=["dataset_name", "collection_name"],
                    expected_output="List[Dataset]",
                    notes="Resolves log IDs from human-readable names.",
                ),
            ),
            AgentToolSpec(
                name="get_keys",
                handler="get_dataset_keys",
                kind="tool",
                description="List all keys present in a dataset identified by log ID.",
                execution=ToolExecutionSpec(
                    required_inputs=["log_id"],
                    expected_output="List[str]",
                    notes="Use before building filters to avoid invalid key names.",
                ),
            ),
            AgentToolSpec(
                name="get_all_datasets_keys",
                handler="get_all_datasets_keys",
                kind="tool",
                description="List keys for every dataset, grouped by dataset ID.",
                execution=ToolExecutionSpec(
                    required_inputs=[],
                    expected_output="Dict[str, List[str]]",
                    notes="Helps identify candidate datasets for a given key.",
                ),
            ),
            AgentToolSpec(
                name="get_key_values",
                handler="get_key_values",
                kind="tool",
                description="Fetch sample values for a key in a specific dataset.",
                execution=ToolExecutionSpec(
                    required_inputs=["key", "log_id"],
                    expected_output="List[str]",
                    notes="Useful for building valid filter predicates.",
                ),
            ),
        ]
    )
