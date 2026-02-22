from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import StatementIdsToolName


class StatementIdsAgentSpec(BaseModel):
    description: str = Field(
        default="Generates and manages statement IDs and deployment workflows."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=StatementIdsToolName.CREATE_STMT_ID.value,
                handler=StatementIdsToolName.CREATE_STMT_ID.value,
                description="Generate a random 16-character statement ID.",
            ),
            AgentToolSpec(
                name=StatementIdsToolName.DEPLOY_STATEMENTS.value,
                handler=StatementIdsToolName.DEPLOY_STATEMENTS.value,
                description="Deploy a CSV mapping of statement IDs and log statements to Bronto.",
            ),
            AgentToolSpec(
                name=StatementIdsToolName.STATEMENT_IDS_PLAYBOOK.value,
                handler=StatementIdsToolName.STATEMENT_IDS_PLAYBOOK.value,
                description="Playbook for statement ID workflow, from injection to deployment.",
            ),
            AgentToolSpec(
                name=StatementIdsToolName.INJECT_STMT_IDS.value,
                handler=StatementIdsToolName.INJECT_STMT_IDS.value,
                description="Playbook template explaining how to inject statement IDs in source files.",
            ),
            AgentToolSpec(
                name=StatementIdsToolName.EXTRACT_STMT_IDS.value,
                handler=StatementIdsToolName.EXTRACT_STMT_IDS.value,
                description="Playbook template explaining how to extract statement IDs and write statementIds.csv.",
            ),
            AgentToolSpec(
                name=StatementIdsToolName.UPDATE_STMT_IDS.value,
                handler=StatementIdsToolName.UPDATE_STMT_IDS.value,
                description="Playbook template for updating injected IDs and refreshing statementIds.csv.",
            ),
        ]
    )
