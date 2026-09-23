"""One direct diagnosis question; no local disease inference or point scoring."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from importlib.resources import files
import json
import math
from typing import Any

MODEL = "jev-1.13.0"
THRESHOLD = 0.8
POLICY_VERSION = "0.2.0"
FALLBACK_LABELS = {
    "insufficient_information": "Insufficient information",
    "none_of_the_above": "None of the above",
}


class ContractError(ValueError):
    """The request or response does not satisfy this version's contract."""


def load_data(name: str) -> Any:
    return json.loads(files("gsd_demo").joinpath("data", name).read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def question_bank() -> dict:
    return load_data("questions.json")


def option_labels() -> dict[str, str]:
    return {
        **{item["id"]: item["label"] for item in load_data("disorders.json")["disorders"]},
        **FALLBACK_LABELS,
    }


def cases(split: str = "pilot") -> list[dict]:
    if split not in ("pilot", "evaluation"):
        raise ValueError("Split must be pilot or evaluation.")
    return load_data(f"{split}_cases.json")["cases"]


def get_case(case_id: str) -> dict:
    for split in ("pilot", "evaluation"):
        for case in cases(split):
            if case["id"] == case_id:
                return deepcopy(case)
    raise ValueError(f"Unknown case: {case_id}")


def build_request(vignette: str) -> dict:
    """Send only the vignette and the diagnosis-choice definitions to Jev."""
    if not isinstance(vignette, str) or not vignette.strip():
        raise ContractError("A non-empty English synthetic vignette is required.")
    if len(vignette) > 20_000:
        raise ContractError("The vignette exceeds the 20,000-character demo limit.")
    return {
        "model": MODEL,
        "state": {"case": {"vignette": vignette}},
        "questions": deepcopy(question_bank()["questions"]),
    }


def validate_request(request: Any) -> None:
    if not isinstance(request, dict) or set(request) != {"model", "state", "questions"}:
        raise ContractError("Request must contain exactly model, state, and questions.")
    try:
        vignette = request["state"]["case"]["vignette"]
    except (KeyError, TypeError) as error:
        raise ContractError("Request is missing state.case.vignette.") from error
    if request != build_request(vignette):
        raise ContractError("Request differs from the canonical questions or pinned model. Keep versions separate.")


def unit_interval(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError(f"{field} must be a number.")
    if not 0 <= value <= 1 or not math.isfinite(value):
        raise ContractError(f"{field} must be finite and between zero and one.")
    return float(value)


def interpret_response(raw: Any) -> dict:
    """Display Jev's decision and distribution without choosing another diagnosis."""
    if not isinstance(raw, dict) or raw.get("model") != MODEL:
        raise ContractError("Response must include the pinned returned model version.")
    answers = raw.get("answers")
    if not isinstance(answers, dict) or set(answers) != {"diagnosis"}:
        raise ContractError("Expected exactly one answer named diagnosis.")
    answer = answers["diagnosis"]
    if not isinstance(answer, dict) or answer.get("type") != "choice":
        raise ContractError("diagnosis must be a Choice answer.")
    labels = option_labels()
    probabilities = answer.get("probabilities")
    if not isinstance(probabilities, dict) or set(probabilities) != set(labels):
        raise ContractError("Probabilities must cover all five disorders and both fallback options.")
    probabilities = {key: unit_interval(value, key) for key, value in probabilities.items()}
    if not math.isclose(sum(probabilities.values()), 1, rel_tol=0, abs_tol=1e-6):
        raise ContractError("Option probabilities must sum to one.")
    choice = answer.get("choice")
    if not isinstance(choice, str) or choice not in labels:
        raise ContractError("The selected diagnosis option is unknown.")
    maximum = max(probabilities.values())
    if not math.isclose(probabilities[choice], maximum, rel_tol=0, abs_tol=1e-9):
        raise ContractError("The selected option must have maximum probability.")
    confidence = unit_interval(answer.get("confidence"), "confidence")
    leaders = [key for key in labels if math.isclose(probabilities[key], maximum, rel_tol=0, abs_tol=1e-9)]
    if maximum < THRESHOLD:
        status = "uncertain"
        reason = "Maximum option probability is below the unvalidated 0.8 demo threshold."
    elif choice in FALLBACK_LABELS:
        status = choice
        reason = "Jev selected a fallback option rather than one of the five diagnoses."
    else:
        status = "diagnosis_selected"
        reason = "Jev selected this diagnosis option; the demo threshold is met."
    return {
        "model_choice": choice,
        "model_label": labels[choice],
        "status": status,
        "reason": reason,
        "diagnosis": choice if status == "diagnosis_selected" else None,
        "max_probability": maximum,
        "model_confidence": confidence,
        "probabilities": probabilities,
        "leading_options": leaders,
        "option_ranking": [
            {"option": key, "label": labels[key], "probability": probabilities[key],
             "kind": "fallback" if key in FALLBACK_LABELS else "disorder"}
            for key in sorted(labels, key=lambda key: -probabilities[key])
        ],
        "probability_label": "Model answer-option probabilities; not validated clinical disease probabilities",
    }


def policy_snapshot() -> dict:
    return {
        "version": POLICY_VERSION,
        "task": "direct_diagnosis_choice",
        "minimum_max_option_probability": THRESHOLD,
        "threshold_status": "unvalidated_demo_threshold",
        "diagnosis_source": "Jev Choice answer only; no local disease scoring or reranking",
        "fallback_options": list(FALLBACK_LABELS),
    }


def evaluate_against_labels(result: dict, expected: dict) -> dict:
    """Separate the model's raw option match from the local uncertainty display."""
    return {
        "reference": deepcopy(expected),
        "model_choice_matches": result["model_choice"] == expected["choice"],
        "display_status_matches": result["status"] == expected["status"],
        "reference_label_status": "Author-defined synthetic expectations; no independent clinical review",
        "note": "Jev chooses the diagnosis; no local disease comparison is applied.",
    }
