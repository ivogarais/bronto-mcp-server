from unittest.mock import Mock

import pytest

from bronto.agents import build_agent_registry
from bronto.clients import BrontoClient
from bronto.runtime import BrontoRuntime


def _sample_payload() -> dict:
    return {
        "title": "Errors (Last 30m)",
        "density": "comfortable",
        "charts": [
            {
                "title": "Errors by Service",
                "family": "bar",
                "labels": ["api", "worker"],
                "values": [120, 80],
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
                    {"key": "@time", "title": "ts", "width": "auto"},
                    {"key": "service", "title": "service", "width": 12},
                    {"key": "message", "title": "message", "width": "flex"},
                ],
                "rows": [["2026-02-22T12:00:01Z", "api", "NullPointerException"]],
                "live_query": {
                    "mode": "logs",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "search_filter": "\"level\"='error'",
                    "limit": 20,
                },
            }
        ],
    }


def _sample_timeseries_payload() -> dict:
    return {
        "title": "AI Agent SRE Essentials",
        "charts": [
            {
                "title": "Req Volume (30m)",
                "family": "timeseries",
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ["COUNT(*)"],
                    "group_by_keys": [],
                    "lookback_sec": 1800,
                    "limit": 200,
                },
            }
        ],
        "tables": [],
    }


def _sample_line_payload() -> dict:
    return {
        "title": "AI Agent SRE Essentials",
        "charts": [
            {
                "title": "Avg Latency ms",
                "family": "line",
                "live_query": {
                    "mode": "metrics",
                    "log_ids": ["fb7f985f-3558-0232-d30e-42142719a400"],
                    "metric_functions": ['AVG("event.latencyMs")'],
                    "group_by_keys": [],
                    "lookback_sec": 1800,
                    "limit": 120,
                },
            }
        ],
        "tables": [],
    }


@pytest.fixture
def runtime() -> BrontoRuntime:
    client = Mock(spec=BrontoClient)
    client.search_post.return_value = {"totals": {"count": 0, "timeseries": []}}
    client.search.return_value = []
    return BrontoRuntime(client, build_agent_registry())


def test_build_dashboard_spec_returns_valid_document(runtime):
    spec = runtime.build_dashboard_spec(_sample_payload())

    assert spec["version"] == "bronto-tui/v1"
    assert spec["title"] == "Errors (Last 30m)"
    assert spec["theme"]["brand"] == "bronto"


def test_serve_dashboard_executes_bronto(monkeypatch, runtime, tmp_path):
    command_calls = []

    def _fake_run(command, check):
        command_calls.append(command)
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.shutil.which",
        lambda _: "/usr/local/bin/bronto",
    )
    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.subprocess.run", _fake_run
    )

    spec_path = tmp_path / "dashboard.json"
    result = runtime.serve_dashboard(
        _sample_payload(), spec_file_path=str(spec_path), launch_mode="blocking"
    )

    assert command_calls == [
        ["/usr/local/bin/bronto", "serve", "--spec", str(spec_path)]
    ]
    assert result["status"] == "ok"
    assert result["spec_retained"] is True
    assert spec_path.exists()


def test_serve_dashboard_fails_when_bronto_is_missing(monkeypatch, runtime):
    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.shutil.which", lambda _: None
    )

    with pytest.raises(RuntimeError, match="Could not find `bronto` in PATH"):
        runtime.serve_dashboard(_sample_payload())


def test_serve_dashboard_prepares_command_without_launch(
    monkeypatch, runtime, tmp_path
):
    subprocess_calls = []

    def _fake_run(command, check):
        subprocess_calls.append(command)
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.shutil.which",
        lambda _: "/usr/local/bin/bronto",
    )
    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.subprocess.run", _fake_run
    )

    spec_path = tmp_path / "dashboard.json"
    result = runtime.serve_dashboard(
        _sample_payload(), spec_file_path=str(spec_path), launch_mode="none"
    )

    assert subprocess_calls == []
    assert result["status"] == "prepared"
    assert result["command"] == [
        "/usr/local/bin/bronto",
        "serve",
        "--spec",
        str(spec_path),
    ]
    assert result["spec_path"] == str(spec_path)
    assert result["spec_retained"] is True
    assert "command_str" in result
    assert spec_path.exists()
    assert result["command_str"].startswith("bronto serve --spec ")


def test_serve_dashboard_rejects_invalid_launch_mode(monkeypatch, runtime):
    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.shutil.which",
        lambda _: "/usr/local/bin/bronto",
    )

    with pytest.raises(ValueError, match="Invalid launch_mode"):
        runtime.serve_dashboard(_sample_payload(), launch_mode="async")


def test_dashboard_playbook_returns_expected_guidance(runtime):
    playbook = runtime.dashboard_playbook()

    assert "Required top-level shape" in playbook
    assert "charts" in playbook
    assert "tables" in playbook
    assert "Do NOT use top-level `widgets` or `chart`" in playbook


def test_serve_dashboard_hydrates_live_timeseries_seed_data(
    monkeypatch, runtime, tmp_path
):
    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.shutil.which",
        lambda _: "/usr/local/bin/bronto",
    )
    runtime.bronto_client.search_post.return_value = {
        "totals": {
            "count": 42,
            "timeseries": [
                {
                    "@timestamp": 1771802470000,
                    "count": 42,
                    "quantiles": {},
                    "value": 42,
                }
            ],
        }
    }

    spec_path = tmp_path / "dashboard.json"
    result = runtime.serve_dashboard(
        _sample_timeseries_payload(),
        spec_file_path=str(spec_path),
        launch_mode="none",
    )

    assert result["status"] == "prepared"
    spec = spec_path.read_text(encoding="utf-8")
    assert '"family": "timeseries"' in spec
    assert '"series": [' in spec
    assert '"name": "total"' in spec
    assert '"points": [' in spec


def test_serve_dashboard_hydrates_live_line_seed_data(monkeypatch, runtime, tmp_path):
    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.shutil.which",
        lambda _: "/usr/local/bin/bronto",
    )
    runtime.bronto_client.search_post.return_value = {
        "totals": {
            "count": 42,
            "timeseries": [
                {
                    "@timestamp": 1771802470000,
                    "count": 42,
                    "quantiles": {},
                    "value": 123.4,
                }
            ],
        }
    }

    spec_path = tmp_path / "line-dashboard.json"
    result = runtime.serve_dashboard(
        _sample_line_payload(),
        spec_file_path=str(spec_path),
        launch_mode="none",
    )

    assert result["status"] == "prepared"
    spec = spec_path.read_text(encoding="utf-8")
    assert '"family": "line"' in spec
    assert '"line": {' in spec
    assert '"series": [' in spec
    assert '"name": "total"' in spec
    assert '"xy": [' in spec


def test_serve_dashboard_writes_default_specs_to_dashboards_folder(
    monkeypatch, runtime, tmp_path
):
    monkeypatch.setattr(
        "bronto.agents.dashboard.tools.handlers.shutil.which",
        lambda _: "/usr/local/bin/bronto",
    )
    monkeypatch.setenv("HOME", str(tmp_path))

    result = runtime.serve_dashboard(_sample_payload(), launch_mode="none")

    expected_dir = tmp_path / "bronto-dashboards"
    assert result["status"] == "prepared"
    assert result["spec_path"].startswith(str(expected_dir))
    assert result["command_str"].startswith("bronto serve --spec ")
