# Individual → Family Data Mapping Guide

## Overview

Each individual row has an `id` and an `Id_Parent`. All members sharing the same `Id_Parent`
form one family unit. The household head is the member whose `id == Id_Parent`.

**Grouping key:** `Id_Parent`

---

## Step 0 — Always Derive First

Before any aggregation, compute these two helper columns on the individual table:

| Derived Column | Logic |
|---|---|
| `is_head` | `1` if `id == Id_Parent`, else `0` |
| `family_size` | `COUNT(id)` grouped by `Id_Parent` |

---

## Step 1 — Identity & Location Fields
> Take directly from the **household head** (`is_head == 1`). These are household-level attributes, not personal ones.

| # | Source Field | Family Field | Rule |
|---|---|---|---|
| 1 | `Id_Parent` | `family_id` | Use as the family's unique identifier |
| 4 | `Digits7postalcode_Dashboard` | `postal_code_7` | Head's value |
| 4 | `Digits7postalcode_Dashboard` | `postal_code_5` | First 5 digits of postal code |
| 5 | `SabteAhval_countyname` | `county` | Head's value |
| 5 | `SabteAhval_countyname` | `county_code` | Numeric encoding of county |
| 6 | `SabteAhval_provincename` | `province` | Head's value |
| 6 | `SabteAhval_provincename` | `province_code` | Numeric encoding of province |
| 7 | `isurban` | `is_urban` | Head's value |
| 8 | `Decile` | `welfare_decile` | Head's value |
| 9 | `Percentile` | `welfare_percentile` | Head's value |
| 3 | `GenderId` | `head_gender` | Head's value |
| 2 | `Age` | `head_age` | Head's value |

---

## Step 2 — Family Size & Composition
> Derived from aggregating all members.

| Family Field | Source Field(s) | Rule | Notes |
|---|---|---|---|
| `family_size` | `id` | `COUNT(id)` per `Id_Parent` | Includes head |
| `num_children` | `Age` | `COUNT` where `Age < 18` | |
| `num_adults` | `Age` | `COUNT` where `18 <= Age <= 59` | |
| `num_elderly` | `Age` | `COUNT` where `Age >= 60` | |
| `num_male` | `GenderId` | `COUNT` where `GenderId == male` | |
| `num_female` | `GenderId` | `COUNT` where `GenderId == female` | |
| `age_mean` | `Age` | `MEAN(Age)` | Average family age |
| `age_max` | `Age` | `MAX(Age)` | Oldest member |
| `age_min` | `Age` | `MIN(Age)` | Youngest member |
| `dependency_ratio` | `Age` | `(num_children + num_elderly) / family_size` | Higher = more dependents |

---

## Step 3 — Income & Wealth Fields
> Sum across all members. Each member's registered income and assets are individual, so summing gives the family total.

| # | Source Field | Family Field | Rule | Notes |
|---|---|---|---|---|
| 41 | `Daramad` | `total_income` | `SUM` | Total registered family income (IRR) |
| 39 | `CarsCount` | `total_cars` | `SUM` | Total number of vehicles |
| 40 | `CarsPrice` | `total_cars_value` | `SUM` | Total vehicle value (IRR) |
| 42 | `NetPortfoValue_Bourse` | `total_stock_portfolio` | `SUM` | Total stock market portfolio (IRR) |
| — | `Daramad` | `income_per_capita` | `SUM(Daramad) / family_size` | Welfare-normalized income |

> ⚠️ **Check before summing:** If CarsPrice and Daramad appear identical across members of the same household, they may already be household-level figures duplicated per row — in that case use `MAX` instead of `SUM`.

---

## Step 4 — Yearly Financial Totals
> Collapse all non-card financial characteristics into one family-level total per year.

| Family Field | Source Field(s) | Rule | Notes |
|---|---|---|---|
| `financial_1398_total` | — | `0` | No non-card financial component in 1398 |
| `financial_1399_total` | `1399_MandehAval`, `1399_MandehAkhar` | `SUM` | Total 1399 non-card financial activity |
| `financial_1400_total` | `1400_Variz`, `1400_MandehAval`, `1400_MandehAkhar` | `SUM` | Total 1400 non-card financial activity |
| `financial_1401_total` | `1401_CardBeCardPerMonth`, `1401_PayaPerMonth`, `1401_SatnaPerMonth` | `SUM` | Total 1401 non-card financial activity |
| `financial_1402_total` | `1402_CardBeCardPerMonth`, `1402_PayaPerMonth`, `1402_SatnaPerMonth` | `SUM` | Total 1402 non-card financial activity |

