import pytest

from bronto.schemas import ComputeMetricsInput, Datapoint, LogEvent, SearchLogsInput, Timeseries


def test_log_event_add_attribute_updates_existing_value():
    event = LogEvent(message="hello", attributes={"service": "api"})

    event.add_attribute("service", "worker")
    event.add_attribute("level", "info")

    assert event.attributes == {"service": "worker", "level": "info"}


def test_log_event_default_attributes_are_isolated_between_instances():
    first = LogEvent(message="first")
    second = LogEvent(message="second")

    first.add_attribute("stmt_id", "abcd")

    assert first.attributes == {"stmt_id": "abcd"}
    assert second.attributes == {}


def test_timeseries_model_contains_datapoints():
    datapoint = Datapoint(timestamp=1, count=2, quantiles={}, value=3.5)
    series = Timeseries(count=2, timeseries=[datapoint])

    assert series.count == 2
    assert len(series.timeseries) == 1
    assert series.timeseries[0].value == 3.5


def test_compute_metrics_accepts_utc_datetime_strings_for_timerange():
    payload = ComputeMetricsInput(
        log_ids=["fb7f985f-3558-0232-d30e-42142719a400"],
        metric_functions=["COUNT(*)"],
        timerange_start="2024-01-01 00:00:00",
        timerange_end="2026-02-22 23:59:59",
    )

    assert payload.timerange_start == 1704067200000
    assert payload.timerange_end == 1771804799000


def test_search_logs_accepts_unix_ms_string_for_timerange():
    payload = SearchLogsInput(
        log_ids=["fb7f985f-3558-0232-d30e-42142719a400"],
        timerange_start="1704067200000",
        timerange_end="1771804799000",
    )

    assert payload.timerange_start == 1704067200000
    assert payload.timerange_end == 1771804799000


def test_compute_metrics_rejects_invalid_datetime_format():
    with pytest.raises(ValueError):
        ComputeMetricsInput(
            log_ids=["fb7f985f-3558-0232-d30e-42142719a400"],
            metric_functions=["COUNT(*)"],
            timerange_start="2024/01/01 00:00:00",
        )


def test_search_logs_accepts_filter_alias():
    payload = SearchLogsInput(
        log_ids=["fb7f985f-3558-0232-d30e-42142719a400"],
        filter="\"event.status\" = 'ERROR'",
    )

    assert payload.search_filter == "\"event.status\" = 'ERROR'"


def test_compute_metrics_accepts_filter_alias():
    payload = ComputeMetricsInput(
        log_ids=["fb7f985f-3558-0232-d30e-42142719a400"],
        metric_functions=["COUNT(*)"],
        filter="\"level\"='error'",
    )

    assert payload.search_filter == "\"level\"='error'"
