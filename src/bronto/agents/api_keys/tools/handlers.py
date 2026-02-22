from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import ApiKeyByIdInput, ApiKeyCreateInput, ApiKeyUpdateInput


class ApiKeysToolHandlers:
    """API key handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_api_keys(
        self,
    ) -> Annotated[
        list[dict[str, Any]],
        Field(description="List of API key objects returned by Bronto."),
    ]:
        return self.bronto_client.list_api_keys()

    def create_api_key(
        self,
        payload: Annotated[
            ApiKeyCreateInput,
            Field(description="Structured API key creation payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Created API key payload."),
    ]:
        return self.bronto_client.create_api_key(payload.model_dump(exclude_none=True))

    def update_api_key(
        self,
        payload: Annotated[
            ApiKeyUpdateInput,
            Field(description="Structured API key update payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Updated API key payload."),
    ]:
        body = payload.model_dump(exclude_none=True)
        api_key_id = body.pop("api_key_id")
        return self.bronto_client.update_api_key(api_key_id, body)

    def delete_api_key(
        self,
        payload: Annotated[
            ApiKeyByIdInput,
            Field(description="Structured payload containing api_key_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="API key deletion result."),
    ]:
        return self.bronto_client.delete_api_key(payload.api_key_id)
