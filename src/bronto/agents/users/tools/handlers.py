from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient


class UsersToolHandlers:
    """User handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_users(
        self,
    ) -> Annotated[
        list[dict[str, Any]],
        Field(description="List of users returned by Bronto."),
    ]:
        return self.bronto_client.list_users()
