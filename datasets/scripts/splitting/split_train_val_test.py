"""
split_train_val_test.py — Split a processed dataset into train / val / test sets.

Supports:
    - Stratified random split (tabular classification)
    - Temporal split (time-series, recommendation)

Usage:
    # Stratified split
    python datasets/scripts/splitting/split_train_val_test.py \\
        --input datasets/processed/marketing/consumer-conjoint-cleaned-v1.parquet \\
        --target purchase_intent \\
        --strategy stratified

    # Temporal split
    python datasets/scripts/splitting/split_train_val_test.py \\
        --input datasets/processed/recommendation/interactions-v1.parquet \\
        --timestamp-col timestamp \\
        --strategy temporal
"""

import argparse
import logging
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)


def stratified_split(
    df: pd.DataFrame, target: str, train_ratio: float, val_ratio: float, seed: int
) -> tuple:
    test_ratio = round(1 - train_ratio - val_ratio, 4)
    train, temp = train_test_split(
        df, test_size=(val_ratio + test_ratio), random_state=seed, stratify=df[target]
    )
    val, test = train_test_split(
        temp,
        test_size=(test_ratio / (val_ratio + test_ratio)),
        random_state=seed,
        stratify=temp[target],
    )
    return train, val, test


def temporal_split(
    df: pd.DataFrame, timestamp_col: str, train_ratio: float, val_ratio: float
) -> tuple:
    df = df.sort_values(timestamp_col).reset_index(drop=True)
    n = len(df)
    train = df.iloc[: int(n * train_ratio)]
    val = df.iloc[int(n * train_ratio) : int(n * (train_ratio + val_ratio))]
    test = df.iloc[int(n * (train_ratio + val_ratio)) :]
    return train, val, test


def save_splits(train, val, test, output_dir: str, stem: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for split, name in [(train, "train"), (val, "val"), (test, "test")]:
        path = out / f"{stem}-{name}-v1.parquet"
        split.to_parquet(path, index=False)
        log.info(f"Saved {name}: {path} ({len(split)} rows)")


def parse_args():
    parser = argparse.ArgumentParser(description="Split dataset into train/val/test.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", type=str, default="datasets/processed/splits")
    parser.add_argument(
        "--strategy", choices=["stratified", "temporal"], default="stratified"
    )
    parser.add_argument(
        "--target",
        type=str,
        default="purchase_intent",
        help="Target column (stratified only)",
    )
    parser.add_argument(
        "--timestamp-col",
        type=str,
        default="timestamp",
        help="Timestamp column (temporal only)",
    )
    parser.add_argument("--train-ratio", type=float, default=0.70)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    log.info(f"Loading: {args.input}")
    df = pd.read_parquet(args.input)
    stem = Path(args.input).stem.replace("-v1", "").replace("-cleaned", "")

    log.info(f"Shape: {df.shape} | Strategy: {args.strategy}")

    if args.strategy == "stratified":
        train, val, test = stratified_split(
            df, args.target, args.train_ratio, args.val_ratio, args.seed
        )
    else:
        train, val, test = temporal_split(
            df, args.timestamp_col, args.train_ratio, args.val_ratio
        )

    log.info(f"Train: {len(train)} | Val: {len(val)} | Test: {len(test)}")
    save_splits(train, val, test, args.output_dir, stem)
    log.info("Done.")
