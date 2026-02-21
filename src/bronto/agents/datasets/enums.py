from enum import Enum


class DatasetsAgentName(str, Enum):
    DATASETS = "datasets"


class DatasetsToolName(str, Enum):
    GET_DATASETS = "get_datasets"
    GET_DATASETS_BY_NAME = "get_datasets_by_name"
    GET_KEYS = "get_keys"
    GET_ALL_DATASETS_KEYS = "get_all_datasets_keys"
    GET_KEY_VALUES = "get_key_values"
    DATASETS_PLAYBOOK = "datasets_playbook"


class DatasetsToolHandler(str, Enum):
    GET_DATASETS = "get_datasets"
    GET_DATASETS_BY_NAME = "get_datasets_by_name"
    GET_KEYS = "get_dataset_keys"
    GET_ALL_DATASETS_KEYS = "get_all_datasets_keys"
    GET_KEY_VALUES = "get_key_values"
    DATASETS_PLAYBOOK = "datasets_playbook"
