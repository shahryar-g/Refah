# HEIS 1402 — Dataset Guide

## Overview

The Household Expenditure and Income Survey (HEIS / طرح آمارگیری هزینه و درامد خانوار) is Iran's national household survey
conducted annually by the Statistical Centre of Iran (SCI). The 1402 edition covers both rural (`R`) and urban (`U`) households.
It is the primary public source for household-level consumption, income, housing conditions, and demographic composition in Iran.

---

## Source & Coverage

| Attribute | Value |
|---|---|
| Survey year | 1402 (2023–2024) |
| Conducted by | Statistical Centre of Iran (SCI) |
| Geographic scope | All provinces — rural and urban |
| Sample design | Stratified multi-stage cluster sampling |
| Weighting variable | `weight` (household-level expansion weight) |

---

## Unit of Analysis

**One row per record within each questionnaire section.**
The survey is split into multiple files (parts and sections); the household `Address` field is the join key across all files.
Part 1 (social characteristics) has one row per household member. All other parts have one row per item/transaction or per member.

---

## Files / Tables

| File | Content |
|---|---|
| `Data1402R` / `Data1402U` | Questionnaire metadata (rural / urban) |
| `1P1402R` / `1P1402U` | Part 1 — Social characteristics of household members |
| `2P1402R` / `2P1402U` | Part 2 — Housing and dwelling characteristics |
| `P3S01` – `P3S14` (R & U) | Part 3 — Expenditure by category (14 sections) |
| `P4S1` – `P4S4` (R & U) | Part 4 — Income by source (4 sections) |

---

## Feature Categories

### 1. Questionnaire Metadata (`Data1402R` / `Data1402U`)

> One row per household. Administrative fields used for sampling and weighting.

| Field | Description |
|---|---|
| `Address` | Household address (join key across all files) |
| `Fasl` | Survey season (quarter) |
| `weight` | Household expansion weight |
| `NoeKhn` | Household type |
| `Takmil` | Questionnaire completion status — main household |
| `Jaygozin` | Questionnaire completion status — substitute household |
| `BlkAbdJaygozin` | Block or village of substitute household |
| `RadifJaygozin` | Row number of substitute household |

---

### 2. Social Characteristics of Household Members (`1P1402R` / `1P1402U`)

> One row per household member. Demographic and socioeconomic status of each individual.

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Member row number within household |
| `DyCol03` | Relationship to household head |
| `DyCol04` | Gender |
| `DyCol05` | Age |
| `DyCol06` | Literacy status |
| `DyCol07` | Currently enrolled in education? |
| `DyCol08` | Education level / degree |
| `DyCol09` | Activity status (employed / unemployed / inactive) |
| `DyCol10` | Marital status |

---

### 3. Housing & Dwelling Characteristics (`2P1402R` / `2P1402U`)

> One row per household.

