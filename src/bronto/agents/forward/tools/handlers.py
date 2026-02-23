from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import (
    ForwardConfigCreateInput,
    ForwardConfigDeleteInput,
    ForwardConfigTestInput,
    ForwardConfigUpdateInput,
)


class ForwardToolHandlers:
    """Forwarding handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_forward_configs(
        self,
    ) -> Annotated[
        list[dict[str, Any]],
        Field(description="List of forward configuration objects returned by Bronto."),
    ]:
        """List forward configurations.

        Returns
        -------
        list[dict[str, Any]]
            Forward configuration list response payload.
        """
        return self.bronto_client.list_forward_configs()

    def create_forward_config(
        self,
        payload: Annotated[
            ForwardConfigCreateInput,
            Field(description="Structured forward-config creation payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Created forward-config payload."),
    ]:
        """Create a forward configuration.

        Parameters
        ----------
        payload : ForwardConfigCreateInput
            Structured forward configuration creation input.

        Returns
        -------
        dict[str, Any]
            Created forward configuration response payload.
        """
        return self.bronto_client.create_forward_config(payload.payload)

    def update_forward_config(
        self,
        payload: Annotated[
            ForwardConfigUpdateInput,
            Field(description="Structured forward-config update payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Updated forward-config payload."),
    ]:
        """Update a forward configuration.

        Parameters
        ----------
        payload : ForwardConfigUpdateInput
            Structured forward configuration update input.

        Returns
        -------
        dict[str, Any]
            Updated forward configuration response payload.
        """
        return self.bronto_client.update_forward_config(
            payload.forward_config_id, payload.payload
        )

    def delete_forward_config(
        self,
        payload: Annotated[
            ForwardConfigDeleteInput,
            Field(description="Structured payload containing forward_config_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Forward-config deletion result."),
    ]:
        """Delete a forward configuration.

        Parameters
        ----------
        payload : ForwardConfigDeleteInput
            Structured payload containing a forward configuration ID.

        Returns
        -------
        dict[str, Any]
            Forward configuration deletion response payload.
        """
        return self.bronto_client.delete_forward_config(payload.forward_config_id)

    def test_forward_destination(
        self,
        payload: Annotated[
            ForwardConfigTestInput,
            Field(description="Structured forward destination test payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Forward destination test result payload."),
    ]:
        """Test a forward destination.

        Parameters
        ----------
        payload : ForwardConfigTestInput
            Structured forward destination test input.

        Returns
        -------
        dict[str, Any]
            Forward destination test response payload.
        """
        return self.bronto_client.test_forward_destination(payload.payload)
