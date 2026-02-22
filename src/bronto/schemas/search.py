from typing import Annotated, Dict, List

from pydantic import BaseModel, Field


class LogEvent(BaseModel):
    message: Annotated[
        str,
        Field(
            description="The message of the event. This represents a log message generated from a "
            "log statement in a piece of software"
        ),
    ]
    attributes: Annotated[
        Dict[str, str],
        Field(
            default_factory=dict,
            description="List of attributes associated to the log event. An attribute is a key-value "
            "pair that provide context about the event. For instance, "
            '"$hostname"="i-1234567890" may indicate that the service generated the log event'
            ' on the host named "i-1234567890"',
        ),
    ]

    def add_attribute(self, key: str, value: str) -> None:
        """Associate the key=value key-value pair to the log event. If the key is already associated to the log event,
        then the previously associated value is overwritten with the new one.
        """
        self.attributes.update({key: value})


class Datapoint(BaseModel):
    timestamp: Annotated[
        int, Field(description="The unix epoch timestamp of the datapoint")
    ]
    count: Annotated[
        int,
        Field(
            description="The number of events used to compute the metric value of the datapoint"
        ),
    ]
    quantiles: Annotated[
        Dict[float, float], Field(description="Map containing quantiles values")
    ]
    value: Annotated[
        float, Field(description="The value of the metric associated to the datapoint")
    ]


class Timeseries(BaseModel):
    count: Annotated[
        int,
        Field(
            description="The number of events used to compute the total metric value"
        ),
    ]
    timeseries: Annotated[
        List[Datapoint], Field(description="A list of datapoints per timestamp")
    ]
