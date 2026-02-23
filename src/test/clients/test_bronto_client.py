from unittest.mock import Mock

import httpx
import pytest

from bronto.clients import (
    BrontoClient,
    BrontoConnectionException,
    BrontoResponseDecodingException,
    BrontoResponseException,
    FailedBrontoRequestException,
)


def _response(status_code: int, *, json_body=None, text=None) -> httpx.Response:
    request = httpx.Request("GET", "https://api.eu.bronto.io/test")
    if json_body is not None:
        return httpx.Response(status_code, request=request, json=json_body)
    if text is not None:
        return httpx.Response(status_code, request=request, text=text)
    return httpx.Response(status_code, request=request)


@pytest.fixture
def client() -> BrontoClient:
    return BrontoClient("api-key", "https://api.eu.bronto.io")


def test_request_success(client):
    mock_http = Mock()
    mock_http.request.return_value = _response(200, json_body={"ok": True})
    client.__dict__["http_client"] = mock_http

    response = client._request("GET", "/search")

    assert response.status_code == 200
    mock_http.request.assert_called_once()


@pytest.mark.parametrize(
    ("status_code", "expected_exception", "message_part"),
    [
        (400, BrontoResponseException, "unsuitable"),
        (401, BrontoResponseException, "not authorised"),
        (403, BrontoResponseException, "not allowed"),
        (500, FailedBrontoRequestException, "Cannot retrieve data from Bronto"),
    ],
)
def test_request_http_error_mapping(
    client, status_code, expected_exception, message_part
):
    mock_http = Mock()
    mock_http.request.return_value = _response(status_code)
    client.__dict__["http_client"] = mock_http

    with pytest.raises(expected_exception, match=message_part):
        client._request("GET", "/search")


def test_request_network_error(client):
    mock_http = Mock()
    request = httpx.Request("GET", "https://api.eu.bronto.io/search")
    mock_http.request.side_effect = httpx.RequestError("boom", request=request)
    client.__dict__["http_client"] = mock_http

    with pytest.raises(BrontoConnectionException, match="connectivity issue"):
        client._request("GET", "/search")


def test_decode_json_response_invalid_json_raises():
    response = httpx.Response(
        200,
        request=httpx.Request("GET", "https://api.eu.bronto.io/test"),
        content=b"not-json",
    )
    with pytest.raises(BrontoResponseDecodingException):
        BrontoClient._decode_json_response(
            response,
            error_log_message="decode failed",
            decoding_error_message="Unexpected format",
        )


def test_get_datasets_returns_logs_payload(client, monkeypatch):
    response = _response(200, json_body={"logs": [{"log": "svc", "log_id": "id"}]})
    request_mock = Mock(return_value=response)
    monkeypatch.setattr(client, "_request", request_mock)

    datasets = client.get_datasets()

    assert datasets == [{"log": "svc", "log_id": "id"}]
    request_mock.assert_called_once()


def test_search_transforms_events(client, monkeypatch):
    payload = {
        "events": [
            {
                "@raw": "hello",
                "@status": "info",
                "@time": "2025-01-01T00:00:00Z",
                "attributes": {"service": "api"},
                "message_kvs": {"stmt_id": "abc"},
            }
        ]
    }
    response = _response(200, json_body=payload)
    request_mock = Mock(return_value=response)
    monkeypatch.setattr(client, "_request", request_mock)

    events = client.search(1, 2, ["id1"])

    assert len(events) == 1
    assert events[0].message == "hello"
    assert events[0].attributes["service"] == "api"
    assert events[0].attributes["stmt_id"] == "abc"
    params = request_mock.call_args.kwargs["params"]
    assert ("from", "id1") in params
    assert ("from_ts", 1) in params
    assert ("to_ts", 2) in params


def test_search_post_builds_expected_payload(client, monkeypatch):
    response = _response(200, json_body={"totals": {"count": 1, "timeseries": []}})
    request_mock = Mock(return_value=response)
    monkeypatch.setattr(client, "_request", request_mock)

    result = client.search_post(10, 20, ["id1"], where="x", _select=["COUNT(*)"])

    assert "totals" in result
    assert request_mock.call_args.args == ("POST", "/search")
    body = request_mock.call_args.kwargs["json_body"]
    assert body["from_ts"] == 10
    assert body["to_ts"] == 20
    assert body["from"] == ["id1"]
    assert body["select"] == ["COUNT(*)"]


