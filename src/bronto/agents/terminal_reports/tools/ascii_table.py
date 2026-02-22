import re
import textwrap
from typing import Any


_ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
_MARKDOWN_SEPARATOR_RE = re.compile(r"^\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*$")
_BOX_DRAWING_CHARS = set("┌┐└┘├┤┬┴┼│─═╔╗╚╝╠╣╬┃━")


def render_ascii_table(
    columns: list[str],
    rows: list[dict[str, Any]],
    *,
    max_width: int,
) -> str:
    normalized_rows = _normalize_rows(columns, rows)
    if len(normalized_rows) == 0:
        normalized_rows = [["No rows"] + [""] * (len(columns) - 1)]

    col_widths = _compute_column_widths(columns, normalized_rows, max_width=max_width)
    border = _render_border(col_widths)

    lines = [border]
    lines.extend(_render_wrapped_row(columns, col_widths))
    lines.append(border)
    for row in normalized_rows:
        lines.extend(_render_wrapped_row(row, col_widths))
    lines.append(border)
    return "\n".join(lines)


def validate_terminal_report(text: str, *, max_width: int) -> tuple[bool, list[str], int]:
    violations: list[str] = []
    lines = text.splitlines()

    if _ANSI_ESCAPE_RE.search(text):
        violations.append("ANSI escape sequences are not allowed.")
    if any(char in _BOX_DRAWING_CHARS for char in text):
        violations.append("Unicode box drawing characters are not allowed.")
    if any(ord(char) > 127 for char in text):
        violations.append("Non-ASCII characters are not allowed.")
    if any(_MARKDOWN_SEPARATOR_RE.match(line) for line in lines):
        violations.append("Markdown table separator patterns are not allowed.")

    for idx, line in enumerate(lines, start=1):
        if len(line) > max_width:
            violations.append(
                f"Line {idx} exceeds max width {max_width} (actual={len(line)})."
            )

    return len(violations) == 0, violations, len(lines)


def _normalize_rows(columns: list[str], rows: list[dict[str, Any]]) -> list[list[str]]:
    normalized: list[list[str]] = []
    for row in rows:
        normalized.append([_stringify_cell(row.get(column, "")) for column in columns])
    return normalized


def _stringify_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _compute_column_widths(
    columns: list[str], rows: list[list[str]], *, max_width: int
) -> list[int]:
    column_count = len(columns)
    max_available = max_width - (3 * column_count + 1)
    if max_available < column_count * 3:
        raise ValueError("max_width is too small for the number of columns")

    max_content_widths = [len(column) for column in columns]
    for row in rows:
        for col_idx, cell in enumerate(row):
            for logical_line in str(cell).splitlines() or [""]:
                max_content_widths[col_idx] = max(
                    max_content_widths[col_idx], len(logical_line)
                )

    preferred_cap = max(12, min(40, max_available // column_count))
    min_widths = [max(3, min(len(column), 18)) for column in columns]
    widths = [
        max(min_widths[idx], min(max_content_widths[idx], preferred_cap))
        for idx in range(column_count)
    ]

    while sum(widths) > max_available:
        candidates = [
            idx for idx in range(column_count) if widths[idx] > min_widths[idx]
        ]
        if not candidates:
            break
        biggest_idx = max(candidates, key=lambda idx: widths[idx])
        widths[biggest_idx] -= 1

    if sum(widths) > max_available:
        even_width = max(3, max_available // column_count)
        widths = [even_width for _ in range(column_count)]

    return widths


def _render_border(widths: list[int]) -> str:
    return "+" + "+".join("-" * (width + 2) for width in widths) + "+"


def _render_wrapped_row(values: list[str], widths: list[int]) -> list[str]:
    wrapped_cells = [
        _wrap_cell_text(value, width)
        for value, width in zip(values, widths, strict=True)
    ]
    row_height = max(len(lines) for lines in wrapped_cells)

    rendered_lines: list[str] = []
    for line_idx in range(row_height):
        parts = []
        for col_idx, width in enumerate(widths):
            cell_lines = wrapped_cells[col_idx]
            value = cell_lines[line_idx] if line_idx < len(cell_lines) else ""
            parts.append(f" {value.ljust(width)} ")
        rendered_lines.append("|" + "|".join(parts) + "|")
    return rendered_lines


def _wrap_cell_text(value: str, width: int) -> list[str]:
    if value == "":
        return [""]

    wrapped_lines: list[str] = []
    for logical_line in value.splitlines() or [""]:
        lines = textwrap.wrap(
            logical_line,
            width=width,
            break_long_words=True,
            break_on_hyphens=False,
        )
        wrapped_lines.extend(lines or [""])
    return wrapped_lines or [""]
