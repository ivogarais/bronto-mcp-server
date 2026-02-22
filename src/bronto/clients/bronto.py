import csv
import json
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


class BrontoConnectionException(Exception):
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
            logger.exception("%s failed due to network error", action, exc_info=True)
            raise BrontoConnectionException(
                f"{action} failed due to connectivity issue. Please check BRONTO_API_ENDPOINT and network reachability."
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

    def get_datasets(self) -> List[Dict[str, Any]]:
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

    def list_api_keys(self) -> List[Dict[str, Any]]:
        response = self._request(
            "GET",
            "/api-keys",
            action="API key retrieval",
            failure_message="Cannot retrieve API keys from Bronto",
        )
        payload = self._decode_json_response(
            response,
            error_log_message="Cannot decode API key retrieval response",
            decoding_error_message="Unexpected format for retrieved API keys",
        )
        return payload.get("api_keys", [])

    def create_api_key(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/api-keys",
            json_body=payload,
            action="API key creation",
            failure_message="Cannot create API key in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode API key creation response",
            decoding_error_message="Unexpected format for created API key",
        )

    def update_api_key(self, api_key_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "PATCH",
            f"/api-keys/{api_key_id}",
            json_body=payload,
            action="API key update",
            failure_message="Cannot update API key in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode API key update response",
            decoding_error_message="Unexpected format for updated API key",
        )

    def delete_api_key(self, api_key_id: str) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/api-keys/{api_key_id}",
            action="API key deletion",
            failure_message="Cannot delete API key in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode API key deletion response",
                decoding_error_message="Unexpected format for API key deletion response",
            )
        return {"success": True}

    def list_users(self) -> List[Dict[str, Any]]:
        response = self._request(
            "GET",
            "/users",
            action="User retrieval",
            failure_message="Cannot retrieve users from Bronto",
        )
        payload = self._decode_json_response(
            response,
            error_log_message="Cannot decode user retrieval response",
            decoding_error_message="Unexpected format for retrieved users",
        )
        return payload.get("users", [])

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/users",
            json_body=payload,
            action="User creation",
            failure_message="Cannot create user in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode user creation response",
            decoding_error_message="Unexpected format for created user",
        )

    def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/users/{user_id}",
            action="User retrieval by ID",
            failure_message="Cannot retrieve user from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode user retrieval-by-id response",
            decoding_error_message="Unexpected format for retrieved user",
        )

    def update_user(self, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "PATCH",
            f"/users/{user_id}",
            json_body=payload,
            action="User update",
            failure_message="Cannot update user in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode user update response",
            decoding_error_message="Unexpected format for updated user",
        )

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/users/{user_id}",
            action="User deletion",
            failure_message="Cannot delete user in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode user deletion response",
                decoding_error_message="Unexpected format for user deletion response",
            )
        return {"success": True}

    def deactivate_user(self, user_id: str) -> Dict[str, Any]:
        response = self._request(
            "POST",
            f"/users/{user_id}/deactivate",
            action="User deactivation",
            failure_message="Cannot deactivate user in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode user deactivation response",
                decoding_error_message="Unexpected format for user deactivation response",
            )
        return {"success": True}

    def reactivate_user(self, user_id: str) -> Dict[str, Any]:
        response = self._request(
            "POST",
            f"/users/{user_id}/reactivate",
            action="User reactivation",
            failure_message="Cannot reactivate user in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode user reactivation response",
                decoding_error_message="Unexpected format for user reactivation response",
            )
        return {"success": True}

    def resend_user_invitation(self, user_id: str) -> Dict[str, Any]:
        response = self._request(
            "POST",
            f"/users/{user_id}/resend-invitation",
            action="User invitation resend",
            failure_message="Cannot resend invitation in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode user invitation resend response",
                decoding_error_message="Unexpected format for user invitation resend response",
            )
        return {"success": True}

    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/users/{user_id}/preferences",
            action="User preferences retrieval",
            failure_message="Cannot retrieve user preferences from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode user preferences response",
            decoding_error_message="Unexpected format for user preferences",
        )

    def update_user_preferences(
        self, user_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = self._request(
            "PATCH",
            f"/users/{user_id}/preferences",
            json_body=payload,
            action="User preferences update",
            failure_message="Cannot update user preferences in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode user preferences update response",
            decoding_error_message="Unexpected format for updated user preferences",
        )

    def get_user_organizations(self, user_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/users/{user_id}/organizations",
            action="User organizations retrieval",
            failure_message="Cannot retrieve user organizations from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode user organizations response",
            decoding_error_message="Unexpected format for user organizations",
        )

    def list_groups(self) -> List[Dict[str, Any]]:
        response = self._request(
            "GET",
            "/groups",
            action="Group retrieval",
            failure_message="Cannot retrieve groups from Bronto",
        )
        payload = self._decode_json_response(
            response,
            error_log_message="Cannot decode groups retrieval response",
            decoding_error_message="Unexpected format for retrieved groups",
        )
        return payload.get("groups", payload if isinstance(payload, list) else [])

    def create_group(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/groups",
            json_body=payload,
            action="Group creation",
            failure_message="Cannot create group in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode group creation response",
            decoding_error_message="Unexpected format for created group",
        )

    def get_group(self, group_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/groups/{group_id}",
            action="Group retrieval by ID",
            failure_message="Cannot retrieve group from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode group retrieval response",
            decoding_error_message="Unexpected format for retrieved group",
        )

    def delete_group(self, group_id: str) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/groups/{group_id}",
            action="Group deletion",
            failure_message="Cannot delete group in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode group deletion response",
                decoding_error_message="Unexpected format for group deletion response",
            )
        return {"success": True}

    def update_group(self, group_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "PATCH",
            f"/groups/{group_id}",
            json_body=payload,
            action="Group update",
            failure_message="Cannot update group in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode group update response",
            decoding_error_message="Unexpected format for updated group",
        )

    def list_group_members(self, group_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/groups/{group_id}/members",
            action="Group members retrieval",
            failure_message="Cannot retrieve group members from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode group members response",
            decoding_error_message="Unexpected format for group members",
        )

    def add_group_members(self, group_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            f"/groups/{group_id}/members",
            json_body=payload,
            action="Group member add",
            failure_message="Cannot add group members in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode group add-members response",
            decoding_error_message="Unexpected format for group add-members response",
        )

    def remove_group_members(
        self, group_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/groups/{group_id}/members",
            json_body=payload,
            action="Group member removal",
            failure_message="Cannot remove group members in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode group remove-members response",
                decoding_error_message="Unexpected format for group remove-members response",
            )
        return {"success": True}

    def list_member_groups(self, member_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/groups/members/{member_id}",
            action="Member groups retrieval",
            failure_message="Cannot retrieve member groups from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode member groups response",
            decoding_error_message="Unexpected format for member groups",
        )

    def list_monitors_by_log(self, log_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            "/monitors",
            params={"log_id": log_id},
            action="Monitor retrieval by log",
            failure_message="Cannot retrieve monitors from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode monitors response",
            decoding_error_message="Unexpected format for monitors",
        )

    def list_dashboards_by_log(self, log_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            "/dashboards",
            params={"log_id": log_id},
            action="Dashboard retrieval by log",
            failure_message="Cannot retrieve dashboards from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode dashboards response",
            decoding_error_message="Unexpected format for dashboards",
        )

    def grant_access(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/access",
            json_body=payload,
            action="Access grant",
            failure_message="Cannot grant access in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode access grant response",
            decoding_error_message="Unexpected format for access grant response",
        )

    def revoke_access(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            "/access",
            json_body=payload,
            action="Access revoke",
            failure_message="Cannot revoke access in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode access revoke response",
                decoding_error_message="Unexpected format for access revoke response",
            )
        return {"success": True}

    def list_access_members(self) -> Dict[str, Any]:
        response = self._request(
            "GET",
            "/access",
            action="Access members retrieval",
            failure_message="Cannot retrieve access members from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode access members response",
            decoding_error_message="Unexpected format for access members response",
        )

    def check_access(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "GET",
            "/access/check",
            params=payload,
            action="Access check",
            failure_message="Cannot check access in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode access check response",
            decoding_error_message="Unexpected format for access check response",
        )

    def switch_active_organization(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/access/switch",
            json_body=payload,
            action="Organization switch",
            failure_message="Cannot switch organization in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode organization switch response",
            decoding_error_message="Unexpected format for organization switch response",
        )

    def get_context(
        self,
        *,
        from_: str | None = None,
        from_tags: str | None = None,
        from_expr: str | None = None,
        sequence: int | None = None,
        timestamp: int | None = None,
        direction: str | None = None,
        limit: int | None = None,
        include_explain: bool | None = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if from_ is not None:
            params["from"] = from_
        if from_tags is not None:
            params["from_tags"] = from_tags
        if from_expr is not None:
            params["from_expr"] = from_expr
        if sequence is not None:
            params["sequence"] = sequence
        if timestamp is not None:
            params["timestamp"] = timestamp
        if direction is not None:
            params["direction"] = direction
        if limit is not None:
            params["limit"] = limit
        if include_explain is not None:
            params["explain"] = include_explain

        response = self._request(
            "GET",
            "/context",
            params=params,
            action="Context retrieval",
            failure_message="Cannot retrieve context from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode context retrieval response",
            decoding_error_message="Unexpected format for retrieved context",
        )

    def list_exports(self) -> List[Dict[str, Any]]:
        response = self._request(
            "GET",
            "/exports",
            action="Export retrieval",
            failure_message="Cannot retrieve exports from Bronto",
        )
        payload = self._decode_json_response(
            response,
            error_log_message="Cannot decode export retrieval response",
            decoding_error_message="Unexpected format for retrieved exports",
        )
        return payload.get("exports", [])

    def create_export(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/exports",
            json_body=payload,
            action="Export creation",
            failure_message="Cannot create export in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode export creation response",
            decoding_error_message="Unexpected format for created export",
        )

    def get_export(self, export_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/exports/{export_id}",
            action="Export retrieval by ID",
            failure_message="Cannot retrieve export from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode export retrieval-by-id response",
            decoding_error_message="Unexpected format for retrieved export",
        )

    def delete_export(self, export_id: str) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/exports/{export_id}",
            action="Export deletion",
            failure_message="Cannot delete export in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode export deletion response",
                decoding_error_message="Unexpected format for export deletion response",
            )
        return {"success": True}

    def get_usage_for_log_id(
        self,
        *,
        time_range: str | None = None,
        from_ts: int | None = None,
        to_ts: int | None = None,
        usage_type: str | None = None,
        limit: int | None = None,
        num_of_slices: int | None = None,
        metric: str | None = None,
        delta: bool | None = None,
        delta_time_range: str | None = None,
        delta_from_ts: int | None = None,
        delta_to_ts: int | None = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if time_range is not None:
            params["time_range"] = time_range
        if from_ts is not None:
            params["from_ts"] = from_ts
        if to_ts is not None:
            params["to_ts"] = to_ts
        if usage_type is not None:
            params["usage_type"] = usage_type
        if limit is not None:
            params["limit"] = limit
        if num_of_slices is not None:
            params["num_of_slices"] = num_of_slices
        if metric is not None:
            params["metric"] = metric
        if delta is not None:
            params["delta"] = delta
        if delta_time_range is not None:
            params["delta_time_range"] = delta_time_range
        if delta_from_ts is not None:
            params["delta_from_ts"] = delta_from_ts
        if delta_to_ts is not None:
            params["delta_to_ts"] = delta_to_ts

        response = self._request(
            "GET",
            "/usage/organizations/logs",
            params=params,
            action="Usage retrieval by log ID",
            failure_message="Cannot retrieve usage from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode usage-by-log-id response",
            decoding_error_message="Unexpected format for retrieved usage",
        )

    def get_usage_for_user_per_log_id(
        self,
        *,
        time_range: str | None = None,
        from_ts: int | None = None,
        to_ts: int | None = None,
        usage_type: str | None = None,
        limit: int | None = None,
        num_of_slices: int | None = None,
        metric: str | None = None,
        delta: bool | None = None,
        delta_time_range: str | None = None,
        delta_from_ts: int | None = None,
        delta_to_ts: int | None = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if time_range is not None:
            params["time_range"] = time_range
        if from_ts is not None:
            params["from_ts"] = from_ts
        if to_ts is not None:
            params["to_ts"] = to_ts
        if usage_type is not None:
            params["usage_type"] = usage_type
        if limit is not None:
            params["limit"] = limit
        if num_of_slices is not None:
            params["num_of_slices"] = num_of_slices
        if metric is not None:
            params["metric"] = metric
        if delta is not None:
            params["delta"] = delta
        if delta_time_range is not None:
            params["delta_time_range"] = delta_time_range
        if delta_from_ts is not None:
            params["delta_from_ts"] = delta_from_ts
        if delta_to_ts is not None:
            params["delta_to_ts"] = delta_to_ts

        response = self._request(
            "GET",
            "/usage/users",
            params=params,
            action="Usage retrieval by user per log ID",
            failure_message="Cannot retrieve usage from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode usage-by-user-per-log-id response",
            decoding_error_message="Unexpected format for retrieved usage",
        )

    def list_forward_configs(self) -> List[Dict[str, Any]]:
        response = self._request(
            "GET",
            "/forward-configs",
            action="Forward config retrieval",
            failure_message="Cannot retrieve forward configs from Bronto",
        )
        payload = self._decode_json_response(
            response,
            error_log_message="Cannot decode forward config retrieval response",
            decoding_error_message="Unexpected format for retrieved forward configs",
        )
        return payload.get("forward_configs", [])

    def update_tag(self, tag_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "PUT",
            f"/tags/{tag_name}",
            json_body=payload,
            action="Tag update",
            failure_message="Cannot update tag in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode tag update response",
            decoding_error_message="Unexpected format for tag update response",
        )

    def create_tag(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/tags",
            json_body=payload,
            action="Tag creation",
            failure_message="Cannot create tag in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode tag creation response",
            decoding_error_message="Unexpected format for tag creation response",
        )

    def delete_tag(self, tag_name: str) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/tags/{tag_name}",
            action="Tag deletion",
            failure_message="Cannot delete tag in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode tag deletion response",
                decoding_error_message="Unexpected format for tag deletion response",
            )
        return {"success": True}

    def list_tags(self) -> Dict[str, Any]:
        response = self._request(
            "GET",
            "/tags",
            action="Tag listing",
            failure_message="Cannot list tags from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode tag list response",
            decoding_error_message="Unexpected format for tag list response",
        )

    def get_parsers_usage_for_log_id(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "GET",
            "/parsers/usage/logs",
            params=payload,
            action="Parser usage retrieval by log",
            failure_message="Cannot retrieve parser usage from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode parser usage response",
            decoding_error_message="Unexpected format for parser usage response",
        )

    def get_parsers_usage_for_user_per_log_id(
        self, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = self._request(
            "GET",
            "/parsers/usage/users",
            params=payload,
            action="Parser usage retrieval by user and log",
            failure_message="Cannot retrieve parser usage from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode parser usage by user response",
            decoding_error_message="Unexpected format for parser usage by user response",
        )

    def list_policies_by_resource(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "GET",
            "/policies",
            params=payload,
            action="Policy retrieval by resource",
            failure_message="Cannot retrieve policies from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode policies response",
            decoding_error_message="Unexpected format for policies response",
        )

    def list_encryption_keys(self) -> List[Dict[str, Any]]:
        response = self._request(
            "GET",
            "/encryption-keys",
            action="Encryption key retrieval",
            failure_message="Cannot retrieve encryption keys from Bronto",
        )
        payload = self._decode_json_response(
            response,
            error_log_message="Cannot decode encryption key retrieval response",
            decoding_error_message="Unexpected format for encryption keys",
        )
        return payload.get(
            "encryption_keys", payload if isinstance(payload, list) else []
        )

    def create_encryption_key(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/encryption-keys",
            json_body=payload,
            action="Encryption key creation",
            failure_message="Cannot create encryption key in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode encryption key creation response",
            decoding_error_message="Unexpected format for created encryption key",
        )

    def get_encryption_key(self, encryption_key_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/encryption-keys/{encryption_key_id}",
            action="Encryption key retrieval by ID",
            failure_message="Cannot retrieve encryption key from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode encryption key retrieval-by-id response",
            decoding_error_message="Unexpected format for retrieved encryption key",
        )

    def delete_encryption_key(self, encryption_key_id: str) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/encryption-keys/{encryption_key_id}",
            action="Encryption key deletion",
            failure_message="Cannot delete encryption key in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode encryption key deletion response",
                decoding_error_message="Unexpected format for encryption key deletion response",
            )
        return {"success": True}

    def update_encryption_key(
        self, encryption_key_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = self._request(
            "PATCH",
            f"/encryption-keys/{encryption_key_id}",
            json_body=payload,
            action="Encryption key update",
            failure_message="Cannot update encryption key in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode encryption key update response",
            decoding_error_message="Unexpected format for updated encryption key",
        )

    def create_forward_config(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/forward-configs",
            json_body=payload,
            action="Forward config creation",
            failure_message="Cannot create forward config in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode forward config creation response",
            decoding_error_message="Unexpected format for created forward config",
        )

    def update_forward_config(
        self, forward_config_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        response = self._request(
            "PUT",
            f"/forward-configs/{forward_config_id}",
            json_body=payload,
            action="Forward config update",
            failure_message="Cannot update forward config in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode forward config update response",
            decoding_error_message="Unexpected format for updated forward config",
        )

    def delete_forward_config(self, forward_config_id: str) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/forward-configs/{forward_config_id}",
            action="Forward config deletion",
            failure_message="Cannot delete forward config in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode forward config deletion response",
                decoding_error_message="Unexpected format for forward config deletion response",
            )
        return {"success": True}

    def test_forward_destination(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/forward-configs/test",
            json_body=payload,
            action="Forward destination test",
            failure_message="Cannot test forward destination in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode forward destination test response",
            decoding_error_message="Unexpected format for forward destination test",
        )

    def create_log(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._request(
            "POST",
            "/logs",
            json_body=payload,
            action="Log creation",
            failure_message="Cannot create log in Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode log creation response",
            decoding_error_message="Unexpected format for created log",
        )

    def get_search_status(self, status_id: str) -> Dict[str, Any]:
        response = self._request(
            "GET",
            f"/search/status/{status_id}",
            action="Search status retrieval",
            failure_message="Cannot retrieve search status from Bronto",
        )
        return self._decode_json_response(
            response,
            error_log_message="Cannot decode search status response",
            decoding_error_message="Unexpected format for search status",
        )

    def cancel_search(self, status_id: str) -> Dict[str, Any]:
        response = self._request(
            "DELETE",
            f"/search/status/{status_id}",
            action="Search cancellation",
            failure_message="Cannot cancel search in Bronto",
        )
        if response.content:
            return self._decode_json_response(
                response,
                error_log_message="Cannot decode search cancel response",
                decoding_error_message="Unexpected format for search cancel response",
            )
        return {"success": True}

    def search(
        self,
        timestamp_start: int,
        timestamp_end: int,
        log_ids: list[str],
        where: str = "",
        limit: int | None = None,
        _select: Optional[List[str]] = None,
        group_by_keys: Optional[List[str]] = None,
    ) -> List[LogEvent]:
        if group_by_keys is None:
            group_by_keys = []
        if _select is None:
            _select = ["@raw"]
        query_params: list[tuple[str, Any]] = [("from", log_id) for log_id in log_ids]
        query_params.append(("from_ts", timestamp_start))
        query_params.append(("to_ts", timestamp_end))
        query_params.append(("where", where))
        if limit is not None:
            query_params.append(("limit", limit))
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
        where: str = "",
        _select: Optional[List[str]] = None,
        group_by_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
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

    def get_top_keys(self, log_id: str) -> Dict[str, List[str]]:
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

        dataset_payload = body.get(log_id, {})
        if not isinstance(dataset_payload, dict):
            raise BrontoResponseDecodingException(
                "Unexpected format for retrieved top keys"
            )

        keys_and_values: Dict[str, List[str]] = {}
        for key, key_payload in dataset_payload.items():
            values = key_payload.get("values", {})
            if not isinstance(values, dict):
                continue
            keys_and_values[key] = list(values.keys())
        logger.info("keys_and_values=%s", keys_and_values)
        return keys_and_values

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
        for log_id, dataset_payload in body.items():
            if not isinstance(dataset_payload, dict):
                log_ids_and_keys[log_id] = []
                continue
            log_ids_and_keys[log_id] = list(dataset_payload.keys())
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
        for log_id, dataset_payload in body.items():
            if not isinstance(dataset_payload, dict):
                log_ids_and_keys_and_values[log_id] = {}
                continue

            log_ids_and_keys_and_values[log_id] = {}
            for key, key_payload in dataset_payload.items():
                values = key_payload.get("values", {})
                if not isinstance(values, dict):
                    log_ids_and_keys_and_values[log_id][key] = []
                    continue
                log_ids_and_keys_and_values[log_id][key] = list(values.keys())
        logger.info("log_ids_and_keys_and_values=%s", log_ids_and_keys_and_values)
        return log_ids_and_keys_and_values

    def get_keys(self, log_id: str) -> List[DatasetKey]:
        top_keys = self.get_top_keys(log_id)
        return [DatasetKey(name=key, values=values) for key, values in top_keys.items()]

    @staticmethod
    def _read_statement_ids_csv(
        csv_file_path: str,
    ) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Read the statement IDs CSV file and return a dictionary.

        Args:
            csv_file_path (str): Path to the CSV file

        Returns:
            dict: Dictionary with statement_id as key and log_statement as value
        """
        statement_ids: Dict[str, Dict[str, Any]] = {}

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
        except (KeyError, csv.Error, OSError):
            logger.exception("Error reading statement IDs CSV: %s", csv_file_path)
            return None

    @staticmethod
    def create_payload(
        statement_ids_dict: Dict[str, Dict[str, Any]],
        project_id: str,
        version: str,
        repo_url: str,
    ) -> Dict[str, Any]:
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

    def post_statement_ids(self, payload: Dict[str, Any]) -> bool:
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

    def deploy_statements(
        self,
        csv_file_path: str,
        project_id: str,
        version: str,
        repo_url: str,
    ) -> Dict[str, bool]:
        stmt_ids = self._read_statement_ids_csv(csv_file_path)
        if stmt_ids is None:
            return {"success": False}
        payload = self.create_payload(stmt_ids, project_id, version, repo_url)
        return {"success": self.post_statement_ids(payload)}
