from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import AccessCheckInput, AccessGrantInput, AccessRevokeInput, AccessSwitchInput


class AccessToolHandlers:
    bronto_client: BrontoClient

    def grant_access(self, payload: Annotated[AccessGrantInput, Field(description="Access grant payload.")]) -> Annotated[dict[str, Any], Field(description="Access grant result.")]:
        return self.bronto_client.grant_access(payload.payload)

    def revoke_access(self, payload: Annotated[AccessRevokeInput, Field(description="Access revoke payload.")]) -> Annotated[dict[str, Any], Field(description="Access revoke result.")]:
        return self.bronto_client.revoke_access(payload.payload)

    def list_access_members(self) -> Annotated[dict[str, Any], Field(description="Access members payload.")]:
        return self.bronto_client.list_access_members()

    def check_access(self, payload: Annotated[AccessCheckInput, Field(description="Access check payload.")]) -> Annotated[dict[str, Any], Field(description="Access check result.")]:
        return self.bronto_client.check_access(payload.payload)

    def switch_active_organization(self, payload: Annotated[AccessSwitchInput, Field(description="Organization switch payload.")]) -> Annotated[dict[str, Any], Field(description="Organization switch result.")]:
        return self.bronto_client.switch_active_organization(payload.payload)
