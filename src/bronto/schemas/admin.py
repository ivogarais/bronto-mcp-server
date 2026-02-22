from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ApiKeyCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, description="API key display name.")
    roles: list[str] = Field(
        min_length=1, description="Role identifiers assigned to this API key."
    )
    tags: dict[str, str] = Field(
        default_factory=dict,
        description="Optional key-value tags.",
    )
    expires_at: int | None = Field(
        default=None,
        description="Expiration time as Unix timestamp. If omitted, key does not expire.",
    )


class ApiKeyByIdInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key_id: str = Field(min_length=1, description="API key ID.")


class ApiKeyUpdateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key_id: str = Field(min_length=1, description="API key ID.")
    name: str | None = Field(default=None, description="Updated API key name.")
    roles: list[str] | None = Field(default=None, description="Updated role IDs.")
    tags: dict[str, str] | None = Field(default=None, description="Updated tags.")
    expires_at: int | None = Field(
        default=None,
        description="Updated expiration timestamp.",
    )


class UserCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str = Field(min_length=1, description="User first name.")
    last_name: str = Field(min_length=1, description="User last name.")
    email: str = Field(min_length=1, description="User email.")
    roles: list[str] = Field(min_length=1, description="Role identifiers for this user.")
    tags: dict[str, str] = Field(default_factory=dict, description="Optional tags.")
    login_methods: list[str] | None = Field(
        default=None, description="Optional login method identifiers."
    )


class UserByIdInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(min_length=1, description="User ID.")


class UserUpdateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(min_length=1, description="User ID.")
    first_name: str | None = Field(default=None, description="Updated first name.")
    last_name: str | None = Field(default=None, description="Updated last name.")
    email: str | None = Field(default=None, description="Updated email.")
    roles: list[str] | None = Field(default=None, description="Updated role IDs.")
    tags: dict[str, str] | None = Field(default=None, description="Updated tags.")
    login_methods: list[str] | None = Field(
        default=None, description="Updated login method identifiers."
    )


class UserPreferencesUpdateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(min_length=1, description="User ID.")
    payload: dict[str, Any] = Field(description="User preferences update payload.")


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


class ExportCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(
        description="Raw export creation payload as defined by Bronto exports API."
    )


class ForwardConfigCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(
        description="Raw forward-config creation payload."
    )


class ForwardConfigUpdateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    forward_config_id: str = Field(min_length=1, description="Forward config ID.")
    payload: dict[str, Any] = Field(description="Forward config update payload.")


class ForwardConfigDeleteInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    forward_config_id: str = Field(min_length=1, description="Forward config ID.")


class ForwardConfigTestInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(
        description="Forward destination connectivity test payload."
    )


class LogCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    log: str = Field(min_length=1, description="Log (dataset) name.")
    logset: str = Field(min_length=1, description="Collection name.")
    tags: dict[str, str] = Field(default_factory=dict, description="Optional tags.")


class SearchStatusInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status_id: str = Field(
        min_length=1, description="Search status ID returned by async search execution."
    )
