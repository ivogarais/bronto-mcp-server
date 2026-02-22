from bronto.schemas import Datapoint, LogEvent, Timeseries


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
