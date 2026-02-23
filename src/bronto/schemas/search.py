from datetime import datetime, timezone
from typing import Annotated, Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _parse_timerange_to_unix_ms(value: Any) -> Any:
    """Parse timerange values to unix milliseconds.

    Parameters
    ----------
    value : Any
        Input value, int or datetime string.

    Returns
    -------
    Any
        Parsed unix milliseconds or original value.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        trimmed = value.strip()
        if not trimmed:
            return None
        if trimmed.isdigit():
            return int(trimmed)
        try:
            return int(
                datetime.strptime(trimmed, "%Y-%m-%d %H:%M:%S")
                .replace(tzinfo=timezone.utc)
                .timestamp()
                * 1000
            )
        except ValueError as exc:
            raise ValueError(
                "timerange values must be unix milliseconds or "
                'UTC datetime in "YYYY-MM-DD HH:mm:ss" format'
            ) from exc
    return value


class LogEvent(BaseModel):
    message: Annotated[
        str,
        Field(
            description="The message of the event. This represents a log message generated from a "
            "log statement in a piece of software"
        ),
    ]
    attributes: Annotated[
        Dict[str, str],
        Field(
            default_factory=dict,
            description="List of attributes associated to the log event. An attribute is a key-value "
            "pair that provide context about the event. For instance, "
            '"$hostname"="i-1234567890" may indicate that the service generated the log event'
            ' on the host named "i-1234567890"',
        ),
    ]

    def add_attribute(self, key: str, value: str) -> None:
        """Associate the key=value key-value pair to the log event. If the key is already associated to the log event,
        then the previously associated value is overwritten with the new one.
        """
        self.attributes.update({key: value})


class Datapoint(BaseModel):
    timestamp: Annotated[
        int, Field(description="The unix epoch timestamp of the datapoint")
    ]
    count: Annotated[
        int,
        Field(
            description="The number of events used to compute the metric value of the datapoint"
        ),
    ]
    quantiles: Annotated[
        Dict[float, float], Field(description="Map containing quantiles values")
    ]
    value: Annotated[
        float, Field(description="The value of the metric associated to the datapoint")
    ]


class Timeseries(BaseModel):
    count: Annotated[
        int,
        Field(
            description="The number of events used to compute the total metric value"
        ),
    ]
    timeseries: Annotated[
        List[Datapoint], Field(description="A list of datapoints per timestamp")
    ]


class SearchLogsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timerange_start: Optional[int] = Field(
        default=None,
        description=(
            "Unix timestamp in millisecond (or UTC datetime string "
            '"YYYY-MM-DD HH:mm:ss") representing the start of a time range, '
            "e.g. 1756063146000. If omitted, defaults to 20 minutes ago."
        ),
    )
    timerange_end: Optional[int] = Field(
        default=None,
        description=(
            "Unix timestamp in millisecond (or UTC datetime string "
            '"YYYY-MM-DD HH:mm:ss") representing the end of a time range, '
            "e.g. 1756063254000. If omitted, defaults to now."
        ),
    )
    log_ids: list[str] = Field(
        min_length=1,
        description="List of dataset IDs identifying sets of log data.",
    )
    search_filter: Optional[str] = Field(
        default="",
        description=(
            "Optional SQL-like WHERE filter. Key names should be double-quoted; "
            "string values single-quoted. Alias `filter` is also accepted."
        ),
    )
    limit: Optional[int] = Field(
        default=None,
        ge=1,
        description="Optional maximum number of events to return.",
    )

    @field_validator("timerange_start", "timerange_end", mode="before")
    @classmethod
    def _normalize_timerange_fields(cls, value: Any) -> Any:
        return _parse_timerange_to_unix_ms(value)

    @model_validator(mode="before")
    @classmethod
    def _normalize_filter_alias(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if "filter" in data:
            if "search_filter" not in data:
                data["search_filter"] = data["filter"]
            data.pop("filter", None)
        return data


class ComputeMetricsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timerange_start: Optional[int] = Field(
        default=None,
        description=(
            "Unix timestamp in millisecond (or UTC datetime string "
            '"YYYY-MM-DD HH:mm:ss") representing the start of a time range, '
            "e.g. 1756063146000. If omitted, defaults to 20 minutes ago."
        ),
    )
    timerange_end: Optional[int] = Field(
        default=None,
        description=(
            "Unix timestamp in millisecond (or UTC datetime string "
            '"YYYY-MM-DD HH:mm:ss") representing the end of a time range, '
            "e.g. 1756063254000. If omitted, defaults to now."
        ),
    )
    log_ids: list[str] = Field(
        min_length=1,
        description="List of dataset IDs identifying sets of log data.",
    )
    metric_functions: list[str] = Field(
        description=(
            "Metric functions such as AVG, MIN, MAX, COUNT(*), MEAN, MEDIAN, SUM."
        )
    )
    search_filter: str = Field(
        default="",
        description=(
            "Optional SQL-like WHERE filter. Key names should be double-quoted; "
            "string values single-quoted. Alias `filter` is also accepted."
        ),
    )
    group_by_keys: Optional[List[str]] = Field(
        default=None,
        description=(
            "Optional list of key names used to group computed metrics. "
            "A single comma-separated string is normalized to a list."
        ),
    )

    @field_validator("group_by_keys", mode="before")
    @classmethod
    def _normalize_group_by_keys(cls, value: Any) -> Optional[List[str]]:
        if value is None:
            return None
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        if isinstance(value, list):
            normalized: List[str] = []
            for item in value:
                if not isinstance(item, str):
                    raise ValueError("group_by_keys must contain only strings.")
                trimmed = item.strip()
                if trimmed:
                    normalized.append(trimmed)
            return normalized
        raise ValueError("group_by_keys must be a list of strings or a string.")

    @field_validator("timerange_start", "timerange_end", mode="before")
    @classmethod
    def _normalize_timerange_fields(cls, value: Any) -> Any:
        return _parse_timerange_to_unix_ms(value)

    @model_validator(mode="before")
    @classmethod
    def _normalize_filter_alias(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if "filter" in data:
            if "search_filter" not in data:
                data["search_filter"] = data["filter"]
            data.pop("filter", None)
        return data
