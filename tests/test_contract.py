"""Offline contracts; handcrafted labels do not establish Jev accuracy."""

from copy import deepcopy
import json

import pytest

from gsd_demo.cli import export_request, main
from gsd_demo.core import (
    ContractError, MODEL, build_request, cases, evaluate_against_labels, get_case,
    interpret_response, load_data, option_labels, question_bank, validate_request,
)
from gsd_demo.runner import attach_response, import_response, mock_response, new_record, save_record


@pytest.fixture
def raw():
    return mock_response("pompe_gsd_ii")


def test_one_diagnosis_question_has_disorders_as_criteria_and_no_expected_labels(tmp_path):
    case = get_case("pilot-02")
    request = build_request(case["vignette"])
    assert request["state"] == {"case": {"vignette": case["vignette"]}}
    assert request["model"] == MODEL
    assert set(request["questions"]) == {"diagnosis"}
    question = request["questions"]["diagnosis"]
    assert question["type"] == "choice"
    assert isinstance(question["instructions"], dict)
    assert set(question["criteria"]) == set(option_labels())
    assert len(question["criteria"]) == 7
    assert all(isinstance(value, dict) for value in question["criteria"].values())
    assert "expected" not in json.dumps(request)
    assert "pilot-02" not in json.dumps(request)
    export_request(request, tmp_path, case["id"])
    assert json.loads((tmp_path / "questions.json").read_text()) == question_bank()["questions"]
    assert json.loads((tmp_path / "state.json").read_text()) == request["state"]
    assert json.loads((tmp_path / "request.json").read_text()) == request
    request["questions"]["diagnosis"]["criteria"].clear()
    assert len(build_request(case["vignette"])["questions"]["diagnosis"]["criteria"]) == 7


def test_source_catalog_maps_to_canonical_criteria_without_local_scoring():
    catalog = load_data("disorders.json")
    criteria = question_bank()["questions"]["diagnosis"]["criteria"]
    for disorder in catalog["disorders"]:
        assert disorder["id"] in criteria
        assert disorder["criteria_path"].endswith(disorder["id"])
        assert disorder["references"][0]["url"].startswith("https://www.ncbi.nlm.nih.gov/books/")
        assert "rules" not in disorder
    assert len(catalog["disorders"]) == 5


def test_separate_case_sets_cover_every_disorder_and_fallback():
    pilot, evaluation = cases("pilot"), cases("evaluation")
    assert len(pilot) == 6 and len(evaluation) == 12
    assert len({case["vignette"] for case in pilot + evaluation}) == 18
    assert not {c["family_id"] for c in pilot} & {c["family_id"] for c in evaluation}
    assert {c["expected"]["choice"] for c in pilot + evaluation} == set(option_labels())
    assert get_case("pilot-06")["expected"]["compatible_diagnoses"] == ["cori_forbes_gsd_iii", "hers_gsd_vi"]


@pytest.mark.parametrize("case", cases("pilot") + cases("evaluation"), ids=lambda case: case["id"])
def test_mock_diagnosis_replay_is_a_contract_check_only(case):
    record = new_record(build_request(case["vignette"]), "mock_offline", case["id"])
    response = mock_response(case["expected"]["choice"])
    attach_response(record, response, case["expected"])
    assert record["execution_status"] == "completed"
    assert record["evaluation"]["model_choice_matches"]
    assert record["evaluation"]["display_status_matches"]
    assert record["result"]["model_choice"] == response["answers"]["diagnosis"]["choice"]
    assert "support_score" not in json.dumps(record)
    assert record["elapsed_seconds"] is None


def test_response_choice_is_not_replaced_by_local_pattern_matching(raw):
    # Deliberately pair a Pompe response with a von Gierke-style vignette.
    case = get_case("pilot-01")
    record = attach_response(new_record(build_request(case["vignette"]), "mock_offline"), raw, case["expected"])
    assert record["result"]["model_choice"] == "pompe_gsd_ii"
    assert record["result"]["diagnosis"] == "pompe_gsd_ii"
    assert not record["evaluation"]["model_choice_matches"]
    assert record["evaluation"]["display_status_matches"]


@pytest.mark.parametrize("maximum, status", [(0.799999, "uncertain"), (0.8, "diagnosis_selected")])
def test_threshold_does_not_rewrite_model_choice(raw, maximum, status):
    answer = raw["answers"]["diagnosis"]
    answer["probabilities"]["pompe_gsd_ii"] = maximum
    answer["probabilities"]["insufficient_information"] = 1 - maximum
    answer["confidence"] = 0.01
    result = interpret_response(raw)
    assert result["status"] == status
    assert result["model_choice"] == "pompe_gsd_ii"
    assert result["model_label"] == "Pompe disease (GSD II)"
    assert result["model_confidence"] == 0.01
    assert result["probabilities"] == answer["probabilities"]
    expected = {"choice": "pompe_gsd_ii", "status": "diagnosis_selected"}
    evaluation = evaluate_against_labels(result, expected)
    assert evaluation["model_choice_matches"]
    assert evaluation["display_status_matches"] == (maximum >= 0.8)


def test_tied_options_are_retained_without_local_diagnosis(raw):
    answer = raw["answers"]["diagnosis"]
    answer["choice"] = "cori_forbes_gsd_iii"
    answer["probabilities"] = dict.fromkeys(option_labels(), 0.0)
    answer["probabilities"]["cori_forbes_gsd_iii"] = 0.5
    answer["probabilities"]["hers_gsd_vi"] = 0.5
    result = interpret_response(raw)
    assert result["leading_options"] == ["cori_forbes_gsd_iii", "hers_gsd_vi"]
    assert result["diagnosis"] is None
    assert result["status"] == "uncertain"


