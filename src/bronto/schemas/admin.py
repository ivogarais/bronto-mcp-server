from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ExportByIdInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    export_id: str = Field(
        min_length=1,
        description="Export job ID.",
    )


class ContextQueryInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    from_: str | None = Field(
        default=None,
        alias="from",
        description="Dataset identifier or query scope expression for context retrieval.",
    )
    from_tags: str | None = Field(
        default=None,
        description="Optional from-tags selector expression.",
    )
    from_expr: str | None = Field(
        default=None,
        description="Optional advanced from expression.",
    )
    sequence: int | None = Field(
        default=None,
        description="Sequence number of the anchor event.",
    )
    timestamp: int | None = Field(
        default=None,
        description="Anchor timestamp in milliseconds since epoch.",
    )
    direction: str | None = Field(
        default=None,
        description="Direction selector (before/after/both).",
    )
    limit: int | None = Field(
        default=None,
        ge=1,
        le=1000,
        description="Maximum number of context events to return.",
    )
    include_explain: bool | None = Field(
        default=None,
        alias="explain",
        description="Whether to include explain metadata in response.",
    )


class UsageQueryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time_range: str | None = Field(default=None, description="Named time range, e.g. 24h.")
    from_ts: int | None = Field(default=None, description="Start timestamp in ms.")
    to_ts: int | None = Field(default=None, description="End timestamp in ms.")
    usage_type: str | None = Field(default=None, description="Usage type selector.")
    limit: int | None = Field(
        default=None, ge=1, le=1000, description="Maximum rows returned."
    )
    num_of_slices: int | None = Field(
        default=None, ge=1, le=200, description="Number of timeseries slices."
    )
    metric: str | None = Field(default=None, description="Metric name to aggregate.")
    delta: bool | None = Field(
        default=None, description="Whether to compute delta metrics."
    )
    delta_time_range: str | None = Field(
        default=None, description="Baseline named time range for delta."
    )
    delta_from_ts: int | None = Field(
        default=None, description="Baseline start timestamp in ms."
    )
    delta_to_ts: int | None = Field(
        default=None, description="Baseline end timestamp in ms."
    )
