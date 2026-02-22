from enum import Enum


class ForwardAgentName(str, Enum):
    FORWARD = "forward"


class ForwardToolName(str, Enum):
    LIST_FORWARD_CONFIGS = "list_forward_configs"
    CREATE_FORWARD_CONFIG = "create_forward_config"
    UPDATE_FORWARD_CONFIG = "update_forward_config"
    DELETE_FORWARD_CONFIG = "delete_forward_config"
    TEST_FORWARD_DESTINATION = "test_forward_destination"
