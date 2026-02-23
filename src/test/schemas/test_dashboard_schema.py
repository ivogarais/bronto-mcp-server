import pytest
from pydantic import ValidationError

from bronto.schemas import DashboardBuildInput, build_bronto_app_spec


def _sample_payload() -> dict:
    return {
        "title": "Errors (Last 30m)",
        "density": "comfortable",
        "charts": [
            {
                "title": "Errors by Service",
                "family": "bar",
                "labels": ["api", "worker", "web"],
                "values": [120, 80, 60],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                    "group_by_keys": ["service"],
                },
            }
        ],
        "tables": [
            {
                "title": "Latest Errors",
                "columns": [
                    {"title": "ts", "width": "auto"},
                    {"title": "service", "width": 12},
                    {"title": "message", "width": "flex"},
                ],
                "rows": [
                    ["2026-02-22T12:00:01Z", "api", "NullPointerException"],
                    ["2026-02-22T12:00:03Z", "worker", "timeout contacting db"],
                ],
                "row_limit": 200,
                "live_query": {
                    "mode": "logs",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "search_filter": "\"level\"='error'",
                    "limit": 25,
                },
            }
        ],
    }


def test_build_bronto_app_spec_contains_expected_sections():
    payload = DashboardBuildInput.model_validate(_sample_payload())

    spec = build_bronto_app_spec(payload)

    assert spec["version"] == "bronto-tui/v1"
    assert spec["title"] == "Errors (Last 30m)"
    assert spec["theme"]["brand"] == "bronto"
    assert "charts" in spec
    assert "tables" in spec
    assert "datasets" in spec
    first_table_ref = next(iter(spec["tables"]))
    assert spec["tables"][first_table_ref]["title"] == "Latest Errors"


def test_dashboard_build_input_requires_at_least_one_widget():
    with pytest.raises(ValidationError):
        DashboardBuildInput.model_validate({"title": "Empty", "charts": [], "tables": []})


def test_dashboard_table_column_title_has_length_limit():
    payload = _sample_payload()
    payload["tables"][0]["columns"][0]["title"] = "this column title is way too long"

    with pytest.raises(ValidationError):
        DashboardBuildInput.model_validate(payload)


def test_dashboard_table_rows_must_match_column_count():
    payload = _sample_payload()
    payload["tables"][0]["rows"] = [["only", "two"]]

    with pytest.raises(ValidationError):
        DashboardBuildInput.model_validate(payload)


def test_dashboard_payload_rejects_unknown_top_level_keys():
    payload = _sample_payload()
    payload["chart"] = {"title": "Errors", "type": "metric"}

    with pytest.raises(ValidationError) as exc_info:
        DashboardBuildInput.model_validate(payload)

    assert "Extra inputs are not permitted" in str(exc_info.value)


def test_dashboard_column_keys_are_normalized_and_deduplicated():
    payload = _sample_payload()
    payload["tables"][0]["columns"] = [
        {"title": "Service"},
        {"title": "Service"},
        {"title": "Message"},
    ]
    payload["tables"][0]["rows"] = [
        ["api", "worker", "boom"],
    ]

    spec = build_bronto_app_spec(DashboardBuildInput.model_validate(payload))

    table_ref = next(iter(spec["tables"]))
    columns = spec["tables"][table_ref]["columns"]
    keys = [column["key"] for column in columns]
    assert keys == ["service", "service_2", "message"]


