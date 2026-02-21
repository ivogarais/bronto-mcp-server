from pydantic import Field

from .base import AgentToolSpec, BrontoAgent


class SearchAgent(BrontoAgent):
    name: str = Field(default="search")
    description: str = Field(
        default=(
            "Searches log events, computes metrics on log data, and provides time conversion helpers."
        )
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(name="search_logs", handler="search_logs"),
            AgentToolSpec(name="compute_metrics", handler="compute_metrics"),
            AgentToolSpec(
                name="get_timestamp_as_unix_epoch",
                handler="get_timestamp_as_unix_epoch",
            ),
            AgentToolSpec(name="get_current_time", handler="get_current_time"),
        ]
    )
