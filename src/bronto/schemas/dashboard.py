from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_COLUMN_KEY_PATTERN = re.compile(r"^[@A-Za-z0-9_.:-]{1,64}$")


def _normalize_non_empty_text(value: str, field_name: str) -> str:
    normalized = " ".join(value.split()).strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


class DashboardTableColumnInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        description="Column title shown in the table header"
        ".",
        min_length=1,
        max_length=16,
    )
    key: str = Field(
        description=(
            "Required data key path used to fill this column from records "
            '(e.g. "@time", "event.type", "event.toolName").'
        ),
    )
    width: str | int | None = Field(
        default=None,
        description='Optional width hint: "auto", "flex", or a fixed integer width.',
    )

    @field_validator("title")
    @classmethod
    def _normalize_title(cls, value: str) -> str:
        return _normalize_non_empty_text(value, "column title")

    @field_validator("key")
    @classmethod
    def _validate_key(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("column key must not be empty")
        if not _COLUMN_KEY_PATTERN.match(normalized):
            raise ValueError(
                "column key must be 1..64 chars and may include letters, numbers, @, _, ., :, -"
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
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        description=(
            "Specific chart title (max 48 chars). Avoid generic names like "
            "'Bar Chart 1'; summarize what is being measured."
        ),
        min_length=1,
        max_length=48,
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
        return _normalize_non_empty_text(value, "bar chart title")

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


class DashboardSeriesRefInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, description="Series name.")
    variant: Literal["primary", "muted", "danger"] | None = Field(
        default=None, description="Optional series variant."
    )


class DashboardXYPointInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: float
    y: float


class DashboardXYSeriesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    points: list[DashboardXYPointInput] = Field(min_length=1)


class DashboardTimePointInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    t: str = Field(min_length=1, description="RFC3339 timestamp")
    v: float


class DashboardTimeSeriesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    points: list[DashboardTimePointInput] = Field(min_length=1)


class DashboardCandleInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    t: str = Field(min_length=1, description="RFC3339 timestamp")
    open: float
    high: float
    low: float
    close: float


class DashboardHeatCellInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: int = Field(ge=0)
    y: int = Field(ge=0)
    v: float


class DashboardHeatmapDataInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    width: int | None = Field(default=None, ge=1)
    height: int | None = Field(default=None, ge=1)
    values: list[float] | None = Field(default=None)
    cells: list[DashboardHeatCellInput] | None = Field(default=None)

    @model_validator(mode="after")
    def _validate_shape(self) -> "DashboardHeatmapDataInput":
        has_dense = bool(self.values)
        has_sparse = bool(self.cells)
        if has_dense and has_sparse:
            raise ValueError("heatmap must define either dense values or sparse cells")
        if not has_dense and not has_sparse:
            raise ValueError("heatmap must define dense values or sparse cells")
        if has_dense:
            if self.width is None or self.height is None:
                raise ValueError("dense heatmap requires width and height")
            expected = self.width * self.height
            if len(self.values or []) != expected:
                raise ValueError("dense heatmap values length must equal width*height")
        return self


class DashboardLiveQueryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: Literal["metrics", "logs"] = Field(
        default="metrics",
        description="Live query mode used by bronto-cli runtime polling.",
    )
    log_ids: list[str] = Field(
        min_length=1,
        description="List of Bronto dataset IDs used for live polling.",
    )
    metric_functions: list[str] = Field(
        default_factory=list,
        description=(
            "Metrics expressions (e.g. COUNT(*), AVG(\"event.latencyMs\")). "
            "Required when mode=metrics."
        ),
    )
    search_filter: str = Field(
        default="",
        description="Optional SQL-like filter applied to live queries.",
    )
    group_by_keys: list[str] = Field(
        default_factory=list,
        description="Optional grouping keys for metrics mode.",
    )
    lookback_sec: int = Field(
        default=1800,
        ge=30,
        le=604800,
        description="Sliding lookback window in seconds (30s to 7d).",
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=5000,
        description="Maximum rows for logs mode.",
    )

    @model_validator(mode="after")
    def _validate_mode_requirements(self) -> "DashboardLiveQueryInput":
        if self.mode == "metrics" and len(self.metric_functions) == 0:
            raise ValueError("metric_functions is required when mode='metrics'")
        return self


class DashboardChartInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        description=(
            "Specific chart title (max 48 chars). Avoid generic names like "
            "'Bar Chart 1'; describe the signal and scope."
        ),
        min_length=1,
        max_length=48,
    )
    family: Literal[
        "bar",
        "heatmap",
        "line",
        "ohlc",
        "scatter",
        "streamline",
        "timeseries",
        "waveline",
        "sparkline",
    ]

    unit: str | None = None
    format: Literal["number", "bytes", "duration"] | None = None
    render_mode: Literal["ascii", "braille"] | None = None
    show_axis: bool | None = None

    labels: list[str] | None = None
    values: list[float] | None = None
    bar_orientation: Literal["horizontal", "vertical"] | None = None

    xy: list[DashboardXYSeriesInput] | None = None
    line_series: list[DashboardSeriesRefInput] | None = None
    line_interpolation: Literal["linear", "step"] | None = None
    line_markers: bool | None = None
    scatter_point_rune: str | None = None
    waveline_series: list[DashboardSeriesRefInput] | None = None

    heatmap: DashboardHeatmapDataInput | None = None
    heatmap_min: float | None = None
    heatmap_max: float | None = None

    candles: list[DashboardCandleInput] | None = None
    ohlc_style: Literal["candle", "ohlc"] | None = None

    value: list[float] | None = None
    streamline_window: int | None = Field(default=None, ge=0)
    sparkline_window: int | None = Field(default=None, ge=0)

    time: list[DashboardTimeSeriesInput] | None = None
    timeseries_series: list[DashboardSeriesRefInput] | None = None
    time_format: str | None = None
    live_query: DashboardLiveQueryInput = Field(
        description="Required live query definition for bronto-cli polling.",
    )

    @field_validator("scatter_point_rune")
    @classmethod
    def _validate_point_rune(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if len(value) != 1:
            raise ValueError("scatter_point_rune must be a single character")
        return value

    @model_validator(mode="after")
    def _validate_for_family(self) -> "DashboardChartInput":
        if self.live_query is None:  # defensive; field is required
            raise ValueError("chart live_query is required")
        if self.family == "bar":
            if (
                self.labels is not None
                and self.values is not None
                and len(self.labels) != len(self.values)
            ):
                raise ValueError("bar chart labels and values length must match")
        elif self.family == "heatmap":
            if (
                self.heatmap_min is not None
                and self.heatmap_max is not None
                and self.heatmap_min > self.heatmap_max
            ):
                raise ValueError("heatmap_min must be <= heatmap_max")
        return self


class DashboardTableInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        description=(
            "Specific table title (max 48 chars). Avoid generic names like "
            "'Table 1'; describe the rows shown."
        ),
        min_length=1,
        max_length=48,
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
    live_query: DashboardLiveQueryInput = Field(
        description="Required live query definition for bronto-cli polling.",
    )

    @field_validator("title")
    @classmethod
    def _normalize_title(cls, value: str) -> str:
        return _normalize_non_empty_text(value, "table title")

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
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        description=(
            "Dashboard title (max 64 chars). Use a concise, descriptive summary "
            "of the dashboard purpose."
        ),
        min_length=1,
        max_length=64,
    )
    density: Literal["compact", "comfortable"] = Field(default="comfortable")
    charts: list[DashboardChartInput] = Field(default_factory=list)
    bar_charts: list[DashboardBarChartInput] = Field(default_factory=list)
    tables: list[DashboardTableInput] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def _normalize_title(cls, value: str) -> str:
        return _normalize_non_empty_text(value, "dashboard title")

    @model_validator(mode="after")
    def _validate_has_widgets(self) -> "DashboardBuildInput":
        if len(self.bar_charts) > 0:
            raise ValueError(
                "bar_charts is not supported in live-only mode; use charts[] with live_query"
            )
        if len(self.charts) == 0 and len(self.bar_charts) == 0 and len(self.tables) == 0:
            raise ValueError("dashboard must include at least one chart or table")
        return self


