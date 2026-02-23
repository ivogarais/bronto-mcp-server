Dashboard Payload Playbook

Use this playbook before calling `build_dashboard_spec` or `serve_dashboard`.

Serve behavior:
- `serve_dashboard` defaults to `launch_mode: "none"`.
- In this mode, it writes the spec file and returns a runnable command.
- Run the returned `command_str` in a real terminal to open the interactive TUI.
- Use `launch_mode: "blocking"` only when you explicitly want MCP to wait on `bronto serve`.
- `bronto-cli` live auto-refresh is enabled by default at a tuned interval.

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

Table item shape:

```json
{
  "title": "Latest Errors",
  "columns": [
    { "title": "ts", "width": "auto" },
    { "title": "service", "width": 12 },
    { "title": "message", "width": "flex" }
  ],
  "rows": [
    ["2026-02-22T12:00:01Z", "api", "NullPointerException"]
  ],
  "row_limit": 200
}
```

Column rules:
- `title` max length: 16 characters.
- Optional `key`: snake_case, max 24 chars.
- Optional `width`: `"auto"`, `"flex"`, or integer `1..80`.

Quick valid example payload (multi-family):

```json
{
  "title": "All Families",
  "density": "comfortable",
  "charts": [
    {
      "title": "Errors by Type",
      "family": "bar",
      "labels": ["Timeout", "Validation"],
      "values": [31, 29]
    },
    {
      "title": "Latency",
      "family": "line",
      "xy": [
        {
          "name": "p95",
          "points": [
            { "x": 1, "y": 220 },
            { "x": 2, "y": 245 }
          ]
        }
      ]
    },
    {
      "title": "Request Rate",
      "family": "timeseries",
      "time": [
        {
          "name": "req_rate",
          "points": [
            { "t": "2026-02-22T12:00:00Z", "v": 140 },
            { "t": "2026-02-22T12:05:00Z", "v": 155 }
          ]
        }
      ]
    }
  ],
  "tables": [
    {
      "title": "Latest Errors",
      "columns": [
        { "title": "ts", "width": "auto" },
        { "title": "service", "width": 12 },
        { "title": "message", "width": "flex" }
      ],
      "rows": [
        ["2026-02-22T12:00:01Z", "api", "NullPointerException"]
      ]
    }
  ]
}
```
