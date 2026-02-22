from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient


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
