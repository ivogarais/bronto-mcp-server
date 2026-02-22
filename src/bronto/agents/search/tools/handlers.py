import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BeforeValidator, Field
from typing_extensions import Annotated

from bronto.agents.playbooks import resolve_playbook
from bronto.clients import BrontoClient
from bronto.logger import module_logger
from bronto.schemas import (
    ComputeMetricsInput,
    Datapoint,
    LogEvent,
    SearchLogsInput,
    SearchStatusInput,
    Timeseries,
)

logger = module_logger(__name__)


class SearchToolHandlers:
    """Search and metrics handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    @staticmethod
    def search_logs_playbook() -> Annotated[
        str,
        Field(
            description=(
                "Playbook for retrieving raw events with safe filters, "
                "validated keys, and explicit time windows."
            )
        ),
    ]:
        return resolve_playbook(
            "bronto.agents.search", "playbooks/search_logs_playbook.md"
        )

    def search_logs(
        self,
        payload: Annotated[
            SearchLogsInput,
            Field(description="Structured payload for log search execution."),
        ],
    ) -> Annotated[
        List[LogEvent],
        Field(
            description="A list of log events and their attributes. Attributes are key-value pairs associated with "
            "the event, e.g. key=value"
        ),
    ]:
        timerange_start = payload.timerange_start
        timerange_end = payload.timerange_end
        if timerange_start is None:
            timerange_start = (int(time.time()) - (20 * 60)) * 1000
        if timerange_end is None:
            timerange_end = int(time.time()) * 1000
        logger.info(
            "timerange_start=%s, timerange_end=%s, log_ids=%s",
            timerange_start,
            timerange_end,
            payload.log_ids,
        )
        log_events = self.bronto_client.search(
            timerange_start,
            timerange_end,
            payload.log_ids,
            payload.search_filter or "",
            payload.limit,
            _select=["*", "@raw"],
        )
        return log_events

    def get_search_status(
        self,
        payload: Annotated[
            SearchStatusInput,
            Field(description="Structured payload containing async search status_id."),
        ],
    ) -> Annotated[
        Dict[str, Any],
        Field(description="Raw status payload for the asynchronous search."),
    ]:
        return self.bronto_client.get_search_status(payload.status_id)

    def cancel_search(
        self,
        payload: Annotated[
            SearchStatusInput,
            Field(description="Structured payload containing async search status_id."),
        ],
    ) -> Annotated[
        Dict[str, Any],
        Field(description="Cancellation result payload."),
    ]:
        return self.bronto_client.cancel_search(payload.status_id)

    def compute_metrics(
        self,
        payload: Annotated[
            ComputeMetricsInput,
            Field(description="Structured payload for metrics computation."),
        ],
    ) -> Annotated[
        Dict[str, Timeseries],
        Field(
            description="Map of Timeseries. The keys of the map represent group names based on the group_by_keys "
            "parameter. The Timeseries represent a list of data points for the given group. Each list "
            "represents the value of the computed metrics for a subset of the provided time range"
        ),
    ]:
        timerange_start = payload.timerange_start
        timerange_end = payload.timerange_end
        if timerange_start is None:
            timerange_start = (int(time.time()) - (20 * 60)) * 1000
        if timerange_end is None:
            timerange_end = int(time.time()) * 1000
        group_by_keys = payload.group_by_keys or []
        logger.info(
            "timerange_start=%s, timerange_end=%s, log_ids=%s, metric_functions=%s, group_by_keys=[%s]",
            timerange_start,
            timerange_end,
            payload.log_ids,
            ",".join(payload.metric_functions),
            ",".join(group_by_keys),
        )
        resp = self.bronto_client.search_post(
            timerange_start,
            timerange_end,
            payload.log_ids,
            payload.search_filter,
            _select=payload.metric_functions,
            group_by_keys=group_by_keys,
        )
        if len(group_by_keys) == 0:
            totals = resp["totals"]
            count = totals["count"]
            timeseries = totals.get("timeseries", [])
            name = ""
            group_series = [{"name": name, "timeseries": timeseries, "count": count}]
        else:
            group_series = resp.get("groups_series", [])
        result = {}
        for group_serie in group_series:
            datapoints = []
            for datapoint in group_serie.get("timeseries", []):
                datapoints.append(
                    Datapoint(
                        timestamp=datapoint["@timestamp"],
                        count=datapoint["count"],
                        quantiles=datapoint["quantiles"],
                        value=datapoint["value"],
                    )
                )
            timeseries = Timeseries(count=group_serie["count"], timeseries=datapoints)
            result[group_serie["name"]] = timeseries
        return result

    @staticmethod
    def _validate_input_time(input_time: str) -> str:
        datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
        return input_time

    @staticmethod
    def get_timestamp_as_unix_epoch(
        input_time: Annotated[
            str,
            BeforeValidator(_validate_input_time),
            Field(
                description='Time represented in the "%Y-%m-%d %H:%M:%S" format. Timezone is assumed to be UTC'
            ),
        ],
    ) -> Annotated[
        int,
        Field(
            description="A unix timestamp (in milliseconds) since epoch, representing the `input_time` parameter"
        ),
    ]:
        return (
            int(
                datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
                .replace(tzinfo=timezone.utc)
                .timestamp()
            )
            * 1000
        )

    @staticmethod
    def get_current_time() -> (
        Annotated[
            str, Field(description="Current time in the YYYY-MM-DD HH:mm:ss format.")
        ]
    ):
        return datetime.strftime(datetime.now(timezone.utc), "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def compute_metrics_playbook() -> Annotated[
        str,
        Field(
            description=(
                "Playbook for metric selection, grouping strategy, and "
                "post-metric drill-down."
            )
        ),
    ]:
        return resolve_playbook(
            "bronto.agents.search", "playbooks/compute_metrics_playbook.md"
        )
