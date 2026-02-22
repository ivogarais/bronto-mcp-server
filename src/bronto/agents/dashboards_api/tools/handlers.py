from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import LogByIdInput


class DashboardsApiToolHandlers:
    bronto_client: BrontoClient

    def list_dashboards_by_log(self, payload: Annotated[LogByIdInput, Field(description="Log ID payload.")]) -> Annotated[dict[str, Any], Field(description="Dashboards payload.")]:
        return self.bronto_client.list_dashboards_by_log(payload.log_id)