@pytest.mark.parametrize("choice", ["insufficient_information", "none_of_the_above"])
def test_model_fallbacks_are_not_rendered_as_disease_diagnoses(choice):
    result = interpret_response(mock_response(choice))
    assert result["status"] == choice
    assert result["diagnosis"] is None
    assert result["model_choice"] == choice
    assert result["option_ranking"][0]["kind"] == "fallback"


@pytest.mark.parametrize("defect", ["extra_answer", "missing_answer", "wrong_type", "missing_option", "sum", "nan", "bool", "choice", "choice_type", "confidence", "model"])
def test_invalid_response_is_preserved_without_a_diagnosis(raw, defect, tmp_path):
    answer = raw["answers"]["diagnosis"]
    if defect == "extra_answer":
        raw["answers"]["hepatomegaly"] = deepcopy(answer)
    elif defect == "missing_answer":
        raw["answers"].clear()
    elif defect == "wrong_type":
        answer["type"] = "score"
    elif defect == "missing_option":
        answer["probabilities"].pop("none_of_the_above")
    elif defect == "sum":
        answer["probabilities"]["hers_gsd_vi"] = 0.2
    elif defect == "nan":
        answer["probabilities"]["pompe_gsd_ii"] = float("nan")
    elif defect == "bool":
        answer["probabilities"]["pompe_gsd_ii"] = True
    elif defect == "choice":
        answer["choice"] = "hers_gsd_vi"
    elif defect == "choice_type":
        answer["choice"] = ["pompe_gsd_ii"]
    elif defect == "confidence":
        answer.pop("confidence")
    else:
        raw["model"] = "jev-other-version"
    record = attach_response(new_record(build_request("Synthetic example."), "mock_offline"), raw)
    assert record["execution_status"] == "response_error"
    assert record["result"] is None
    assert record["raw_response"] is raw
    saved = json.loads(save_record(record, tmp_path).read_text())
    assert saved["execution_status"] == "response_error"
    if defect == "nan":
        assert saved["raw_response"] is None
        assert "NaN" in saved["raw_response_nonstandard_json"]
    else:
        assert saved["raw_response"] == raw


def test_export_refuses_changed_content_and_import_rejects_old_contract(tmp_path):
    request = build_request("Synthetic first vignette.")
    export_request(request, tmp_path)
    with pytest.raises(ContractError, match="replace"):
        export_request(build_request("Synthetic changed vignette."), tmp_path)
    assert json.loads((tmp_path / "request.json").read_text()) == request
    old = deepcopy(request)
    old["questions"] = {"hepatomegaly": {"type": "choice", "criteria": {"present": None, "absent": None}}}
    with pytest.raises(ContractError, match="canonical"):
        validate_request(old)


def test_import_provenance_and_case_binding(raw):
    case = get_case("pilot-02")
    request = build_request(case["vignette"])
    assert import_response(request, json.dumps(raw), case["id"])["execution_origin"] == "mock_offline"
    raw.pop("_fixture")
    record = import_response(request, json.dumps(raw), case["id"], 0.7)
    assert record["execution_origin"] == "playground_import_unverified"
    assert record["original_response_text"] == json.dumps(raw)
    assert record["elapsed_seconds"] == 0.7
    assert record["timing_source"] == "user_reported"
    with pytest.raises(ContractError, match="does not match"):
        import_response(request, json.dumps(raw), "pilot-01")


@pytest.mark.parametrize("body", ["<html>Login</html>", '{"value": NaN}'])
def test_invalid_json_is_kept_as_original_text(body, tmp_path):
    record = import_response(build_request("Synthetic example."), body)
    saved = json.loads(save_record(record, tmp_path).read_text())
    assert saved["original_response_text"] == body
    assert saved["execution_status"] == "response_error"
    assert saved["result"] is None


def test_records_are_append_only_and_versioned(raw, tmp_path):
    request = build_request("Synthetic original.")
    record = attach_response(new_record(request, "mock_offline"), raw)
    request["state"]["case"]["vignette"] = "Changed later"
    path = save_record(record, tmp_path)
    assert path.name.endswith(".json")
    assert json.loads(path.read_text()) == record
    assert record["request"]["state"]["case"]["vignette"] == "Synthetic original."
    assert record["question_version"] == record["content_version"] == record["policy"]["version"] == "0.2.0"
    assert record["software"]["demo"] == "0.2.0"
    with pytest.raises(FileExistsError):
        save_record(record, tmp_path)


def test_cli_export_mock_replay_review_and_no_overwrite(tmp_path, capsys):
    exports = tmp_path / "exports"
    assert main(["export-pilots", "--out", str(exports)]) == 0
    assert len(list(exports.glob("*/request.json"))) == 6
    offline = tmp_path / "offline"
    assert main(["check-offline", "--out", str(offline)]) == 0
    assert len(list(offline.glob("*.json"))) == 18
    review = (offline / "review.md").read_text()
    assert "MOCK ONLY" in capsys.readouterr().out
    assert "no evidence of model accuracy" in review
    assert "Pompe disease (GSD II)" in review
    assert "Model probability" in review
    assert main(["check-offline", "--out", str(offline)]) == 2
    assert (offline / "review.md").read_text() == review
    assert len(list(offline.glob("*.json"))) == 18
    assert main(["review", "--records", str(offline), "--out", str(tmp_path / "combined.md")]) == 0
