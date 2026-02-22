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
        return self.bronto_client.test_forward_destination(payload.payload)
