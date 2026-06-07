# Iranian Welfare Databank — Variable Metadata

**Source:** Iranian Welfare Database ([refahdb.mcls.gov.ir](https://refahdb.mcls.gov.ir))

The data is compiled from multiple government organizations including the Social Security Organization, Health Insurance Organization, National Pension Fund, Rural and Nomadic Social Insurance Fund, Welfare Organization, Imam Khomeini Relief Committee, Civil Registration Organization, Real Estate Union, Technical and Vocational Training Organization, Ministry of Education, Ministry of Science, Police, Central Bank, Targeted Subsidies Organization, Tax Affairs Organization, Ministry of Health, Martyrs and Veterans Foundation, Post Company, and the Ministry of Welfare.

The Ministry of Welfare publishes a public 2% sample of this data (with confidential information removed) for researchers.

---

## Variable Dictionary

| # | Variable Name | Description | Type |
|---|---------------|-------------|------|
| 0 | `id` | Individual identifier | ID |
| 1 | `Id_Parent` | Household head identifier | ID |
| 2 | `Age` | Age | Numeric |
| 3 | `GenderId` | Gender | Categorical |
| 4 | `Digits7postalcode_Dashboard` | First 7 digits of postal code | Categorical |
| 5 | `SabteAhval_countyname` | County (city/district) name | Categorical |
| 6 | `SabteAhval_provincename` | Province name | Categorical |
| 7 | `isurban` | Urban / Rural | Binary |
| 8 | `Decile` | Welfare decile (1–10) | Ordinal |
| 9 | `Percentile` | Welfare percentile (1–100) | Ordinal |
| 10 | `SoeTaghzie_Has` | Has malnutrition | Binary |
| 11 | `Edalat_Saham_Has` | Has Justice Shares (Edalat stock) | Binary |
| 12 | `HasMojavezSenfi` | Has a trade/business license | Binary |
| 13 | `ISBimarKhas` | Has a special/chronic illness | Binary |
| 14 | `IsMalool` | Has a disability | Binary |
| 15 | `shedat_Malool` | Disability severity | Ordinal |
| 16 | `AfzayeshMostamari_IsBehzisti` | Covered by Welfare Organization | Binary |
| 17 | `AfzayeshMostamari_IsKomite` | Covered by Imam Khomeini Relief Committee | Binary |
| 18 | `AfzayeshMostamariSayer_IsKomite` | Covered by Relief Committee (other) | Binary |
| 19 | `darman_bime_is` | Has health insurance | Binary |
| 20 | `IsBimePardaz` | Is an insurance payer (contributor) | Binary |
| 21 | `1402_ISKarmanddolat` | Is a government employee (1402 / 2023) | Binary |
| 22 | `Asli_IsRetired` | Primary retiree | Binary |
| 23 | `Tabaie_IsRetired` | Dependent retiree | Binary |
| 24 | `99to95_TripCountAirNonPilgrimage` | Number of non-pilgrimage air trips (1395–1399) | Numeric |
| 25 | `99to95_TripCountAirPilgrimage` | Number of pilgrimage air trips (1395–1399) | Numeric |
| 26 | `99to95_TripCountNonAirNonPilgrimage` | Number of non-pilgrimage non-air trips (1395–1399) | Numeric |
| 27 | `99to95_TripCountNonAirPilgrimage` | Number of pilgrimage non-air trips (1395–1399) | Numeric |
| 28 | `1398_CardPerMonth` | Monthly card purchases 1398 / 2019 (IRR) | Numeric |
| 29 | `CardPerMonth_1399` | Monthly card purchases 1399 / 2020 (IRR) | Numeric |
| 30 | `1400_CardPerMonth` | Monthly card purchases 1400 / 2021 (IRR) | Numeric |
| 31 | `1401_CardPerMonth` | Monthly card purchases 1401 / 2022 (IRR) | Numeric |
| 32 | `1402_CardPerMonth` | Monthly card purchases 1402 / 2023 (IRR) | Numeric |
| 33 | `1401_CardBeCardPerMonth` | Monthly card-to-card transfers 1401 / 2022 (IRR) | Numeric |
| 34 | `1402_CardBeCardPerMonth` | Monthly card-to-card transfers 1402 / 2023 (IRR) | Numeric |
| 35 | `1401_PayaPerMonth` | Monthly PAYA (ACH) transfers 1401 / 2022 (IRR) | Numeric |
| 36 | `1402_PayaPerMonth` | Monthly PAYA (ACH) transfers 1402 / 2023 (IRR) | Numeric |
| 37 | `1401_SatnaPerMonth` | Monthly SATNA (RTGS) transfers 1401 / 2022 (IRR) | Numeric |
| 38 | `1402_SatnaPerMonth` | Monthly SATNA (RTGS) transfers 1402 / 2023 (IRR) | Numeric |
| 39 | `CarsCount` | Number of vehicles owned | Numeric |
| 40 | `CarsPrice` | Total vehicle value (IRR) | Numeric |
| 41 | `Daramad` | Total registered income (IRR) | Numeric |
| 42 | `NetPortfoValue_Bourse` | Stock market portfolio value (IRR) | Numeric |
| 43 | `1400_Variz` | Bank deposits in 1400 / 2021 (IRR) | Numeric |
| 44 | `1399_MandehAkhar` | End-of-year bank balance 1399 / 2020 (IRR) | Numeric |
| 45 | `1400_MandehAkhar` | End-of-year bank balance 1400 / 2021 (IRR) | Numeric |
| 46 | `1399_MandehAval` | Start-of-year bank balance 1399 / 2020 (IRR) | Numeric |
| 47 | `1400_MandehAval` | Start-of-year bank balance 1400 / 2021 (IRR) | Numeric |

---

## Notes

- **IRR** = Iranian Rial
- **Iranian calendar years:** 1395–1402 correspond roughly to 2016–2023 in the Gregorian calendar
- **PAYA** = Iran's ACH (Automated Clearing House) interbank transfer system
- **SATNA** = Iran's RTGS (Real-Time Gross Settlement) high-value transfer system
- **Justice Shares (Edalat)** = government-distributed shares in state-owned companies given to lower-income households
- **`Id_Parent`** is the key field for linking individuals to households/families — use this for Stage 1 family construction