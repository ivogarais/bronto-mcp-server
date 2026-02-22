import time
from datetime import datetime, timezone
from typing import Dict, List, Optional

from pydantic import BeforeValidator, Field
from typing_extensions import Annotated

from bronto.agents.playbooks import resolve_playbook
from bronto.clients import BrontoClient
from bronto.logger import module_logger
from bronto.schemas import Datapoint, LogEvent, Timeseries

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
        timerange_start: Annotated[
            Optional[int],
            Field(
                description="Unix timestamp in millisecond representing the start of a time range, e.g. 1756063146000. "
                "If not specify, the current time is selected",
                default_factory=lambda _: (int(time.time()) - (20 * 60)) * 1000,
            ),
        ],
        timerange_end: Annotated[
            Optional[int],
            Field(
                description="Unix timestamp in millisecond representing the end of a time range, e.g. 1756063254000. "
                "If not specify, the time from 20 minutes ago is selected",
                default_factory=lambda _: int(time.time()) * 1000,
            ),
        ],
        log_ids: Annotated[
            list[str],
            Field(
                description="List of dataset IDs, identifying sets of log data. Each log ID "
                "represents a UUID",
                min_length=1,
            ),
        ],
        search_filter: Annotated[
            Optional[str],
            Field(
                default="",
                description="""
                If no value is specified for this field, then no filter is apply when searching log data. Otherwise, 
                this field must follow the syntax of an SQL `WHERE` clause. Unless the search filter is 
                explicitly provided by the user, it is CRITICAL to use keys present in the dataset, e.g. 
                "key_name"='key_value'. For this, the list of keys present in dataset can be retrieved via another tool 
                exposed by this MCP server. In any case, following SQL syntax,
                    - key names should be double-quoted
                    - key value should be single-quoted if they are expected to be strings of characters
                    - key value should not be quoted if they are expected to be numbers.""",
            ),
        ] = "",
    ) -> Annotated[
        List[LogEvent],
        Field(
            description="A list of log events and their attributes. Attributes are key-value pairs associated with "
            "the event, e.g. key=value"
        ),
    ]:
        logger.info(
            "timerange_start=%s, timerange_end=%s, log_ids=%s",
            timerange_start,
            timerange_end,
            log_ids,
        )
        log_events = self.bronto_client.search(
            timerange_start,
            timerange_end,
            log_ids,
            search_filter,
            _select=["*", "@raw"],
        )
        return log_events

    def compute_metrics(
        self,
        timerange_start: Annotated[
            int,
            Field(
                description="Unix timestamp in millisecond representing the start of a time range, e.g. 1756063146000",
                default_factory=lambda _: (int(time.time()) - (20 * 60)) * 1000,
            ),
        ],
        timerange_end: Annotated[
            int,
            Field(
                description="Unix timestamp in millisecond representing the end of a time range, e.g. 1756063254000",
                default_factory=lambda _: int(time.time()) * 1000,
            ),
        ],
        log_ids: Annotated[
            list[str],
            Field(
                description="List of dataset IDs, identifying sets of log data. Each log ID "
                "represents a UUID",
                min_length=1,
            ),
        ],
        metric_functions: Annotated[
            list[str],
            Field(
                description="""
                The metric function can be one of AVG, MIN, MAX, COUNT, MEAN, MEDIAN and SUM. The metric function takes a 
                key name as attribute, except for COUNT which only takes the character '*' as attribute (i.e. 
                "COUNT(*)"). Key names can be determined for given datasets, using one of the other tools provided by 
                this MCP server."""
            ),
        ],
        search_filter: Annotated[
            str,
            Field(
                description="""
                The `search_filter` attribute can follow the syntax of an SQL `WHERE` clause. Unless the search filter is 
                explicitly provided by the user, it is CRITICAL to use keys present in the dataset, e.g. 
                "key_name"='key_value'. For this, the list of keys present in dataset can be retrieved via another tool 
                exposed by this MCP server. In any case, following SQL syntax,
                    - key names should be double-quoted
                    - key value should be single-quoted if they are expected to be strings of characters
                    - key value should not be quoted if they are expected to be numbers."""
            ),
        ] = "",
        group_by_keys: Annotated[
            Optional[List[str]],
            Field(
                description="List of keys expected to be present in log datasets and "
                "by which the metric computed should be grouped"
            ),
        ] = None,
    ) -> Annotated[
        Dict[str, Timeseries],
        Field(
            description="Map of Timeseries. The keys of the map represent group names based on the group_by_keys "
            "parameter. The Timeseries represent a list of data points for the given group. Each list "
            "represents the value of the computed metrics for a subset of the provided time range"
        ),
    ]:
        if group_by_keys is None:
            group_by_keys = []
        logger.info(
            "timerange_start=%s, timerange_end=%s, log_ids=%s, metric_functions=%s, group_by_keys=[%s]",
            timerange_start,
            timerange_end,
            log_ids,
            ",".join(metric_functions),
            ",".join(group_by_keys),
        )
        resp = self.bronto_client.search_post(
            timerange_start,
            timerange_end,
            log_ids,
            search_filter,
            _select=metric_functions,
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
