# Pilot outcomes and next steps

Six user-supplied Playground responses and eight live SDK responses are preserved. All eight SDK calls completed without API or response-contract failures. Each call used the unchanged canonical inputs and explicitly selected `jev-1.13.0`; automatic retries were disabled.

## Outcomes

| Pilot | Playground choice | SDK choice, first pass | Playground selected-option probability | SDK selected-option probability |
| --- | --- | --- | ---: | ---: |
| pilot-01 | Von Gierke / I | Von Gierke / I | 100% | 100% |
| pilot-02 | Pompe / II | Pompe / II | 100% | 100% |
| pilot-03 | McArdle / V | McArdle / V | 100% | 100% |
| pilot-04 | Cori/Forbes / III | Cori/Forbes / III | 100% | 100% |
| pilot-05 | Hers / VI | Hers / VI | 100% | 100% |
| pilot-06 | Insufficient information | Insufficient information | 72% | 73% |

The six distinct pilot choices matched their author-defined labels in both sources. Repeating pilot 06 added two SDK responses, for eight SDK calls in total. This is a small synthetic demonstration, not a clinical accuracy benchmark.

## Two findings

**1. The integration reproduced the five characteristic pilot outputs.** The first five SDK responses matched the Playground choices, option probabilities, confidence values, and display statuses. This confirms observed agreement for these inputs, not broader diagnostic performance.

**2. The ambiguous choice stayed stable while its probability distribution varied.** Pilot 06 selected `insufficient_information` in the Playground and all three SDK runs:

| Source | Insufficient information | Hers / VI | Cori/Forbes / III | Separate confidence | Display status |
| --- | ---: | ---: | ---: | ---: | --- |
| Playground | 72% | 21% | 7% | 68% | `uncertain` |
| SDK run 1 | 73% | 21% | 6% | 68% | `uncertain` |
| SDK run 2 | 77% | 16% | 7% | 73% | `uncertain` |
| SDK run 3 | 70% | 22% | 8% | 65% | `uncertain` |

The other four options received zero probability in all four responses. Every maximum remained below the unchanged, unvalidated 0.8 display threshold; the interpreter retained the fallback choice and left `diagnosis` unset. These are answer-option probabilities, not validated patient-level disease probabilities.

The three SDK requests for pilot 06 have identical request hashes. Their results establish variation in this batch; they do not identify its cause or characterize long-term repeatability. The Playground inputs were associated by case folder rather than captured on the wire, so the Playground comparison retains that limitation. No prompts, labels, thresholds, or unfavorable outputs were changed to improve agreement.

## Next build steps

1. Run the [twelve prepared evaluation cases](../playground/evaluation/) to examine sparse evidence, conflicting reports, an unlisted disorder, uninterpretable numbers, and embedded instructions.
2. Preserve errors and use them to decide whether criteria or fallback wording need a separately versioned revision.
3. Consider a small UI only if it helps combine the vignette, full distribution, separate confidence, fallback choice, uncertainty flag, and saved-run comparison.

## Evidence

- [SDK run manifest](sdk_run_manifest.json) and [complete SDK review](sdk_review.md): all eight attempts, with request IDs and links to the original responses.
- [Playground import manifest](playground_import_manifest.json), [source audit](playground_results.md), and [complete Playground review](playground_review.md): six imported responses and original screenshot/RTF provenance.
- [Repository verification](repository_verification.json): software checks. The eighteen [offline fixtures](offline/) are mocks and are not model-performance evidence.

SDK elapsed time is measured by the local client. Playground `evaluation_time_ms` is provider-reported and is not treated as the same latency measurement. The twelve additional evaluation cases have only been checked offline; no live evaluation results are claimed for them.
