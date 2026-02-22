from pydantic import BaseModel, Field

from ...base import AgentToolSpec
from ..enums import TerminalReportsToolName


class TerminalReportsAgentSpec(BaseModel):
    description: str = Field(
        default=(
            "Renders deterministic terminal-safe ASCII reports and validates output "
            "against strict formatting rules."
        )
    )
    tools: list[AgentToolSpec] = Field(
        default_factory=lambda: [
            AgentToolSpec(
                name=TerminalReportsToolName.RENDER_ASCII_TABLE.value,
                handler=TerminalReportsToolName.RENDER_ASCII_TABLE.value,
                description=(
                    "Render an ASCII table from structured rows/columns with deterministic widths and wrapping."
                ),
            ),
            AgentToolSpec(
                name=TerminalReportsToolName.VALIDATE_TERMINAL_REPORT.value,
                handler=TerminalReportsToolName.VALIDATE_TERMINAL_REPORT.value,
                description=(
                    "Validate terminal report text for markdown-table, unicode, ANSI, and width violations."
                ),
            ),
            AgentToolSpec(
                name=TerminalReportsToolName.TERMINAL_REPORT_PLAYBOOK.value,
                handler=TerminalReportsToolName.TERMINAL_REPORT_PLAYBOOK.value,
                description=(
                    "Playbook for deterministic terminal report flow: render, validate, then respond."
                ),
            ),
        ]
    )
