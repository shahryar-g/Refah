#!/usr/bin/env python3
"""Build a one-row-per-family dataset from the individual-level Refah sample.

The source file stores one row per person with ``Parent_Id`` identifying the
household/family and exactly one head row per family where ``id == Parent_Id``.
This script normalizes the source column names to the vocabulary used in the
mapping document, aggregates the family features, and writes both the family
table and a schema dictionary.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


RAW_TO_CANONICAL = {
    "Parent_Id": "Id_Parent",
    "Dashboard_postalcode7Digits": "Digits7postalcode_Dashboard",
    "Has_SoeTaghzie": "SoeTaghzie_Has",
    "TripCountAirPilgrimage_95to99": "99to95_TripCountAirPilgrimage",
    "TripCountAirNonPilgrimage_95to99": "99to95_TripCountAirNonPilgrimage",
    "TripCountNonAirPilgrimage_95to99": "99to95_TripCountNonAirPilgrimage",
    "TripCountNonAirNonPilgrimage_95to99": "99to95_TripCountNonAirNonPilgrimage",
    "Has_Saham_Edalat": "Edalat_Saham_Has",
    "IsBehzisti_AfzayeshMostamari": "AfzayeshMostamari_IsBehzisti",
    "IsKomite_AfzayeshMostamari": "AfzayeshMostamari_IsKomite",
    "IsKomite_AfzayeshMostamariSayer": "AfzayeshMostamariSayer_IsKomite",
    "Malool_shedat": "shedat_Malool",
    "is_bime_darman": "darman_bime_is",
    "IsRetired_Asli": "Asli_IsRetired",
    "IsRetired_Tabaie": "Tabaie_IsRetired",
    "Bourse_NetPortfoValue": "NetPortfoValue_Bourse",
    "ISKarmanddolat_1402": "1402_ISKarmanddolat",
    "MandehAval_1399": "1399_MandehAval",
    "MandehAkhar_1399": "1399_MandehAkhar",
    "MandehAval_1400": "1400_MandehAval",
    "MandehAkhar_1400": "1400_MandehAkhar",
    "CardPerMonth_1398": "1398_CardPerMonth",
    "CardPerMonth_1399": "1399_CardPerMonth",
    "CardPerMonth_1400": "1400_CardPerMonth",
    "CardPerMonth_1401": "1401_CardPerMonth",
    "CardPerMonth_1402": "1402_CardPerMonth",
    "CardBeCardPerMonth_1401": "1401_CardBeCardPerMonth",
    "CardBeCardPerMonth_1402": "1402_CardBeCardPerMonth",
    "SatnaPerMonth_1401": "1401_SatnaPerMonth",
    "SatnaPerMonth_1402": "1402_SatnaPerMonth",
    "PayaPerMonth_1401": "1401_PayaPerMonth",
    "PayaPerMonth_1402": "1402_PayaPerMonth",
    "Variz_1400": "1400_Variz",
}


FINANCIAL_YEAR_COMPONENTS = {
    "financial_1398_total": ["1398_CardPerMonth"],
    "financial_1399_total": ["1399_CardPerMonth", "1399_MandehAval", "1399_MandehAkhar"],
    "financial_1400_total": ["1400_CardPerMonth", "1400_Variz", "1400_MandehAval", "1400_MandehAkhar"],
    "financial_1401_total": [
        "1401_CardPerMonth",
        "1401_CardBeCardPerMonth",
        "1401_PayaPerMonth",
        "1401_SatnaPerMonth",
    ],
    "financial_1402_total": [
        "1402_CardPerMonth",
        "1402_CardBeCardPerMonth",
        "1402_PayaPerMonth",
        "1402_SatnaPerMonth",
    ],
}


OUTPUT_SCHEMA = [
    # identity and location
    {"output": "family_id", "source": "Id_Parent", "aggregation": "head"},
    {"output": "postal_code_7", "source": "Digits7postalcode_Dashboard", "aggregation": "head"},
    {"output": "county", "source": "SabteAhval_countyname", "aggregation": "head"},
    {"output": "province", "source": "SabteAhval_provincename", "aggregation": "head"},
    {"output": "is_urban", "source": "isurban", "aggregation": "head"},
    {"output": "welfare_decile", "source": "Decile", "aggregation": "head"},
    {"output": "welfare_percentile", "source": "Percentile", "aggregation": "head"},
    {"output": "head_gender", "source": "GenderId", "aggregation": "head"},
    {"output": "head_age", "source": "Age", "aggregation": "head"},
    # family composition
    {"output": "family_size", "source": "id", "aggregation": "count"},
    {"output": "num_children", "source": "Age", "aggregation": "count_if_age_lt_18"},
    {"output": "num_adults", "source": "Age", "aggregation": "count_if_age_18_to_59"},
    {"output": "num_elderly", "source": "Age", "aggregation": "count_if_age_ge_60"},
    {"output": "num_male", "source": "GenderId", "aggregation": "count_if_gender_1"},
    {"output": "num_female", "source": "GenderId", "aggregation": "count_if_gender_2"},
    {"output": "age_mean", "source": "Age", "aggregation": "mean"},
    {"output": "age_max", "source": "Age", "aggregation": "max"},
    {"output": "age_min", "source": "Age", "aggregation": "min"},
    {"output": "dependency_ratio", "source": "Age", "aggregation": "(num_children + num_elderly) / family_size"},
    # income and wealth
    {"output": "total_income", "source": "Daramad", "aggregation": "sum"},
    {"output": "total_cars", "source": "CarsCount", "aggregation": "sum"},
    {"output": "total_cars_value", "source": "CarsPrice", "aggregation": "sum"},
    {"output": "total_stock_portfolio", "source": "NetPortfoValue_Bourse", "aggregation": "sum"},
    {"output": "income_per_capita", "source": "Daramad", "aggregation": "total_income / family_size"},
    # bank and financial totals
    {"output": "financial_1398_total", "source": None, "aggregation": "sum of 1398 financial components"},
    {"output": "financial_1399_total", "source": None, "aggregation": "sum of 1399 financial components"},
    {"output": "financial_1400_total", "source": None, "aggregation": "sum of 1400 financial components"},
    {"output": "financial_1401_total", "source": None, "aggregation": "sum of 1401 financial components"},
    {"output": "financial_1402_total", "source": None, "aggregation": "sum of 1402 financial components"},
    # travel
    {"output": "air_trips_nonpilgrimage", "source": "99to95_TripCountAirNonPilgrimage", "aggregation": "sum"},
    {"output": "air_trips_pilgrimage", "source": "99to95_TripCountAirPilgrimage", "aggregation": "sum"},
    {"output": "nonair_trips_nonpilgrimage", "source": "99to95_TripCountNonAirNonPilgrimage", "aggregation": "sum"},
    {"output": "nonair_trips_pilgrimage", "source": "99to95_TripCountNonAirPilgrimage", "aggregation": "sum"},
    {"output": "total_trips", "source": None, "aggregation": "sum of all trip count columns"},
    {"output": "total_air_trips", "source": None, "aggregation": "air_trips_nonpilgrimage + air_trips_pilgrimage"},
    {"output": "pilgrimage_ratio", "source": None, "aggregation": "(air_trips_pilgrimage + nonair_trips_pilgrimage) / total_trips"},
    # health and disability
    {"output": "any_malnutrition", "source": "SoeTaghzie_Has", "aggregation": "max"},
    {"output": "any_chronic_illness", "source": "ISBimarKhas", "aggregation": "max"},
    {"output": "any_disability", "source": "IsMalool", "aggregation": "max"},
    {"output": "num_disabled", "source": "IsMalool", "aggregation": "sum"},
    {"output": "max_disability_severity", "source": "shedat_Malool", "aggregation": "max"},
    {"output": "mean_disability_severity", "source": "shedat_Malool", "aggregation": "mean among disabled"},
    # welfare and social support
    {"output": "any_behzisti_support", "source": "AfzayeshMostamari_IsBehzisti", "aggregation": "max"},
    {"output": "any_komite_support", "source": "AfzayeshMostamari_IsKomite", "aggregation": "max"},
    {"output": "any_komite_support_other", "source": "AfzayeshMostamariSayer_IsKomite", "aggregation": "max"},
    {"output": "any_welfare_support", "source": None, "aggregation": "max(any_behzisti_support, any_komite_support, any_komite_support_other)"},
    {"output": "any_edalat_shares", "source": "Edalat_Saham_Has", "aggregation": "max"},
    {"output": "num_edalat_shares", "source": "Edalat_Saham_Has", "aggregation": "sum"},
    # insurance
    {"output": "any_health_insured", "source": "darman_bime_is", "aggregation": "max"},
    {"output": "all_health_insured", "source": "darman_bime_is", "aggregation": "min"},
    {"output": "num_health_insured", "source": "darman_bime_is", "aggregation": "sum"},
    {"output": "insurance_coverage_rate", "source": "darman_bime_is", "aggregation": "num_health_insured / family_size"},
    {"output": "any_insurance_contributor", "source": "IsBimePardaz", "aggregation": "max"},
    {"output": "num_insurance_contributors", "source": "IsBimePardaz", "aggregation": "sum"},
    # employment and retirement
    {"output": "any_government_employee", "source": "1402_ISKarmanddolat", "aggregation": "max"},
    {"output": "num_government_employees", "source": "1402_ISKarmanddolat", "aggregation": "sum"},
    {"output": "any_primary_retired", "source": "Asli_IsRetired", "aggregation": "max"},
    {"output": "num_primary_retired", "source": "Asli_IsRetired", "aggregation": "sum"},
    {"output": "any_dependent_retired", "source": "Tabaie_IsRetired", "aggregation": "max"},
    {"output": "num_dependent_retired", "source": "Tabaie_IsRetired", "aggregation": "sum"},
    {"output": "any_business_license", "source": "HasMojavezSenfi", "aggregation": "max"},
    {"output": "num_business_licenses", "source": "HasMojavezSenfi", "aggregation": "sum"},
    {"output": "num_working_adults", "source": None, "aggregation": "sum(IsBimePardaz == 1 or 1402_ISKarmanddolat == 1)"},
    {"output": "employment_ratio", "source": None, "aggregation": "num_working_adults / family_size"},
    {"output": "family_type", "source": None, "aggregation": "rule-based label"},
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build family-level Refah dataset")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("Raw Data/Data/sample_1402.csv"),
        help="Path to the individual-level CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Family Dimention/Code/outputs/family_dimension.csv"),
        help="Path for the family-level CSV",
    )
    return parser.parse_args()


def rename_source_columns(df: pd.DataFrame) -> pd.DataFrame:
    missing = [src for src in RAW_TO_CANONICAL if src not in df.columns]
    if missing:
        raise KeyError(f"Missing expected source columns: {missing}")
    return df.rename(columns=RAW_TO_CANONICAL)


def fill_binary(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0).astype("int8")


def fill_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def build_family_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = rename_source_columns(df).copy()
    df["family_id"] = df["Id_Parent"]
    df["is_head"] = (df["id"] == df["family_id"]).astype("int8")

    # Normalize numeric fields.
    numeric_fields = [
        "Age",
        "GenderId",
        "isurban",
        "ISBimarKhas",
        "IsMalool",
        "shedat_Malool",
        "SoeTaghzie_Has",
        "AfzayeshMostamari_IsBehzisti",
        "AfzayeshMostamari_IsKomite",
        "AfzayeshMostamariSayer_IsKomite",
        "99to95_TripCountAirPilgrimage",
        "99to95_TripCountAirNonPilgrimage",
        "99to95_TripCountNonAirPilgrimage",
        "99to95_TripCountNonAirNonPilgrimage",
        "Edalat_Saham_Has",
        "Decile",
        "Percentile",
        "HasMojavezSenfi",
        "1402_ISKarmanddolat",
        "Asli_IsRetired",
        "Tabaie_IsRetired",
        "darman_bime_is",
        "IsBimePardaz",
        "1399_MandehAval",
        "1399_MandehAkhar",
        "1399_CardPerMonth",
        "1400_Variz",
        "1400_MandehAval",
        "1400_MandehAkhar",
        "1400_CardPerMonth",
        "1398_CardPerMonth",
        "1401_CardPerMonth",
        "1402_CardPerMonth",
        "1401_CardBeCardPerMonth",
        "1402_CardBeCardPerMonth",
        "1401_SatnaPerMonth",
        "1402_SatnaPerMonth",
        "1401_PayaPerMonth",
        "1402_PayaPerMonth",
        "CarsPrice",
        "CarsCount",
        "NetPortfoValue_Bourse",
        "Daramad",
    ]
    for field in numeric_fields:
        df[field] = fill_numeric(df[field])

    binary_fields = [
        "ISBimarKhas",
        "IsMalool",
        "SoeTaghzie_Has",
        "AfzayeshMostamari_IsBehzisti",
        "AfzayeshMostamari_IsKomite",
        "AfzayeshMostamariSayer_IsKomite",
        "Edalat_Saham_Has",
        "HasMojavezSenfi",
        "1402_ISKarmanddolat",
        "Asli_IsRetired",
        "Tabaie_IsRetired",
        "darman_bime_is",
        "IsBimePardaz",
    ]
    for field in binary_fields:
        df[field] = fill_binary(df[field])

    df["Age"] = fill_numeric(df["Age"])
    df["GenderId"] = fill_numeric(df["GenderId"]).fillna(0).astype("int8")
    df["isurban"] = fill_numeric(df["isurban"]).fillna(0).astype("int8")
    df["shedat_Malool"] = fill_numeric(df["shedat_Malool"])

    # Family composition helpers.
    df["age_child"] = (df["Age"] < 18).astype("int8")
    df["age_adult"] = ((df["Age"] >= 18) & (df["Age"] <= 59)).astype("int8")
    df["age_elderly"] = (df["Age"] >= 60).astype("int8")
    df["male_flag"] = (df["GenderId"] == 1).astype("int8")
    df["female_flag"] = (df["GenderId"] == 2).astype("int8")
    df["disabled_flag"] = (df["IsMalool"] == 1).astype("int8")
    df["working_flag"] = ((df["IsBimePardaz"] == 1) | (df["1402_ISKarmanddolat"] == 1)).astype("int8")
    df["insured_flag"] = (df["darman_bime_is"] == 1).astype("int8")
    df["welfare_flag"] = (
        (df["AfzayeshMostamari_IsBehzisti"] == 1)
        | (df["AfzayeshMostamari_IsKomite"] == 1)
        | (df["AfzayeshMostamariSayer_IsKomite"] == 1)
    ).astype("int8")

    group = df.groupby("family_id", sort=False)

    family = pd.DataFrame(index=group.size().index)
    family["family_size"] = group["id"].size().astype("int64")
    family["num_children"] = group["age_child"].sum().astype("int64")
    family["num_adults"] = group["age_adult"].sum().astype("int64")
    family["num_elderly"] = group["age_elderly"].sum().astype("int64")
    family["num_male"] = group["male_flag"].sum().astype("int64")
    family["num_female"] = group["female_flag"].sum().astype("int64")
    family["age_mean"] = group["Age"].mean()
    family["age_max"] = group["Age"].max()
    family["age_min"] = group["Age"].min()
    family["dependency_ratio"] = ((family["num_children"] + family["num_elderly"]) / family["family_size"]).astype(
        "float64"
    )

    sum_fields = {
        "total_income": "Daramad",
        "total_cars": "CarsCount",
        "total_cars_value": "CarsPrice",
        "total_stock_portfolio": "NetPortfoValue_Bourse",
        "air_trips_nonpilgrimage": "99to95_TripCountAirNonPilgrimage",
        "air_trips_pilgrimage": "99to95_TripCountAirPilgrimage",
        "nonair_trips_nonpilgrimage": "99to95_TripCountNonAirNonPilgrimage",
        "nonair_trips_pilgrimage": "99to95_TripCountNonAirPilgrimage",
        "any_malnutrition": "SoeTaghzie_Has",
        "any_chronic_illness": "ISBimarKhas",
        "any_disability": "IsMalool",
        "num_disabled": "IsMalool",
        "max_disability_severity": "shedat_Malool",
        "any_behzisti_support": "AfzayeshMostamari_IsBehzisti",
        "any_komite_support": "AfzayeshMostamari_IsKomite",
        "any_komite_support_other": "AfzayeshMostamariSayer_IsKomite",
        "any_edalat_shares": "Edalat_Saham_Has",
        "num_edalat_shares": "Edalat_Saham_Has",
        "any_health_insured": "darman_bime_is",
        "all_health_insured": "darman_bime_is",
        "num_health_insured": "darman_bime_is",
        "any_insurance_contributor": "IsBimePardaz",
        "num_insurance_contributors": "IsBimePardaz",
        "any_government_employee": "1402_ISKarmanddolat",
        "num_government_employees": "1402_ISKarmanddolat",
        "any_primary_retired": "Asli_IsRetired",
        "num_primary_retired": "Asli_IsRetired",
        "any_dependent_retired": "Tabaie_IsRetired",
        "num_dependent_retired": "Tabaie_IsRetired",
        "any_business_license": "HasMojavezSenfi",
        "num_business_licenses": "HasMojavezSenfi",
        "num_working_adults": "working_flag",
    }

    max_fields = {
        "any_malnutrition",
        "any_chronic_illness",
        "any_disability",
        "max_disability_severity",
        "any_behzisti_support",
        "any_komite_support",
        "any_komite_support_other",
        "any_edalat_shares",
        "any_health_insured",
        "any_insurance_contributor",
        "any_government_employee",
        "any_primary_retired",
        "any_dependent_retired",
        "any_business_license",
    }
    min_fields = {"all_health_insured"}
    mean_fields = {"age_mean", "mean_disability_severity"}

    for output_name, source_name in sum_fields.items():
        if output_name in max_fields:
            family[output_name] = group[source_name].max().fillna(0)
        elif output_name in min_fields:
            family[output_name] = group[source_name].min().fillna(0)
        elif output_name in mean_fields:
            continue
        else:
            family[output_name] = group[source_name].sum().fillna(0)

    family["mean_disability_severity"] = (
        df.loc[df["disabled_flag"] == 1]
        .groupby("family_id", sort=False)["shedat_Malool"]
        .mean()
        .reindex(family.index)
        .fillna(0)
    )

    for output_name, source_columns in FINANCIAL_YEAR_COMPONENTS.items():
        family[output_name] = group[source_columns].sum().sum(axis=1)

    # Head-based fields with fallback to the first non-null family value.
    head_field_map = [
        ("Digits7postalcode_Dashboard", "postal_code_7"),
        ("SabteAhval_countyname", "county"),
        ("SabteAhval_provincename", "province"),
        ("isurban", "is_urban"),
        ("Decile", "welfare_decile"),
        ("Percentile", "welfare_percentile"),
        ("GenderId", "head_gender"),
        ("Age", "head_age"),
    ]
    head_rows = df.loc[df["is_head"] == 1, ["family_id", *[src for src, _ in head_field_map]]].set_index("family_id")
    for source_field, output_field in head_field_map:
        family[output_field] = head_rows[source_field].combine_first(group[source_field].first())

    for col in ["is_urban", "welfare_decile", "welfare_percentile", "head_gender", "head_age"]:
        family[col] = pd.to_numeric(family[col], errors="coerce").fillna(0).round().astype("int64")

    # Normalize output dtypes for the key count/binary columns.
    int_columns = [
        "family_size",
        "num_children",
        "num_adults",
        "num_elderly",
        "num_male",
        "num_female",
        "total_cars",
        "num_disabled",
        "num_edalat_shares",
        "num_health_insured",
        "num_insurance_contributors",
        "num_government_employees",
        "num_primary_retired",
        "num_dependent_retired",
        "num_business_licenses",
        "num_working_adults",
        "any_malnutrition",
        "any_chronic_illness",
        "any_disability",
        "max_disability_severity",
        "any_behzisti_support",
        "any_komite_support",
        "any_komite_support_other",
        "any_welfare_support",
        "any_edalat_shares",
        "any_health_insured",
        "all_health_insured",
        "any_insurance_contributor",
        "any_government_employee",
        "any_primary_retired",
        "any_dependent_retired",
        "any_business_license",
        "is_urban",
        "welfare_decile",
        "welfare_percentile",
        "head_gender",
        "head_age",
    ]
    for col in int_columns:
        if col in family.columns:
            family[col] = pd.to_numeric(family[col], errors="coerce").fillna(0).round().astype("int64")

    family["total_trips"] = (
        family["air_trips_nonpilgrimage"]
        + family["air_trips_pilgrimage"]
        + family["nonair_trips_nonpilgrimage"]
        + family["nonair_trips_pilgrimage"]
    )
    family["total_air_trips"] = family["air_trips_nonpilgrimage"] + family["air_trips_pilgrimage"]
    family["total_trips"] = pd.to_numeric(family["total_trips"], errors="coerce").fillna(0).round().astype("int64")
    family["total_air_trips"] = pd.to_numeric(family["total_air_trips"], errors="coerce").fillna(0).round().astype("int64")
    family["pilgrimage_ratio"] = np.where(
        family["total_trips"] > 0,
        (family["air_trips_pilgrimage"] + family["nonair_trips_pilgrimage"]) / family["total_trips"],
        0.0,
    )
    family["income_per_capita"] = np.where(
        family["family_size"] > 0, family["total_income"] / family["family_size"], 0.0
    )
    family["insurance_coverage_rate"] = np.where(
        family["family_size"] > 0, family["num_health_insured"] / family["family_size"], 0.0
    )
    family["employment_ratio"] = np.where(
        family["family_size"] > 0, family["num_working_adults"] / family["family_size"], 0.0
    )
    family["any_welfare_support"] = (
        family["any_behzisti_support"].astype("int64")
        | family["any_komite_support"].astype("int64")
        | family["any_komite_support_other"].astype("int64")
    ).astype("int64")

    family["family_type"] = np.select(
        [
            family["any_government_employee"].eq(1),
            family["any_primary_retired"].eq(1),
            family["any_business_license"].eq(1),
            family["any_welfare_support"].eq(1),
            family["num_working_adults"].gt(0),
        ],
        [
            "government_employee_family",
            "retired_family",
            "self_employed_family",
            "welfare_supported_family",
            "private_sector_family",
        ],
        default="unclassified",
    )

    family = family.reset_index().rename(columns={"index": "family_id"})

    # Reorder columns to match the documented output schema.
    ordered_columns = [entry["output"] for entry in OUTPUT_SCHEMA]
    extra_columns = [col for col in family.columns if col not in ordered_columns]
    family = family[[*ordered_columns, *extra_columns]]

    return family


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input, low_memory=False)
    family = build_family_dataset(df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    family.to_csv(args.output, index=False)
    print(f"Wrote {len(family):,} family rows to {args.output}")


if __name__ == "__main__":
    main()
