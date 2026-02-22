from typing import Any, Dict, List

from pydantic import Field
from typing_extensions import Annotated

from bronto.agents.playbooks import resolve_playbook
from ..dtos import (
    AsciiTableRenderResult,
    RenderAsciiTableInput,
    TerminalReportValidationResult,
    ValidateTerminalReportInput,
)
from .ascii_table import render_ascii_table, validate_terminal_report


class TerminalReportsToolHandlers:
    """Terminal report rendering and validation handlers."""

    @staticmethod
    def render_ascii_table(
        columns: Annotated[
            List[str],
            Field(
                description="Ordered table column names.",
                min_length=1,
            ),
        ],
        rows: Annotated[
            List[Dict[str, Any]],
            Field(
                description=(
                    "Row objects keyed by column name. Missing keys are rendered as empty cells."
                )
            ),
        ],
        max_width: Annotated[
            int,
            Field(
                description="Maximum terminal width used to render wrapped table lines.",
                ge=40,
                le=180,
            ),
        ] = 100,
    ) -> Annotated[
        AsciiTableRenderResult,
        Field(
            description="Rendered ASCII table plus metadata (line count, rows, columns)."
        ),
    ]:
        input_spec = RenderAsciiTableInput(
            columns=columns,
            rows=rows,
            max_width=max_width,
        )
        table = render_ascii_table(
            input_spec.columns,
            input_spec.rows,
            max_width=input_spec.max_width,
        )
        return AsciiTableRenderResult(
            table=table,
            line_count=len(table.splitlines()),
            column_count=len(input_spec.columns),
            row_count=len(input_spec.rows),
        )

    @staticmethod
    def validate_terminal_report(
        text: Annotated[
            str,
            Field(description="Report text to validate for terminal-safe output."),
        ],
        max_width: Annotated[
            int,
            Field(
                description="Maximum terminal width to enforce on each line.",
                ge=40,
                le=180,
            ),
        ] = 100,
    ) -> Annotated[
        TerminalReportValidationResult,
        Field(
            description=(
                "Validation result with success flag and detailed formatting violations."
            )
        ),
    ]:
        input_spec = ValidateTerminalReportInput(text=text, max_width=max_width)
        valid, violations, line_count = validate_terminal_report(
            input_spec.text, max_width=input_spec.max_width
        )
        return TerminalReportValidationResult(
            valid=valid,
            violations=violations,
            line_count=line_count,
        )

    @staticmethod
    def terminal_report_playbook() -> Annotated[
        str,
        Field(
            description=(
                "Playbook for deterministic terminal report generation and validation flow."
            )
        ),
    ]:
        return resolve_playbook(
            "bronto.agents.terminal_reports",
            "playbooks/terminal_report_playbook.md",
        )
