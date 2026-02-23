from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import (
    GroupByIdInput,
    GroupCreateInput,
    GroupMemberUpdateInput,
    GroupUpdateInput,
    MemberByIdInput,
)


class GroupsToolHandlers:
    """Group management handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_groups(
        self,
    ) -> Annotated[list[dict[str, Any]], Field(description="Groups list payload.")]:
        """List groups.

        Returns
        -------
        list[dict[str, Any]]
            Group list response payload.
        """
        return self.bronto_client.list_groups()

    def create_group(
        self,
        payload: Annotated[
            GroupCreateInput, Field(description="Group creation payload.")
        ],
    ) -> Annotated[dict[str, Any], Field(description="Created group payload.")]:
        """Create a group.

        Parameters
        ----------
        payload : GroupCreateInput
            Structured group creation payload.

        Returns
        -------
        dict[str, Any]
            Created group response payload.
        """
        return self.bronto_client.create_group(payload.payload)

    def get_group(
        self, payload: Annotated[GroupByIdInput, Field(description="Group ID payload.")]
    ) -> Annotated[dict[str, Any], Field(description="Group payload.")]:
        """Get group details by ID.

        Parameters
        ----------
        payload : GroupByIdInput
            Structured payload containing a group ID.

        Returns
        -------
        dict[str, Any]
            Group details response payload.
        """
        return self.bronto_client.get_group(payload.group_id)

    def update_group(
        self,
        payload: Annotated[
            GroupUpdateInput, Field(description="Group update payload.")
        ],
    ) -> Annotated[dict[str, Any], Field(description="Updated group payload.")]:
        """Update a group.

        Parameters
        ----------
        payload : GroupUpdateInput
            Structured group update payload.

        Returns
        -------
        dict[str, Any]
            Updated group response payload.
        """
        return self.bronto_client.update_group(payload.group_id, payload.payload)

    def delete_group(
        self, payload: Annotated[GroupByIdInput, Field(description="Group ID payload.")]
    ) -> Annotated[dict[str, Any], Field(description="Group deletion result.")]:
        """Delete a group.

        Parameters
        ----------
        payload : GroupByIdInput
            Structured payload containing a group ID.

        Returns
        -------
        dict[str, Any]
            Group deletion result payload.
        """
        return self.bronto_client.delete_group(payload.group_id)

    def list_group_members(
        self, payload: Annotated[GroupByIdInput, Field(description="Group ID payload.")]
    ) -> Annotated[dict[str, Any], Field(description="Group members payload.")]:
        """List group members.

        Parameters
        ----------
        payload : GroupByIdInput
            Structured payload containing a group ID.

        Returns
        -------
        dict[str, Any]
            Group members response payload.
        """
        return self.bronto_client.list_group_members(payload.group_id)

    def add_group_members(
        self,
        payload: Annotated[
            GroupMemberUpdateInput, Field(description="Group members add payload.")
        ],
    ) -> Annotated[dict[str, Any], Field(description="Group members add result.")]:
        """Add members to a group.

        Parameters
        ----------
        payload : GroupMemberUpdateInput
            Structured member update payload.

        Returns
        -------
        dict[str, Any]
            Add-members response payload.
        """
        return self.bronto_client.add_group_members(payload.group_id, payload.payload)

    def remove_group_members(
        self,
        payload: Annotated[
            GroupMemberUpdateInput, Field(description="Group members remove payload.")
        ],
    ) -> Annotated[dict[str, Any], Field(description="Group members remove result.")]:
        """Remove members from a group.

        Parameters
        ----------
        payload : GroupMemberUpdateInput
            Structured member update payload.

        Returns
        -------
        dict[str, Any]
            Remove-members response payload.
        """
        return self.bronto_client.remove_group_members(
            payload.group_id, payload.payload
        )

    def list_member_groups(
        self,
        payload: Annotated[MemberByIdInput, Field(description="Member ID payload.")],
    ) -> Annotated[dict[str, Any], Field(description="Member groups payload.")]:
        """List groups for a member.

        Parameters
        ----------
        payload : MemberByIdInput
            Structured payload containing a member ID.

        Returns
        -------
        dict[str, Any]
            Member groups response payload.
        """
        return self.bronto_client.list_member_groups(payload.member_id)
