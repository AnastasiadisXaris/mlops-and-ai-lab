"""
clean_consumer_conjoint.py — Clean raw conjoint survey data.

Input:  datasets/raw/surveys/consumer-conjoint-raw.csv
        (or datasets/synthetic/marketing/marketing-synthetic-conjoint-v1.parquet for testing)
Output: datasets/processed/marketing/consumer-conjoint-cleaned-v1.parquet

Usage:
    # With synthetic data (no raw data needed):
    python datasets/scripts/cleaning/clean_consumer_conjoint.py --use-synthetic

    # With real raw data:
    python datasets/scripts/cleaning/clean_consumer_conjoint.py \\
        --input datasets/raw/surveys/consumer-conjoint-raw.csv \\
        --output datasets/processed/marketing/consumer-conjoint-cleaned-v1.parquet
"""

import argparse
import logging
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import LabelEncoder

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

DEFAULT_INPUT = "datasets/raw/surveys/consumer-conjoint-raw.csv"
DEFAULT_OUTPUT = "datasets/processed/marketing/consumer-conjoint-cleaned-v1.parquet"
SYNTHETIC_PATH = "datasets/synthetic/marketing/marketing-synthetic-conjoint-v1.parquet"


def load(input_path: str, use_synthetic: bool) -> pd.DataFrame:
    if use_synthetic:
        log.info(f"Loading synthetic data: {SYNTHETIC_PATH}")
        return pd.read_parquet(SYNTHETIC_PATH)
    ext = Path(input_path).suffix.lower()
    log.info(f"Loading raw data: {input_path}")
    return pd.read_csv(input_path) if ext == ".csv" else pd.read_parquet(input_path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    log.info(f"Input shape: {df.shape}")

    # 1. Drop duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["respondent_id", "task_id"])
    log.info(f"Removed {before - len(df)} duplicate rows")

    # 2. Drop rows with missing target
    before = len(df)
    df = df.dropna(subset=["purchase_intent"])
    log.info(f"Removed {before - len(df)} rows with missing purchase_intent")

    # 3. Filter valid ranges
    before = len(df)
    df = df[
        df["price_level"].between(1, 5)
        & df["quality"].between(1, 5)
        & df["delivery_days"].between(1, 7)
    ]
    log.info(f"Removed {before - len(df)} rows outside valid attribute ranges")

    # 4. Encode brand (fit on train only in production)
    le = LabelEncoder()
    df = df.copy()
    df["brand_encoded"] = le.fit_transform(df["brand"])
    log.info(f"Encoded brand: {list(le.classes_)}")

    # 5. Normalize utility score to [0, 1]
    if "utility_score" in df.columns and df["utility_score"].notna().any():
        mn, mx = df["utility_score"].min(), df["utility_score"].max()
        df["utility_score"] = ((df["utility_score"] - mn) / (mx - mn)).round(4)
        log.info(f"Normalized utility_score: min={mn:.4f}, max={mx:.4f}")

    # 6. Cast types
    df["purchase_intent"] = df["purchase_intent"].astype(int)

    log.info(f"Output shape: {df.shape}")
    log.info(f"Target distribution:\n{df['purchase_intent'].value_counts()}")
    return df


def save(df: pd.DataFrame, output_path: str) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    log.info(f"Saved: {out} ({len(df)} rows, {df.shape[1]} columns)")


def parse_args():
    parser = argparse.ArgumentParser(description="Clean conjoint survey data.")
    parser.add_argument("--input", type=str, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--use-synthetic",
        action="store_true",
        help="Use synthetic data instead of raw CSV",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    df = load(args.input, args.use_synthetic)
    df = clean(df)
    save(df, args.output)
