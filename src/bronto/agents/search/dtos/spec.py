from pydantic import BaseModel, Field

from ...base import AgentKind, AgentToolSpec, ToolExecutionSpec
from ..enums import SearchToolHandler, SearchToolName


class SearchAgentSpec(BaseModel):
    description: str = Field(
        default="Searches Bronto log events and computes metrics over selected time windows."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=SearchToolName.SEARCH_LOGS.value,
                handler=SearchToolHandler.SEARCH_LOGS.value,
                kind=AgentKind.TOOL,
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
                name=SearchToolName.COMPUTE_METRICS.value,
                handler=SearchToolHandler.COMPUTE_METRICS.value,
                kind=AgentKind.TOOL,
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
                name=SearchToolName.GET_TIMESTAMP_AS_UNIX_EPOCH.value,
                handler=SearchToolHandler.GET_TIMESTAMP_AS_UNIX_EPOCH.value,
                kind=AgentKind.TOOL,
                description="Convert a timestamp in YYYY-MM-DD HH:mm:ss to unix epoch milliseconds.",
                execution=ToolExecutionSpec(
                    required_inputs=["input_time"],
                    expected_output="int",
                    notes="Timezone is expected to be UTC.",
                ),
            ),
            AgentToolSpec(
                name=SearchToolName.GET_CURRENT_TIME.value,
                handler=SearchToolHandler.GET_CURRENT_TIME.value,
                kind=AgentKind.TOOL,
                description="Return current time in YYYY-MM-DD HH:mm:ss.",
                execution=ToolExecutionSpec(
                    required_inputs=[],
                    expected_output="str",
                    notes="Use when callers need current wall-clock reference.",
                ),
            ),
        ]
    )
