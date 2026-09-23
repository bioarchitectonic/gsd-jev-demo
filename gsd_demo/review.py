"""Review direct diagnosis answers while keeping observed and mock origins clear."""

from __future__ import annotations


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_review(records: list[dict]) -> str:
    lines = [
        "# Diagnosis-choice review", "",
        "Jev selects a diagnosis option directly. No local feature scores or disease reranking are applied. "
        "These model answer probabilities are not validated clinical disease probabilities.", "",
        "`mock_offline` means handcrafted responses with no evidence of model accuracy. "
        "`playground_import_unverified` means a supplied file whose execution provenance cannot be authenticated. "
        "Each attempt remains a separate record, including failures and repeated cases.", "",
        "| Origin | Records | Completed | Failed / not run |",
        "| --- | ---: | ---: | ---: |",
    ]
    for origin in sorted({r["execution_origin"] for r in records}):
        selected = [r for r in records if r["execution_origin"] == origin]
        completed = sum(r["execution_status"] == "completed" for r in selected)
        lines.append(f"| {origin} | {len(selected)} | {completed} | {len(selected) - completed} |")
    for record in records:
        lines += [
            "", f"## {cell(record.get('case_id') or 'Custom vignette')} / {cell(record['record_id'])}", "",
            f"Origin: `{cell(record['execution_origin'])}`. Execution: `{cell(record['execution_status'])}`. "
            f"Returned model: `{cell(record['returned_model'])}`.", "",
            f"Elapsed seconds: `{cell(record['elapsed_seconds'])}` ({cell(record.get('timing_source') or 'not measured')}). "
            f"Question/content/policy versions: `{cell(record['question_version'])}` / "
            f"`{cell(record['content_version'])}` / `{cell(record['policy']['version'])}`.", "",
        ]
        if record["error"]:
            lines.append(f"Technical issue: {cell(record['error']['kind'])}. {cell(record['error']['message'])}")
        if not record["result"]:
            lines.append("No interpreted answer. This is an execution issue, not a model abstention.")
            continue
        result = record["result"]
        lines += [
            f"**Jev's option: {cell(result['model_label'])}** (`{cell(result['model_choice'])}`).", "",
            f"Display status: `{result['status']}`. {result['reason']}", "",
            f"Maximum option probability: {result['max_probability']:.6g}. "
            f"Separate model confidence: {result['model_confidence']:.6g}.", "",
        ]
        evaluation = record.get("evaluation")
        if evaluation:
            reference = evaluation["reference"]
            lines += [
                f"Expected option: `{cell(reference['choice'])}`. "
                f"Model option matches: `{evaluation['model_choice_matches']}`. "
                f"Display status matches reference: `{evaluation['display_status_matches']}`.", "",
            ]
            if reference.get("compatible_diagnoses"):
                lines += [
                    "Reference-label note only: compatible diagnoses include "
                    + ", ".join(reference["compatible_diagnoses"])
                    + ". This note is not a model-generated differential.", "",
                ]
        lines += ["| Answer option | Kind | Model probability |", "| --- | --- | ---: |"]
        for option in result["option_ranking"]:
            lines.append(f"| {cell(option['label'])} | {option['kind']} | {option['probability']:.6g} |")
    return "\n".join(lines) + "\n"
