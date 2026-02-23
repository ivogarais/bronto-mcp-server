from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import ExportByIdInput, ExportCreateInput


class ExportsToolHandlers:
    """Export handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_exports(
        self,
    ) -> Annotated[
        list[dict[str, Any]],
        Field(description="List of export jobs returned by Bronto."),
    ]:
        """List export jobs.

        Returns
        -------
        list[dict[str, Any]]
            Export list response payload.
        """
        return self.bronto_client.list_exports()

    def create_export(
        self,
        payload: Annotated[
            ExportCreateInput,
            Field(description="Structured export creation payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Created export payload."),
    ]:
        """Create an export job.

        Parameters
        ----------
        payload : ExportCreateInput
            Structured export creation payload.

        Returns
        -------
        dict[str, Any]
            Created export response payload.
        """
        return self.bronto_client.create_export(payload.payload)

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
        """Get export job details.

        Parameters
        ----------
        payload : ExportByIdInput
            Structured payload containing an export ID.

        Returns
        -------
        dict[str, Any]
            Export details response payload.
        """
        return self.bronto_client.get_export(payload.export_id)

    def delete_export(
        self,
        payload: Annotated[
            ExportByIdInput,
            Field(description="Structured payload containing export_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Export deletion result."),
    ]:
        """Delete an export job.

        Parameters
        ----------
        payload : ExportByIdInput
            Structured payload containing an export ID.

        Returns
        -------
        dict[str, Any]
            Export deletion response payload.
        """
        return self.bronto_client.delete_export(payload.export_id)