def build_bronto_app_spec(payload: DashboardBuildInput) -> dict[str, Any]:
    charts: dict[str, Any] = {}
    tables: dict[str, Any] = {}
    datasets: dict[str, Any] = {}

    normalized_charts = list(payload.charts)

    for idx, chart in enumerate(normalized_charts, start=1):
        chart_ref = f"chart{idx}"
        dataset_ref = f"chart_dataset_{idx}"
        charts[chart_ref] = _build_chart_spec(chart, dataset_ref)
        datasets[dataset_ref] = _build_chart_dataset(chart)

    for idx, table in enumerate(payload.tables, start=1):
        table_ref = f"table{idx}"
        dataset_ref = f"table_dataset_{idx}"

        resolved_columns = _resolve_table_columns(table.columns)
        dataset_columns = [column["key"] for column in resolved_columns]

        tables[table_ref] = {
            "title": table.title,
            "datasetRef": dataset_ref,
            "columns": [_to_table_column_spec(column) for column in resolved_columns],
            "rowLimit": table.row_limit,
        }
        table_dataset: dict[str, Any] = {
            "kind": "table",
            "columns": dataset_columns,
            "rows": table.rows,
        }
        table_dataset["liveQuery"] = _live_query_to_spec(table.live_query)
        datasets[dataset_ref] = table_dataset
    return {
        "version": "bronto-tui/v1",
        "title": payload.title,
        "theme": {"brand": "bronto", "density": payload.density},
        "charts": charts,
        "tables": tables,
        "datasets": datasets,
    }


