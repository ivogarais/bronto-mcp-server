Dashboard Payload Playbook

Use this playbook before calling `build_dashboard_spec` or `serve_dashboard`.

Serve behavior:
- `serve_dashboard` defaults to `launch_mode: "none"`.
- In this mode, it writes the spec file and returns a runnable command.
- When `spec_file_path` is omitted, specs are written to `~/bronto-dashboards/`
  using a human-readable filename derived from dashboard title.
- Run the returned `command_str` in a real terminal to open the interactive TUI.
- Use `launch_mode: "blocking"` only when you explicitly want MCP to wait on `bronto serve`.
- `bronto-cli` live auto-refresh is enabled by default at a tuned interval.
- `serve_dashboard` seeds charts/tables with real data from Bronto before writing
  the spec, then `bronto-cli` keeps polling live.

Recommended workflow (for agents):
1. Discover dataset IDs with `get_datasets`.
2. Validate available keys with `get_keys(log_id)` before writing filters/groupings.
3. Build each widget with a required `live_query` using real `log_ids`.
4. Prefer `serve_dashboard` over `build_dashboard_spec` for runnable specs
   (it hydrates seed data from Bronto and avoids empty datasets).
5. Return the exact `command_str` to the user and explain that it must be run in
   a real terminal.

Required top-level shape:

```json
{
  "title": "Errors (Last 30m)",
  "density": "comfortable",
  "charts": [],
  "tables": []
}
```

Rules:
- `title` is required.
- Include at least one widget in `charts` or `tables`.
- `density` can be `comfortable` or `compact`.
- Do NOT use top-level `widgets` or `chart`.
- Do NOT use top-level `bar_charts` (live-only mode).
- Grid/layout is renderer-owned. Do not try to encode panel layout strategy in payload.
  `bronto-cli` enforces Charts as 3-per-row and Logs as 2-per-row.
- Use descriptive titles for dashboard/charts/tables and avoid generic names like
  `Bar Chart 1` or `Table 1`.
- Title limits: dashboard `<= 64` chars, chart/table `<= 48` chars.

`charts[]` supports families aligned with `bronto-cli`:
- `bar` (dataset kind: `categorySeries`)
- `line`, `scatter`, `waveline` (dataset kind: `xySeries`)
- `timeseries` (dataset kind: `timeSeries`)
- `ohlc` (dataset kind: `ohlcSeries`)
- `heatmap` (dataset kind: `heatmapCells`)
- `streamline`, `sparkline` (dataset kind: `valueSeries`)

Required live polling:
- Every item in `charts[]` and `tables[]` must include `live_query` so `bronto-cli`
  polls Bronto and refreshes datasets continuously.
- `live_query` shape:
  - `mode`: `metrics` or `logs`
  - `log_ids`: required list of dataset IDs
  - `metric_functions`: required when `mode=metrics`
  - `search_filter`, `group_by_keys`
  - `lookback_sec` (default `1800`)
  - `limit` (default `100`)
- `bronto-cli` requires `BRONTO_API_KEY` (and optional `BRONTO_API_ENDPOINT`) for
  live query execution.
- For `timeseries`, `line`, and `waveline` live charts, avoid grouping by `@time`;
  Bronto already returns sliced timeseries in totals.

Table item shape:

```json
{
  "title": "Latest Errors",
  "columns": [
    { "key": "@time", "title": "ts", "width": "auto" },
    { "key": "service", "title": "service", "width": 12 },
    { "key": "message", "title": "message", "width": "flex" }
  ],
  "rows": [
    ["2026-02-22T12:00:01Z", "api", "NullPointerException"]
  ],
  "row_limit": 200
}
```

Column rules:
- `title` max length: 16 characters.
- Required `key`: data field path used to populate the column.
  Examples: `@time`, `event.type`, `event.toolName`, `event.error.type`.
- Optional `width`: `"auto"`, `"flex"`, or integer `1..80`.

Quick valid example payload (multi-family, live):

```json
{
  "title": "All Families",
  "density": "comfortable",
  "charts": [
    {
      "title": "Errors by Type",
      "family": "bar",
      "live_query": {
        "mode": "metrics",
        "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
        "metric_functions": ["COUNT(*)"],
        "search_filter": "\"level\"='error'",
        "group_by_keys": ["event.error.type"],
        "lookback_sec": 1800,
        "limit": 20
      }
    },
    {
      "title": "Latency",
      "family": "line",
      "live_query": {
        "mode": "metrics",
        "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
        "metric_functions": ["AVG(\"event.latencyMs\")"],
        "group_by_keys": [],
        "lookback_sec": 1800,
        "limit": 120
      }
    },
    {
      "title": "Request Rate",
      "family": "timeseries",
      "live_query": {
        "mode": "metrics",
        "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
        "metric_functions": ["COUNT(*)"],
        "group_by_keys": [],
        "lookback_sec": 1800,
        "limit": 120
      }
    }
  ],
  "tables": [
    {
      "title": "Latest Errors",
      "columns": [
        { "key": "@time", "title": "ts", "width": "auto" },
        { "key": "service", "title": "service", "width": 12 },
        { "key": "message", "title": "message", "width": "flex" }
      ],
      "rows": [],
      "live_query": {
        "mode": "logs",
        "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
        "search_filter": "\"level\"='error'",
        "lookback_sec": 1800,
        "limit": 100
      }
    }
  ]
}
```
