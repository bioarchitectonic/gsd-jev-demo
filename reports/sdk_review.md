# Diagnosis-choice review

Jev selects a diagnosis option directly. No local feature scores or disease reranking are applied. These model answer probabilities are not validated clinical disease probabilities.

`mock_offline` means handcrafted responses with no evidence of model accuracy. `playground_import_unverified` means a supplied file whose execution provenance cannot be authenticated. Each attempt remains a separate record, including failures and repeated cases.

| Origin | Records | Completed | Failed / not run |
| --- | ---: | ---: | ---: |
| live_api | 8 | 8 | 0 |

## pilot-01 / c0e713c6-8f33-4960-9c36-5921ccdace2f

Origin: `live_api`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.89538` (client_wall_clock). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-02 / cd03850a-7789-482e-8f2a-448360bb42c0

Origin: `live_api`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.514466` (client_wall_clock). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-03 / 587f9032-effb-4176-aad5-58a43ae5ee17

Origin: `live_api`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.785405` (client_wall_clock). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-04 / ab0d178c-ade0-4d55-bb10-72e622182187

Origin: `live_api`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.499162` (client_wall_clock). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-05 / f0148fbb-26eb-453c-a00c-654958936ac5

Origin: `live_api`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.483361` (client_wall_clock). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-06 / e645ef4d-0e39-48ef-acb1-2160c76368fd

Origin: `live_api`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.517725` (client_wall_clock). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `uncertain`. Maximum option probability is below the unvalidated 0.8 demo threshold.

Maximum option probability: 0.73. Separate model confidence: 0.68.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `False`.

Reference-label note only: compatible diagnoses include cori_forbes_gsd_iii, hers_gsd_vi. This note is not a model-generated differential.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 0.73 |
| Hers disease (GSD VI) | disorder | 0.21 |
| Cori/Forbes disease (GSD III) | disorder | 0.06 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| None of the above | fallback | 0 |

## pilot-06 / a17cfdf0-a481-441a-ac21-dd11845753fa

Origin: `live_api`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.501911` (client_wall_clock). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `uncertain`. Maximum option probability is below the unvalidated 0.8 demo threshold.

Maximum option probability: 0.77. Separate model confidence: 0.73.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `False`.

Reference-label note only: compatible diagnoses include cori_forbes_gsd_iii, hers_gsd_vi. This note is not a model-generated differential.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 0.77 |
| Hers disease (GSD VI) | disorder | 0.16 |
| Cori/Forbes disease (GSD III) | disorder | 0.07 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| None of the above | fallback | 0 |

## pilot-06 / 8af74dc5-31bf-4751-bc73-180d5dfa741c

Origin: `live_api`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `0.484296` (client_wall_clock). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `uncertain`. Maximum option probability is below the unvalidated 0.8 demo threshold.

Maximum option probability: 0.7. Separate model confidence: 0.65.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `False`.

Reference-label note only: compatible diagnoses include cori_forbes_gsd_iii, hers_gsd_vi. This note is not a model-generated differential.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 0.7 |
| Hers disease (GSD VI) | disorder | 0.22 |
| Cori/Forbes disease (GSD III) | disorder | 0.08 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| None of the above | fallback | 0 |
