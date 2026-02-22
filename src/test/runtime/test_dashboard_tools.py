from unittest.mock import Mock

import pytest

from bronto.agents import build_agent_registry
from bronto.clients import BrontoClient
from bronto.runtime import BrontoRuntime


def _sample_payload() -> dict:
    return {
        "title": "Errors (Last 30m)",
        "density": "comfortable",
        "bar_charts": [
            {
                "title": "Errors by Service",
                "labels": ["api", "worker"],
                "values": [120, 80],
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
                "rows": [["2026-02-22T12:00:01Z", "api", "NullPointerException"]],
            }
        ],
    }


@pytest.fixture
def runtime() -> BrontoRuntime:
    client = Mock(spec=BrontoClient)
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


def test_serve_dashboard_prepares_command_without_launch(monkeypatch, runtime, tmp_path):
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
    assert "bar_charts" in playbook
    assert "tables" in playbook
    assert "Do NOT use `widgets`, `chart`, or `charts`" in playbook
