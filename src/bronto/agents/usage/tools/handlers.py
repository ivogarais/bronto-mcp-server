from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import UsageQueryInput


class UsageToolHandlers:
    """Usage analytics handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def get_usage_for_log_id(
        self,
        payload: Annotated[
            UsageQueryInput,
            Field(
                description=(
                    "Usage query payload for log-ID aggregation. "
                    "Includes optional window, metric, and delta fields."
                )
            ),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Usage payload grouped by log ID."),
    ]:
        """Get usage grouped by log ID.

        Parameters
        ----------
        payload : UsageQueryInput
            Structured usage query input.

        Returns
        -------
        dict[str, Any]
            Usage response payload grouped by log ID.
        """
        return self.bronto_client.get_usage_for_log_id(
            time_range=payload.time_range,
            from_ts=payload.from_ts,
            to_ts=payload.to_ts,
            usage_type=payload.usage_type,
            limit=payload.limit,
            num_of_slices=payload.num_of_slices,
            metric=payload.metric,
            delta=payload.delta,
            delta_time_range=payload.delta_time_range,
            delta_from_ts=payload.delta_from_ts,
            delta_to_ts=payload.delta_to_ts,
        )

    def get_usage_for_user_per_log_id(
        self,
        payload: Annotated[
            UsageQueryInput,
            Field(
                description=(
                    "Usage query payload for user-per-log aggregation. "
                    "Includes optional window, metric, and delta fields."
                )
            ),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Usage payload grouped by user and log ID."),
    ]:
        """Get usage grouped by user per log ID.

        Parameters
        ----------
        payload : UsageQueryInput
            Structured usage query input.

        Returns
        -------
        dict[str, Any]
            Usage response payload grouped by user and log ID.
        """
        return self.bronto_client.get_usage_for_user_per_log_id(
            time_range=payload.time_range,
            from_ts=payload.from_ts,
            to_ts=payload.to_ts,
            usage_type=payload.usage_type,
            limit=payload.limit,
            num_of_slices=payload.num_of_slices,
            metric=payload.metric,
            delta=payload.delta,
            delta_time_range=payload.delta_time_range,
            delta_from_ts=payload.delta_from_ts,
            delta_to_ts=payload.delta_to_ts,
        )
