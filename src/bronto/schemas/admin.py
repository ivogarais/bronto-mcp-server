from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ApiKeyCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, description="API key display name.")
    roles: list[str] | None = Field(
        default=None,
        description="Role identifiers assigned to this API key.",
    )
    tags: dict[str, str] = Field(
        default_factory=dict,
        description="Optional key-value tags.",
    )
    expires_at: int | None = Field(
        default=None,
        description="Expiration time as Unix timestamp. If omitted, key does not expire.",
    )

    @model_validator(mode="before")
    @classmethod
    def _coerce_nested_payload(cls, value: Any) -> Any:
        # Backward compatibility: allow {"payload": {...}} wrapper.
        if isinstance(value, dict) and "payload" in value and isinstance(
            value["payload"], dict
        ):
            merged = dict(value["payload"])
            for key, item in value.items():
                if key != "payload":
                    merged[key] = item
            return merged
        return value


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


class GroupByIdInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    group_id: str = Field(min_length=1, description="Group ID.")


class GroupCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(description="Group creation payload.")

    @model_validator(mode="before")
    @classmethod
    def _coerce_direct_payload(cls, value: Any) -> Any:
        # Backward compatibility: allow direct shape {"name": "..."} as payload.
        if isinstance(value, dict) and "payload" not in value:
            return {"payload": value}
        return value


class GroupUpdateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    group_id: str = Field(min_length=1, description="Group ID.")
    payload: dict[str, Any] = Field(description="Group update payload.")


class GroupMemberUpdateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    group_id: str = Field(min_length=1, description="Group ID.")
    payload: dict[str, Any] = Field(description="Group members update payload.")


class MemberByIdInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    member_id: str = Field(min_length=1, description="Member ID.")


class LogByIdInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    log_id: str = Field(min_length=1, description="Log ID.")


class AccessGrantInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(description="Access grant payload.")


class AccessRevokeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(description="Access revoke payload.")


class AccessCheckInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(description="Access check query parameters.")


class AccessSwitchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(description="Active organization switch payload.")


class TagByNameInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tag_name: str = Field(min_length=1, description="Tag name.")


class TagCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(description="Tag creation payload.")


class TagUpdateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tag_name: str = Field(min_length=1, description="Tag name.")
    payload: dict[str, Any] = Field(description="Tag update payload.")


class ParsersUsageQueryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(
        description="Parser usage query parameters as defined by Bronto API."
    )


class PolicyByResourceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(
        description="Policy query parameters for identifying target resource."
    )


class EncryptionKeyByIdInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    encryption_key_id: str = Field(min_length=1, description="Encryption key ID.")


class EncryptionKeyCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(description="Encryption key creation payload.")


class EncryptionKeyUpdateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    encryption_key_id: str = Field(min_length=1, description="Encryption key ID.")
    payload: dict[str, Any] = Field(description="Encryption key update payload.")
