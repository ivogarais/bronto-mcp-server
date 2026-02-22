import pytest
import time
from datetime import datetime
from unittest.mock import Mock

from bronto.agents import build_agent_registry
from bronto.clients import BrontoClient
from bronto.runtime import BrontoRuntime
from bronto.schemas import (
    ContextQueryInput,
    Datapoint,
    ExportByIdInput,
    LogEvent,
    Timeseries,
    UsageQueryInput,
)


@pytest.fixture
def mock_bronto_client(monkeypatch):
    client_mock = Mock(spec=BrontoClient)
    return client_mock


@pytest.fixture
def bronto_tools(mock_bronto_client):
    return BrontoRuntime(mock_bronto_client, build_agent_registry())


def test_get_current_time():
    current_time = BrontoRuntime.get_current_time()
    assert isinstance(current_time, str)
    datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")


def test_get_timestamp_as_unix_epoch():
    test_time = "2025-05-01 00:00:00"
    timestamp = BrontoRuntime.get_timestamp_as_unix_epoch(test_time)
    assert isinstance(timestamp, int)
    assert timestamp == 1746057600000


def test_get_timestamp_as_unix_epoch_wrong_format():
    test_time = "2025/05/01 00:00:00"
    with pytest.raises(ValueError):
        BrontoRuntime.get_timestamp_as_unix_epoch(test_time)


def test_get_datasets(bronto_tools, mock_bronto_client):
    mock_datasets = [
        {
            "log": "test_dataset",
            "logset": "test_collection",
            "log_id": "test_log_id",
            "tags": {"team": "test_team"},
        }
    ]
    mock_bronto_client.get_datasets.return_value = mock_datasets
    datasets = bronto_tools.get_datasets()
    assert len(datasets) == 1
    assert datasets[0].name == "test_dataset"
    assert datasets[0].collection == "test_collection"
    assert datasets[0].log_id == "test_log_id"
    assert datasets[0].tags == {"team": "test_team"}


def test_get_datasets_by_name(bronto_tools, mock_bronto_client):
    mock_datasets = [
        {
            "log": "test_dataset",
            "logset": "test_collection",
            "log_id": "test_log_id",
            "tags": {"team": "test_team"},
        }
    ]
    mock_bronto_client.get_datasets.return_value = mock_datasets
    datasets = bronto_tools.get_datasets_by_name("test_dataset", "test_collection")
    assert len(datasets) == 1
    assert datasets[0].name == "test_dataset"


def test_get_datasets_by_name_no_match(bronto_tools, mock_bronto_client):
    mock_datasets = [
        {
            "log": "other_dataset",
            "logset": "other_collection",
            "log_id": "other_log_id",
            "tags": {},
        }
    ]
    mock_bronto_client.get_datasets.return_value = mock_datasets
    datasets = bronto_tools.get_datasets_by_name("test_dataset", "test_collection")
    assert len(datasets) == 0


def test_get_keys(monkeypatch):
    bronto_client = BrontoClient("some_api_key", "some_endpoint")
    monkeypatch.setattr(
        BrontoClient,
        "get_top_keys",
        lambda _, __: {"key1": ["value1", "1"], "key2": ["value2", "2"]},
    )
    bronto_tools = BrontoRuntime(bronto_client, build_agent_registry())
    keys = bronto_tools.get_keys("test_log_id")
    assert len(keys) == 2
    assert "key1" in keys
    assert "key2" in keys


def test_playbook_prompts_are_registered():
    registry = build_agent_registry()
    tool_names = {tool.name for tool in registry.iter_tool_specs()}

    assert "datasets_playbook" in tool_names
    assert "dashboard_playbook" in tool_names
    assert "search_logs_playbook" in tool_names
    assert "compute_metrics_playbook" in tool_names
    assert "statement_ids_playbook" in tool_names


def test_datasets_playbook_prompt(bronto_tools):
    prompt = bronto_tools.datasets_playbook()

    assert "get_datasets" in prompt
    assert "get_keys" in prompt
    assert "double-quoted" in prompt


def test_search_logs_playbook_prompt(bronto_tools):
    prompt = bronto_tools.search_logs_playbook()

    assert "log_ids" in prompt
    assert "get_timestamp_as_unix_epoch" in prompt
    assert "single-quoted" in prompt


def test_compute_metrics_playbook_prompt(bronto_tools):
    prompt = bronto_tools.compute_metrics_playbook()

    assert "COUNT(*)" in prompt
    assert "group_by_keys" in prompt
    assert "search_logs" in prompt


def test_statement_ids_playbook_prompt(bronto_tools):
    prompt = bronto_tools.statement_ids_playbook()

    assert "create_stmt_id" in prompt
    assert "inject_stmt_ids" in prompt
    assert "deploy_statements" in prompt