def _build_chart_spec(chart: DashboardChartInput, dataset_ref: str) -> dict[str, Any]:
    spec: dict[str, Any] = {
        "title": chart.title,
        "family": chart.family,
        "datasetRef": dataset_ref,
    }

    render: dict[str, Any] = {}
    if chart.render_mode is not None:
        render["mode"] = chart.render_mode
    if chart.show_axis is not None:
        render["showAxis"] = chart.show_axis
    if render:
        spec["render"] = render

    if chart.family == "bar":
        spec["bar"] = {"orientation": chart.bar_orientation or "vertical"}
    elif chart.family == "heatmap":
        heatmap_opts: dict[str, Any] = {}
        if chart.heatmap_min is not None:
            heatmap_opts["min"] = chart.heatmap_min
        if chart.heatmap_max is not None:
            heatmap_opts["max"] = chart.heatmap_max
        spec["heatmap"] = heatmap_opts
    elif chart.family == "line":
        refs = chart.line_series or _series_refs_from_xy(chart.xy or [])
        spec["line"] = {
            "series": [_series_ref_to_spec(ref) for ref in refs],
            "style": {
                "interpolation": chart.line_interpolation or "linear",
                "markers": bool(chart.line_markers),
            },
        }
    elif chart.family == "scatter":
        scatter: dict[str, Any] = {}
        if chart.scatter_point_rune is not None:
            scatter["pointRune"] = chart.scatter_point_rune
        spec["scatter"] = scatter
    elif chart.family == "waveline":
        refs = chart.waveline_series or _series_refs_from_xy(chart.xy or [])
        spec["waveline"] = {"series": [_series_ref_to_spec(ref) for ref in refs]}
    elif chart.family == "timeseries":
        refs = chart.timeseries_series or _series_refs_from_time(chart.time or [])
        timeseries: dict[str, Any] = {
            "series": [_series_ref_to_spec(ref) for ref in refs]
        }
        if chart.time_format is not None:
            timeseries["timeFormat"] = chart.time_format
        spec["timeseries"] = timeseries
    elif chart.family == "ohlc":
        spec["ohlc"] = {"style": chart.ohlc_style or "candle"}
    elif chart.family == "streamline":
        spec["streamline"] = {"window": chart.streamline_window or 120}
    elif chart.family == "sparkline":
        spec["sparkline"] = {"window": chart.sparkline_window or 120}

    return spec


