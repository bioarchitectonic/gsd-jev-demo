# Diagnosis-choice review

Jev selects a diagnosis option directly. No local feature scores or disease reranking are applied. These model answer probabilities are not validated clinical disease probabilities.

`mock_offline` means handcrafted responses with no evidence of model accuracy. `playground_import_unverified` means a supplied file whose execution provenance cannot be authenticated. Each attempt remains a separate record, including failures and repeated cases.

| Origin | Records | Completed | Failed / not run |
| --- | ---: | ---: | ---: |
| playground_import_unverified | 6 | 6 | 0 |

## pilot-01 / 7c2607bd-cb18-4773-94ec-33b31fee98d4

Origin: `playground_import_unverified`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.09591538999666227` (user_reported). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Von Gierke disease (GSD I)** (`von_gierke_gsd_i`).

Display status: `diagnosis_selected`. Jev selected this diagnosis option; the demo threshold is met.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `von_gierke_gsd_i`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Von Gierke disease (GSD I) | disorder | 1 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| Insufficient information | fallback | 0 |
| None of the above | fallback | 0 |

## pilot-02 / 5638831a-e72a-4e50-87ba-13e382344d22

Origin: `playground_import_unverified`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.07561531700048363` (user_reported). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Pompe disease (GSD II)** (`pompe_gsd_ii`).

Display status: `diagnosis_selected`. Jev selected this diagnosis option; the demo threshold is met.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `pompe_gsd_ii`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Pompe disease (GSD II) | disorder | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| Insufficient information | fallback | 0 |
| None of the above | fallback | 0 |

## pilot-03 / a44cd02d-5d9d-4e08-ac34-a47daa2c6aa7

Origin: `playground_import_unverified`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.09860429000036675` (user_reported). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: McArdle disease (GSD V)** (`mcardle_gsd_v`).

Display status: `diagnosis_selected`. Jev selected this diagnosis option; the demo threshold is met.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `mcardle_gsd_v`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| McArdle disease (GSD V) | disorder | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| Insufficient information | fallback | 0 |
| None of the above | fallback | 0 |

## pilot-04 / 13be87b2-9571-48c4-832e-4baa41533e91

Origin: `playground_import_unverified`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.08913600599044003` (user_reported). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Cori/Forbes disease (GSD III)** (`cori_forbes_gsd_iii`).

Display status: `diagnosis_selected`. Jev selected this diagnosis option; the demo threshold is met.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `cori_forbes_gsd_iii`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Cori/Forbes disease (GSD III) | disorder | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| Insufficient information | fallback | 0 |
| None of the above | fallback | 0 |

## pilot-05 / 43201430-3afa-40bb-acd9-a23300d1f1e9

Origin: `playground_import_unverified`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.1193496160012728` (user_reported). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Hers disease (GSD VI)** (`hers_gsd_vi`).

Display status: `diagnosis_selected`. Jev selected this diagnosis option; the demo threshold is met.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `hers_gsd_vi`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Hers disease (GSD VI) | disorder | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Insufficient information | fallback | 0 |
| None of the above | fallback | 0 |

## pilot-06 / db9da11f-d714-4caf-9440-8789df180bef

Origin: `playground_import_unverified`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.07110985399049241` (user_reported). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `uncertain`. Maximum option probability is below the unvalidated 0.8 demo threshold.

Maximum option probability: 0.72. Separate model confidence: 0.68.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `False`.

Reference-label note only: compatible diagnoses include cori_forbes_gsd_iii, hers_gsd_vi. This note is not a model-generated differential.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 0.72 |
| Hers disease (GSD VI) | disorder | 0.21 |
| Cori/Forbes disease (GSD III) | disorder | 0.07 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| None of the above | fallback | 0 |
