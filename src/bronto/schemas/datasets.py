from typing import Annotated, Dict, List

from pydantic import BaseModel, Field


class Dataset(BaseModel):
    name: Annotated[
        str,
        Field(
            description="The dataset name. This often represents the name of the service that "
            "generates the log data that the dataset contains"
        ),
    ]
    collection: Annotated[
        str,
        Field(
            description="The name of the collection that the dataset belongs to. The same "
            "dataset name may be associated to different collections."
        ),
    ]
    log_id: Annotated[
        str,
        Field(
            description="The ID of the dataset. This ID is a UUID identifying a dataset uniquely"
        ),
    ]
    tags: Annotated[
        Dict[str, str],
        Field(
            description="Tags are key-value pair associated to the dataset. For instance,"
            '"environment"="production" may indicate that this dataset '
            "contains data generated from a production environment."
        ),
    ]


class DatasetKey(BaseModel):
    name: Annotated[
        str, Field(description="The name of the key, e.g. `environment`, `$service`, etc")
    ]
    values: Annotated[List[str], Field(default=[], description="Sample values of the key")]

    def add_values(self, values: List[str]) -> None:
        for value in values:
            if value in self.values:
                continue
            else:
                self.values.append(value)
