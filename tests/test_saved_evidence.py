"""Regression checks against the supplied Playground evidence, without API calls."""

from hashlib import sha256
import json
from pathlib import Path

import pytest

from gsd_demo.core import build_request, fingerprint, get_case, interpret_response

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("case_id", [f"pilot-{n:02d}" for n in range(1, 7)])
def test_saved_playground_request_response_and_provenance(case_id):
    directory = ROOT / "playground" / case_id
    request = json.loads((directory / "request.json").read_text())
    assert request == build_request(get_case(case_id)["vignette"])
    assert json.loads((directory / "state.json").read_text()) == request["state"]
    assert json.loads((directory / "questions.json").read_text()) == request["questions"]
    response_text = (directory / "response.json").read_text()
    response = json.loads(response_text)
    records = [
        json.loads(path.read_text())
        for path in (ROOT / "reports/playground_records").glob("*.json")
    ]
    record, = [item for item in records if item["case_id"] == case_id]
    assert record["execution_origin"] == "playground_import_unverified"
    assert record["raw_response"] == response
    assert record["original_response_text"] == response_text
    assert record["result"] == interpret_response(response)
    assert record["request_sha256"] == fingerprint(request)
    assert record["questions_sha256"] == fingerprint(request["questions"])
    assert record["content_sha256"] == fingerprint(record["disorder_catalog"])
    assert record["policy_sha256"] == fingerprint(record["policy"])
    evidence = record["source_evidence"]
    for kind in ("rtf", "screenshot", "extracted_json"):
        assert sha256((ROOT / evidence[f"{kind}_path"]).read_bytes()).hexdigest() == evidence[f"{kind}_sha256"]
    if case_id == "pilot-06":
        result = record["result"]
        assert result["model_choice"] == "insufficient_information"
        assert result["status"] == "uncertain"
        assert result["diagnosis"] is None
        assert result["probabilities"]["insufficient_information"] == 0.72
        assert result["probabilities"]["hers_gsd_vi"] == 0.21
        assert result["probabilities"]["cori_forbes_gsd_iii"] == 0.07
