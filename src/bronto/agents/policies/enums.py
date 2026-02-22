from enum import Enum


class PoliciesAgentName(str, Enum):
    POLICIES = "policies"


class PoliciesToolName(str, Enum):
    LIST_POLICIES_BY_RESOURCE = "list_policies_by_resource"
