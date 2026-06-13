# Refah — Dataset Guide

## Overview

The Refah dataset is an individual-level administrative register compiled from multiple government sources
(civil registration, banking records, welfare organizations, tax authority, and social insurance).
Each row represents one person; members of the same household are linked via a shared `Id_Parent` identifier.
The primary use of this dataset is constructing a family-dimension table (one row per household) for welfare analysis and clustering.

---

## Source & Coverage

| Attribute | Value |
|---|---|
| Reference year | 1402 (2023–2024) |
| Primary file | `sample_1402.csv` |
| Geographic scope | National (all provinces) |
| Unit | One row per individual |
| Linkage key | `Id_Parent` (family grouping) / `id` (individual identifier) |

---

## Unit of Analysis

**One row per individual.**
All members sharing the same `Id_Parent` form one family. The household head is the member where `id == Id_Parent`.
See [`refah_family_mapping.md`](refah_family_mapping.md) for how to aggregate to family level.

---

## Files / Tables

| File | Content |
|---|---|
| `Data/Raw/sample_1402.csv` | Individual-level source data (raw column names) |
| `Data/Family_Dimension/family_dimension.csv` | Output: aggregated family-level table (72 features) |
| `Data/Clustering/clustering_dataset.csv` | Output: 18-variable clustering-ready table |

> Raw column names differ from the canonical names used in the mapping and code.
> See `RAW_TO_CANONICAL` in [`Family_Dimension/Code/build_family_dataset.py`](../Family_Dimension/Code/build_family_dataset.py).

---

## Feature Categories

### 1. Identity & Location

> Household-level attributes — taken from the household head's row.

| Canonical Field | Raw Field | Description |
|---|---|---|
| `id` | `id` | Individual unique identifier |
| `Id_Parent` | `Parent_Id` | Family head identifier (grouping key) |
| `Digits7postalcode_Dashboard` | `Dashboard_postalcode7Digits` | 7-digit postal code |
| `SabteAhval_countyname` | `SabteAhval_countyname` | County name (civil registration) |
| `SabteAhval_provincename` | `SabteAhval_provincename` | Province name (civil registration) |
| `isurban` | `isurban` | Urban / rural flag (1 = urban, 0 = rural) |
| `Decile` | `Decile` | Welfare decile (1–10) |
| `Percentile` | `Percentile` | Welfare percentile (1–100) |

---

### 2. Demographics

> Per-individual attributes.

| Canonical Field | Raw Field | Description |
|---|---|---|
| `Age` | `Age` | Age in years |
| `GenderId` | `GenderId` | Gender (1 = male, 2 = female) |

---

### 3. Health & Disability

> Binary flags and severity scores per individual.

| Canonical Field | Raw Field | Description |
|---|---|---|
| `SoeTaghzie_Has` | `Has_SoeTaghzie` | Malnutrition flag (0/1) |
| `ISBimarKhas` | `ISBimarKhas` | Chronic / special illness flag (0/1) |
| `IsMalool` | `IsMalool` | Disability flag (0/1) |
| `shedat_Malool` | `Malool_shedat` | Disability severity score |

---

### 4. Welfare & Social Support

> Binary flags indicating receipt of state support — per individual.

| Canonical Field | Raw Field | Description |
|---|---|---|
| `AfzayeshMostamari_IsBehzisti` | `IsBehzisti_AfzayeshMostamari` | Covered by Welfare Organization (Behzisti) (0/1) |
| `AfzayeshMostamari_IsKomite` | `IsKomite_AfzayeshMostamari` | Covered by Relief Committee (Komite Emdad) (0/1) |
| `AfzayeshMostamariSayer_IsKomite` | `IsKomite_AfzayeshMostamariSayer` | Covered by Relief Committee — other scheme (0/1) |
| `Edalat_Saham_Has` | `Has_Saham_Edalat` | Holds Justice Shares (Saham Edalat) (0/1) |

---

### 5. Insurance & Employment

> Per-individual flags for insurance, employment, and business status.

| Canonical Field | Raw Field | Description |
|---|---|---|
| `darman_bime_is` | `is_bime_darman` | Health insurance coverage (0/1) |
| `IsBimePardaz` | `IsBimePardaz` | Active social insurance contributor — proxy for employed (0/1) |
| `1402_ISKarmanddolat` | `ISKarmanddolat_1402` | Government employee in 1402 (0/1) |
| `Asli_IsRetired` | `IsRetired_Asli` | Primary retiree status (0/1) |
| `Tabaie_IsRetired` | `IsRetired_Tabaie` | Dependent retiree status (0/1) |
| `HasMojavezSenfi` | `HasMojavezSenfi` | Holds a trade / business license (0/1) |

