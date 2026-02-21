from pydantic import BaseModel, Field

from bronto.schemas import LogEvent, Timeseries

from ...base import (
    AgentKind,
    AgentToolSpec,
    ToolExecutionSpec,
    ToolInputSpec,
    ToolOutputSpec,
)
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
                    inputs=[
                        ToolInputSpec(
                            name="timerange_start",
                            value_type=int,
                            required=False,
                        ),
                        ToolInputSpec(
                            name="timerange_end",
                            value_type=int,
                            required=False,
                        ),
                        ToolInputSpec(name="log_ids", value_type=list[str]),
                        ToolInputSpec(
                            name="search_filter",
                            value_type=str,
                            required=False,
                        ),
                    ],
                    output=ToolOutputSpec(
                        value_type=list[LogEvent],
                    ),
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
                    inputs=[
                        ToolInputSpec(
                            name="timerange_start",
                            value_type=int,
                            required=False,
                        ),
                        ToolInputSpec(
                            name="timerange_end",
                            value_type=int,
                            required=False,
                        ),
                        ToolInputSpec(name="log_ids", value_type=list[str]),
                        ToolInputSpec(
                            name="metric_functions", value_type=list[str]
                        ),
                        ToolInputSpec(
                            name="search_filter",
                            value_type=str,
                            required=False,
                        ),
                        ToolInputSpec(
                            name="group_by_keys",
                            value_type=list[str],
                            required=False,
                        ),
                    ],
                    output=ToolOutputSpec(
                        value_type=dict[str, Timeseries],
                    ),
                    notes="Useful when trend or aggregation is needed.",
                ),
            ),
            AgentToolSpec(
                name=SearchToolName.GET_TIMESTAMP_AS_UNIX_EPOCH.value,
                handler=SearchToolHandler.GET_TIMESTAMP_AS_UNIX_EPOCH.value,
                kind=AgentKind.TOOL,
                description="Convert a timestamp in YYYY-MM-DD HH:mm:ss to unix epoch milliseconds.",
                execution=ToolExecutionSpec(
                    inputs=[ToolInputSpec(name="input_time", value_type=str)],
                    output=ToolOutputSpec(value_type=int),
                    notes="Timezone is expected to be UTC.",
                ),
            ),
            AgentToolSpec(
                name=SearchToolName.GET_CURRENT_TIME.value,
                handler=SearchToolHandler.GET_CURRENT_TIME.value,
                kind=AgentKind.TOOL,
                description="Return current time in YYYY-MM-DD HH:mm:ss.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=str),
                    notes="Use when callers need current wall-clock reference.",
                ),
            ),
            AgentToolSpec(
                name=SearchToolName.SEARCH_LOGS_PLAYBOOK.value,
                handler=SearchToolHandler.SEARCH_LOGS_PLAYBOOK.value,
                kind=AgentKind.PROMPT,
                description="Playbook for safe raw log retrieval workflow.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=str),
                    notes="On-demand usage guidance and filter safety rules.",
                ),
            ),
            AgentToolSpec(
                name=SearchToolName.COMPUTE_METRICS_PLAYBOOK.value,
                handler=SearchToolHandler.COMPUTE_METRICS_PLAYBOOK.value,
                kind=AgentKind.PROMPT,
                description="Playbook for robust metric computation workflow.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=str),
                    notes="On-demand guidance for metric and grouping strategy.",
                ),
            ),
        ]
    )
