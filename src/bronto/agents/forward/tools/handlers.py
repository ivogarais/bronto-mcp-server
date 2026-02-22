from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient


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
