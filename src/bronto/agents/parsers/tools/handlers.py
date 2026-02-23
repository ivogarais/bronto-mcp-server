from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import ParsersUsageQueryInput


class ParsersToolHandlers:
    """Parser usage handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def get_parsers_usage_for_log_id(
        self,
        payload: Annotated[
            ParsersUsageQueryInput,
            Field(description="Parser usage-by-log query payload."),
        ],
    ) -> Annotated[dict[str, Any], Field(description="Parser usage payload.")]:
        """Get parser usage aggregated by log ID.

        Parameters
        ----------
        payload : ParsersUsageQueryInput
            Structured parser usage query payload.

        Returns
        -------
        dict[str, Any]
            Parser usage response payload.
        """
        return self.bronto_client.get_parsers_usage_for_log_id(payload.payload)

    def get_parsers_usage_for_user_per_log_id(
        self,
        payload: Annotated[
            ParsersUsageQueryInput,
            Field(description="Parser usage-by-user query payload."),
        ],
    ) -> Annotated[dict[str, Any], Field(description="Parser usage-by-user payload.")]:
        """Get parser usage aggregated by user for a log ID.

        Parameters
        ----------
        payload : ParsersUsageQueryInput
            Structured parser usage query payload.

        Returns
        -------
        dict[str, Any]
            Parser usage-by-user response payload.
        """
        return self.bronto_client.get_parsers_usage_for_user_per_log_id(payload.payload)
