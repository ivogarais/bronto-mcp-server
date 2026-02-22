import pytest
from pydantic import ValidationError

from bronto.schemas import DashboardBuildInput, build_bronto_app_spec


def _sample_payload() -> dict:
    return {
        "title": "Errors (Last 30m)",
        "density": "comfortable",
        "bar_charts": [
            {
                "title": "Errors by Service",
                "labels": ["api", "worker", "web"],
                "values": [120, 80, 60],
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
            }
        ],
    }


def test_build_bronto_app_spec_contains_expected_sections():
    payload = DashboardBuildInput.model_validate(_sample_payload())

    spec = build_bronto_app_spec(payload)

    assert spec["version"] == "bronto-tui/v1"
    assert spec["title"] == "Errors (Last 30m)"
    assert spec["theme"]["brand"] == "bronto"
    assert "layout" in spec
    assert "charts" in spec
    assert "tables" in spec
    assert "datasets" in spec


def test_dashboard_build_input_requires_at_least_one_widget():
    with pytest.raises(ValidationError):
        DashboardBuildInput.model_validate(
            {"title": "Empty", "bar_charts": [], "tables": []}
        )


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
