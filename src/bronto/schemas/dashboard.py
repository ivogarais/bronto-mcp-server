from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

_COLUMN_KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,23}$")


class DashboardTableColumnInput(BaseModel):
    title: str = Field(
        description="Column title shown in the table header.",
        min_length=1,
        max_length=16,
    )
    key: str | None = Field(
        default=None,
        description=(
            "Optional short key used by the renderer and dataset rows "
            "(snake_case, max 24 chars). If omitted, derived from title."
        ),
    )
    width: str | int | None = Field(
        default=None,
        description='Optional width hint: "auto", "flex", or a fixed integer width.',
    )

    @field_validator("title")
    @classmethod
    def _normalize_title(cls, value: str) -> str:
        normalized = " ".join(value.split()).strip()
        if not normalized:
            raise ValueError("column title must not be empty")
        return normalized

    @field_validator("key")
    @classmethod
    def _validate_key(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower()
        if not _COLUMN_KEY_PATTERN.match(normalized):
            raise ValueError(
                "column key must match ^[a-z][a-z0-9_]{0,23}$ (snake_case, max 24 chars)"
            )
        return normalized

    @field_validator("width")
    @classmethod
    def _validate_width(cls, value: str | int | None) -> str | int | None:
        if value is None:
            return None
        if isinstance(value, str):
            if value not in {"auto", "flex"}:
                raise ValueError('width string must be either "auto" or "flex"')
            return value
        if value < 1 or value > 80:
            raise ValueError("fixed width must be between 1 and 80")
        return value


class DashboardBarChartInput(BaseModel):
    title: str = Field(
        description="Panel title for this bar chart.", min_length=1, max_length=48
    )
    labels: list[str] = Field(
        description="Category labels for the bar chart.",
        min_length=1,
    )
    values: list[float] = Field(
        description="Bar values aligned with labels.",
        min_length=1,
    )

    @field_validator("title")
    @classmethod
    def _normalize_title(cls, value: str) -> str:
        normalized = " ".join(value.split()).strip()
        if not normalized:
            raise ValueError("bar chart title must not be empty")
        return normalized

    @field_validator("labels")
    @classmethod
    def _validate_labels(cls, labels: list[str]) -> list[str]:
        normalized: list[str] = []
        for label in labels:
            cleaned = " ".join(label.split()).strip()
            if not cleaned:
                raise ValueError("bar chart labels must not contain empty values")
            if len(cleaned) > 24:
                raise ValueError("bar chart labels must be <= 24 characters")
            normalized.append(cleaned)
        return normalized

    @model_validator(mode="after")
    def _validate_lengths(self) -> "DashboardBarChartInput":
        if len(self.labels) != len(self.values):
            raise ValueError("bar chart labels and values must have matching lengths")
        return self


class DashboardTableInput(BaseModel):
    title: str = Field(
        description="Panel title for this table.", min_length=1, max_length=48
    )
    columns: list[DashboardTableColumnInput] = Field(
        description="Table columns definition.",
        min_length=1,
    )
    rows: list[list[str]] = Field(
        default_factory=list,
        description="Table rows. Each row must match columns length.",
    )
    row_limit: int = Field(default=200, ge=1, le=500)

    @field_validator("title")
    @classmethod
    def _normalize_title(cls, value: str) -> str:
        normalized = " ".join(value.split()).strip()
        if not normalized:
            raise ValueError("table title must not be empty")
        return normalized

    @field_validator("rows")
    @classmethod
    def _validate_row_cells(cls, rows: list[list[str]]) -> list[list[str]]:
        normalized_rows: list[list[str]] = []
        for row in rows:
            normalized_row: list[str] = []
            for cell in row:
                cell_text = str(cell)
                if len(cell_text) > 160:
                    raise ValueError("table cell values must be <= 160 characters")
                normalized_row.append(cell_text)
            normalized_rows.append(normalized_row)
        return normalized_rows

    @model_validator(mode="after")
    def _validate_row_shape(self) -> "DashboardTableInput":
        expected = len(self.columns)
        for i, row in enumerate(self.rows):
            if len(row) != expected:
                raise ValueError(
                    f"table row at index {i} has {len(row)} cells; expected {expected}"
                )
        return self


class DashboardBuildInput(BaseModel):
    title: str = Field(description="Dashboard title.", min_length=1, max_length=64)
    density: Literal["compact", "comfortable"] = Field(default="comfortable")
    bar_charts: list[DashboardBarChartInput] = Field(default_factory=list)
    tables: list[DashboardTableInput] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def _normalize_title(cls, value: str) -> str:
        normalized = " ".join(value.split()).strip()
        if not normalized:
            raise ValueError("dashboard title must not be empty")
        return normalized

    @model_validator(mode="after")
    def _validate_has_widgets(self) -> "DashboardBuildInput":
        if len(self.bar_charts) == 0 and len(self.tables) == 0:
            raise ValueError("dashboard must include at least one chart or table")
        return self


def build_bronto_app_spec(payload: DashboardBuildInput) -> dict[str, Any]:
    charts: dict[str, Any] = {}
    tables: dict[str, Any] = {}
    datasets: dict[str, Any] = {}

    main_row_children: list[dict[str, Any]] = []
    weights: list[int] = []

    for idx, chart in enumerate(payload.bar_charts, start=1):
        chart_ref = f"barChart{idx}"
        dataset_ref = f"bar_dataset_{idx}"
        charts[chart_ref] = {
            "family": "bar",
            "datasetRef": dataset_ref,
            "bar": {"orientation": "horizontal"},
        }
        datasets[dataset_ref] = {
            "kind": "categorySeries",
            "labels": chart.labels,
            "values": chart.values,
        }
        main_row_children.append(
            {
                "type": "chart",
                "id": f"bar_panel_{idx}",
                "title": chart.title,
                "chartRef": chart_ref,
            }
        )
        weights.append(2)

    for idx, table in enumerate(payload.tables, start=1):
        table_ref = f"table{idx}"
        dataset_ref = f"table_dataset_{idx}"

        resolved_columns = _resolve_table_columns(table.columns)
        dataset_columns = [column["key"] for column in resolved_columns]

        tables[table_ref] = {
            "datasetRef": dataset_ref,
            "columns": [_to_table_column_spec(column) for column in resolved_columns],
            "rowLimit": table.row_limit,
        }
        datasets[dataset_ref] = {
            "kind": "table",
            "columns": dataset_columns,
            "rows": table.rows,
        }
        main_row_children.append(
            {
                "type": "table",
                "id": f"table_panel_{idx}",
                "title": table.title,
                "tableRef": table_ref,
            }
        )
        weights.append(3)

    layout = {
        "type": "col",
        "id": "root",
        "gap": 1,
        "children": [
            {"type": "header", "id": "hdr", "titleRef": "$title"},
            {
                "type": "row",
                "id": "main",
                "gap": 1,
                "weights": weights,
                "children": main_row_children,
            },
        ],
    }

    return {
        "version": "bronto-tui/v1",
        "title": payload.title,
        "theme": {"brand": "bronto", "density": payload.density},
        "layout": layout,
        "charts": charts,
        "tables": tables,
        "datasets": datasets,
    }


def _resolve_table_columns(
    columns: list[DashboardTableColumnInput],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    used_keys: set[str] = set()
    for idx, column in enumerate(columns, start=1):
        base_key = column.key or _normalize_column_key(column.title)
        key = _dedupe_key(base_key, used_keys, idx)
        used_keys.add(key)
        resolved.append(
            {
                "key": key,
                "title": column.title,
                "width": column.width,
            }
        )
    return resolved


def _to_table_column_spec(column: dict[str, Any]) -> dict[str, Any]:
    spec: dict[str, Any] = {"key": column["key"], "title": column["title"]}
    if column["width"] is not None:
        spec["width"] = column["width"]
    return spec


def _normalize_column_key(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    normalized = re.sub(r"_+", "_", normalized)
    if not normalized:
        normalized = "col"
    if normalized[0].isdigit():
        normalized = f"col_{normalized}"
    normalized = normalized[:24].rstrip("_")
    if not normalized:
        normalized = "col"
    if not _COLUMN_KEY_PATTERN.match(normalized):
        normalized = f"col_{normalized}"[:24].rstrip("_")
    if not _COLUMN_KEY_PATTERN.match(normalized):
        normalized = "col"
    return normalized


def _dedupe_key(base_key: str, used_keys: set[str], idx: int) -> str:
    if base_key not in used_keys:
        return base_key

    suffix_counter = 2
    while True:
        suffix = f"_{suffix_counter}"
        candidate = f"{base_key[: 24 - len(suffix)]}{suffix}"
        candidate = candidate.rstrip("_")
        if (
            candidate
            and candidate not in used_keys
            and _COLUMN_KEY_PATTERN.match(candidate)
        ):
            return candidate
        suffix_counter += 1
        if suffix_counter > 999:
            fallback = f"col_{idx}"[:24]
            if fallback not in used_keys:
                return fallback
