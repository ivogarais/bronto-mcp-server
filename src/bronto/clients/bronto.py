import json
import csv
from functools import cached_property
from typing import Any, Dict, List, Optional

import httpx

from bronto.logger import module_logger
from bronto.schemas import DatasetKey, LogEvent

logger = module_logger(__name__)


class FailedBrontoRequestException(Exception):
    pass


class BrontoResponseDecodingException(Exception):
    pass


class BrontoResponseException(Exception):
    pass


class BrontoClient:
    def __init__(self, api_key: str, api_endpoint: str):
        self.api_key = api_key
        self.api_endpoint = api_endpoint.rstrip("/")
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "bronto-mcp",
            "x-bronto-api-key": self.api_key,
        }

    @cached_property
    def http_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.api_endpoint,
            headers=self.headers,
            timeout=30.0,
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Any = None,
        json_body: Any = None,
        timeout: float | None = None,
        action: str = "Bronto request",
        failure_message: str = "Cannot retrieve data from Bronto",
    ) -> httpx.Response:
        try:
            request_kwargs = dict(
                method=method,
                url=path,
                params=params,
                json=json_body,
            )
            if timeout is not None:
                request_kwargs["timeout"] = timeout

            response = self.http_client.request(**request_kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            if status_code == 400:
                raise BrontoResponseException(
                    "One of the search parameters is unsuitable. Check the filter syntax as "
                    'well as the names of the keys used in the "where", "_select" and '
                    '"group_by_keys" parameters.'
                ) from e
            if status_code == 403:
                raise BrontoResponseException(
                    "You are not allowed to perform this Bronto search. Please check your "
                    "Bronto API key"
                ) from e
            if status_code == 401:
                raise BrontoResponseException(
                    "You are not authorised to perform this Bronto search. Please check your "
                    "Bronto API key, as well as the Bronto endpoint, to make sure that they "
                    "match"
                ) from e

            logger.error(
                "%s failed, status=%s, reason=%s",
                action,
                status_code,
                e.response.reason_phrase,
            )
            raise FailedBrontoRequestException(
                f'{failure_message}. status={status_code}, reason="{e.response.reason_phrase}"'
            ) from e
        except httpx.RequestError as e:
            logger.exception("Cannot interact with Bronto", exc_info=True)
            raise Exception(
                "Cannot interact with Bronto. Please check endpoint configuration."
            ) from e

    @staticmethod
    def _decode_json_response(
        response: httpx.Response,
        *,
        error_log_message: str,
        decoding_error_message: str,
    ) -> Dict[str, Any]:
        try:
            return response.json()
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(error_log_message, exc_info=True)
            raise BrontoResponseDecodingException(decoding_error_message) from e

    def get_datasets(self):
        response = self._request(
            "GET",
            "/logs",
            action="Dataset retrieval",
            failure_message="Cannot retrieve datasets from Bronto",
        )
        datasets_payload = self._decode_json_response(
            response,
            error_log_message="Cannot decode dataset retrieval response",
            decoding_error_message="Unexpected format for retrieved datasets",
        )
        return datasets_payload.get("logs", [])

    def search(
        self,
        timestamp_start: int,
        timestamp_end: int,
        log_ids: list[str],
        where="",
        _select=None,
        group_by_keys=None,
    ) -> List[LogEvent]:
        if group_by_keys is None:
            group_by_keys = []
        if _select is None:
            _select = ["@raw"]
        query_params: list[tuple[str, Any]] = [("from", log_id) for log_id in log_ids]
        query_params.append(("from_ts", timestamp_start))
        query_params.append(("to_ts", timestamp_end))
        query_params.append(("where", where))
        query_params.extend([("select", selected_field) for selected_field in _select])
        query_params.extend([("groups", group_key) for group_key in group_by_keys])

        response = self._request("GET", "/search", params=query_params, action="Search")
        result = self._decode_json_response(
            response,
            error_log_message="Cannot decode search response",
            decoding_error_message="Unexpected format for retrieved data",
        )

        log_events: List[LogEvent] = []
        for event in result.get("events", []):
            log_event = LogEvent(
                message=event["@raw"],
                attributes={"@status": event["@status"], "@time": event["@time"]},
            )
            log_event.attributes.update(event["attributes"])
            log_event.attributes.update(event["message_kvs"])
            log_events.append(log_event)
        return log_events

    def search_post(
        self,
        timestamp_start: int,
        timestamp_end: int,
        log_ids: list[str],
        where="",
        _select=None,
        group_by_keys=None,
    ):
        if group_by_keys is None:
            group_by_keys = []
        if _select is None:
            _select = ["@raw"]
        params = {
            "from_ts": timestamp_start,
            "to_ts": timestamp_end,
            "where": where,
            "select": _select,
            "from": log_ids,
            "groups": group_by_keys,
            "num_of_slices": 10,
        }
        response = self._request(
            "POST",
            "/search",
            json_body=params,
            action="Search",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode search response",
            decoding_error_message="Unexpected format for retrieved data",
        )

    def get_top_keys(self, log_id) -> Dict[str, List[str]]:
        response = self._request(
            "GET",
            "/top-keys",
            params={"log_id": log_id},
            action="Keys retrieval",
            failure_message="Cannot retrieve top keys from Bronto",
        )
        body = self._decode_json_response(
            response,
            error_log_message="Cannot decode search response",
            decoding_error_message="Unexpected format for retrieved data",
        )

        keys_and_values = {}
        for key in body[log_id]:
            if key in keys_and_values:
                keys_and_values[key].extend(body[log_id][key].get("values", {}).keys())
            else:
                keys_and_values[key] = body[log_id][key].get("values", {}).keys()
        logger.info("keys_and_values=%s", keys_and_values)
        return {key: list(set(keys_and_values[key])) for key in keys_and_values}

    def get_all_datasets_top_keys(self) -> Dict[str, List[str]]:
        response = self._request(
            "GET",
            "/top-keys",
            action="Keys retrieval",
            failure_message="Cannot retrieve top keys from Bronto",
        )
        body = self._decode_json_response(
            response,
            error_log_message="Cannot decode search response",
            decoding_error_message="Unexpected format for retrieved data",
        )

        log_ids_and_keys: Dict[str, List[str]] = {}
        for log_id in body:
            if log_id not in log_ids_and_keys:
                log_ids_and_keys[log_id] = []
            log_ids_and_keys[log_id].extend(body[log_id].keys())
        logger.info("log_ids_and_keys=%s", log_ids_and_keys)
        return log_ids_and_keys

    def get_all_datasets_top_keys_and_values(self) -> Dict[str, Dict[str, List[str]]]:
        response = self._request(
            "GET",
            "/top-keys",
            action="Keys retrieval",
            failure_message="Cannot retrieve top keys from Bronto",
        )
        body = self._decode_json_response(
            response,
            error_log_message="Cannot decode search response",
            decoding_error_message="Unexpected format for retrieved data",
        )

        log_ids_and_keys_and_values: Dict[str, Dict[str, List[str]]] = {}
        for log_id in body:
            if log_id not in log_ids_and_keys_and_values:
                log_ids_and_keys_and_values[log_id] = {}
            log_ids_and_keys_and_values[log_id].update(
                {
                    key: [value for value in body[log_id][key]["values"].keys()]
                    for key in body[log_id]
                }
            )
        logger.info("log_ids_and_keys_and_values=%s", log_ids_and_keys_and_values)
        return log_ids_and_keys_and_values

    @staticmethod
    def get_dataset_key(
        key_name: str, dataset_keys: List[DatasetKey]
    ) -> Optional[DatasetKey]:
        for dataset_key in dataset_keys:
            if dataset_key.name == key_name:
                return dataset_key
        return None

    def get_keys(self, log_id) -> List[DatasetKey]:
        top_keys = self.get_top_keys(log_id)
        result = []
        processed_keys = set()
        for key in top_keys:
            if key in processed_keys:
                dataset = BrontoClient.get_dataset_key(key, result)
                dataset.add_values(top_keys[key])
            else:
                result.append(DatasetKey(name=key, values=top_keys[key]))
                processed_keys.add(key)
        return result

    @staticmethod
    def _read_statement_ids_csv(csv_file_path):
        """
        Read the statement IDs CSV file and return a dictionary.

        Args:
            csv_file_path (str): Path to the CSV file

        Returns:
            dict: Dictionary with statement_id as key and log_statement as value
        """
        statement_ids = {}

        try:
            with open(csv_file_path, "r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    statement_id = row["statement_id"].strip()
                    log_statement = row["log_statement"].strip()
                    file_path = row["file_path"]
                    line_number = row["line_number"]

                    # Remove surrounding quotes if they exist (from CSV parsing)
                    if log_statement.startswith('"') and log_statement.endswith('"'):
                        log_statement = log_statement[1:-1]

                    if statement_id.startswith('"') and statement_id.endswith('"'):
                        statement_id = statement_id[1:-1]

                    if file_path.startswith('"') and file_path.endswith('"'):
                        file_path = file_path[1:-1]

                    if line_number.startswith('"') and line_number.endswith('"'):
                        line_number = line_number[1:-1]
                    try:
                        line_number = int(line_number)
                    except ValueError as _:
                        line_number = -1

                    # Handle escaped quotes within the log statement
                    log_statement = log_statement.replace('""', '"')

                    statement_ids[statement_id] = {
                        "stmt_id": statement_id,
                        "log_statement": log_statement,
                        "file_path": file_path,
                        "line_number": line_number,
                    }

            return statement_ids

        except FileNotFoundError:
            logger.error("Statement IDs CSV file not found: %s", csv_file_path)
            return None
        except Exception:
            logger.exception("Error reading statement IDs CSV: %s", csv_file_path)
            return None

    @staticmethod
    def create_payload(statement_ids_dict, project_id, version, repo_url):
        """
        Create the JSON payload in the required format.
        """
        return {
            "project_id": project_id,
            "version": version,
            "repo_url": repo_url,
            "statements": [
                {
                    "id": stmt_id,
                    "message": stmt.get("log_statement"),
                    "file": stmt.get("file_path"),
                    "line": stmt.get("line_number"),
                }
                for stmt_id, stmt in statement_ids_dict.items()
            ],
        }

    def post_statement_ids(self, payload) -> bool:
        """
        POST the statement IDs to the API endpoint.
        """
        try:
            logger.info("Posting statement IDs to: %s/statements", self.api_endpoint)

            response = self.http_client.post("/statements", json=payload, timeout=30.0)
            status_code = response.status_code
            response_headers = dict(response.headers)
            response_data = response.text

            logger.info("Statement IDs POST status: %s", status_code)
            logger.debug("Statement IDs POST headers: %s", response_headers)

            if status_code == 200 or status_code == 201:
                logger.info("Successfully posted statement IDs to API")
                try:
                    response_json = json.loads(response_data)
                    logger.debug(
                        "Statement IDs POST response: %s",
                        json.dumps(response_json, indent=2),
                    )
                except json.JSONDecodeError:
                    logger.debug("Statement IDs POST response text: %s", response_data)
                return True
            else:
                logger.error("Failed to post statement IDs. status=%s", status_code)
                logger.error("Statement IDs POST response: %s", response_data)
                return False

        except httpx.RequestError as e:
            logger.error("URL error while posting statement IDs: %s", str(e))
            return False
        except Exception:
            logger.exception("Unexpected error while posting statement IDs")
            return False

    def deploy_statements(self, csv_file_path, project_id, version, repo_url) -> Dict:
        stmt_ids = self._read_statement_ids_csv(csv_file_path)
        payload = self.create_payload(stmt_ids, project_id, version, repo_url)
        return {"success": self.post_statement_ids(payload)}
