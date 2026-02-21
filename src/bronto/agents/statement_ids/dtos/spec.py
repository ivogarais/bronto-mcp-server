from pydantic import BaseModel, Field

from ...base import (
    AgentKind,
    AgentToolSpec,
    ToolExecutionSpec,
    ToolInputSpec,
    ToolOutputSpec,
)
from ..enums import StatementIdsToolHandler, StatementIdsToolName


class StatementIdsAgentSpec(BaseModel):
    description: str = Field(
        default="Generates and manages statement IDs and deployment workflows."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=StatementIdsToolName.CREATE_STMT_ID.value,
                handler=StatementIdsToolHandler.CREATE_STMT_ID.value,
                kind=AgentKind.TOOL,
                description="Generate a random 16-character statement ID.",
                execution=ToolExecutionSpec(
                    output=ToolOutputSpec(value_type=str),
                    notes="Use when injecting statement IDs into log statements.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.DEPLOY_STATEMENTS.value,
                handler=StatementIdsToolHandler.DEPLOY_STATEMENTS.value,
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
                name=StatementIdsToolName.INJECT_STMT_IDS.value,
                handler=StatementIdsToolHandler.INJECT_STMT_IDS.value,
                kind=AgentKind.PROMPT,
                description="Prompt template explaining how to inject statement IDs in source files.",
                execution=ToolExecutionSpec(
                    inputs=[ToolInputSpec(name="src_path", value_type=str)],
                    output=ToolOutputSpec(value_type=str),
                    notes="Reference file for statement IDs defaults to statementIds.csv.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.EXTRACT_STMT_IDS.value,
                handler=StatementIdsToolHandler.EXTRACT_STMT_IDS.value,
                kind=AgentKind.PROMPT,
                description="Prompt template explaining how to extract statement IDs and write statementIds.csv.",
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
                handler=StatementIdsToolHandler.UPDATE_STMT_IDS.value,
                kind=AgentKind.PROMPT,
                description="Prompt template for updating injected IDs and refreshing statementIds.csv.",
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
