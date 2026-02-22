from bronto.schemas import Dataset, DatasetKey


def test_dataset_model_fields():
    dataset = Dataset(
        name="ai-agent",
        collection="local-dev",
        log_id="fb7f985f-3558-0232-d30e-42142719a400",
        tags={"environment": "dev"},
    )

    assert dataset.name == "ai-agent"
    assert dataset.collection == "local-dev"
    assert dataset.tags["environment"] == "dev"


def test_dataset_key_add_values_deduplicates_and_appends_new_values():
    key = DatasetKey(name="service", values=["api"])

    key.add_values(["api", "worker", "api", "cron"])

    assert key.values == ["api", "worker", "cron"]
