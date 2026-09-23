"""Command-line requests, exports, execution, and review without a UI dependency."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .core import ContractError, MODEL, build_request, cases, fingerprint, get_case, question_bank
from .review import render_review
from .runner import attach_response, import_response, mock_response, new_record, run_live, save_record


def write_artifact(path: Path, text: str) -> None:
    if path.exists():
        if path.read_text(encoding="utf-8") == text:
            return
        raise ContractError(f"Refusing to overwrite an existing artifact: {path}. Choose a new versioned output path.")
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_artifact(path, json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def export_request(request: dict, directory: Path, case_id: str | None = None) -> Path:
    """Export the exact SDK inputs; never export reference labels into state."""
    payloads = {
        "request.json": request,
        "state.json": request["state"],
        "questions.json": request["questions"],
        "manifest.json": {
            "execution_status": "not_run",
            "model": MODEL,
            "case_id": case_id,
            "question_version": question_bank()["version"],
            "request_sha256": fingerprint(request),
            "playground_url": "https://console.typesafe.ai/decode",
        },
    }
    directory.mkdir(parents=True, exist_ok=True)
    # Verify all existing files before writing; changed exports need a new directory.
    for name, value in payloads.items():
        path = directory / name
        if path.exists() and json.loads(path.read_text(encoding="utf-8")) != value:
            raise ContractError(f"Export would replace different content: {path}. Choose a new directory.")
    for name, value in payloads.items():
        write_json(directory / name, value)
    return directory


def add_input(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--case", help="Built-in pilot or evaluation case ID")
    group.add_argument("--text", help="An English synthetic educational vignette")
    group.add_argument("--file", type=Path, help="UTF-8 text file containing a vignette")


def resolve_input(args: argparse.Namespace) -> tuple[dict, dict | None]:
    if args.case:
        case = get_case(args.case)
        return build_request(case["vignette"]), case
    text = args.file.read_text(encoding="utf-8") if args.file else args.text
    return build_request(text), None


def print_record(record: dict, path: Path) -> None:
    summary = {
        "record": str(path.resolve()),
        "execution_origin": record["execution_origin"],
        "execution_status": record["execution_status"],
        "returned_model": record["returned_model"],
        "elapsed_seconds": record["elapsed_seconds"],
        "diagnosis_result": record["result"],
        "error": record["error"],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Jev recognizes a synthetic vignette and directly chooses a GSD diagnosis.")
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="List built-in synthetic cases")
    listing.add_argument("--split", choices=("pilot", "evaluation", "all"), default="pilot")
    export = commands.add_parser("export", help="Export a request plus separate Playground inputs")
    add_input(export)
    export.add_argument("--out", type=Path, required=True)
    pilots = commands.add_parser("export-pilots", help="Prepare all six pilot requests; no API calls")
    pilots.add_argument("--out", type=Path, default=Path("playground"))
    run = commands.add_parser("run", help="Ask Jev for a diagnosis using TYPESAFE_API_KEY")
    add_input(run)
    run.add_argument("--out", type=Path, default=Path("runs"))
    ingest = commands.add_parser("import-response", help="Interpret a saved Playground response; provenance is unverified")
    ingest.add_argument("--request", type=Path, required=True)
    ingest.add_argument("--response", type=Path, required=True)
    ingest.add_argument("--case", help="Optional built-in case ID; must match the request vignette")
    ingest.add_argument("--elapsed-seconds", type=float, help="Optional user-reported Playground elapsed time")
    ingest.add_argument("--out", type=Path, default=Path("runs"))
    offline = commands.add_parser("check-offline", help="Replay labeled MOCK responses, never call Jev")
    offline.add_argument("--out", type=Path, default=Path("runs/offline"))
    review = commands.add_parser("review", help="Compare stored runs and preserve origin distinctions")
    review.add_argument("--records", type=Path, nargs="+", required=True, help="Record files or directories")
    review.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            splits = ("pilot", "evaluation") if args.split == "all" else (args.split,)
            for split in splits:
                for case in cases(split):
                    print(f"{case['id']}\t{split}\t{case['title']}")
        elif args.command == "export":
            request, case = resolve_input(args)
            export_request(request, args.out, case["id"] if case else None)
            print(f"Exported to {args.out.resolve()}. Execution status: not_run.")
        elif args.command == "export-pilots":
            for case in cases("pilot"):
                export_request(build_request(case["vignette"]), args.out / case["id"], case["id"])
            print(f"Exported six pilot requests to {args.out.resolve()}. Execution status: not_run.")
        elif args.command == "run":
            request, case = resolve_input(args)
            record = run_live(request, case["id"] if case else None, case["expected"] if case else None)
            path = save_record(record, args.out)
            print_record(record, path)
            return 0 if record["execution_status"] == "completed" else 2
        elif args.command == "import-response":
            request = json.loads(args.request.read_text(encoding="utf-8"))
            record = import_response(
                request, args.response.read_text(encoding="utf-8"), args.case, args.elapsed_seconds,
            )
            path = save_record(record, args.out)
            print_record(record, path)
            return 0 if record["execution_status"] == "completed" else 2
        elif args.command == "check-offline":
            if (args.out / "review.md").exists():
                raise ContractError("This offline batch already has a review. Use a new output directory.")
            records = []
            for split in ("pilot", "evaluation"):
                for case in cases(split):
                    request = build_request(case["vignette"])
                    record = new_record(request, "mock_offline", case["id"])
                    attach_response(record, mock_response(case["expected"]["choice"]), case["expected"])
                    save_record(record, args.out)
                    records.append(record)
            args.out.mkdir(parents=True, exist_ok=True)
            write_artifact(args.out / "review.md", render_review(records))
            print(f"MOCK ONLY: replayed {len(records)} handcrafted responses; no API calls. Review: {args.out.resolve() / 'review.md'}")
            valid = all(r["execution_status"] == "completed" and r["evaluation"]["model_choice_matches"] and r["evaluation"]["display_status_matches"] for r in records)
            return 0 if valid else 1
        elif args.command == "review":
            paths = []
            for source in args.records:
                paths.extend(sorted(source.glob("*.json")) if source.is_dir() else [source])
            records = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(set(paths))]
            if not records or any(record.get("record_version") != "0.2.0" for record in records):
                raise ContractError("Review requires execution records with record_version 0.2.0.")
            args.out.parent.mkdir(parents=True, exist_ok=True)
            write_artifact(args.out, render_review(records))
            print(f"Saved review to {args.out.resolve()}.")
    except (ContractError, ValueError, OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0
