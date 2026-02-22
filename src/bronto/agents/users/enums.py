from enum import Enum


class UsersAgentName(str, Enum):
    USERS = "users"


class UsersToolName(str, Enum):
    LIST_USERS = "list_users"
    CREATE_USER = "create_user"
    GET_USER_BY_ID = "get_user_by_id"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    DEACTIVATE_USER = "deactivate_user"
    REACTIVATE_USER = "reactivate_user"
    RESEND_USER_INVITATION = "resend_user_invitation"
    GET_USER_PREFERENCES = "get_user_preferences"
    UPDATE_USER_PREFERENCES = "update_user_preferences"
    GET_USER_ORGANIZATIONS = "get_user_organizations"
