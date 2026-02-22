from enum import Enum


class TagsAgentName(str, Enum):
    TAGS = "tags"


class TagsToolName(str, Enum):
    LIST_TAGS = "list_tags"
    CREATE_TAG = "create_tag"
    UPDATE_TAG = "update_tag"
    DELETE_TAG = "delete_tag"
