from enum import Enum


class GroupsAgentName(str, Enum):
    GROUPS = "groups"


class GroupsToolName(str, Enum):
    LIST_GROUPS = "list_groups"
    CREATE_GROUP = "create_group"
    GET_GROUP = "get_group"
    UPDATE_GROUP = "update_group"
    DELETE_GROUP = "delete_group"
    LIST_GROUP_MEMBERS = "list_group_members"
    ADD_GROUP_MEMBERS = "add_group_members"
    REMOVE_GROUP_MEMBERS = "remove_group_members"
    LIST_MEMBER_GROUPS = "list_member_groups"
