import json
import os
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import Field, ValidationError
from typing_extensions import Annotated

from bronto.agents.playbooks import resolve_playbook
from bronto.logger import module_logger
from bronto.schemas import DashboardBuildInput, build_bronto_app_spec

logger = module_logger(__name__)


class DashboardToolHandlers:
    """Dashboard spec generation and Bronto CLI launch handlers."""

    @staticmethod
    def build_dashboard_spec(
        payload: Annotated[
            DashboardBuildInput,
            Field(
                description=(
                    "Structured dashboard payload following DashboardBuildInput "
                    "({title, density?, charts, tables}; each widget requires live_query)."
                )
            ),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="A validated full Bronto dashboard spec JSON object."),
    ]:
        """Build and validate a Bronto dashboard spec.

        Parameters
        ----------
        payload : DashboardBuildInput
            Structured dashboard payload.

        Returns
        -------
        dict[str, Any]
            Validated dashboard spec JSON.
        """
        request = _coerce_payload(payload)
        return build_bronto_app_spec(request)

    def serve_dashboard(
        self,
        payload: Annotated[
            DashboardBuildInput,
            Field(
                description=(
                    "Structured dashboard payload following DashboardBuildInput "
                    "({title, density?, charts, tables}; each widget requires live_query)."
                )
            ),
        ],
        keep_spec_file: Annotated[
            bool,
            Field(
                description=(
                    "If true, keep the generated spec JSON on disk for inspection. "
                    "If false, remove it after successful exit."
                )
            ),
        ] = False,
        spec_file_path: Annotated[
            str | None,
            Field(
                description=(
                    "Optional path where generated spec JSON will be written. "
                    "When provided, file is always kept."
                )
            ),
        ] = None,
        launch_mode: Annotated[
            str,
            Field(
                description=(
                    "How to handle the Bronto process. "
                    "`none` (default) only writes spec + returns command. "
                    "`blocking` executes `bronto serve` and waits for exit."
                )
            ),
        ] = "none",
    ) -> Annotated[
        dict[str, Any],
        Field(
            description=(
                "Result metadata for Bronto launch, including the command and the "
                "spec file path."
            )
        ),
    ]:
        """Prepare and optionally launch a Bronto dashboard.

        Parameters
        ----------
        payload : DashboardBuildInput
            Structured dashboard payload.
        keep_spec_file : bool, default=False
            Whether to retain generated specs after blocking launch.
        spec_file_path : str | None, default=None
            Optional explicit output path for the generated spec.
        launch_mode : str, default="none"
            Launch mode: ``none`` or ``blocking``.

        Returns
        -------
        dict[str, Any]
            Launch metadata and command details.
        """
        request = _coerce_payload(payload)
        app_spec = build_bronto_app_spec(request)
        _hydrate_live_seed_data(self.bronto_client, app_spec)
        spec_path = _write_spec_file(app_spec, spec_file_path, request.title)

        bronto_bin = _resolve_bronto_binary()
        command = [bronto_bin, "serve", "--spec", str(spec_path)]
        user_command = ["bronto", "serve", "--spec", str(spec_path)]
        normalized_mode = launch_mode.strip().lower()
        if normalized_mode not in {"none", "blocking"}:
            raise ValueError("Invalid launch_mode. Use one of: 'none', 'blocking'.")

        if normalized_mode == "none":
            logger.info(
                "Prepared Bronto dashboard spec without launching, command=%s", command
            )
            # When not launching, keep the spec by default so callers can run
            # the returned command in a real terminal session.
            return {
                "status": "prepared",
                "command": command,
                "command_str": " ".join(user_command),
                "spec_path": str(spec_path),
                "spec_retained": True,
                "launch_mode": normalized_mode,
                "note": (
                    "Interactive TUI launch is not executed in MCP by default. "
                    "Run `command_str` in your terminal."
                ),
            }

        logger.info("Launching Bronto dashboard (blocking), command=%s", command)

        try:
            completed = subprocess.run(command, check=False)
        except OSError as exc:
            raise RuntimeError(
                f"Failed to execute Bronto CLI using command: {' '.join(command)}"
            ) from exc

        if completed.returncode != 0:
            raise RuntimeError(
                "`bronto serve` failed with exit code "
                f"{completed.returncode}. Command: {' '.join(command)}"
            )

        retained = keep_spec_file or spec_file_path is not None
        if not retained:
            spec_path.unlink(missing_ok=True)

        return {
            "status": "ok",
            "command": command,
            "command_str": " ".join(user_command),
            "spec_path": str(spec_path),
            "spec_retained": retained,
            "exit_code": completed.returncode,
            "launch_mode": normalized_mode,
        }

    @staticmethod
    def dashboard_playbook() -> Annotated[
        str,
        Field(
            description=(
                "Playbook with exact payload contract and examples for "
                "build_dashboard_spec and serve_dashboard."
            )
        ),
    ]:
        """Return the dashboard payload playbook.

        Returns
        -------
        str
            Dashboard playbook content.
        """
        return resolve_playbook(
            "bronto.agents.dashboard", "playbooks/dashboard_playbook.md"
        )


