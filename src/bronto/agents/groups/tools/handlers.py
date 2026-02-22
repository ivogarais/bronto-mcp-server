from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import GroupByIdInput, GroupCreateInput, GroupMemberUpdateInput, GroupUpdateInput, MemberByIdInput


class GroupsToolHandlers:
    bronto_client: BrontoClient

    def list_groups(self) -> Annotated[list[dict[str, Any]], Field(description="Groups list payload.")]:
        return self.bronto_client.list_groups()

    def create_group(self, payload: Annotated[GroupCreateInput, Field(description="Group creation payload.")]) -> Annotated[dict[str, Any], Field(description="Created group payload.")]:
        return self.bronto_client.create_group(payload.payload)

    def get_group(self, payload: Annotated[GroupByIdInput, Field(description="Group ID payload.")]) -> Annotated[dict[str, Any], Field(description="Group payload.")]:
        return self.bronto_client.get_group(payload.group_id)

    def update_group(self, payload: Annotated[GroupUpdateInput, Field(description="Group update payload.")]) -> Annotated[dict[str, Any], Field(description="Updated group payload.")]:
        return self.bronto_client.update_group(payload.group_id, payload.payload)

    def delete_group(self, payload: Annotated[GroupByIdInput, Field(description="Group ID payload.")]) -> Annotated[dict[str, Any], Field(description="Group deletion result.")]:
        return self.bronto_client.delete_group(payload.group_id)

    def list_group_members(self, payload: Annotated[GroupByIdInput, Field(description="Group ID payload.")]) -> Annotated[dict[str, Any], Field(description="Group members payload.")]:
        return self.bronto_client.list_group_members(payload.group_id)

    def add_group_members(self, payload: Annotated[GroupMemberUpdateInput, Field(description="Group members add payload.")]) -> Annotated[dict[str, Any], Field(description="Group members add result.")]:
        return self.bronto_client.add_group_members(payload.group_id, payload.payload)

    def remove_group_members(self, payload: Annotated[GroupMemberUpdateInput, Field(description="Group members remove payload.")]) -> Annotated[dict[str, Any], Field(description="Group members remove result.")]:
        return self.bronto_client.remove_group_members(payload.group_id, payload.payload)

    def list_member_groups(self, payload: Annotated[MemberByIdInput, Field(description="Member ID payload.")]) -> Annotated[dict[str, Any], Field(description="Member groups payload.")]:
        return self.bronto_client.list_member_groups(payload.member_id)
