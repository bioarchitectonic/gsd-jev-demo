# GSD diagnosis demo with Jev

A small Python integration that asks Jev to recognize glycogen storage disease patterns in synthetic USMLE-style vignettes. The vignette is the **State**; five disorders and two fallback answers are the options in one **Choice** question. Jev selects the answer and returns its full option distribution.

Built with Python 3.12, the official `typesafe-sdk==0.7.1`, and model `jev-1.13.0`. Project version: `0.2.0`.

## Observed outcomes

Six user-run Playground responses and eight live SDK responses are preserved. All selected options matched their author-defined pilot labels. The first five SDK cases reproduced the Playground choices and probability values. Pilot 06 kept the same fallback choice across three SDK calls, with varying probabilities:

| Pilot | Selected option | Playground probability | SDK probability |
| --- | --- | ---: | ---: |
| 01 | Von Gierke / GSD I | 100% | 100% |
| 02 | Pompe / GSD II | 100% | 100% |
| 03 | McArdle / GSD V | 100% | 100% |
| 04 | Cori/Forbes / GSD III | 100% | 100% |
| 05 | Hers / GSD VI | 100% | 100% |
| 06 | Insufficient information | 72% | 73%, 77%, 70% |

The probability column describes the selected answer option. In pilot 06, probability also remained on GSD VI and GSD III. The complete distributions, confidence values, two findings, and next steps are in [the results report](reports/RESULTS.md). These small synthetic runs establish observed behavior on these inputs; they are not a clinical accuracy benchmark.

## Run locally

Run from the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-build-isolation --no-deps -e .

python -m gsd_demo list
python -m gsd_demo export --case pilot-03 --out runs/pilot-03
python -m gsd_demo export --file examples/synthetic-vignette.txt --out runs/custom
python -m gsd_demo check-offline --out runs/offline
python -m pytest
```

An [included synthetic vignette](examples/synthetic-vignette.txt) is provided for the custom-file example.

The installed `gsd-demo` command is equivalent to `python -m gsd_demo`. Both `export` and `run` accept `--case`, `--text`, or `--file`. [requirements.txt](requirements.txt) pins the tested runtime and test dependencies.

If the environment path contains literal quotation marks, use the module command above; the generated console launcher can fail in that path.

Set `TYPESAFE_API_KEY` in your shell environment before making a live request:

```bash
python -m gsd_demo run --case pilot-03 --out runs/live
python -m gsd_demo review --records runs/live --out runs/live-review.md
```

Each `run` sends one request with automatic retries disabled. The application does not automatically load `.env` files; [.env.example](.env.example) documents the variable. Keep credentials local. Missing credentials, API failures, and invalid responses are recorded separately from a model selecting insufficient information.

## Try the official Playground

Open the [TypeSafe Playground](https://console.typesafe.ai/decode) and select `jev-1.13.0` where available. Paste [pilot 03 State](playground/pilot-03/state.json) into State and [pilot 03 Questions](playground/pilot-03/questions.json) into Questions. All cases share the same Questions payload.

See the [Playground guide](docs/PLAYGROUND.md) for all six pilots, twelve prepared evaluation inputs, and the response-import workflow. Reference labels are kept outside requests. The saved screenshots used the `jev-latest` alias; all six returned responses identify `jev-1.13.0`. The SDK check explicitly pinned that version.

## How the integration works

1. [core.py](gsd_demo/core.py) builds a request using the canonical [question definitions](gsd_demo/data/questions.json). Each disorder's criteria describe its clinical pattern and mechanism.
2. [runner.py](gsd_demo/runner.py) calls the official SDK and saves the request, original response, request ID, model version, timing, content/policy versions, and hashes.
3. The interpreter validates the response and preserves Jev's selected option, all seven probabilities, and separate confidence value. [review.py](gsd_demo/review.py) compares saved outputs with local reference labels.

The options are Von Gierke (I), Pompe (II), Cori/Forbes (III), McArdle (V), Hers (VI), `insufficient_information`, and `none_of_the_above`. The [source catalog](gsd_demo/data/disorders.json) links each disorder to its criterion and GeneReviews reference. Python does not compute a disease score or substitute another diagnosis.

A maximum option probability below **0.8** adds an `uncertain` display status and leaves `diagnosis` unset. This is an **unvalidated demo threshold**. It does not alter `model_choice` or the distribution; the separate `confidence` value is retained but not thresholded. Pilot 06 illustrates why a display should show both the fallback choice and the uncertainty flag. The interpreter's `reason` describes this display rule, not a model-generated clinical rationale.

## Evidence and limitations

All vignettes are original synthetic educational examples, not copied USMLE questions or patient records. The project has no clinical validation. Criteria and reference labels have not received independent clinical review, and the twelve author-defined evaluation cases are not a blinded benchmark.

This demonstration uses **Choice alone** to keep the build focused. [Choice](https://docs.typesafe.ai/primitives/choice) returns a selected option, an option-probability distribution, and confidence. [Noul](https://docs.typesafe.ai/primitives/noul) returns a yes-answer probability. [Score](https://docs.typesafe.ai/primitives/score) returns probabilities over ordered descriptive levels, their probability-weighted position, and confidence. None is established here as a calibrated clinical disease probability. No local heuristic disease scores are used in this implementation; a heuristic score would not itself be a disease probability.

Evidence is kept distinct:

- [Live SDK records](reports/sdk_records/) and [run manifest](reports/sdk_run_manifest.json): eight actual API requests, including every repeated pilot 06 result.
- [Playground records](reports/playground_records/) and [import manifest](reports/playground_import_manifest.json): six user-supplied responses, with original screenshots and RTF files in each pilot folder. Their origin remains `playground_import_unverified`; the exact manually submitted inputs were not captured.
- [Offline fixtures](reports/offline/): eighteen explicitly labeled mock responses. They test software behavior and provide no evidence of Jev's diagnostic accuracy.
- [Repository verification](reports/repository_verification.json): checks of this prepared copy. [Earlier observations](reports/observations.md) and [earlier verification](reports/verification.json) are historical snapshots from before the Playground imports.

Exports describe prepared inputs; their `not_run` manifests are not an execution ledger. Actual attempts are recorded separately. Output commands preserve existing artifacts and refuse to overwrite different content.

## Next steps

Run the twelve prepared evaluation cases, inspect errors and fallback behavior, then decide whether a small UI adds value by combining the vignette, option distribution, uncertainty, references, and run comparison. The present release is a CLI and Playground demonstration.

## License

[MIT](LICENSE).
