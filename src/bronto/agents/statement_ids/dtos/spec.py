from pydantic import BaseModel, Field

from ...base import AgentKind, AgentToolSpec, ToolExecutionSpec
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
                    required_inputs=[],
                    expected_output="str",
                    notes="Use when injecting statement IDs into log statements.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.DEPLOY_STATEMENTS.value,
                handler=StatementIdsToolHandler.DEPLOY_STATEMENTS.value,
                kind=AgentKind.TOOL,
                description="Deploy a CSV mapping of statement IDs and log statements to Bronto.",
                execution=ToolExecutionSpec(
                    required_inputs=[
                        "csv_file_path",
                        "project_id",
                        "version",
                        "repo_url",
                    ],
                    expected_output="Dict",
                    notes="Publishes statement metadata for downstream usage.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.INJECT_STMT_IDS.value,
                handler=StatementIdsToolHandler.INJECT_STMT_IDS.value,
                kind=AgentKind.PROMPT,
                description="Prompt template explaining how to inject statement IDs in source files.",
                execution=ToolExecutionSpec(
                    required_inputs=["src_path"],
                    expected_output="str",
                    notes="Reference file for statement IDs defaults to statementIds.csv.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.EXTRACT_STMT_IDS.value,
                handler=StatementIdsToolHandler.EXTRACT_STMT_IDS.value,
                kind=AgentKind.PROMPT,
                description="Prompt template explaining how to extract statement IDs and write statementIds.csv.",
                execution=ToolExecutionSpec(
                    required_inputs=[],
                    expected_output="str",
                    notes="Can override output filename when needed.",
                ),
            ),
            AgentToolSpec(
                name=StatementIdsToolName.UPDATE_STMT_IDS.value,
                handler=StatementIdsToolHandler.UPDATE_STMT_IDS.value,
                kind=AgentKind.PROMPT,
                description="Prompt template for updating injected IDs and refreshing statementIds.csv.",
                execution=ToolExecutionSpec(
                    required_inputs=["src_path"],
                    expected_output="str",
                    notes="Combines inject and extract guidance.",
                ),
            ),
        ]
    )
