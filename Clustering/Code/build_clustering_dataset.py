#!/usr/bin/env python3
"""Build the clustering dataset from the family-level Refah data."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]


CLUSTER_COLUMNS = [
    "province",
    "county",
    "is_urban",
    "family_size",
    "num_children",
    "num_elderly",
    "dependency_ratio",
    "head_age",
    "total_income",
    "total_stock_portfolio",
    "card_spend_1402_total",
    "financial_1402_total",
    "total_trips",
    "any_chronic_illness",
    "any_disability",
    "any_welfare_support",
    "insurance_coverage_rate",
    "employment_ratio",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build clustering-ready family dataset")
    parser.add_argument(
        "--input",
        type=Path,
        default=REPO_ROOT / "Data" / "Family_Dimension" / "family_dimension.csv",
        help="Path to the family-level CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "Data" / "Clustering" / "clustering_dataset.csv",
        help="Path for the clustering dataset CSV",
    )
    return parser.parse_args()


def log1p_safe(series: pd.Series) -> pd.Series:
    return np.log1p(pd.to_numeric(series, errors="coerce").fillna(0).clip(lower=0))


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input, low_memory=False)

    missing = [col for col in CLUSTER_COLUMNS if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required clustering columns: {missing}")

    cluster = df[CLUSTER_COLUMNS].copy()

    cluster["province"] = cluster["province"].fillna("unknown").astype(str)
    cluster["county"] = cluster["county"].fillna("unknown").astype(str)

    numeric_zero_fill = [
        "is_urban",
        "family_size",
        "num_children",
        "num_elderly",
        "dependency_ratio",
        "head_age",
        "total_income",
        "total_stock_portfolio",
        "card_spend_1402_total",
        "financial_1402_total",
        "total_trips",
        "any_chronic_illness",
        "any_disability",
        "any_welfare_support",
        "insurance_coverage_rate",
        "employment_ratio",
    ]
    for col in numeric_zero_fill:
        cluster[col] = pd.to_numeric(cluster[col], errors="coerce").fillna(0)

    cluster["head_age"] = cluster["head_age"].fillna(cluster["head_age"].median())

    cluster["total_income_log1p"] = log1p_safe(cluster["total_income"])
    cluster["total_stock_portfolio_log1p"] = log1p_safe(cluster["total_stock_portfolio"])
    cluster["card_spend_1402_total_log1p"] = log1p_safe(cluster["card_spend_1402_total"])
    cluster["financial_1402_total_log1p"] = log1p_safe(cluster["financial_1402_total"])

    # Keep the requested clustering variables plus the transformed versions.
    output_columns = [
        "province",
        "county",
        "is_urban",
        "family_size",
        "num_children",
        "num_elderly",
        "dependency_ratio",
        "head_age",
        "total_income_log1p",
        "total_stock_portfolio_log1p",
        "card_spend_1402_total_log1p",
        "financial_1402_total_log1p",
        "total_trips",
        "any_chronic_illness",
        "any_disability",
        "any_welfare_support",
        "insurance_coverage_rate",
        "employment_ratio",
    ]
    cluster = cluster[output_columns]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cluster.to_csv(args.output, index=False)
    print(f"Wrote {len(cluster):,} clustering rows to {args.output}")


if __name__ == "__main__":
    main()
