from pydantic import Field

from .base import AgentToolSpec, BrontoAgent


class DatasetsAgent(BrontoAgent):
    name: str = Field(default="datasets")
    description: str = Field(
        default=(
            "Discovers datasets, resolves dataset IDs, and explores keys and values in dataset metadata."
        )
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(name="get_datasets", handler="get_datasets"),
            AgentToolSpec(name="get_datasets_by_name", handler="get_datasets_by_name"),
            AgentToolSpec(name="get_keys", handler="get_dataset_keys"),
            AgentToolSpec(
                name="get_all_datasets_keys", handler="get_all_datasets_keys"
            ),
            AgentToolSpec(name="get_key_values", handler="get_key_values"),
        ]
    )