---

### 6. Wealth & Assets

> Monetary values and asset counts per individual.
> ⚠ Some fields (e.g., `Daramad`, `CarsPrice`) may be stored at household level and duplicated across members — verify before summing.

| Canonical Field | Raw Field | Description | Unit |
|---|---|---|---|
| `Daramad` | `Daramad` | Registered income | IRR |
| `CarsCount` | `CarsCount` | Number of vehicles owned | Count |
| `CarsPrice` | `CarsPrice` | Total vehicle value | IRR |
| `NetPortfoValue_Bourse` | `Bourse_NetPortfoValue` | Stock market portfolio value (net) | IRR |

---

### 7. Travel (1395–1399 / 2016–2020)

> Trip counts per individual, covering five years (1395–1399).

| Canonical Field | Raw Field | Description |
|---|---|---|
| `99to95_TripCountAirNonPilgrimage` | `TripCountAirNonPilgrimage_95to99` | Air trips — non-pilgrimage |
| `99to95_TripCountAirPilgrimage` | `TripCountAirPilgrimage_95to99` | Air trips — pilgrimage (Hajj / Umrah / Mashhad) |
| `99to95_TripCountNonAirNonPilgrimage` | `TripCountNonAirNonPilgrimage_95to99` | Ground/sea trips — non-pilgrimage |
| `99to95_TripCountNonAirPilgrimage` | `TripCountNonAirPilgrimage_95to99` | Ground/sea trips — pilgrimage |

---

### 8. Financial Activity — Non-Card (1399–1402)

> Monthly averages of bank transfers per individual, from banking records.

| Canonical Field | Raw Field | Year | Description |
|---|---|---|---|
| `1399_MandehAval` | `MandehAval_1399` | 1399 | Opening account balance |
| `1399_MandehAkhar` | `MandehAkhar_1399` | 1399 | Closing account balance |
| `1400_Variz` | `Variz_1400` | 1400 | Deposits |
| `1400_MandehAval` | `MandehAval_1400` | 1400 | Opening account balance |
| `1400_MandehAkhar` | `MandehAkhar_1400` | 1400 | Closing account balance |
| `1401_CardBeCardPerMonth` | `CardBeCardPerMonth_1401` | 1401 | Card-to-card transfers per month |
| `1401_PayaPerMonth` | `PayaPerMonth_1401` | 1401 | PAYA interbank transfers per month |
| `1401_SatnaPerMonth` | `SatnaPerMonth_1401` | 1401 | SATNA (large-value) transfers per month |
| `1402_CardBeCardPerMonth` | `CardBeCardPerMonth_1402` | 1402 | Card-to-card transfers per month |
| `1402_PayaPerMonth` | `PayaPerMonth_1402` | 1402 | PAYA interbank transfers per month |
| `1402_SatnaPerMonth` | `SatnaPerMonth_1402` | 1402 | SATNA (large-value) transfers per month |

> No non-card financial data exists for 1398.

---

### 9. Financial Activity — Card Spending (1398–1402)

> Monthly average card (POS/online) spending per individual.

| Canonical Field | Raw Field | Year |
|---|---|---|
| `1398_CardPerMonth` | `CardPerMonth_1398` | 1398 |
| `1399_CardPerMonth` | `CardPerMonth_1399` | 1399 |
| `1400_CardPerMonth` | `CardPerMonth_1400` | 1400 |
| `1401_CardPerMonth` | `CardPerMonth_1401` | 1401 |
| `1402_CardPerMonth` | `CardPerMonth_1402` | 1402 |

---

## Notes & Caveats

- **Raw vs. canonical names:** The source CSV uses raw names (right column above). The pipeline renames them to canonical names on load — always use canonical names in downstream code.
- **Household-level fields duplicated per row:** `Daramad` and `CarsPrice` may contain household totals repeated for every member. Check whether all members of a family share the exact same value before deciding whether to `SUM` or `MAX` when aggregating.
- **Financial coverage gaps:** Non-card financial data starts in 1399. Card spend starts in 1398. Do not compare 1398 totals to later years on the non-card dimension.
- **Travel data period:** Trip counts cover 1395–1399 (solar) / 2016–2020. There is no travel data for 1400–1402.
- **Welfare decile:** Assigned at household level and stored on every member row. Take the head's value — do not average.
- **Single-person households:** Valid — head is the only member. `Id_Parent == id` for these rows.
