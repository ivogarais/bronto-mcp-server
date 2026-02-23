from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import LogByIdInput


class DashboardsApiToolHandlers:
    """Dashboard API handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_dashboards_by_log(
        self, payload: Annotated[LogByIdInput, Field(description="Log ID payload.")]
    ) -> Annotated[dict[str, Any], Field(description="Dashboards payload.")]:
        """List dashboards bound to a log ID.

        Parameters
        ----------
        payload : LogByIdInput
            Structured payload containing the target log ID.

        Returns
        -------
        dict[str, Any]
            Dashboard list response payload.
        """
        return self.bronto_client.list_dashboards_by_log(payload.log_id)
