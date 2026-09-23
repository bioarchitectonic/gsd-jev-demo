# Playground inputs: vignette to diagnosis

In the [official Playground](https://console.typesafe.ai/decode), use model `jev-1.13.0`. Paste a case's `state.json` into State and `questions.json` into Questions. The latter is the bare question map, ready to paste; the canonical data file's version wrapper is not included. Keep the structured criteria as objects.

There is **one question**, `diagnosis`. Its **answer options are the disorders**. Each option's criteria describe the corresponding pattern. Do not create a separate question for each disorder; the single Choice compares the alternatives and returns one answer plus the full distribution.

All cases share the same Questions payload. The request's state contains only the vignette. The labels below are local review expectations and must not be added to the State field.

| Pilot | State | Questions | Complete request | Expected teaching answer |
| --- | --- | --- | --- | --- |
| 01: fasting hepatic pattern | [state](../playground/pilot-01/state.json) | [questions](../playground/pilot-01/questions.json) | [request](../playground/pilot-01/request.json) | Von Gierke |
| 02: infantile cardiac/muscle pattern | [state](../playground/pilot-02/state.json) | [questions](../playground/pilot-02/questions.json) | [request](../playground/pilot-02/request.json) | Pompe |
| 03: exertional symptoms/second wind | [state](../playground/pilot-03/state.json) | [questions](../playground/pilot-03/questions.json) | [request](../playground/pilot-03/request.json) | McArdle |
| 04: liver and muscle findings | [state](../playground/pilot-04/state.json) | [questions](../playground/pilot-04/questions.json) | [request](../playground/pilot-04/request.json) | Cori/Forbes |
| 05: liver phosphorylase evidence | [state](../playground/pilot-05/state.json) | [questions](../playground/pilot-05/questions.json) | [request](../playground/pilot-05/request.json) | Hers |
| 06: overlapping liver-only pattern | [state](../playground/pilot-06/state.json) | [questions](../playground/pilot-06/questions.json) | [request](../playground/pilot-06/request.json) | Insufficient information |

All six user-run Playground responses have been imported, and eight live SDK requests have now completed. See [the current results](../reports/RESULTS.md). Export manifests describe preparation, not execution. The screenshots used the `jev-latest` alias; the saved responses and pinned SDK runs returned `jev-1.13.0`.

## Preserve what Jev actually returns

Save the complete response, including the returned `model`, `answers.diagnosis`, its `choice`, `probabilities`, `confidence`, and usage. Import it against the exact corresponding request from the repository root:

```bash
python -m gsd_demo import-response \
  --request playground/pilot-03/request.json \
  --response runs/playground_responses/pilot-03.json \
  --case pilot-03 \
  --out runs/playground_records

python -m gsd_demo review \
  --records runs/playground_records \
  --out runs/playground_review.md
```

Use `--elapsed-seconds` only for an actual measurement; imported timing is stored as user-reported. The importer does not attest to a file's origin, so records are labeled `playground_import_unverified`. It preserves model-version mismatches and malformed responses as failures instead of inventing diagnoses.

Inspect the model's raw choice and all seven probabilities first. The CLI's `uncertain` display uses an unvalidated maximum-option threshold of 0.8 and never changes the raw choice. If Jev chooses the wrong disorder with high confidence, that error stays visible. If it selects a fallback, assess whether the vignette truly lacks distinguishing evidence or supports an unlisted disorder.

There is no local disease-scoring policy in this implementation. Diagnosis mismatches now belong to model/prompt/content evaluation; the remaining local rules validate the response and display uncertainty. In particular, a normal CK result must not be treated as proof that IIIb is impossible.

The twelve evaluation cases are exported under [playground/evaluation](../playground/evaluation/). They have not been run against Jev. They can also be prepared with `export --case eval-01` through `eval-12`. Keep every attempt. For changed prompts, preserve the current artifacts and create another version before exporting fresh requests.
