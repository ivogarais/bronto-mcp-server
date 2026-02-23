from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import PolicyByResourceInput


class PoliciesToolHandlers:
    """Policy handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_policies_by_resource(
        self,
        payload: Annotated[
            PolicyByResourceInput, Field(description="Policy resource query payload.")
        ],
    ) -> Annotated[dict[str, Any], Field(description="Policies payload.")]:
        """List policies attached to a resource.

        Parameters
        ----------
        payload : PolicyByResourceInput
            Structured resource query payload.

        Returns
        -------
        dict[str, Any]
            Policy list response payload.
        """
        return self.bronto_client.list_policies_by_resource(payload.payload)
