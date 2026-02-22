from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import ExportByIdInput


class ExportsToolHandlers:
    """Export handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_exports(
        self,
    ) -> Annotated[
        list[dict[str, Any]],
        Field(description="List of export jobs returned by Bronto."),
    ]:
        return self.bronto_client.list_exports()

    def get_export(
        self,
        payload: Annotated[
            ExportByIdInput,
            Field(description="Structured payload containing export_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Export job details payload."),
    ]:
        return self.bronto_client.get_export(payload.export_id)