def test_get_key_values(bronto_tools, mock_bronto_client):
    mock_bronto_client.get_top_keys.return_value = {
        "service": ["api", "worker"],
        "agent.name": ["codex"],
    }

    values = bronto_tools.get_key_values("service", "test_log_id")

    mock_bronto_client.get_top_keys.assert_called_once_with("test_log_id")
    assert values == ["api", "worker"]


def test_get_key_values_missing_key_returns_empty_list(
    bronto_tools, mock_bronto_client
):
    mock_bronto_client.get_top_keys.return_value = {"service": ["api", "worker"]}

    values = bronto_tools.get_key_values("missing", "test_log_id")

    mock_bronto_client.get_top_keys.assert_called_once_with("test_log_id")
    assert values == []


def test_search_logs(bronto_tools, mock_bronto_client):
    log_event1 = LogEvent(message="test_event1", attributes={"key1": "value1"})
    log_event2 = LogEvent(message="test_event2", attributes={"key2": "value2"})
    mock_log_events = [log_event1, log_event2]
    mock_bronto_client.search.return_value = mock_log_events

    log_events = bronto_tools.search_logs(
        log_ids=["test_log_id"],
        timerange_start=int(time.time()) * 1000,
        timerange_end=int(time.time()) * 1000,
    )

    assert len(log_events) == 2
    assert log_event1 in log_events
    assert log_event2 in log_events


def test_compute_metrics_no_group(bronto_tools, mock_bronto_client):
    timestamp = BrontoRuntime.get_timestamp_as_unix_epoch("2023-01-01 00:00:00")
    mock_response = {
        "totals": {
            "count": 100,
            "timeseries": [
                {"@timestamp": timestamp, "count": 50, "quantiles": {}, "value": 10.5}
            ],
        }
    }
    mock_bronto_client.search_post.return_value = mock_response

    metrics = bronto_tools.compute_metrics(
        log_ids=["test_log_id"],
        metric_functions=["SUM"],
        timerange_start=int(time.time()) * 1000,
        timerange_end=int(time.time()) * 1000,
    )

    groups = list(metrics.keys())
    assert len(groups) == 1
    assert groups[0] == ""
    group = metrics[groups[0]]
    assert isinstance(group, Timeseries)
    assert group.count == 100
    assert len(group.timeseries) == 1
    assert group.timeseries[0] == Datapoint(
        timestamp=timestamp, count=50, quantiles={}, value=10.5
    )
    assert mock_bronto_client.search_post.call_args.kwargs["group_by_keys"] == []


def test_compute_metrics_single_group(bronto_tools, mock_bronto_client):
    timestamp = BrontoRuntime.get_timestamp_as_unix_epoch("2023-01-01 00:00:00")
    mock_response = {
        "groups_series": [
            {
                "name": "my_group",
                "count": 100,
                "timeseries": [
                    {
                        "@timestamp": timestamp,
                        "count": 50,
                        "quantiles": {},
                        "value": 10.5,
                    }
                ],
            }
        ]
    }
    mock_bronto_client.search_post.return_value = mock_response

    metrics = bronto_tools.compute_metrics(
        log_ids=["test_log_id"],
        metric_functions=["SUM"],
        timerange_start=int(time.time()) * 1000,
        timerange_end=int(time.time()) * 1000,
        group_by_keys=["some_key"],
    )

    groups = list(metrics.keys())
    assert len(groups) == 1
    assert groups[0] == "my_group"
    group = metrics[groups[0]]
    assert isinstance(group, Timeseries)
    assert group.count == 100
    assert len(group.timeseries) == 1
    assert group.timeseries[0] == Datapoint(
        timestamp=timestamp, count=50, quantiles={}, value=10.5
    )
    assert mock_bronto_client.search_post.call_args.kwargs["group_by_keys"] == [
        "some_key"
    ]


def test_compute_metrics_group_by_keys_string_is_normalized_to_list(
    bronto_tools, mock_bronto_client
):
    mock_bronto_client.search_post.return_value = {"groups_series": []}

    bronto_tools.compute_metrics(
        log_ids=["test_log_id"],
        metric_functions=["COUNT(*)"],
        timerange_start=int(time.time()) * 1000,
        timerange_end=int(time.time()) * 1000,
        group_by_keys="event.status",
    )

    assert mock_bronto_client.search_post.call_args.kwargs["group_by_keys"] == [
        "event.status"
    ]


