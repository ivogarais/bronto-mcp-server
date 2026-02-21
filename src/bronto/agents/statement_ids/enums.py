from enum import Enum


class StatementIdsAgentName(str, Enum):
    STATEMENT_IDS = "statement_ids"


class StatementIdsToolName(str, Enum):
    CREATE_STMT_ID = "create_stmt_id"
    DEPLOY_STATEMENTS = "deploy_statements"
    STATEMENT_IDS_PLAYBOOK = "statement_ids_playbook"
    INJECT_STMT_IDS = "inject_stmt_ids"
    EXTRACT_STMT_IDS = "extract_stmt_ids"
    UPDATE_STMT_IDS = "update_stmt_ids"