## Step 4b — Card Spend Totals
> Keep monthly card spend separate from the main financial totals.

| Family Field | Source Field(s) | Rule | Notes |
|---|---|---|---|
| `card_spend_1398_total` | `1398_CardPerMonth` | `SUM` | 1398 card spend total |
| `card_spend_1399_total` | `1399_CardPerMonth` | `SUM` | 1399 card spend total |
| `card_spend_1400_total` | `1400_CardPerMonth` | `SUM` | 1400 card spend total |
| `card_spend_1401_total` | `1401_CardPerMonth` | `SUM` | 1401 card spend total |
| `card_spend_1402_total` | `1402_CardPerMonth` | `SUM` | 1402 card spend total |

> These totals replace the earlier per-transaction financial outputs in the family dataset.

---

## Step 5 — Travel Fields
> Sum across all members. Travel reflects the family's overall mobility and economic activity.

| # | Source Field | Family Field | Rule |
|---|---|---|---|
| 24 | `99to95_TripCountAirNonPilgrimage` | `air_trips_nonpilgrimage` | `SUM` |
| 25 | `99to95_TripCountAirPilgrimage` | `air_trips_pilgrimage` | `SUM` |
| 26 | `99to95_TripCountNonAirNonPilgrimage` | `nonair_trips_nonpilgrimage` | `SUM` |
| 27 | `99to95_TripCountNonAirPilgrimage` | `nonair_trips_pilgrimage` | `SUM` |

**Derived travel fields (recommended):**

| Family Field | Rule |
|---|---|
| `total_trips` | Sum of all four trip count columns |
| `total_air_trips` | `air_trips_nonpilgrimage + air_trips_pilgrimage` |
| `pilgrimage_ratio` | `(air_trips_pilgrimage + nonair_trips_pilgrimage) / total_trips` (handle zero division) |

---

## Step 6 — Health & Disability Fields
> Use `MAX` (i.e., flag the family if **any** member has the condition). Also count affected members.

| # | Source Field | Family Field | Rule | Notes |
|---|---|---|---|---|
| 10 | `SoeTaghzie_Has` | `any_malnutrition` | `MAX` | 1 if any member has malnutrition |
| 13 | `ISBimarKhas` | `any_chronic_illness` | `MAX` | 1 if any member has a chronic illness |
| 14 | `IsMalool` | `any_disability` | `MAX` | 1 if any member has a disability |
| 14 | `IsMalool` | `num_disabled` | `SUM` | Number of disabled members |
| 15 | `shedat_Malool` | `max_disability_severity` | `MAX` | Worst disability severity in family |
| 15 | `shedat_Malool` | `mean_disability_severity` | `MEAN` (among disabled only) | Average severity where `IsMalool == 1` |

---

## Step 7 — Welfare & Social Support Fields
> Use `MAX` — a family is considered covered if at least one member receives support.

| # | Source Field | Family Field | Rule | Notes |
|---|---|---|---|---|
| 16 | `AfzayeshMostamari_IsBehzisti` | `any_behzisti_support` | `MAX` | Covered by Welfare Organization |
| 17 | `AfzayeshMostamari_IsKomite` | `any_komite_support` | `MAX` | Covered by Relief Committee |
| 18 | `AfzayeshMostamariSayer_IsKomite` | `any_komite_support_other` | `MAX` | Covered by Relief Committee (other scheme) |
| — | — | `any_welfare_support` | `MAX(any_behzisti_support, any_komite_support, any_komite_support_other)` | Any form of social safety net |
| 11 | `Edalat_Saham_Has` | `any_edalat_shares` | `MAX` | Any member holds Justice Shares |
| 11 | `Edalat_Saham_Has` | `num_edalat_shares` | `SUM` | Count of members holding Justice Shares |

---

## Step 8 — Insurance Fields
> Two perspectives: does anyone have insurance? Is everyone covered?

