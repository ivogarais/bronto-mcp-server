from pydantic import BaseModel, Field

from ...base import (
    AgentKind,
    AgentToolSpec,
    ToolExecutionSpec,
    ToolInputSpec,
    ToolOutputSpec,
)
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
                kind=AgentKind.TOOL,
                description="Generate a random 16-character statement ID.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=str),
                    notes="Use when injecting statement IDs into log statements.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.DEPLOY_STATEMENTS.value,
                handler=StatementIdsToolName.DEPLOY_STATEMENTS.value,
                kind=AgentKind.TOOL,
                description="Deploy a CSV mapping of statement IDs and log statements to Bronto.",
                execution=ToolExecutionSpec(
                    inputs=[
                        ToolInputSpec(name="csv_file_path", value_type=str),
                        ToolInputSpec(name="project_id", value_type=str),
                        ToolInputSpec(name="version", value_type=str),
                        ToolInputSpec(name="repo_url", value_type=str),
                    ],
                    output=ToolOutputSpec(value_type=dict[str, bool]),
                    notes="Publishes statement metadata for downstream usage.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.STATEMENT_IDS_PLAYBOOK.value,
                handler=StatementIdsToolName.STATEMENT_IDS_PLAYBOOK.value,
                kind=AgentKind.TOOL,
                description="Playbook for statement ID workflow, from injection to deployment.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=str),
                    notes="On-demand overview for statement ID lifecycle tasks.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.INJECT_STMT_IDS.value,
                handler=StatementIdsToolName.INJECT_STMT_IDS.value,
                kind=AgentKind.TOOL,
                description="Playbook template explaining how to inject statement IDs in source files.",
                execution=ToolExecutionSpec(
                    inputs=[ToolInputSpec(name="src_path", value_type=str)],
                    output=ToolOutputSpec(value_type=str),
                    notes="Reference file for statement IDs defaults to statementIds.csv.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.EXTRACT_STMT_IDS.value,
                handler=StatementIdsToolName.EXTRACT_STMT_IDS.value,
                kind=AgentKind.TOOL,
                description="Playbook template explaining how to extract statement IDs and write statementIds.csv.",
                execution=ToolExecutionSpec(
                    inputs=[
                        ToolInputSpec(
                            name="stmt_id_filepath",
                            value_type=str,
                            required=False,
                        )
                    ],
                    output=ToolOutputSpec(value_type=str),
                    notes="Can override output filename when needed.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.UPDATE_STMT_IDS.value,
                handler=StatementIdsToolName.UPDATE_STMT_IDS.value,
                kind=AgentKind.TOOL,
                description="Playbook template for updating injected IDs and refreshing statementIds.csv.",
                execution=ToolExecutionSpec(
                    inputs=[
                        ToolInputSpec(name="src_path", value_type=str),
                        ToolInputSpec(
                            name="stmt_id_filepath",
                            value_type=str,
                            required=False,
                        ),
                    ],
                    output=ToolOutputSpec(value_type=str),
                    notes="Combines inject and extract guidance.",
                ),
            ),
        ]
    )
