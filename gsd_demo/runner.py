"""SDK transport and append-only execution records."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from time import perf_counter
from typing import Any
import json
import math
import os
import platform
import uuid

from .core import (
    ContractError, MODEL, build_request, evaluate_against_labels, fingerprint, get_case, option_labels,
    interpret_response, load_data, policy_snapshot, question_bank, validate_request,
)

ORIGINS = ("live_api", "playground_import_unverified", "mock_offline")


def execute_api(request: dict) -> tuple[dict, str | None, str]:
    """One SDK invocation evaluates the diagnosis question; the key is never part of the request body."""
    from typesafe_sdk import RetryPolicy, TypeSafeClient

    with TypeSafeClient(
        api_key=os.environ["TYPESAFE_API_KEY"],
        base_url="https://api.typesafe.ai",
        model=request["model"],
        timeout=30.0,
        retry=RetryPolicy(max_retries=0),
    ) as client:
        response = client.system_one(state=request["state"], questions=request["questions"])
        return response.raw_http_response.json(), response.request_id, response.raw_http_response.text


def new_record(request: dict, origin: str, case_id: str | None = None) -> dict:
    validate_request(request)
    if origin not in ORIGINS:
        raise ValueError("Unknown execution origin.")
    cards = load_data("disorders.json")
    return {
        "record_version": "0.2.0",
        "software": {"demo": version("gsd-jev-demo"), "python": platform.python_version(), "typesafe_sdk": version("typesafe-sdk")},
        "record_id": str(uuid.uuid4()),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_origin": origin,
        "execution_status": "not_started",
        "case_id": case_id,
        "request": deepcopy(request),
        "request_sha256": fingerprint(request),
        "question_version": question_bank()["version"],
        "questions_sha256": fingerprint(request["questions"]),
        "content_version": cards["version"],
        "content_sha256": fingerprint(cards),
        "disorder_catalog": cards,
        "policy": policy_snapshot(),
        "policy_sha256": fingerprint(policy_snapshot()),
        "raw_response": None,
        "returned_model": None,
        "request_id": None,
        "original_response_text": None,
        "elapsed_seconds": None,
        "timing_source": None,
        "result": None,
        "error": None,
    }


def attach_response(record: dict, raw: Any, expected: dict | None = None) -> dict:
    """Keep malformed or mismatched responses for inspection without selecting a diagnosis."""
    record["raw_response"] = raw
    if isinstance(raw, dict) and not record.get("request_id"):
        record["request_id"] = raw.get("request_id")
    record["returned_model"] = raw.get("model") if isinstance(raw, dict) else None
    try:
        if record["returned_model"] != record["request"]["model"]:
            raise ContractError("Returned model does not match the pinned request model.")
        record["result"] = interpret_response(raw)
        record["execution_status"] = "completed"
        if expected is not None:
            record["evaluation"] = evaluate_against_labels(record["result"], expected)
    except ContractError as error:
        record["execution_status"] = "response_error"
        record["error"] = {"kind": "response_contract", "message": str(error)}
    return record


def run_live(request: dict, case_id: str | None = None, expected: dict | None = None) -> dict:
    record = new_record(request, "live_api", case_id)
    if not os.environ.get("TYPESAFE_API_KEY", "").strip():
        record["execution_status"] = "not_run_missing_key"
        record["error"] = {"kind": "configuration", "message": "Set TYPESAFE_API_KEY before a live run."}
        return record
    from typesafe_sdk import TypeSafeAPIError, TypeSafeAPIResponseValidationError

    start = perf_counter()
    record["timing_source"] = "client_wall_clock"
    try:
        raw, request_id, response_text = execute_api(request)
        record["request_id"] = request_id
        record["original_response_text"] = response_text
    except TypeSafeAPIError as error:
        record["request_id"] = error.request_id
        record["raw_response"] = error.body
        record["returned_model"] = error.body.get("model") if isinstance(error.body, dict) else None
        record["execution_status"] = (
            "response_error" if isinstance(error, TypeSafeAPIResponseValidationError) else "api_error"
        )
        record["error"] = {
            "kind": type(error).__name__,
            "message": "The SDK rejected the response. The original body is preserved.",
            "http_status": error.status,
            "request_id": error.request_id,
            "field_path": getattr(error, "field_path", None),
        }
    except Exception as error:
        # Do not serialize exception text: provider errors can contain request data.
        record["execution_status"] = "api_error"
        record["error"] = {
            "kind": type(error).__name__,
            "message": "The API call failed. No model result was substituted.",
            "http_status": getattr(error, "status", None),
        }
    else:
        attach_response(record, raw, expected)
    finally:
        record["elapsed_seconds"] = round(perf_counter() - start, 6)
    return record


def save_record(record: dict, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{record['record_id']}.json"
    saved = deepcopy(record)
    try:
        json.dumps(saved["raw_response"], allow_nan=False)
    except ValueError:
        # Nonstandard JSON numbers cannot appear inside a valid JSON record.
        saved["raw_response_nonstandard_json"] = json.dumps(saved["raw_response"], ensure_ascii=False)
        saved["raw_response"] = None
    serialized = json.dumps(saved, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8") as stream:
        stream.write(serialized)
    return path


def mock_response(choice: str) -> dict:
    """A labeled fixture, never an observed Jev diagnosis."""
    return {
        "model": MODEL,
        "_fixture": "MOCK: handcrafted diagnosis answer; no API execution",
        "answers": {"diagnosis": {
            "type": "choice", "choice": choice, "confidence": 1.0,
            "probabilities": {option: float(option == choice) for option in option_labels()},
        }},
        "usage": {"input_tokens": 0, "output_tokens": 0},
    }


def import_response(
    request: dict, response_text: str, case_id: str | None = None, elapsed_seconds: float | None = None,
) -> dict:
    """Preserve supplied response text; importing does not verify live execution."""
    case = get_case(case_id) if case_id else None
    if case and request != build_request(case["vignette"]):
        raise ContractError("The supplied case ID does not match the exported request.")
    if elapsed_seconds is not None and (not math.isfinite(elapsed_seconds) or elapsed_seconds < 0):
        raise ContractError("Elapsed seconds must be finite and nonnegative.")
    record = new_record(request, "playground_import_unverified", case_id)
    record["elapsed_seconds"] = elapsed_seconds
    record["timing_source"] = "user_reported" if elapsed_seconds is not None else None
    record["original_response_text"] = response_text
    def reject_constant(value: str) -> None:
        raise ValueError(f"Non-JSON numeric constant: {value}")
    try:
        raw = json.loads(response_text, parse_constant=reject_constant)
    except ValueError:
        record["execution_status"] = "response_error"
        record["error"] = {"kind": "invalid_json", "message": "The supplied response is not valid JSON. Original text preserved."}
        return record
    if isinstance(raw, dict) and "_fixture" in raw:
        record["execution_origin"] = "mock_offline"
    return attach_response(record, raw, case["expected"] if case else None)
