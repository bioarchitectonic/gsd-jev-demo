# Observations: direct diagnosis Choice

> Historical snapshot: this report predates the six Playground imports and the eight live SDK calls. See [current results](RESULTS.md) and [repository verification](repository_verification.json).

Date: 2026-09-21. Implementation, question, content, and display-policy version: 0.2.0.

**The request now matches the intended interaction: USMLE-style vignette in State, disorders as Choice options, and Jev selecting the diagnosis.** The CLI and exports work offline. No real v2 responses have been generated or imported by this implementation; the user's current Playground results have not been supplied as records.

## Preservation context

The original workspace retained the earlier feature-extraction implementation and its preservation manifest separately. Those local archive files are not dependencies of this standalone repository. This historical report describes the transition to the direct diagnosis-choice design; original v2 source files remain preserved outside this copy.

## Changed behavior

| Stage | Archived version | V2 |
| --- | --- | --- |
| State | Synthetic vignette | Synthetic USMLE-style vignette |
| Question | Eight feature-state questions | One `diagnosis` Choice question |
| Options | Present/absent/unreported/conflicting | Five named disorders plus two fallback options |
| Clinical patterns | Feature definitions and local cards | Each disorder's Choice criteria |
| Diagnosis selection | Python compared feature scores | Jev selects the diagnosis directly |
| Local handling | Feature threshold and point comparison | Validate the response, retain probabilities, and display uncertainty |

The disorders are von Gierke, Pompe, Cori/Forbes, McArdle, and Hers. `insufficient_information` covers missing, contradictory, or nondiscriminating evidence; `none_of_the_above` requires affirmative evidence for an unlisted alternative. There is no local clinical point score or diagnosis reranking.

## Verified offline

| Check | Result | What it establishes |
| --- | --- | --- |
| Revised test suite | 50 passed, 0 failed; 0.17 seconds | Software contracts and display behavior, not diagnostic accuracy or API latency |
| Official SDK transport | One mocked request; canonical body preserved | Structured disease criteria reach the wire unchanged |
| Fixture replay | Six pilot and twelve evaluation responses | Parsing, recording, and display work for handcrafted answers |
| Deliberately wrong diagnosis | Preserved and flagged against reference | Local code does not replace Jev's diagnosis |
| Uncertain/tied distributions | Raw choice and tied leading options retained | The display threshold does not rewrite the answer |
| Malformed responses and API failures | Preserved without a diagnosis | Technical failures remain separate from model fallback selections |
| Archive preservation | 77 original content hashes verified | Original artifacts and the concurrent formatting edit remain available |

The [mock-only review](offline/review.md) contains all fixture distributions. The fixture generator directly uses reference answers, so matching them is not evidence that Jev recognizes these vignettes. [verification.json](verification.json) records execution status.

## Pilot expectations

| Case | Focus | Reference teaching answer | Actual Jev result |
| --- | --- | --- | --- |
| pilot-01 | Fasting hepatic biochemical pattern | Von Gierke disease (GSD I) | Not observed |
| pilot-02 | Infantile cardiac and muscle pattern | Pompe disease (GSD II) | Not observed |
| pilot-03 | Exercise intolerance with second wind | McArdle disease (GSD V) | Not observed |
| pilot-04 | Combined hepatic and muscle involvement | Cori/Forbes disease (GSD III) | Not observed |
| pilot-05 | Hepatic pattern with specific enzyme evidence | Hers disease (GSD VI) | Not observed |
| pilot-06 | Undistinguished liver-only presentation | Insufficient information | Not observed |

These are original synthetic teaching cases, not copied exam questions or patient records. Criteria and expected labels are author-defined and have no independent clinical adjudication.

Pilot 05 supplies specific enzyme evidence to distinguish VI. Pilot 06 leaves IIIb versus VI unresolved; it tests whether Jev selects the fallback instead of treating normal muscle findings as proof of VI. A Choice returns one option, not a joint diagnosis; the full probability distribution remains visible.

The twelve separate evaluation cases add later-onset disease, enzyme/genetic evidence, normal muscle findings in III, sparse evidence, a conflicting report, an unlisted disorder, uninterpretable numbers, an embedded instruction, and fasting versus post-meal context. The split is also used for offline checks and is not a blinded benchmark.

## Pending observations

Run the [prepared inputs](../docs/PLAYGROUND.md) and preserve each complete response. Compare actual diagnosis choices, all option probabilities, confidence, and fallback behavior with the local expectations. Confidently wrong diagnoses must remain visible.

A maximum option probability below 0.8 only adds the CLI's `uncertain` status. This is an unvalidated display threshold, separate from model confidence. Model answer-option probabilities are not established clinical disease probabilities. The model's raw choice is retained at every probability level.

There is no live evidence here about diagnostic accuracy, calibration, latency, or handling of the embedded instruction. The previous browser automation limitation was not retried against the user's active session in this revision. No user-run results are inferred from mocks.

The next iteration should use actual answers to refine disorder criteria or fallback wording. The UI decision remains deferred until those results show which display adds value.

## References

The integration follows the official [Choice](https://docs.typesafe.ai/primitives/choice), [structured instructions](https://docs.typesafe.ai/primitives/advanced), and [Python SDK](https://docs.typesafe.ai/sdk/python) contracts. The [disorder catalog](../gsd_demo/data/disorders.json) links each pattern to GeneReviews. The [evaluation set](../gsd_demo/data/evaluation_cases.json) also links the out-of-set MCAD example to its source.
