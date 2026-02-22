from typing import Any

from pydantic import BaseModel, Field, field_validator


class RenderAsciiTableInput(BaseModel):
    columns: list[str] = Field(
        description="Ordered column names to display in the rendered table.",
        min_length=1,
    )
    rows: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Rows keyed by column name. Missing values are rendered as empty strings.",
    )
    max_width: int = Field(
        default=100,
        ge=40,
        le=180,
        description="Maximum line width for the rendered table.",
    )

    @field_validator("columns")
    @classmethod
    def _normalize_columns(cls, columns: list[str]) -> list[str]:
        normalized = [column.strip() for column in columns if column.strip() != ""]
        if len(normalized) == 0:
            raise ValueError("columns must include at least one non-empty value")
        return normalized


class AsciiTableRenderResult(BaseModel):
    table: str = Field(description="Rendered ASCII table text.")
    line_count: int = Field(description="Number of lines in the rendered table.")
    column_count: int = Field(description="Number of columns in the rendered table.")
    row_count: int = Field(description="Number of data rows rendered.")


class ValidateTerminalReportInput(BaseModel):
    text: str = Field(description="Report text to validate.")
    max_width: int = Field(
        default=100,
        ge=40,
        le=180,
        description="Maximum allowed line width for the report text.",
    )


class TerminalReportValidationResult(BaseModel):
    valid: bool = Field(description="Whether the report passes all checks.")
    violations: list[str] = Field(
        default_factory=list,
        description="Human-readable violations detected during validation.",
    )
    line_count: int = Field(description="Number of lines inspected.")
