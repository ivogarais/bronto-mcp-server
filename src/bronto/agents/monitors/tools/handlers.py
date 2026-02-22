from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import LogByIdInput


class MonitorsToolHandlers:
    bronto_client: BrontoClient

    def list_monitors_by_log(self, payload: Annotated[LogByIdInput, Field(description="Log ID payload.")]) -> Annotated[dict[str, Any], Field(description="Monitors payload.")]:
        return self.bronto_client.list_monitors_by_log(payload.log_id)
