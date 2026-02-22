from enum import Enum


class AccessAgentName(str, Enum):
    ACCESS = "access"


class AccessToolName(str, Enum):
    GRANT_ACCESS = "grant_access"
    REVOKE_ACCESS = "revoke_access"
    LIST_ACCESS_MEMBERS = "list_access_members"
    CHECK_ACCESS = "check_access"
    SWITCH_ACTIVE_ORGANIZATION = "switch_active_organization"
