from pydantic import Field

from .base import AgentToolSpec, BrontoAgent


class StatementIdsAgent(BrontoAgent):
    name: str = Field(default="statement_ids")
    description: str = Field(
        default=(
            "Manages statement IDs in source code, including generation, extraction guidance, and deployment."
        )
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(name="create_stmt_id", handler="create_stmt_id"),
            AgentToolSpec(name="deploy_statements", handler="deploy_statements"),
            AgentToolSpec(
                name="inject_stmt_ids", handler="inject_stmt_ids", kind="prompt"
            ),
            AgentToolSpec(
                name="extract_stmt_ids", handler="extract_stmt_ids", kind="prompt"
            ),
            AgentToolSpec(
                name="update_stmt_ids", handler="update_stmt_ids", kind="prompt"
            ),
        ]
    )
