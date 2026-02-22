from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import (
    UserByIdInput,
    UserCreateInput,
    UserPreferencesUpdateInput,
    UserUpdateInput,
)


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

    def create_user(
        self,
        payload: Annotated[
            UserCreateInput,
            Field(description="Structured user creation payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Created user payload."),
    ]:
        return self.bronto_client.create_user(payload.model_dump())

    def get_user_by_id(
        self,
        payload: Annotated[
            UserByIdInput,
            Field(description="Structured payload containing user_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="User payload."),
    ]:
        return self.bronto_client.get_user_by_id(payload.user_id)

    def update_user(
        self,
        payload: Annotated[
            UserUpdateInput,
            Field(description="Structured user update payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Updated user payload."),
    ]:
        body = payload.model_dump(exclude_none=True)
        user_id = body.pop("user_id")
        return self.bronto_client.update_user(user_id, body)

    def delete_user(
        self,
        payload: Annotated[
            UserByIdInput,
            Field(description="Structured payload containing user_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="User deletion result."),
    ]:
        return self.bronto_client.delete_user(payload.user_id)

    def deactivate_user(
        self,
        payload: Annotated[
            UserByIdInput,
            Field(description="Structured payload containing user_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="User deactivation result."),
    ]:
        return self.bronto_client.deactivate_user(payload.user_id)

    def reactivate_user(
        self,
        payload: Annotated[
            UserByIdInput,
            Field(description="Structured payload containing user_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="User reactivation result."),
    ]:
        return self.bronto_client.reactivate_user(payload.user_id)

    def resend_user_invitation(
        self,
        payload: Annotated[
            UserByIdInput,
            Field(description="Structured payload containing user_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="User invitation resend result."),
    ]:
        return self.bronto_client.resend_user_invitation(payload.user_id)

    def get_user_preferences(
        self,
        payload: Annotated[
            UserByIdInput,
            Field(description="Structured payload containing user_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="User preferences payload."),
    ]:
        return self.bronto_client.get_user_preferences(payload.user_id)

    def update_user_preferences(
        self,
        payload: Annotated[
            UserPreferencesUpdateInput,
            Field(description="Structured user preferences update payload."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Updated user preferences payload."),
    ]:
        return self.bronto_client.update_user_preferences(payload.user_id, payload.payload)

    def get_user_organizations(
        self,
        payload: Annotated[
            UserByIdInput,
            Field(description="Structured payload containing user_id."),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="User organizations payload."),
    ]:
        return self.bronto_client.get_user_organizations(payload.user_id)
