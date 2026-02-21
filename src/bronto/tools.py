import time
import logging
import uuid

from pydantic import Field, BeforeValidator
from typing_extensions import Annotated
from datetime import datetime, timezone
from typing import List, Optional, Dict
from agents import BrontoAgentRegistry, create_default_agent_registry
from models import Dataset, LogEvent, Datapoint, Timeseries

from clients import BrontoClient

logger = logging.getLogger()


class BrontoTools:
    """Tools to interact with log data stored in Bronto"""

    def __init__(
        self,
        bronto_client: BrontoClient,
        agent_registry: Optional[BrontoAgentRegistry] = None,
    ):
        self.bronto_client = bronto_client
        self.agent_registry = agent_registry or create_default_agent_registry()

    def register(self, mcp):
        for tool_spec in self.agent_registry.iter_tool_specs():
            handler = getattr(self, tool_spec.handler, None)
            if handler is None:
                raise AttributeError(f"Unknown tool handler: {tool_spec.handler}")
            if tool_spec.kind == "prompt":
                mcp.prompt(name=tool_spec.name)(handler)
            else:
                mcp.tool(name=tool_spec.name)(handler)

    def search_logs(
        self,
        timerange_start: Annotated[
            Optional[int],
            Field(
                description="Unix timestamp in millisecond representing the start of a time range, e.g. 1756063146000. "
                "If not specify, the current time is selected",
                default_factory=lambda _: (int(time.time()) - (20 * 60)) * 1000,
            ),
        ],
        timerange_end: Annotated[
            Optional[int],
            Field(
                description="Unix timestamp in millisecond representing the end of a time range, e.g. 1756063254000. "
                "If not specify, the time from 20 minutes ago is selected",
                default_factory=lambda _: int(time.time()) * 1000,
            ),
        ],
        log_ids: Annotated[
            list[str],
            Field(
                description="List of dataset IDs, identifying sets of log data. Each log ID "
                "represents a UUID",
                min_length=1,
            ),
        ],
        search_filter: Annotated[
            Optional[str],
            Field(
                default="",
                description="""
                If no value is specified for this field, then no filter is apply when searching log data. Otherwise, 
                this field must follow the syntax of an SQL `WHERE` clause. Unless the search filter is 
                explicitly provided by the user, it is CRITICAL to use keys present in the dataset, e.g. 
                "key_name"='key_value'. For this, the list of keys present in dataset can be retrieved via another tool 
                exposed by this MCP server. In any case, following SQL syntax,
                    - key names should be double-quoted
                    - key value should be single-quoted if they are expected to be strings of characters
                    - key value should not be quoted if they are expected to be numbers.""",
            ),
        ] = "",
    ) -> Annotated[
        List[LogEvent],
        Field(
            description="A list of log events and their attributes. Attributes are key-value pairs associated with "
            "the event, e.g. key=value"
        ),
    ]:
        logger.info(
            "timerange_start=%s, timerange_end=%s, log_ids=%s",
            timerange_start,
            timerange_end,
            log_ids,
        )
        log_events = self.bronto_client.search(
            timerange_start,
            timerange_end,
            log_ids,
            search_filter,
            _select=["*", "@raw"],
        )
        return log_events

    def compute_metrics(
        self,
        timerange_start: Annotated[
            int,
            Field(
                description="Unix timestamp in millisecond representing the start of a time range, e.g. 1756063146000",
                default_factory=lambda _: (int(time.time()) - (20 * 60)) * 1000,
            ),
        ],
        timerange_end: Annotated[
            int,
            Field(
                description="Unix timestamp in millisecond representing the end of a time range, e.g. 1756063254000",
                default_factory=lambda _: int(time.time()) * 1000,
            ),
        ],
        log_ids: Annotated[
            list[str],
            Field(
                description="List of dataset IDs, identifying sets of log data. Each log ID "
                "represents a UUID",
                min_length=1,
            ),
        ],
        metric_functions: Annotated[
            list[str],
            Field(
                description="""
                The metric function can be one of AVG, MIN, MAX, COUNT, MEAN, MEDIAN and SUM. The metric function takes a 
                key name as attribute, except for COUNT which only takes the character '*' as attribute (i.e. 
                "COUNT(*)"). Key names can be determined for given datasets, using one of the other tools provided by 
                this MCP server."""
            ),
        ],
        search_filter: Annotated[
            str,
            Field(
                description="""
                The `search_filter` attribute can follow the syntax of an SQL `WHERE` clause. Unless the search filter is 
                explicitly provided by the user, it is CRITICAL to use keys present in the dataset, e.g. 
                "key_name"='key_value'. For this, the list of keys present in dataset can be retrieved via another tool 
                exposed by this MCP server. In any case, following SQL syntax,
                    - key names should be double-quoted
                    - key value should be single-quoted if they are expected to be strings of characters
                    - key value should not be quoted if they are expected to be numbers."""
            ),
        ] = "",
        group_by_keys: Annotated[
            List[str],
            Field(
                description="List of keys expected to be present in log datasets and "
                "by which the metric computed should be grouped"
            ),
        ] = None,
    ) -> Annotated[
        Dict[str, Timeseries],
        Field(
            description="Map of Timeseries. The keys of the map represent group names based on the group_by_keys "
            "parameter. The Timeseries represent a list of data points for the given group. Each list "
            "represents the value of the computed metrics for a subset of the provided time range"
        ),
    ]:
        if group_by_keys is None:
            group_by_keys = []
        logger.info(
            "timerange_start=%s, timerange_end=%s, log_ids=%s, metric_functions=%s, group_by_keys=[%s]",
            timerange_start,
            timerange_end,
            log_ids,
            ",".join(metric_functions),
            ",".join(group_by_keys),
        )
        resp = self.bronto_client.search_post(
            timerange_start,
            timerange_end,
            log_ids,
            search_filter,
            _select=metric_functions,
            group_by_keys=[",".join(group_by_keys)],
        )
        if len(group_by_keys) == 0:
            totals = resp["totals"]
            count = totals["count"]
            timeseries = totals.get("timeseries", [])
            name = ""
            group_series = [{"name": name, "timeseries": timeseries, "count": count}]
        else:
            group_series = resp.get("groups_series", [])
        result = {}
        for group_serie in group_series:
            datapoints = []
            for datapoint in group_serie.get("timeseries", []):
                datapoints.append(
                    Datapoint(
                        timestamp=datapoint["@timestamp"],
                        count=datapoint["count"],
                        quantiles=datapoint["quantiles"],
                        value=datapoint["value"],
                    )
                )
            timeseries = Timeseries(count=group_serie["count"], timeseries=datapoints)
            result[group_serie["name"]] = timeseries
        return result

    @staticmethod
    def _validate_input_time(input_time: str) -> str:
        try:
            datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
            return input_time
        except ValueError as e:
            raise e

    @staticmethod
    def get_timestamp_as_unix_epoch(
        input_time: Annotated[
            str,
            BeforeValidator(_validate_input_time),
            Field(
                description='Time represented in the "%Y-%m-%d %H:%M:%S" format. Timezone is assumed to be UTC'
            ),
        ],
    ) -> Annotated[
        int,
        Field(
            description="A unix timestamp (in milliseconds) since epoch, representing the `input_time` parameter"
        ),
    ]:
        return (
            int(
                datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
                .replace(tzinfo=timezone.utc)
                .timestamp()
            )
            * 1000
        )

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
        result = []
        for dataset in datasets_data:
            result.append(
                Dataset(
                    name=dataset["log"],
                    collection=dataset["logset"],
                    log_id=dataset["log_id"],
                    tags=dataset["tags"],
                )
            )
        return result

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
        result = []
        collection_names = [dataset["logset"] for dataset in datasets]
        if len(collection_names) == 0:
            return []
        for dataset in datasets:
            if dataset["log"] != dataset_name or dataset["logset"] != collection_name:
                continue
            result.append(
                Dataset(
                    name=dataset["log"],
                    collection=dataset["logset"],
                    log_id=dataset["log_id"],
                    tags=dataset["tags"],
                )
            )
        if len(result) == 0:
            return []
        return result

    def get_dataset_keys(
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
        keys = [dataset.name for dataset in self.bronto_client.get_keys(log_id)]
        return keys

    def get_all_datasets_keys(
        self,
    ) -> Annotated[
        Dict[str, List[str]],
        Field(
            description="Map from dataset IDs to the list of key names, for keys present in each dataset"
        ),
    ]:
        keys = self.bronto_client.get_all_datasets_top_keys()
        return keys

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
        datasets_top_keys_and_values = (
            self.bronto_client.get_all_datasets_top_keys_and_values()
        )
        keys_and_values = datasets_top_keys_and_values.get(log_id, {})
        key_and_values = keys_and_values.get(key, {})
        return key_and_values.get("values", {}).get(key, [])

    @staticmethod
    def get_current_time() -> Annotated[
        str, Field(description="the current time in the YYYY-MM-DD HH:mm:ss format")
    ]:
        return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create_stmt_id() -> Annotated[
        str,
        Field(
            description="A statement ID, i.e. a 16 character logn string that can "
            "be used to uniquely identify a log statement"
        ),
    ]:
        return uuid.uuid4().hex[:16]

    @staticmethod
    def inject_stmt_ids(
        src_path: Annotated[
            str,
            Field(
                description="The path to the source code where statement IDs should be "
                "injected into"
            ),
        ],
    ) -> Annotated[
        str,
        Field(description="A prompt indicating how to inject IDs in log statements"),
    ]:
        return f"""A statement ID is a string of characters that uniquely identify a log statement. In order to inject 
        statement IDs, simply update log statements by appending ' stmt_id=<STMT_ID>'. The value of STMT_ID should be 
        constant and unique per log statement. Below are examples of log statements, based on the Python programming 
        language, before and after injecting statement IDs:
        logger.info('a simple log statement') --> logger.info('a simple log statement stmt_id=8320e3c149f34c28')
        logger.info('a log statement with a placeholder %s', value) --> logger.info('a log statement with a placeholder %s stmt_id=be7e775bbaf949a3', value)
        logger.info(expr_representing_a_string) --> logger.info(expr_representing_a_string + ' stmt_id=e0c64be98903425a')
        logger.info('a multiline ' + 
                    'log statement') --> logger.info('a multiline ' + 
                                                     'log statement stmt_id=12fd106cdffc4a09')  
        If structured logging is used in the codebase, such as using the `extra` parameter in Python or the Fluent 
        logging API in Java, then the same pattern should be used to inject statement IDs, e.g. in Python         

        logger.info('a simple log statement') --> logger.info('a simple log statement', extra={{'stmt_id': '8320e3c149f34c28'}})

        and in Java with the Fluent API:
        
        logger.atInfo().setMessage("a simple log statement").log() --> logger.atInfo().setMessage("a simple log statement").addKeyValue("stmt_id, "8320e3c149f34c28").log()

        Also, check available tools that generate statement IDs.
        Finally, the following applies:
        - Statement IDs should only be injected into source code located under {src_path} 
        - Only one statement ID should be defined per log statement.
        - Statement IDs should be injected in log statement messages, regardless of the severity of the log statement
        - Event though the samples above focus on the Python programming language, statement IDs should be injected 
        regardless of the programming language used.
        """

    @staticmethod
    def extract_stmt_ids(
        stmt_id_filepath: str = "statementIds.csv",
    ) -> Annotated[
        str,
        Field(
            description="A prompt that describes how to extract statement IDs from code in order "
            "to create a mapping between these IDs and their corresponding log "
            "statements"
        ),
    ]:
        return f"""The messages of log statements in this project contain a key-value pair where the key name is 
          stmt_id. Can you please extract the value associated to each statement ID and associated it to the log 
          statement itself, as well as the file path and line number where the log statement is located? For instance, 
          if the message of the log statement is 
          
          'this is a %s statement, stmt_id=1234567890'
          
          then extracting the statement ID and log statement should lead to 
          
          1234567890,"this is a %s statement, stmt_id=1234567890",path/to/file,34
          
          If the log message is a concatenation of strings, then please use the 
          evaluated string as log statement, i.e. extracting 
          
          'this is a %s' + ' statement, stmt_id=1234567890'
          
          should lead to 
          
          1234567890,"this is a %s statement, stmt_id=1234567890",path/to/file,34
          
          Finally, if the log statement contains non evaluated string, please replace these 
          parts with %s, for instance extracting 
          
          'this is a %s ' + str(my_object) + ' statement, stmt_id=1234567890'
          
          should lead to 
          
          1234567890,"this is a %s %s statement stmt_id=1234567890",path/to/file,34 
          
          Write all the extracted log statements and statement IDs to a CSV file named {stmt_id_filepath} at 
          the root of this project. This CSV file should contain the following headers: 
          statement_id,log_statement,file_path,line_number
          where 
          - statement_id is the stmt_id value of the log statement
          - log_statement is the log statement message itself
          - is the file where the log statement is located
          - line_number is the line number where the log statement is defined
          """

    @staticmethod
    def update_stmt_ids(
        src_path: str, stmt_id_filepath: str = "statementIds.csv"
    ) -> Annotated[
        str,
        Field(
            description="A prompt that describes how to update the statements file associated to "
            "this project."
        ),
    ]:
        return f"""Updating statement IDs consists of injecting statement IDs in log statements where they would be 
        missing as well as updating the details in {stmt_id_filepath} for log statements for which information would have 
        changed, e.g. filepath or line number would have changed. Descriptions on how to inject and extract statement 
        IDs are provided below:
        
        # Injecting Statement IDS
        {BrontoTools.inject_stmt_ids(src_path)}
        
        # Extracting Lost Statements - Updating {stmt_id_filepath}
        {BrontoTools.extract_stmt_ids(stmt_id_filepath)}
        """

    def deploy_statements(
        self,
        csv_file_path: Annotated[
            str,
            Field(
                description="The path to the file containing the mapping between the log statements of the project and "
                "their corresponding statement IDs."
            ),
        ],
        project_id: Annotated[
            str,
            Field(
                description="This project ID, typically the artifact ID for a Maven project, the module name for a "
                "python project, or the Git repository name."
            ),
        ],
        version: Annotated[
            str, Field(description="The current version of this project")
        ],
        repo_url: Annotated[
            str,
            Field(
                description="The Git repository URL. This is the https URL. This can be inferred from the `git remote` "
                "command"
            ),
        ],
    ) -> Annotated[
        Dict,
        Field(
            description="Sends to Bronto the list of log statements in this project with "
            "their corresponding statement IDs and returns whether this was "
            "performed successfully."
        ),
    ]:
        return self.bronto_client.deploy_statements(
            csv_file_path, project_id, version, repo_url
        )
