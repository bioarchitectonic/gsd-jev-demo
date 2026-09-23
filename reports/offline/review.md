# Diagnosis-choice review

Jev selects a diagnosis option directly. No local feature scores or disease reranking are applied. These model answer probabilities are not validated clinical disease probabilities.

`mock_offline` means handcrafted responses with no evidence of model accuracy. `playground_import_unverified` means a supplied file whose execution provenance cannot be authenticated. Each attempt remains a separate record, including failures and repeated cases.

| Origin | Records | Completed | Failed / not run |
| --- | ---: | ---: | ---: |
| mock_offline | 18 | 18 | 0 |

## pilot-01 / 8b0582a3-115a-4ac7-a48f-fb3ef7d31188

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-02 / 8e0c737c-33a2-4509-9278-e0cadb4379d9

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-03 / d91aadde-dcd4-40e1-9069-a6eb5e6c0339

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-04 / 09f840b8-abe7-4734-b186-3f6cbc27f561

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-05 / 6ef4121b-b972-4d55-aacb-a2eeff269f23

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## pilot-06 / 169ebbac-1e79-4008-97c2-619cc5d02369

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `insufficient_information`. Jev selected a fallback option rather than one of the five diagnoses.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `True`.

Reference-label note only: compatible diagnoses include cori_forbes_gsd_iii, hers_gsd_vi. This note is not a model-generated differential.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| None of the above | fallback | 0 |

## eval-01 / c6d49305-d5e7-4430-8d55-02f7cd373463

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## eval-02 / e8cdb5af-fb8e-4896-916d-c658729c8389

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## eval-03 / 1dbc25ef-35ec-48e8-b302-3c13c90e9e1c

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## eval-04 / ee6285ad-1e73-4045-8481-6d9d98c4fe0d

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## eval-05 / ce37771e-b514-4905-b507-4f91708cfa23

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## eval-06 / 5e6957da-de01-4e04-8a60-282458c7fbe7

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `insufficient_information`. Jev selected a fallback option rather than one of the five diagnoses.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| None of the above | fallback | 0 |

## eval-07 / 0eef90b2-0847-42c5-92b7-f9b3fe65eb93

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `insufficient_information`. Jev selected a fallback option rather than one of the five diagnoses.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| None of the above | fallback | 0 |

## eval-08 / be3f9cb0-2aa2-4741-ae74-868753c50b28

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: None of the above** (`none_of_the_above`).

Display status: `none_of_the_above`. Jev selected a fallback option rather than one of the five diagnoses.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `none_of_the_above`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| None of the above | fallback | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| Insufficient information | fallback | 0 |

## eval-09 / ed7ee3af-6a04-4282-b6fd-1950d0c7e5a4

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `insufficient_information`. Jev selected a fallback option rather than one of the five diagnoses.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| None of the above | fallback | 0 |

## eval-10 / 1cc94351-acdd-4bc9-aed7-c386fcf5d4d2

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## eval-11 / 974d5397-c66f-4be0-80d9-c1cf4b47b2e5

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

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

## eval-12 / 23c0be45-1e6e-4d24-bf6b-0cc9cb093354

Origin: `mock_offline`. Execution: `completed`. Returned model: `jev-1.13.0`.

Elapsed seconds: `None` (not measured). Question/content/policy versions: `0.2.0` / `0.2.0` / `0.2.0`.

**Jev's option: Insufficient information** (`insufficient_information`).

Display status: `insufficient_information`. Jev selected a fallback option rather than one of the five diagnoses.

Maximum option probability: 1. Separate model confidence: 1.

Expected option: `insufficient_information`. Model option matches: `True`. Display status matches reference: `True`.

| Answer option | Kind | Model probability |
| --- | --- | ---: |
| Insufficient information | fallback | 1 |
| Von Gierke disease (GSD I) | disorder | 0 |
| Pompe disease (GSD II) | disorder | 0 |
| Cori/Forbes disease (GSD III) | disorder | 0 |
| McArdle disease (GSD V) | disorder | 0 |
| Hers disease (GSD VI) | disorder | 0 |
| None of the above | fallback | 0 |