def test_dashboard_build_input_supports_all_chart_families():
    payload = {
        "title": "All Families",
        "charts": [
            {
                "title": "Bar",
                "family": "bar",
                "labels": ["a", "b"],
                "values": [1, 2],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                    "group_by_keys": ["event.type"],
                },
            },
            {
                "title": "Line",
                "family": "line",
                "xy": [{"name": "p95", "points": [{"x": 1, "y": 2}]}],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["AVG(\"event.latencyMs\")"],
                },
            },
            {
                "title": "Scatter",
                "family": "scatter",
                "xy": [{"name": "p95", "points": [{"x": 1, "y": 2}]}],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["AVG(\"event.latencyMs\")"],
                },
            },
            {
                "title": "Waveline",
                "family": "waveline",
                "xy": [{"name": "p95", "points": [{"x": 1, "y": 2}]}],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["AVG(\"event.latencyMs\")"],
                },
            },
            {
                "title": "Heatmap",
                "family": "heatmap",
                "heatmap": {"width": 2, "height": 1, "values": [0.2, 0.8]},
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                },
            },
            {
                "title": "OHLC",
                "family": "ohlc",
                "candles": [
                    {
                        "t": "2026-02-22T12:00:00Z",
                        "open": 10,
                        "high": 12,
                        "low": 9,
                        "close": 11,
                    }
                ],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                },
            },
            {
                "title": "Spark",
                "family": "sparkline",
                "value": [1, 2, 3],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                },
            },
            {
                "title": "Stream",
                "family": "streamline",
                "value": [1, 2, 3],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                },
            },
            {
                "title": "Time",
                "family": "timeseries",
                "time": [
                    {
                        "name": "req_rate",
                        "points": [{"t": "2026-02-22T12:00:00Z", "v": 100}],
                    }
                ],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                },
            },
        ],
    }

    spec = build_bronto_app_spec(DashboardBuildInput.model_validate(payload))

    assert set(chart["family"] for chart in spec["charts"].values()) == {
        "bar",
        "line",
        "scatter",
        "waveline",
        "heatmap",
        "ohlc",
        "sparkline",
        "streamline",
        "timeseries",
    }
    assert set(chart["title"] for chart in spec["charts"].values()) == {
        "Bar",
        "Line",
        "Scatter",
        "Waveline",
        "Heatmap",
        "OHLC",
        "Spark",
        "Stream",
        "Time",
    }


def test_dashboard_build_input_emits_live_query_spec():
    payload = {
        "title": "Live Errors",
        "charts": [
            {
                "title": "Errors by Type",
                "family": "bar",
                "labels": ["seed"],
                "values": [0],
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                    "group_by_keys": ["event.type"],
                    "lookback_sec": 900,
                },
            }
        ],
        "tables": [
            {
                "title": "Recent Errors",
                "columns": [{"title": "event.type"}, {"title": "message"}],
                "rows": [],
                "live_query": {
                    "mode": "logs",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "search_filter": "\"level\"='error'",
                    "limit": 50,
                },
            }
        ],
    }

    spec = build_bronto_app_spec(DashboardBuildInput.model_validate(payload))
    chart_dataset = spec["datasets"]["chart_dataset_1"]
    table_dataset = spec["datasets"]["table_dataset_1"]

    assert chart_dataset["liveQuery"]["mode"] == "metrics"
    assert chart_dataset["liveQuery"]["logIds"] == [
        "fb7f985f-3558-0232-d30e-42142719a400"
    ]
    assert chart_dataset["liveQuery"]["metricFunctions"] == ["COUNT(*)"]
    assert table_dataset["liveQuery"]["mode"] == "logs"
    assert table_dataset["liveQuery"]["limit"] == 50


def test_dashboard_build_input_rejects_missing_live_query():
    with pytest.raises(ValidationError):
        DashboardBuildInput.model_validate(
            {
                "title": "Missing live query",
                "charts": [
                    {
                        "title": "Errors by Service",
                        "family": "bar",
                        "labels": ["api"],
                        "values": [1],
                    }
                ],
            }
        )


def test_dashboard_build_input_rejects_legacy_bar_charts():
    with pytest.raises(ValidationError):
        DashboardBuildInput.model_validate(
            {
                "title": "Legacy shape",
                "bar_charts": [
                    {"title": "Errors", "labels": ["api"], "values": [1]}
                ],
            }
        )