def _build_chart_dataset(chart: DashboardChartInput) -> dict[str, Any]:
    dataset: dict[str, Any] = {}

    if chart.family == "bar":
        dataset = {
            "kind": "categorySeries",
            "labels": chart.labels,
            "values": chart.values,
        }
    elif chart.family in {"line", "scatter", "waveline"}:
        dataset = {
            "kind": "xySeries",
            "xy": [
                {
                    "name": series.name,
                    "points": [{"x": p.x, "y": p.y} for p in series.points],
                }
                for series in (chart.xy or [])
            ],
        }
    elif chart.family == "timeseries":
        dataset = {
            "kind": "timeSeries",
            "time": [
                {
                    "name": series.name,
                    "points": [{"t": p.t, "v": p.v} for p in series.points],
                }
                for series in (chart.time or [])
            ],
        }
    elif chart.family == "ohlc":
        dataset = {
            "kind": "ohlcSeries",
            "candles": [
                {
                    "t": c.t,
                    "open": c.open,
                    "high": c.high,
                    "low": c.low,
                    "close": c.close,
                }
                for c in (chart.candles or [])
            ],
        }
    elif chart.family == "heatmap":
        heatmap = chart.heatmap
        assert heatmap is not None
        heatmap_payload: dict[str, Any] = {}
        if heatmap.width is not None:
            heatmap_payload["width"] = heatmap.width
        if heatmap.height is not None:
            heatmap_payload["height"] = heatmap.height
        if heatmap.values is not None:
            heatmap_payload["values"] = heatmap.values
        if heatmap.cells is not None:
            heatmap_payload["cells"] = [
                {"x": cell.x, "y": cell.y, "v": cell.v} for cell in heatmap.cells
            ]
        dataset = {
            "kind": "heatmapCells",
            "heatmap": heatmap_payload,
        }
    elif chart.family in {"streamline", "sparkline"}:
        dataset = {
            "kind": "valueSeries",
            "value": chart.value,
        }

    if chart.unit is not None:
        dataset["unit"] = chart.unit
    if chart.format is not None:
        dataset["format"] = chart.format
    dataset["liveQuery"] = _live_query_to_spec(chart.live_query)

    return dataset


def _live_query_to_spec(live_query: DashboardLiveQueryInput) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "mode": live_query.mode,
        "logIds": live_query.log_ids,
        "searchFilter": live_query.search_filter,
        "groupByKeys": live_query.group_by_keys,
        "lookbackSec": live_query.lookback_sec,
        "limit": live_query.limit,
    }
    if len(live_query.metric_functions) > 0:
        payload["metricFunctions"] = live_query.metric_functions
    return payload


def _series_refs_from_xy(series: list[DashboardXYSeriesInput]) -> list[DashboardSeriesRefInput]:
    if len(series) == 0:
        return [DashboardSeriesRefInput(name="total", variant="primary")]
    return [DashboardSeriesRefInput(name=s.name, variant="primary") for s in series]


def _series_refs_from_time(
    series: list[DashboardTimeSeriesInput],
) -> list[DashboardSeriesRefInput]:
    if len(series) == 0:
        return [DashboardSeriesRefInput(name="total", variant="primary")]
    return [DashboardSeriesRefInput(name=s.name, variant="primary") for s in series]


def _series_ref_to_spec(series: DashboardSeriesRefInput) -> dict[str, Any]:
    out = {"name": series.name}
    if series.variant is not None:
        out["variant"] = series.variant
    return out


def _resolve_table_columns(
    columns: list[DashboardTableColumnInput],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    used_keys: set[str] = set()
    for idx, column in enumerate(columns, start=1):
        key = column.key
        if key in used_keys:
            raise ValueError(f"duplicate table column key: {key}")
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