#### 3a. Dwelling Structure

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol001` | Dwelling type |
| `DyCol002` | Dwelling type — other (with name) |
| `DyCol01` | Tenure type (owner / renter / other) |
| `DyCol03` | Number of rooms available to household |
| `DyCol04` | Floor area (sq meters) |
| `DyCol05` | Building structure type |
| `DyCol06` | Main construction material |

#### 3b. Durable Goods Owned (binary)

| Field | Asset |
|---|---|
| `DyCol07` | Personal car |
| `DyCol08` | Motorcycle |
| `DyCol09` | Bicycle |
| `DyCol10` | Radio |
| `DyCol11` | Radio / cassette / audio player |
| `DyCol12` | Black & white TV |
| `DyCol13` | Color TV |
| `DyCol14` | Video / VCD / DVD player |
| `DyCol15` | Computer |
| `DyCol16` | Mobile phone (non-business) |
| `DyCol17` | Freezer |
| `DyCol18` | Refrigerator |
| `DyCol19` | Fridge-freezer |
| `DyCol20` | Gas stove |
| `DyCol21` | Vacuum cleaner |
| `DyCol22` | Washing machine |
| `DyCol23` | Sewing machine |
| `DyCol24` | Fan |
| `DyCol25` | Portable water cooler (evaporative) |
| `DyCol26` | Portable AC (gas) |
| `DyCol27` | Dishwasher |
| `DyCol29` | None of the above |

#### 3c. Utilities & Infrastructure (binary)

| Field | Utility |
|---|---|
| `DyCol30` | Piped water |
| `DyCol31` | Electricity |
| `DyCol32` | Piped gas |
| `DyCol33` | Landline telephone |
| `DyCol34` | Internet access |
| `DyCol35` | Bathroom |
| `DyCol36` | Kitchen |
| `DyCol37` | Fixed water cooler |
| `DyCol38` | Central cooling system |
| `DyCol39` | Central heating system |
| `DyCol40` | Boiler package |
| `DyCol41` | Fixed AC (gas) |
| `DyCol42` | Urban sewage network |
| `DyCol42_14` | Elevator |

#### 3d. Fuel Types (categorical)

| Field | Description |
|---|---|
| `DyCol43` | Main fuel type for cooking |
| `DyCol44` | Main fuel type for heating |
| `DyCol45` | Main fuel type for hot water |

---

### 4. Expenditure — Part 3 (14 sections)

> One row per item purchased / consumed. Joined to household via `Address`.

#### 4a. Food, Tobacco & Unclassified Beverages (Sections 1 & 2)

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Item code (commodity code) |
| `DyCol02` | Acquisition method (purchased / own-produced / in-kind) |
| `DyCol03` | Quantity in grams |
| `DyCol04` | Quantity in kilograms |
| `DyCol05` | Unit price (IRR) |
| `DyCol06` | Total value (IRR) |

#### 4b. Non-Food Expenditure (Sections 3, 5–9, 11–12)

Clothing, transportation, health, education, recreation, communication, personal goods, miscellaneous.

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Item code |
| `DyCol02` | Acquisition method |
| `DyCol03` | Value (IRR) |

#### 4c. Housing Expenses (Section 4)

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Item code |
| `DyCol02` | Deposit / mortgage amount |
| `DyCol03` | Acquisition method |
| `DyCol04` | Value (IRR) |

#### 4d. Insurance & Loan Payments (Section 13)

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Item code |
| `DyCol02` | Number of insured persons / loan amount |
| `DyCol03` | Loan source |
| `DyCol04` | Acquisition method |
| `DyCol05` | Purchase or expense amount |
| `DyCol06` | Second-hand sale proceeds |

#### 4e. Household Investment — Last 12 Months (Section 14)

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Item code |
| `DyCol02` | Acquisition method |
| `DyCol03` | Purchase or expense amount |
| `DyCol04` | Second-hand sale proceeds |

---

### 5. Income — Part 4 (4 sections)

> One row per employed member (Sections 1–2) or per household (Sections 3–4).

#### 5a. Wage & Salary Employment (Section 1)

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Member row number |
| `DyCol02` | Currently employed? |
| `DyCol03` | Occupation code |
| `DyCol04` | Workplace activity code |
| `DyCol05` | Sector (1 = public, 2 = cooperative, 3 = private) |
| `DyCol06` | Working hours per day |
| `DyCol07` | Working days per week |
| `DyCol08` | Total gross income — last month (IRR) |
| `DyCol09` | Total gross income — last 12 months (IRR) |
| `DyCol10` | Regular wages & benefits — last month (IRR) |
| `DyCol11` | Regular wages & benefits — last 12 months (IRR) |
| `DyCol12` | Irregular bonuses — last month (IRR) |
| `DyCol13` | Irregular bonuses — last 12 months (IRR) |
| `DyCol14` | Net income — last month (IRR) |
| `DyCol15` | Net income — last 12 months (IRR) |

#### 5b. Self-Employment Income (Section 2)

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Member row number |
| `DyCol02` | Currently employed? |
| `DyCol03` | Occupation code |
| `DyCol04` | Workplace activity code |
| `DyCol05` | Employment type (1 = employer, 2 = own-account, 3 = unpaid family) |
| `DyCol06` | Sector (1 = agriculture, 2 = non-agriculture) |
| `DyCol07` | Working hours per day |
| `DyCol08` | Working days per week |
| `DyCol09` | Wages and benefits received |
| `DyCol10` | Input costs: seeds, water, fertilizer (IRR) |
| `DyCol11` | Non-durable tools & equipment (IRR) |
| `DyCol12` | Job wages paid out (IRR) |
| `DyCol13` | Business taxes paid (IRR) |
| `DyCol14` | Gross sales / receipts (IRR) |
| `DyCol15` | Net income (IRR) |

#### 5c. Miscellaneous Household Income (Section 3)

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Member row number |
| `DyCol03` | Pension, disability allowance, or readiness pay (IRR) |
| `DyCol04` | Rental income from business premises, land, garden (IRR) |
| `DyCol05` | Income from savings accounts, fixed deposits, stocks (IRR) |
| `DyCol06` | Educational grants and scholarships (IRR) |
| `DyCol07` | Income from selling handicrafts / cottage industry (IRR) |
| `DyCol08` | Transfers received from other households (IRR) |

#### 5d. Government Subsidies & Cash Transfers (Section 4, Column 9)

| Field | Description |
|---|---|
| `Address` | Household address |
| `DyCol01` | Member row number |
| `DyCol03` | Number of household members who received subsidy |
| `DyCol04` | Number of months subsidy was received |
| `DyCol05` | Total subsidy amount received (IRR) |

---

## Notes & Caveats

- **Rural vs. urban split:** Each part comes in two variants — `R` (rural) and `U` (urban). Stack them vertically after joining on `Address`.
- **Field naming convention:** Within each section, fields follow `DyColNN` numbering. The same column number in different sections refers to different variables — always check the section context.
- **Expenditure item codes:** `DyCol01` in Part 3 is a commodity classification code (COICOP-based). A separate code book is required to decode it.
- **Weighting:** Analysis at the national or provincial level must apply `weight` from the metadata file. Unweighted results represent only the sample.
- **Income coverage:** Part 4 covers only monetary income. In-kind income (own-production consumed at home) is partially captured via the acquisition method flag (`DyCol02`) in Part 3.
- **Reference periods:** Section 1 income figures are available for both last month and last 12 months. The 12-month figure is preferred for annual comparisons.
