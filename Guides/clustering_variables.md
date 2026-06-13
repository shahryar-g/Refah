# Family Clustering — Variable Selection & Construction Guide

## Overview

This document defines the exact 19 variables to use for family clustering.
For each variable: where it comes from, how to build it, and what type it is for Gower distance.

**Grouping key:** `Id_Parent`
**Unit of analysis:** One row per family

---

## Variable List

| # | Variable | Source | Build Rule | Type |
|---|---|---|---|---|
| 1 | `province` | `SabteAhval_provincename` | Head's value | Categorical |
| 2 | `county` | `SabteAhval_countyname` | Head's value | Categorical |
| 3 | `is_urban` | `isurban` | Head's value | Binary |
| 4 | `family_size` | `id` | `COUNT(id)` per `Id_Parent` | Discrete numeric |
| 5 | `num_children` | `Age` | `COUNT` where `Age < 18` | Discrete numeric |
| 6 | `num_elderly` | `Age` | `COUNT` where `Age >= 60` | Discrete numeric |
| 7 | `dependency_ratio` | `Age` | `(num_children + num_elderly) / family_size` | Continuous [0,1] |
| 8 | `head_age` | `Age` | Value where `id == Id_Parent` | Continuous numeric |
| 9 | `total_income` | `Daramad` | `SUM(Daramad)` per family | Continuous, skewed |
| 10 | `total_cars` | `CarsCount` | `SUM(CarsCount)` per family | Discrete numeric |
| 11 | `total_stock_portfolio` | `NetPortfoValue_Bourse` | `SUM(NetPortfoValue_Bourse)` per family | Continuous, skewed |
| 12 | `card_spend_1402_total` | `1402_CardPerMonth` | `SUM(1402_CardPerMonth)` per family | Continuous, skewed |
| 13 | `financial_1402_total` | `1402_CardBeCardPerMonth`, `1402_PayaPerMonth`, `1402_SatnaPerMonth` | `SUM` of all three fields per family | Continuous, skewed |
| 14 | `total_trips` | `99to95_TripCountAirNonPilgrimage`, `99to95_TripCountAirPilgrimage`, `99to95_TripCountNonAirNonPilgrimage`, `99to95_TripCountNonAirPilgrimage` | `SUM` of all four trip fields per family | Discrete numeric |
| 15 | `any_chronic_illness` | `ISBimarKhas` | `MAX(ISBimarKhas)` per family | Binary |
| 16 | `any_disability` | `IsMalool` | `MAX(IsMalool)` per family | Binary |
| 17 | `any_welfare_support` | `AfzayeshMostamari_IsBehzisti`, `AfzayeshMostamari_IsKomite`, `AfzayeshMostamariSayer_IsKomite` | `MAX` of all three fields per family | Binary |
| 18 | `insurance_coverage_rate` | `darman_bime_is` | `SUM(darman_bime_is) / family_size` | Continuous [0,1] |
| 19 | `employment_ratio` | `IsBimePardaz`, `1402_ISKarmanddolat` | `COUNT` where `IsBimePardaz == 1 OR 1402_ISKarmanddolat == 1`, divided by `family_size` | Continuous [0,1] |

---

## Construction Detail per Variable

### 1. `province`
```
source:   SabteAhval_provincename
filter:   row where id == Id_Parent (head only)
type:     categorical — Gower treats as match / no-match
```

### 2. `county`
```
source:   SabteAhval_countyname
filter:   row where id == Id_Parent (head only)
type:     categorical — Gower treats as match / no-match
note:     more granular than province; both kept because
          two families in the same county share province too —
          they get double proximity signal which is intentional
```

### 3. `is_urban`
```
source:   isurban
filter:   row where id == Id_Parent (head only)
type:     binary (0 = rural, 1 = urban)
```

### 4. `family_size`
```
source:   id
rule:     COUNT(id) grouped by Id_Parent
type:     discrete numeric
note:     minimum value is 1 (single-person household)
```

### 5. `num_children`
```
source:   Age
rule:     COUNT of members where Age < 18, grouped by Id_Parent
type:     discrete numeric
```

### 6. `num_elderly`
```
source:   Age
rule:     COUNT of members where Age >= 60, grouped by Id_Parent
type:     discrete numeric
```

### 7. `dependency_ratio`
```
source:   num_children, num_elderly, family_size (derived)
rule:     (num_children + num_elderly) / family_size
type:     continuous [0, 1]
note:     if family_size == 1 and member is elderly, ratio = 1.0
          if family_size == 1 and member is adult, ratio = 0.0
```

### 8. `head_age`
```
source:   Age
filter:   row where id == Id_Parent (head only)
type:     continuous numeric
note:     proxy for family life stage
          (young head = early career, older head = established or retired)
```

### 9. `total_income`
```
source:   Daramad
rule:     SUM(Daramad) grouped by Id_Parent
type:     continuous, right-skewed (apply log1p before clustering)
warning:  verify Daramad is per-person not per-household before summing.
          if all members of a family share the exact same Daramad value,
          use MAX instead of SUM
```

### 10. `total_cars`
```
source:   CarsCount
rule:     SUM(CarsCount) grouped by Id_Parent
type:     discrete numeric
warning:  same household-level duplication check as Daramad
```

### 11. `total_stock_portfolio`
```
source:   NetPortfoValue_Bourse
rule:     SUM(NetPortfoValue_Bourse) grouped by Id_Parent
type:     continuous, right-skewed (apply log1p before clustering)
note:     will be 0 for most families — that zero mass is itself
          a meaningful cluster signal (has investments vs does not)
```

