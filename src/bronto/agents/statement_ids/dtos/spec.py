from pydantic import BaseModel, Field

from ...base import AgentToolSpec, ToolExecutionSpec


class StatementIdsAgentSpec(BaseModel):
    description: str = Field(
        default="Generates and manages statement IDs and deployment workflows."
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name="create_stmt_id",
                handler="create_stmt_id",
                kind="tool",
                description="Generate a random 16-character statement ID.",
                execution=ToolExecutionSpec(
                    required_inputs=[],
                    expected_output="str",
                    notes="Use when injecting statement IDs into log statements.",
                ),
            ),
            AgentToolSpec(
                name="deploy_statements",
                handler="deploy_statements",
                kind="tool",
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
                name="inject_stmt_ids",
                handler="inject_stmt_ids",
                kind="prompt",
                description="Prompt template explaining how to inject statement IDs in source files.",
                execution=ToolExecutionSpec(
                    required_inputs=["src_path"],
                    expected_output="str",
                    notes="Reference file for statement IDs defaults to statementIds.csv.",
                ),
            ),
            AgentToolSpec(
                name="extract_stmt_ids",
                handler="extract_stmt_ids",
                kind="prompt",
                description="Prompt template explaining how to extract statement IDs and write statementIds.csv.",
                execution=ToolExecutionSpec(
                    required_inputs=[],
                    expected_output="str",
                    notes="Can override output filename when needed.",
                ),
            ),
            AgentToolSpec(
                name="update_stmt_ids",
                handler="update_stmt_ids",
                kind="prompt",
                description="Prompt template for updating injected IDs and refreshing statementIds.csv.",
                execution=ToolExecutionSpec(
                    required_inputs=["src_path"],
                    expected_output="str",
                    notes="Combines inject and extract guidance.",
                ),
            ),
        ]
    )
