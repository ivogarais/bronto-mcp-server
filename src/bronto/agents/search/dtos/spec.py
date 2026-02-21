from pydantic import BaseModel, Field

from ...base import AgentToolSpec, ToolExecutionSpec


class SearchAgentSpec(BaseModel):
    description: str = Field(
        default="Searches Bronto log events and computes metrics over selected time windows."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name="search_logs",
                handler="search_logs",
                kind="tool",
                description=(
                    "Search log events from selected dataset IDs and time range, with optional SQL-like filter."
                ),
                execution=ToolExecutionSpec(
                    required_inputs=["log_ids"],
                    expected_output="List[LogEvent]",
                    notes="Use for raw event retrieval in Bronto.",
                ),
            ),
            AgentToolSpec(
                name="compute_metrics",
                handler="compute_metrics",
                kind="tool",
                description=(
                    "Compute metrics such as AVG, MIN, MAX, COUNT, SUM over log data and group keys."
                ),
                execution=ToolExecutionSpec(
                    required_inputs=["log_ids", "metric_functions"],
                    expected_output="Dict[str, Timeseries]",
                    notes="Useful when trend or aggregation is needed.",
                ),
            ),
            AgentToolSpec(
                name="get_timestamp_as_unix_epoch",
                handler="get_timestamp_as_unix_epoch",
                kind="tool",
                description="Convert a timestamp in YYYY-MM-DD HH:mm:ss to unix epoch milliseconds.",
                execution=ToolExecutionSpec(
                    required_inputs=["input_time"],
                    expected_output="int",
                    notes="Timezone is expected to be UTC.",
                ),
            ),
            AgentToolSpec(
                name="get_current_time",
                handler="get_current_time",
                kind="tool",
                description="Return current time in YYYY-MM-DD HH:mm:ss.",
                execution=ToolExecutionSpec(
                    required_inputs=[],
                    expected_output="str",
                    notes="Use when callers need current wall-clock reference.",
                ),
            ),
        ]
    )