### 12. `card_spend_1402_total`
```
source:   1402_CardPerMonth
rule:     SUM(1402_CardPerMonth) grouped by Id_Parent
type:     continuous, right-skewed (apply log1p before clustering)
note:     most recent year — best proxy for current consumption level
```

### 13. `financial_1402_total`
```
source:   1402_CardBeCardPerMonth, 1402_PayaPerMonth, 1402_SatnaPerMonth
rule:     SUM of all three fields per member, then SUM across family
          i.e. for each member: temp = CardBeCard + Paya + Satna
               then family total = SUM(temp) grouped by Id_Parent
type:     continuous, right-skewed (apply log1p before clustering)
note:     captures non-card financial flows — larger transfers,
          interbank settlements — signals higher financial activity
```

### 14. `total_trips`
```
source:   99to95_TripCountAirNonPilgrimage
          99to95_TripCountAirPilgrimage
          99to95_TripCountNonAirNonPilgrimage
          99to95_TripCountNonAirPilgrimage
rule:     for each member: temp = sum of all four fields
          then family total = SUM(temp) grouped by Id_Parent
type:     discrete numeric
note:     covers 1395–1399; sparse for lower-income families
          which is itself a useful signal
```

### 15. `any_chronic_illness`
```
source:   ISBimarKhas
rule:     MAX(ISBimarKhas) grouped by Id_Parent
type:     binary (0/1)
note:     1 if ANY family member has a chronic illness
```

### 16. `any_disability`
```
source:   IsMalool
rule:     MAX(IsMalool) grouped by Id_Parent
type:     binary (0/1)
note:     1 if ANY family member has a disability
```

### 17. `any_welfare_support`
```
source:   AfzayeshMostamari_IsBehzisti
          AfzayeshMostamari_IsKomite
          AfzayeshMostamariSayer_IsKomite
rule:     for each member: temp = MAX of all three fields (1 if any is 1)
          then family flag = MAX(temp) grouped by Id_Parent
type:     binary (0/1)
note:     1 if ANY member receives ANY form of state welfare support
```

### 18. `insurance_coverage_rate`
```
source:   darman_bime_is
rule:     SUM(darman_bime_is) / COUNT(id) grouped by Id_Parent
type:     continuous [0, 1]
note:     0.0 = no one insured, 1.0 = everyone insured
          more informative than a simple binary for clustering
```

### 19. `employment_ratio`
```
source:   IsBimePardaz, 1402_ISKarmanddolat
rule:     for each member: is_working = 1 if IsBimePardaz == 1
                                           OR 1402_ISKarmanddolat == 1
                                        else 0
          then: SUM(is_working) / COUNT(id) grouped by Id_Parent
type:     continuous [0, 1]
note:     0.0 = no working members, 1.0 = all members working
          single-person retired household will be 0.0
```

---

## Pre-Clustering Transformations

### Skewed financial fields → apply log1p
The following fields are heavily right-skewed (most families near zero,
few families with very large values). Apply `log1p(x)` before clustering:

```
total_income
total_stock_portfolio
card_spend_1402_total
financial_1402_total
```

### Categorical encoding for Gower
`province` and `county` must be passed as type `object` (string) in Python.
Gower distance handles them natively as match/no-match.
Do NOT label-encode them to integers — Gower would treat integers as ordinal.

### Missing values
| Field | Recommended fill |
|---|---|
| Financial fields (nulls = no activity) | Fill with `0` |
| `any_chronic_illness`, `any_disability`, `any_welfare_support` | Fill with `0` |
| `total_trips` | Fill with `0` |
| `head_age` | Fill with median age of heads |
| `insurance_coverage_rate`, `employment_ratio` | Fill with `0` |
| `province`, `county` | Flag as `"unknown"` — do not drop |

---

## Feature Type Summary for Gower Distance

| Type | Variables |
|---|---|
| Categorical | `province`, `county` |
| Binary | `is_urban`, `any_chronic_illness`, `any_disability`, `any_welfare_support` |
| Discrete numeric | `family_size`, `num_children`, `num_elderly`, `total_cars`, `total_trips` |
| Continuous numeric | `head_age`, `total_income`*, `total_stock_portfolio`*, `card_spend_1402_total`*, `financial_1402_total`* |
| Continuous [0,1] | `dependency_ratio`, `insurance_coverage_rate`, `employment_ratio` |

*after log1p transformation

---

## Variables Explicitly Excluded

| Variable | Reason for exclusion |
|---|---|
| `welfare_decile`, `welfare_percentile` | Pre-computed welfare rank — using it clusters by outcome not characteristics |
| `postal_code_5`, `postal_code_7` | Replaced by `province` + `county` |
| `family_id` | Identifier, not a feature |
| `total_cars_value` | Highly correlated with `total_cars` |
| `income_per_capita` | Derived from `total_income` + `family_size`, adds multicollinearity |
| `num_adults`, `age_mean`, `age_max`, `age_min` | Captured sufficiently by `family_size`, `num_children`, `num_elderly`, `head_age` |
| `num_male`, `num_female` | Low clustering signal for welfare profiling |
| `any_behzisti_support`, `any_komite_support` separately | Collapsed into `any_welfare_support` |
| `any_health_insured`, `all_health_insured`, `num_health_insured` | Replaced by `insurance_coverage_rate` |
| `any_government_employee` | Captured within `employment_ratio` |
| `num_disabled`, `max_disability_severity` | `any_disability` sufficient for clustering level |
| `card_spend_1398–1401` | 1402 is most recent; older years add multicollinearity |
| `financial_1399–1401` | Same reason |
| `family_type` | Rule-based label derived post-hoc, not a clustering input |