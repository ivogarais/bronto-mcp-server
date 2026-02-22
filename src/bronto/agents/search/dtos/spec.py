from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import SearchToolName


class SearchAgentSpec(BaseModel):
    description: str = Field(
        default="Searches Bronto log events and computes metrics over selected time windows."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=SearchToolName.SEARCH_LOGS.value,
                handler=SearchToolName.SEARCH_LOGS.value,
                description=(
                    "Search log events from selected dataset IDs and time range, with optional SQL-like filter."
                ),
            ),
            AgentToolSpec(
                name=SearchToolName.COMPUTE_METRICS.value,
                handler=SearchToolName.COMPUTE_METRICS.value,
                description=(
                    "Compute metrics such as AVG, MIN, MAX, COUNT, SUM over log data and group keys."
                ),
            ),
            AgentToolSpec(
                name=SearchToolName.GET_TIMESTAMP_AS_UNIX_EPOCH.value,
                handler=SearchToolName.GET_TIMESTAMP_AS_UNIX_EPOCH.value,
                description="Convert a timestamp in YYYY-MM-DD HH:mm:ss to unix epoch milliseconds.",
            ),
            AgentToolSpec(
                name=SearchToolName.GET_CURRENT_TIME.value,
                handler=SearchToolName.GET_CURRENT_TIME.value,
                description="Return current time in YYYY-MM-DD HH:mm:ss.",
            ),
            AgentToolSpec(
                name=SearchToolName.SEARCH_LOGS_PLAYBOOK.value,
                handler=SearchToolName.SEARCH_LOGS_PLAYBOOK.value,
                description="Playbook for safe raw log retrieval workflow.",
            ),
            AgentToolSpec(
                name=SearchToolName.COMPUTE_METRICS_PLAYBOOK.value,
                handler=SearchToolName.COMPUTE_METRICS_PLAYBOOK.value,
                description="Playbook for robust metric computation workflow.",
            ),
            AgentToolSpec(
                name=SearchToolName.TERMINAL_REPORT_PLAYBOOK.value,
                handler=SearchToolName.TERMINAL_REPORT_PLAYBOOK.value,
                description=(
                    "Playbook defining strict terminal-safe report rendering (ASCII-only layout, no markdown tables)."
                ),
            ),
        ]
    )