| # | Source Field | Family Field | Rule | Notes |
|---|---|---|---|---|
| 19 | `darman_bime_is` | `any_health_insured` | `MAX` | 1 if any member has health insurance |
| 19 | `darman_bime_is` | `all_health_insured` | `MIN` | 1 only if all members are insured |
| 19 | `darman_bime_is` | `num_health_insured` | `SUM` | Count of insured members |
| 19 | `darman_bime_is` | `insurance_coverage_rate` | `SUM / family_size` | Share of family with insurance |
| 20 | `IsBimePardaz` | `any_insurance_contributor` | `MAX` | Any member actively paying insurance |
| 20 | `IsBimePardaz` | `num_insurance_contributors` | `SUM` | Count of contributing members |

---

## Step 9 — Employment & Retirement Fields
> Count employed/retired members; flag family types.

| # | Source Field | Family Field | Rule | Notes |
|---|---|---|---|---|
| 21 | `1402_ISKarmanddolat` | `any_government_employee` | `MAX` | Any member is a government employee |
| 21 | `1402_ISKarmanddolat` | `num_government_employees` | `SUM` | Count of government employees |
| 22 | `Asli_IsRetired` | `any_primary_retired` | `MAX` | Any member is a primary retiree |
| 22 | `Asli_IsRetired` | `num_primary_retired` | `SUM` | Count of primary retirees |
| 23 | `Tabaie_IsRetired` | `any_dependent_retired` | `MAX` | Any member is a dependent retiree |
| 23 | `Tabaie_IsRetired` | `num_dependent_retired` | `SUM` | Count of dependent retirees |
| 12 | `HasMojavezSenfi` | `any_business_license` | `MAX` | Any member has a trade/business license |
| 12 | `HasMojavezSenfi` | `num_business_licenses` | `SUM` | Count of members with licenses |

**Derived employment fields (recommended):**

| Family Field | Rule | Notes |
|---|---|---|
| `num_working_adults` | `SUM` where `IsBimePardaz == 1` OR `1402_ISKarmanddolat == 1` | Proxy for employed adults |
| `employment_ratio` | `num_working_adults / family_size` | Share of family that is employed |
| `family_type` | Rule-based label (see below) | Characterize the household |

**Family type classification rule:**

```
if any_government_employee == 1            → "government_employee_family"
elif any_primary_retired == 1              → "retired_family"
elif any_business_license == 1             → "self_employed_family"
elif any_welfare_support == 1              → "welfare_supported_family"
elif num_working_adults > 0                → "private_sector_family"
else                                       → "unclassified"
```

---

## Final Family Feature Summary

| Category | # of Fields |
|---|---|
| Identity & Location | 12 |
| Family Size & Composition | 10 |
| Income & Wealth | 5 |
| Yearly Financial Totals | 5 |
| Card Spend Totals | 5 |
| Travel | 7 |
| Health & Disability | 6 |
| Welfare & Social Support | 6 |
| Insurance | 6 |
| Employment & Retirement | 10 |
| **Total** | **72 family-level features** |

---

## Aggregation Reference Card

| Data type | Aggregation | When to use |
|---|---|---|
| Binary — any member | `MAX` | Health flags, welfare support, insurance |
| Binary — all members | `MIN` | Full-family coverage checks |
| Count | `SUM` | Number of cars, trips, disabled members |
| Numeric — individual | `SUM` | Income, non-card yearly financial totals, card spend totals |
| Numeric — shared | `MAX` or head's value | Location, decile, postal code |
| Categorical | Head's value | Province, county, urban/rural |
| Age | `MEAN`, `MIN`, `MAX` | Family age profile |
| Severity/ordinal | `MAX` + `MEAN` | Disability severity |

---

## Notes & Warnings

- **Single-person households** (`family_size == 1`): valid — head is the only member. All fields map directly.
- **Missing `Id_Parent`**: treat as solo household; assign `family_id = id`.
- **Duplicate financials**: the yearly financial totals are computed by summing the family-level rows across the component fields listed in Step 4. If a new source file duplicates household-level financial values across members, verify before changing the aggregation rule.
- **Welfare decile**: do **not** average across members — take the head's decile. Averaging deciles is statistically meaningless here since it is a household-assigned rank.
- **Year coverage**: financial fields span 1398–1402 (2019–2023), with card spend exported separately from the annual non-card financial totals.