def test_compute_metrics_group_by_keys_csv_string_is_split(
    bronto_tools, mock_bronto_client
):
    mock_bronto_client.search_post.return_value = {"groups_series": []}

    bronto_tools.compute_metrics(
        log_ids=["test_log_id"],
        metric_functions=["COUNT(*)"],
        timerange_start=int(time.time()) * 1000,
        timerange_end=int(time.time()) * 1000,
        group_by_keys="event.status, event.type",
    )

    assert mock_bronto_client.search_post.call_args.kwargs["group_by_keys"] == [
        "event.status",
        "event.type",
    ]


def test_list_api_keys(bronto_tools, mock_bronto_client):
    mock_bronto_client.list_api_keys.return_value = [{"id": "k1", "name": "prod"}]

    result = bronto_tools.list_api_keys()

    mock_bronto_client.list_api_keys.assert_called_once_with()
    assert result == [{"id": "k1", "name": "prod"}]


def test_list_users(bronto_tools, mock_bronto_client):
    mock_bronto_client.list_users.return_value = [{"id": "u1", "email": "a@b.c"}]

    result = bronto_tools.list_users()

    mock_bronto_client.list_users.assert_called_once_with()
    assert result == [{"id": "u1", "email": "a@b.c"}]


def test_get_context_forwards_named_arguments(bronto_tools, mock_bronto_client):
    mock_bronto_client.get_context.return_value = {"events": []}

    result = bronto_tools.get_context(
        ContextQueryInput(
            **{
                "from": "log_id_1",
                "from_tags": "environment=prod",
                "from_expr": "collection='core'",
                "sequence": 123,
                "timestamp": 456,
                "direction": "both",
                "limit": 50,
                "explain": True,
            }
        )
    )

    mock_bronto_client.get_context.assert_called_once_with(
        from_="log_id_1",
        from_tags="environment=prod",
        from_expr="collection='core'",
        sequence=123,
        timestamp=456,
        direction="both",
        limit=50,
        include_explain=True,
    )
    assert result == {"events": []}


def test_list_exports(bronto_tools, mock_bronto_client):
    mock_bronto_client.list_exports.return_value = [{"export_id": "exp1"}]

    result = bronto_tools.list_exports()

    mock_bronto_client.list_exports.assert_called_once_with()
    assert result == [{"export_id": "exp1"}]


def test_get_export(bronto_tools, mock_bronto_client):
    mock_bronto_client.get_export.return_value = {"export_id": "exp1", "status": "DONE"}

    result = bronto_tools.get_export(ExportByIdInput(export_id="exp1"))

    mock_bronto_client.get_export.assert_called_once_with("exp1")
    assert result["status"] == "DONE"


def test_get_usage_for_log_id_forwards_named_arguments(bronto_tools, mock_bronto_client):
    mock_bronto_client.get_usage_for_log_id.return_value = {"rows": []}

    result = bronto_tools.get_usage_for_log_id(
        UsageQueryInput(
            time_range="24h",
            from_ts=1000,
            to_ts=2000,
            usage_type="search",
            limit=25,
            num_of_slices=10,
            metric="bytes_total",
            delta=True,
            delta_time_range="24h",
            delta_from_ts=1,
            delta_to_ts=2,
        )
    )

    mock_bronto_client.get_usage_for_log_id.assert_called_once_with(
        time_range="24h",
        from_ts=1000,
        to_ts=2000,
        usage_type="search",
        limit=25,
        num_of_slices=10,
        metric="bytes_total",
        delta=True,
        delta_time_range="24h",
        delta_from_ts=1,
        delta_to_ts=2,
    )
    assert result == {"rows": []}


def test_get_usage_for_user_per_log_id_forwards_named_arguments(
    bronto_tools, mock_bronto_client
):
    mock_bronto_client.get_usage_for_user_per_log_id.return_value = {"rows": []}

    result = bronto_tools.get_usage_for_user_per_log_id(
        UsageQueryInput(
            time_range="24h",
            from_ts=1000,
            to_ts=2000,
            usage_type="ingestion",
            limit=25,
            num_of_slices=10,
            metric="event_count",
            delta=False,
            delta_time_range="24h",
            delta_from_ts=1,
            delta_to_ts=2,
        )
    )

    mock_bronto_client.get_usage_for_user_per_log_id.assert_called_once_with(
        time_range="24h",
        from_ts=1000,
        to_ts=2000,
        usage_type="ingestion",
        limit=25,
        num_of_slices=10,
        metric="event_count",
        delta=False,
        delta_time_range="24h",
        delta_from_ts=1,
        delta_to_ts=2,
    )
    assert result == {"rows": []}


def test_list_forward_configs(bronto_tools, mock_bronto_client):
    mock_bronto_client.list_forward_configs.return_value = [{"id": "fwd-1"}]

    result = bronto_tools.list_forward_configs()

    mock_bronto_client.list_forward_configs.assert_called_once_with()
    assert result == [{"id": "fwd-1"}]
