# Observed Playground pilot results

> Saved Playground baseline. See [current results and SDK repeatability findings](RESULTS.md).

Review date: 2026-09-21. These are user-run Playground outputs, supplied as six screenshots and six TextEdit RTF documents containing JSON. They are distinct from the earlier mock fixtures. This report supplements the dated [offline observations](observations.md); the earlier report is retained as a historical snapshot with updated repository links.

**All six raw model choices match the author-defined pilot expectations.** The five characteristic disease vignettes each returned the expected disorder with option probability 1.0. The ambiguous hepatic vignette selected insufficient information while retaining probability on Hers and Cori/Forbes.

## Results

| Pilot | Expected option | Observed model choice | Selected-option probability | Separate confidence | CLI display status | Reported evaluation ms |
| --- | --- | --- | ---: | ---: | --- | ---: |
| pilot-01 | Von Gierke disease (GSD I) | Von Gierke disease (GSD I) | 100% | 100% | `diagnosis_selected` | 95.92 |
| pilot-02 | Pompe disease (GSD II) | Pompe disease (GSD II) | 100% | 100% | `diagnosis_selected` | 75.62 |
| pilot-03 | McArdle disease (GSD V) | McArdle disease (GSD V) | 100% | 100% | `diagnosis_selected` | 98.60 |
| pilot-04 | Cori/Forbes disease (GSD III) | Cori/Forbes disease (GSD III) | 100% | 100% | `diagnosis_selected` | 89.14 |
| pilot-05 | Hers disease (GSD VI) | Hers disease (GSD VI) | 100% | 100% | `diagnosis_selected` | 119.35 |
| pilot-06 | Insufficient information | Insufficient information | 72% | 68% | `uncertain` | 71.11 |

These six synthetic cases are a pilot demonstration, not a clinical benchmark or evidence of general diagnostic accuracy. A reported value of 1.0 is the model's answer-option output; it does not establish that the underlying diagnosis is infallible.

## Pilot 06: the informative boundary case

| Answer option | Returned probability |
| --- | ---: |
| Insufficient information | 72% |
| Hers disease / GSD VI | 21% |
| Cori/Forbes disease / GSD III | 7% |
| Von Gierke, Pompe, McArdle, none of the above | 0% each |

The selected option is `insufficient_information`, and the separate `confidence` field is 0.68. The screenshot and JSON agree on all seven option values and confidence.

This is useful evidence of the intended behavior for this vignette: the model favors abstention while keeping the relevant disease alternatives visible. It is more informative than displaying only the winning label. These numbers refer to the supplied answer options and criteria; they are not validated patient-level disease probabilities. In particular, the 21% is assigned to Hers/GSD VI, not to insufficient information. One response cannot establish behavior across repeated calls or differently worded cases.

The official [Choice documentation](https://docs.typesafe.ai/primitives/choice) distinguishes the selected option, its full probability distribution, and a separate confidence summary derived from the distribution. Thus 72% maximum option probability and 68% confidence are different quantities, and both should remain visible.

## Why the Python report shows one display-status mismatch

All six `model_choice_matches` values are true. Five of six `display_status_matches` values are true. The exception is pilot 06: its reference display status was `insufficient_information`, but the existing interpreter checks the unvalidated 0.8 maximum-option threshold first and therefore displays `uncertain` at 0.72.

The raw choice remains `insufficient_information`, all probabilities are retained, and `diagnosis` is null. This is a mismatch between two ways of representing abstention, not a wrong disease answer or an API failure. No threshold, prompt, reference label, or implementation was changed to make the results look better. A future display should show both the model's fallback choice and its uncertainty flag explicitly.

## Source verification and import

The original RTF and PNG files were preserved, and their content hashes were verified after import. macOS `textutil` extracted the plain UTF-8 text from each RTF. That exact text was saved as `response.json` beside its source file, parsed as JSON, and processed by the existing v2 response interpreter. No new API calls were made.

| Pilot | Usable response file | Imported record |
| --- | --- | --- |
| pilot-01 | [extracted JSON](../playground/pilot-01/response.json) | [full record](playground_records/7c2607bd-cb18-4773-94ec-33b31fee98d4.json) |
| pilot-02 | [extracted JSON](../playground/pilot-02/response.json) | [full record](playground_records/5638831a-e72a-4e50-87ba-13e382344d22.json) |
| pilot-03 | [extracted JSON](../playground/pilot-03/response.json) | [full record](playground_records/a44cd02d-5d9d-4e08-ac34-a47daa2c6aa7.json) |
| pilot-04 | [extracted JSON](../playground/pilot-04/response.json) | [full record](playground_records/13be87b2-9571-48c4-832e-4baa41533e91.json) |
| pilot-05 | [extracted JSON](../playground/pilot-05/response.json) | [full record](playground_records/43201430-3afa-40bb-acd9-a23300d1f1e9.json) |
| pilot-06 | [extracted JSON](../playground/pilot-06/response.json) | [full record](playground_records/db9da11f-d714-4caf-9440-8789df180bef.json) |

The [complete generated review](playground_review.md) preserves every distribution, confidence, selected option, and reference comparison. The [import manifest](playground_import_manifest.json) records source paths/hashes, visually observed screenshot values, and import outcomes. Each record retains the original response, request ID, usage, empty `stats` object, and Playground timing metadata.

For pilots 01–05, each screenshot displays the leading option and two zero-probability alternatives, rather than all seven rows. Those visible values and confidence match the JSON; the complete seven-option distribution is supplied by the JSON. Pilot 06 shows all seven options. No full input vignette or all option criteria are visible in these response screenshots, so the records associate each response with its canonical request using the user's folder placement, not a captured wire request.

The screenshot model selector is `jev-latest`, while every saved response's resolved model is `jev-1.13.0`. This matches the version targeted by the canonical exports, but the manually selected alias is not itself a pinned request. Use the explicit version for future comparisons where the console permits it. Records retain `playground_import_unverified` as their origin because importing a user-supplied file does not independently authenticate execution provenance.

The elapsed value stored in each record is the supplied `evaluation_time_ms` divided by 1000, labeled user-reported. It is not locally measured end-to-end latency. The screenshot shows an additional time after a plus sign; its meaning was not visible, so it was recorded without assigning a latency interpretation.

The six supplied evaluation times range from 71.11 to 119.35 ms, with a median of 92.53 ms. These are descriptive values from this batch, not a performance benchmark.

## Implications for the next iteration

The direct diagnosis-choice design works on these supplied pilots. The next useful check is the twelve separate evaluation cases, especially missing data, contradictory evidence, an unlisted disorder, ambiguous exercise symptoms, and embedded instructions. Preserve failures and label changes instead of tuning only to the six successful pilot choices.

The Playground already shows the distribution that makes pilot 06 useful. A dedicated UI would add value if it combines the vignette, full option distribution, fallback/uncertainty display, source references, and saved-run comparison in one place. These observations support preserving those views; they do not require a separate UI yet. No UI or code changes were made during this review.