def _write_spec_file(
    spec_document: dict[str, Any], spec_file_path: str | None, dashboard_title: str
) -> Path:
    """Write dashboard spec to disk.

    Parameters
    ----------
    spec_document : dict[str, Any]
        Spec JSON payload.
    spec_file_path : str | None
        Optional explicit output path.
    dashboard_title : str
        Dashboard title used for default file naming.

    Returns
    -------
    Path
        Written file path.
    """
    if spec_file_path:
        path = Path(spec_file_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        dashboards_dir = Path.home() / "bronto-dashboards"
        dashboards_dir.mkdir(parents=True, exist_ok=True)
        base = _slugify_title(dashboard_title)
        path = dashboards_dir / f"{base}.json"
        if path.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            path = dashboards_dir / f"{base}-{stamp}.json"

    path.write_text(json.dumps(spec_document, indent=2), encoding="utf-8")
    return path


def _slugify_title(title: str) -> str:
    """Convert a title to a filesystem-safe slug.

    Parameters
    ----------
    title : str
        Raw dashboard title.

    Returns
    -------
    str
        Lowercase slug.
    """
    normalized = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not normalized:
        return "dashboard"
    return normalized[:64].rstrip("-")


def _coerce_payload(
    payload: DashboardBuildInput | dict[str, Any],
) -> DashboardBuildInput:
    """Coerce input payload to ``DashboardBuildInput``.

    Parameters
    ----------
    payload : DashboardBuildInput | dict[str, Any]
        Raw payload.

    Returns
    -------
    DashboardBuildInput
        Validated payload model.
    """
    if isinstance(payload, DashboardBuildInput):
        return payload
    try:
        return DashboardBuildInput.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(
            "Invalid dashboard payload. Top-level shape must be: "
            "{title, density?, charts, tables} and each widget must define live_query. "
            "Use `dashboard_playbook` for exact examples. "
            f"Validation details: {exc}"
        ) from exc


def _resolve_bronto_binary() -> str:
    """Resolve the Bronto CLI binary path.

    Returns
    -------
    str
        Executable path.
    """
    configured = os.environ.get("BRONTO_BIN", "bronto").strip() or "bronto"
    if os.path.sep in configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_file():
            raise RuntimeError(
                f"BRONTO_BIN points to a missing file: {candidate}. "
                "Install bronto or update BRONTO_BIN."
            )
        return str(candidate)

    resolved = shutil.which(configured)
    if resolved is None:
        raise RuntimeError(
            "Could not find `bronto` in PATH. Install Bronto CLI or set BRONTO_BIN to the full binary path."
        )
    return resolved


def _hydrate_live_seed_data(bronto_client: Any, app_spec: dict[str, Any]) -> None:
    """Hydrate live-query datasets with seed data.

    Parameters
    ----------
    bronto_client : Any
        Bronto client instance.
    app_spec : dict[str, Any]
        Mutable app spec document.
    """
    datasets = app_spec.get("datasets", {})
    if not isinstance(datasets, dict):
        return

    now_ms = int(time.time() * 1000)
    for dataset_id, dataset in datasets.items():
        if not isinstance(dataset, dict):
            continue
        live = dataset.get("liveQuery")
        if not isinstance(live, dict):
            continue

        mode = str(live.get("mode") or "metrics").strip().lower()
        log_ids = live.get("logIds") or []
        if not isinstance(log_ids, list) or len(log_ids) == 0:
            continue

        lookback_sec = int(live.get("lookbackSec") or 1800)
        start_ms = now_ms - max(30, lookback_sec) * 1000
        end_ms = now_ms

        try:
            if mode == "metrics":
                _hydrate_metrics_dataset(
                    bronto_client=bronto_client,
                    dataset=dataset,
                    live_query=live,
                    start_ms=start_ms,
                    end_ms=end_ms,
                )
            elif mode == "logs":
                _hydrate_logs_dataset(
                    bronto_client=bronto_client,
                    dataset=dataset,
                    live_query=live,
                    start_ms=start_ms,
                    end_ms=end_ms,
                )
        except Exception as exc:  # pragma: no cover - best-effort hydration
            logger.warning(
                "Live seed hydration failed for dataset %s: %s",
                dataset_id,
                exc,
            )

    _backfill_chart_series_refs(app_spec, now_ms)


def _hydrate_metrics_dataset(
    bronto_client: Any,
    dataset: dict[str, Any],
    live_query: dict[str, Any],
    start_ms: int,
    end_ms: int,
) -> None:
    """Hydrate one metrics dataset in place.

    Parameters
    ----------
    bronto_client : Any
        Bronto client instance.
    dataset : dict[str, Any]
        Target dataset mapping.
    live_query : dict[str, Any]
        Live query definition.
    start_ms : int
        Window start in unix milliseconds.
    end_ms : int
        Window end in unix milliseconds.
    """
    response = bronto_client.search_post(
        timestamp_start=start_ms,
        timestamp_end=end_ms,
        log_ids=live_query.get("logIds") or [],
        where=live_query.get("searchFilter") or "",
        _select=live_query.get("metricFunctions") or ["COUNT(*)"],
        group_by_keys=live_query.get("groupByKeys") or [],
    )
    groups = _extract_metric_groups(response)

    kind = str(dataset.get("kind") or "")
    if kind == "timeSeries":
        time_series: list[dict[str, Any]] = []
        for group in groups:
            points = [
                {
                    "t": _ms_to_rfc3339(point.get("@timestamp"), end_ms),
                    "v": _as_float(point.get("value")),
                }
                for point in group.get("timeseries", [])
                if isinstance(point, dict)
            ]
            if len(points) == 0:
                points = [{"t": _ms_to_rfc3339(end_ms, end_ms), "v": 0.0}]
            time_series.append({"name": group.get("name") or "total", "points": points})
        if len(time_series) == 0:
            time_series = [
                {
                    "name": "total",
                    "points": [{"t": _ms_to_rfc3339(end_ms, end_ms), "v": 0.0}],
                }
            ]
        dataset["time"] = time_series
        return

    if kind == "xySeries":
        xy_series: list[dict[str, Any]] = []
        for group in groups:
            points = []
            for idx, point in enumerate(group.get("timeseries", []), start=1):
                if not isinstance(point, dict):
                    continue
                ts_ms = _as_int(point.get("@timestamp"))
                x = float(ts_ms / 1000.0) if ts_ms > 0 else float(idx)
                points.append({"x": x, "y": _as_float(point.get("value"))})
            if len(points) == 0:
                points = [{"x": float(end_ms / 1000.0), "y": 0.0}]
            xy_series.append({"name": group.get("name") or "total", "points": points})
        if len(xy_series) == 0:
            xy_series = [
                {"name": "total", "points": [{"x": float(end_ms / 1000.0), "y": 0.0}]}
            ]
        dataset["xy"] = xy_series
        return

    if kind == "categorySeries":
        labels: list[str] = []
        values: list[float] = []
        for group in groups:
            labels.append(str(group.get("name") or "total"))
            values.append(_latest_metric_value(group.get("timeseries", [])))
        dataset["labels"] = labels
        dataset["values"] = values
        return

    if kind == "valueSeries":
        total_group = groups[0] if groups else {"timeseries": []}
        values = [
            _as_float(point.get("value"))
            for point in total_group.get("timeseries", [])
            if isinstance(point, dict)
        ]
        if len(values) == 0:
            values = [0.0]
        dataset["value"] = values
        return

    if kind == "table":
        rows: list[list[str]] = []
        columns = dataset.get("columns") or []
        for group in groups:
            row_map = {
                "group": str(group.get("name") or ""),
                "value": str(_latest_metric_value(group.get("timeseries", []))),
                "count": str(_as_float(group.get("count"))),
            }
            rows.append([str(row_map.get(col, "")) for col in columns])
        dataset["rows"] = rows


def _hydrate_logs_dataset(
    bronto_client: Any,
    dataset: dict[str, Any],
    live_query: dict[str, Any],
    start_ms: int,
    end_ms: int,
) -> None:
    """Hydrate one logs dataset in place.

    Parameters
    ----------
    bronto_client : Any
        Bronto client instance.
    dataset : dict[str, Any]
        Target dataset mapping.
    live_query : dict[str, Any]
        Live query definition.
    start_ms : int
        Window start in unix milliseconds.
    end_ms : int
        Window end in unix milliseconds.
    """
    events = bronto_client.search(
        timestamp_start=start_ms,
        timestamp_end=end_ms,
        log_ids=live_query.get("logIds") or [],
        where=live_query.get("searchFilter") or "",
        limit=live_query.get("limit") or 100,
        _select=["*", "@raw"],
        group_by_keys=[],
    )
    columns = dataset.get("columns") or []
    rows: list[list[str]] = []
    for event in events:
        attributes = getattr(event, "attributes", {}) or {}
        row: list[str] = []
        for column in columns:
            if column == "time":
                row.append(str(attributes.get("@time", "")))
            else:
                row.append(str(attributes.get(column, "")))
        rows.append(row)
    dataset["rows"] = rows


def _extract_metric_groups(response: Any) -> list[dict[str, Any]]:
    """Extract grouped metric series from search response.

    Parameters
    ----------
    response : Any
        Raw metrics response.

    Returns
    -------
    list[dict[str, Any]]
        Grouped series entries.
    """
    if not isinstance(response, dict):
        return []
    groups = response.get("groups_series")
    if isinstance(groups, list) and len(groups) > 0:
        out: list[dict[str, Any]] = []
        for group in groups:
            if not isinstance(group, dict):
                continue
            out.append(
                {
                    "name": str(group.get("name") or "group"),
                    "timeseries": group.get("timeseries") or [],
                    "count": group.get("count") or 0,
                }
            )
        return out
    totals = response.get("totals") or {}
    if isinstance(totals, dict):
        return [
            {
                "name": "total",
                "timeseries": totals.get("timeseries") or [],
                "count": totals.get("count") or 0,
            }
        ]
    return []


def _backfill_chart_series_refs(app_spec: dict[str, Any], now_ms: int) -> None:
    """Backfill missing chart series refs from hydrated datasets.

    Parameters
    ----------
    app_spec : dict[str, Any]
        Mutable app spec document.
    now_ms : int
        Current unix timestamp in milliseconds.
    """
    charts = app_spec.get("charts", {})
    datasets = app_spec.get("datasets", {})
    if not isinstance(charts, dict) or not isinstance(datasets, dict):
        return

    for chart in charts.values():
        if not isinstance(chart, dict):
            continue
        dataset_ref = chart.get("datasetRef")
        dataset = datasets.get(dataset_ref) if isinstance(dataset_ref, str) else None
        if not isinstance(dataset, dict):
            continue
        family = chart.get("family")

        if family == "timeseries":
            time_series = dataset.get("time")
            if not isinstance(time_series, list) or len(time_series) == 0:
                dataset["time"] = [
                    {
                        "name": "total",
                        "points": [{"t": _ms_to_rfc3339(now_ms, now_ms), "v": 0.0}],
                    }
                ]
                time_series = dataset["time"]

            timeseries_opts = chart.get("timeseries")
            if not isinstance(timeseries_opts, dict):
                continue
            series_refs = timeseries_opts.get("series")
            if isinstance(series_refs, list) and len(series_refs) > 0:
                continue
            names = [
                s.get("name")
                for s in time_series
                if isinstance(s, dict)
                and isinstance(s.get("name"), str)
                and s.get("name")
            ]
            if len(names) == 0:
                names = ["total"]
            timeseries_opts["series"] = [
                {"name": name, "variant": "primary"} for name in names
            ]
            continue

        if family in {"line", "waveline"}:
            xy_series = dataset.get("xy")
            if not isinstance(xy_series, list) or len(xy_series) == 0:
                dataset["xy"] = [
                    {
                        "name": "total",
                        "points": [{"x": float(now_ms / 1000.0), "y": 0.0}],
                    }
                ]
                xy_series = dataset["xy"]

            chart_opts = chart.get(family)
            if not isinstance(chart_opts, dict):
                continue
            series_refs = chart_opts.get("series")
            if isinstance(series_refs, list) and len(series_refs) > 0:
                continue
            names = [
                s.get("name")
                for s in xy_series
                if isinstance(s, dict)
                and isinstance(s.get("name"), str)
                and s.get("name")
            ]
            if len(names) == 0:
                names = ["total"]
            chart_opts["series"] = [
                {"name": name, "variant": "primary"} for name in names
            ]


def _latest_metric_value(timeseries: list[Any]) -> float:
    """Get the latest non-zero metric value.

    Parameters
    ----------
    timeseries : list[Any]
        Raw timeseries points.

    Returns
    -------
    float
        Latest usable value.
    """
    for point in reversed(timeseries):
        if not isinstance(point, dict):
            continue
        value = _as_float(point.get("value"))
        if value != 0:
            return value
    if timeseries and isinstance(timeseries[-1], dict):
        return _as_float(timeseries[-1].get("value"))
    return 0.0


def _as_int(value: Any) -> int:
    """Coerce value to integer.

    Parameters
    ----------
    value : Any
        Input value.

    Returns
    -------
    int
        Parsed integer or zero.
    """
    if isinstance(value, bool):
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return 0
    return 0


def _as_float(value: Any) -> float:
    """Coerce value to float.

    Parameters
    ----------
    value : Any
        Input value.

    Returns
    -------
    float
        Parsed float or zero.
    """
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return 0.0
    return 0.0


def _ms_to_rfc3339(value: Any, fallback_ms: int) -> str:
    """Convert milliseconds timestamp to RFC3339 string.

    Parameters
    ----------
    value : Any
        Candidate timestamp value.
    fallback_ms : int
        Fallback timestamp in milliseconds.

    Returns
    -------
    str
        UTC RFC3339 timestamp.
    """
    ts_ms = _as_int(value)
    if ts_ms <= 0:
        ts_ms = fallback_ms
    return datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
