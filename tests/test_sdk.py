"""Exercise the installed official SDK with an in-memory HTTP transport only."""

import json

import httpx2
import pytest
import typesafe_sdk

from gsd_demo.core import build_request, get_case
from gsd_demo.runner import mock_response, run_live, save_record


def install_transport(monkeypatch, handler):
    actual_client = typesafe_sdk.TypeSafeClient
    monkeypatch.setenv("TYPESAFE_API_KEY", "synthetic-test-key")
    monkeypatch.setattr(typesafe_sdk, "TypeSafeClient", lambda **kwargs: actual_client(transport=httpx2.MockTransport(handler), **kwargs))


def test_actual_sdk_serialization_and_response_preservation(monkeypatch):
    case = get_case("pilot-02")
    request = build_request(case["vignette"])
    raw = mock_response(case["expected"]["choice"])
    raw["provider_extra_field"] = {"preserved": True}
    sent = []
    def handler(wire):
        assert str(wire.url) == "https://api.typesafe.ai/v1/systemone"
        assert wire.method == "POST"
        sent.append(json.loads(wire.content))
        return httpx2.Response(200, json=raw, headers={"x-typesafe-request-id": "synthetic-success-id"})
    install_transport(monkeypatch, handler)
    record = run_live(request, case["id"], case["expected"])
    assert sent == [request]
    assert record["execution_status"] == "completed"
    assert record["raw_response"] == raw
    assert record["request_id"] == "synthetic-success-id"
    assert json.loads(record["original_response_text"]) == raw
    assert record["returned_model"] == request["model"]
    assert record["elapsed_seconds"] >= 0
    assert "synthetic-test-key" not in json.dumps(record)


def test_missing_key_never_calls_sdk(monkeypatch):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    def forbidden(**kwargs):
        pytest.fail("Missing key must not create an SDK client")
    monkeypatch.setattr(typesafe_sdk, "TypeSafeClient", forbidden)
    record = run_live(build_request("Synthetic example."))
    assert record["execution_status"] == "not_run_missing_key"
    assert record["elapsed_seconds"] is None
    assert record["result"] is None


def test_api_error_is_preserved_and_not_retried_or_replaced(monkeypatch, tmp_path):
    calls = []
    error_body = {"error": {"message": "Synthetic service unavailable"}}
    def handler(wire):
        calls.append(wire)
        return httpx2.Response(503, json=error_body, headers={"x-typesafe-request-id": "synthetic-request-id"})
    install_transport(monkeypatch, handler)
    record = run_live(build_request("Synthetic example."))
    assert len(calls) == 1
    assert record["execution_status"] == "api_error"
    assert record["raw_response"] == error_body
    assert record["error"]["http_status"] == 503
    assert record["error"]["request_id"] == "synthetic-request-id"
    assert record["request_id"] == "synthetic-request-id"
    assert record["result"] is None
    save_record(record, tmp_path)


def test_sdk_validation_error_keeps_original_response(monkeypatch):
    raw = {"model": "jev-1.13.0", "answers": {"invalid": 42}}
    install_transport(monkeypatch, lambda wire: httpx2.Response(200, json=raw))
    record = run_live(build_request("Synthetic example."))
    assert record["execution_status"] == "response_error"
    assert record["raw_response"] == raw
    assert record["returned_model"] == "jev-1.13.0"
    assert record["result"] is None


def test_network_failure_is_distinct_from_insufficient_evidence(monkeypatch):
    def handler(wire):
        raise httpx2.ConnectError("Synthetic connection failure", request=wire)
    install_transport(monkeypatch, handler)
    record = run_live(build_request("Synthetic example."))
    assert record["execution_status"] == "api_error"
    assert record["result"] is None
    assert record["raw_response"] is None
