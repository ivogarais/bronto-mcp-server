from enum import Enum


class UsersAgentName(str, Enum):
    USERS = "users"


class UsersToolName(str, Enum):
    LIST_USERS = "list_users"