def test_get_top_keys_returns_values(client, monkeypatch):
    body = {
        "id1": {
            "service": {"values": {"api": 10, "worker": 5}},
            "level": {"values": {"info": 20}},
        }
    }
    monkeypatch.setattr(
        client, "_request", Mock(return_value=_response(200, json_body=body))
    )

    values = client.get_top_keys("id1")

    assert set(values["service"]) == {"api", "worker"}
    assert values["level"] == ["info"]


def test_get_top_keys_handles_missing_log_id_payload(client, monkeypatch):
    body = {"other-log-id": {"service": {"values": {"api": 10}}}}
    monkeypatch.setattr(
        client, "_request", Mock(return_value=_response(200, json_body=body))
    )

    values = client.get_top_keys("id1")

    assert values == {}


def test_get_all_datasets_top_keys(client, monkeypatch):
    body = {
        "id1": {"service": {"values": {"api": 1}}, "level": {"values": {"info": 1}}},
        "id2": {"event.type": {"values": {"x": 1}}},
    }
    monkeypatch.setattr(
        client, "_request", Mock(return_value=_response(200, json_body=body))
    )

    keys = client.get_all_datasets_top_keys()

    assert set(keys["id1"]) == {"service", "level"}
    assert keys["id2"] == ["event.type"]


def test_get_all_datasets_top_keys_and_values(client, monkeypatch):
    body = {
        "id1": {
            "service": {"values": {"api": 1}},
            "level": {"values": {"info": 1, "error": 1}},
        }
    }
    monkeypatch.setattr(
        client, "_request", Mock(return_value=_response(200, json_body=body))
    )

    values = client.get_all_datasets_top_keys_and_values()

    assert values["id1"]["service"] == ["api"]
    assert set(values["id1"]["level"]) == {"info", "error"}


def test_get_keys_uses_top_keys(client, monkeypatch):
    monkeypatch.setattr(client, "get_top_keys", Mock(return_value={"service": ["api"]}))

    keys = client.get_keys("id1")

    assert len(keys) == 1
    assert keys[0].name == "service"
    assert keys[0].values == ["api"]


def test_read_statement_ids_csv(tmp_path):
    csv_file = tmp_path / "statementIds.csv"
    csv_file.write_text(
        "statement_id,log_statement,file_path,line_number\n"
        'abcd1234,"hello stmt_id=abcd1234",src/file.py,12\n',
        encoding="utf-8",
    )

    data = BrontoClient._read_statement_ids_csv(str(csv_file))

    assert data is not None
    assert data["abcd1234"]["stmt_id"] == "abcd1234"
    assert data["abcd1234"]["line_number"] == 12


def test_read_statement_ids_csv_missing_file_returns_none():
    assert BrontoClient._read_statement_ids_csv("/does/not/exist.csv") is None


def test_create_payload():
    payload = BrontoClient.create_payload(
        {
            "a": {
                "log_statement": "msg",
                "file_path": "src/f.py",
                "line_number": 4,
            }
        },
        project_id="proj",
        version="1.0.0",
        repo_url="https://example.com/repo.git",
    )

    assert payload["project_id"] == "proj"
    assert payload["version"] == "1.0.0"
    assert payload["statements"][0]["id"] == "a"


def test_post_statement_ids_success(client):
    mock_http = Mock()
    mock_http.post.return_value = _response(201, json_body={"ok": True})
    client.__dict__["http_client"] = mock_http

    assert client.post_statement_ids({"project_id": "p"}) is True


def test_post_statement_ids_failure_status(client):
    mock_http = Mock()
    mock_http.post.return_value = _response(500, text="error")
    client.__dict__["http_client"] = mock_http

    assert client.post_statement_ids({"project_id": "p"}) is False


def test_post_statement_ids_request_error(client):
    request = httpx.Request("POST", "https://api.eu.bronto.io/statements")
    mock_http = Mock()
    mock_http.post.side_effect = httpx.RequestError("fail", request=request)
    client.__dict__["http_client"] = mock_http

    assert client.post_statement_ids({"project_id": "p"}) is False


def test_deploy_statements_returns_false_when_csv_cannot_be_read(client, monkeypatch):
    monkeypatch.setattr(client, "_read_statement_ids_csv", Mock(return_value=None))

    result = client.deploy_statements("missing.csv", "p", "1.0.0", "https://repo")

    assert result == {"success": False}


def test_deploy_statements_success(client, monkeypatch):
    monkeypatch.setattr(
        client,
        "_read_statement_ids_csv",
        Mock(
            return_value={
                "a": {"log_statement": "m", "file_path": "f", "line_number": 1}
            }
        ),
    )
    monkeypatch.setattr(client, "post_statement_ids", Mock(return_value=True))

    result = client.deploy_statements("x.csv", "p", "1.0.0", "https://repo")

    assert result == {"success": True}
