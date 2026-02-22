Dashboard Payload Playbook

Use this playbook before calling `build_dashboard_spec` or `serve_dashboard`.

Serve behavior:
- `serve_dashboard` defaults to `launch_mode: "none"`.
- In this mode, it writes the spec file and returns a runnable command.
- Run the returned `command_str` in a real terminal to open the interactive TUI.
- Use `launch_mode: "blocking"` only when you explicitly want MCP to wait on `bronto serve`.

Required top-level shape:

```json
{
  "title": "Errors (Last 30m)",
  "density": "comfortable",
  "bar_charts": [],
  "tables": []
}
```

Rules:
- `title` is required.
- Include at least one widget in `bar_charts` or `tables`.
- Do NOT use `widgets`, `chart`, or `charts` keys at top level.
- `density` can be `comfortable` or `compact`.

Bar chart item shape:

```json
{
  "title": "Errors by Service",
  "labels": ["api", "worker", "web"],
  "values": [120, 80, 60]
}
```

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
    ["2026-02-22T12:00:01Z", "api", "NullPointerException"],
    ["2026-02-22T12:00:03Z", "worker", "timeout contacting db"]
  ],
  "row_limit": 200
}
```

Column rules:
- `title` max length: 16 characters.
- Optional `key`: snake_case, max 24 chars.
- Optional `width`: `"auto"`, `"flex"`, or integer `1..80`.

Quick valid example payload:

```json
{
  "title": "AI Agent Error Dashboard",
  "density": "comfortable",
  "bar_charts": [
    {
      "title": "Errors by Service",
      "labels": ["api", "worker", "web", "db"],
      "values": [120, 80, 60, 20]
    }
  ],
  "tables": [
    {
      "title": "Latest Error Rows",
      "columns": [
        { "title": "ts", "width": "auto" },
        { "title": "service", "width": 12 },
        { "title": "message", "width": "flex" }
      ],
      "rows": [
        ["2026-02-22T12:00:01Z", "api", "NullPointerException"],
        ["2026-02-22T12:00:03Z", "worker", "timeout contacting db"]
      ],
      "row_limit": 200
    }
  ]
}
```

Example `serve_dashboard` call (recommended):

```json
{
  "payload": {
    "title": "AI Agent Error Dashboard",
    "density": "comfortable",
    "bar_charts": [
      {
        "title": "Errors by Service",
        "labels": ["api", "worker", "web", "db"],
        "values": [120, 80, 60, 20]
      }
    ],
    "tables": [
      {
        "title": "Latest Error Rows",
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
  },
  "spec_file_path": "/tmp/ai-agent-errors.json",
  "launch_mode": "none"
}
```
