from typing import Dict, List

from pydantic import Field
from typing_extensions import Annotated

from bronto.agents.playbooks import resolve_playbook
from bronto.clients import BrontoClient
from bronto.schemas import Dataset


class DatasetsToolHandlers:
    """Dataset discovery and metadata handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def get_datasets(
        self,
    ) -> Annotated[
        List[Dataset],
        Field(
            description="""List of datasets. Each dataset object contains
                - the name of the dataset
                - the collection it belongs to
                - its log ID, which is a UUID, i.e. a 36 character long string
                - a list of tags associated to the dataset. Each tag is a key-value pair. Both keys and values are 
                represented as strings. Tags such as the `description` tag are particularly useful to understand the type 
                of data that the dataset contains. Other common tags are `service`, `teams` and `environment`"""
        ),
    ]:
        datasets_data = self.bronto_client.get_datasets()
        return [
            Dataset(
                name=dataset["log"],
                collection=dataset["logset"],
                log_id=dataset["log_id"],
                tags=dataset["tags"],
            )
            for dataset in datasets_data
        ]

    def get_datasets_by_name(
        self,
        dataset_name: Annotated[
            str, Field(description="The dataset name", min_length=1)
        ],
        collection_name: Annotated[
            str,
            Field(
                description="The collection that the dataset is part of", min_length=1
            ),
        ],
    ) -> Annotated[
        List[Dataset],
        Field(
            description="List of datasets whose name and collection match the ones provided with the `dataset_name` "
            "and `collection_name` parameters. Details contains for instance the dataset log ID as well "
            "as all the tags associated to this dataset."
        ),
    ]:
        datasets = self.bronto_client.get_datasets()
        return [
            Dataset(
                name=dataset["log"],
                collection=dataset["logset"],
                log_id=dataset["log_id"],
                tags=dataset["tags"],
            )
            for dataset in datasets
            if dataset["log"] == dataset_name and dataset["logset"] == collection_name
        ]

    def get_keys(
        self,
        log_id: Annotated[
            str,
            Field(
                description="The dataset ID, also named log ID",
                min_length=36,
                max_length=36,
            ),
        ],
    ) -> Annotated[
        List[str],
        Field(
            description="list key names for keys present in the provided dataset referenced with the `log_id` parameter"
        ),
    ]:
        return [dataset.name for dataset in self.bronto_client.get_keys(log_id)]

    def get_all_datasets_keys(
        self,
    ) -> Annotated[
        Dict[str, List[str]],
        Field(
            description="Map from dataset IDs to the list of key names, for keys present in each dataset"
        ),
    ]:
        return self.bronto_client.get_all_datasets_top_keys()

    def get_key_values(
        self,
        key: Annotated[str, Field(description="The name of a key")],
        log_id: Annotated[str, Field(description="A string representing a dataset ID")],
    ) -> Annotated[
        List[str],
        Field(
            description="The list of values of the provided key, present in the provided "
            "dataset."
        ),
    ]:
        dataset_top_keys = self.bronto_client.get_top_keys(log_id)
        return dataset_top_keys.get(key, [])

    @staticmethod
    def datasets_playbook() -> Annotated[
        str,
        Field(
            description=(
                "Playbook that explains a safe dataset and key-discovery "
                "workflow before running searches."
            )
        ),
    ]:
        return resolve_playbook(
            "bronto.agents.datasets", "playbooks/datasets_playbook.md"
        )
