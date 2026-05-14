"""
generate_synthetic.py — Generate synthetic datasets for testing and prototyping.

Produces:
    datasets/synthetic/tabular/tabular-synthetic-classification-v1.parquet
    datasets/synthetic/marketing/marketing-synthetic-conjoint-v1.parquet
    datasets/synthetic/recommendation/recommendation-synthetic-user-item-v1.parquet

Usage:
    python datasets/synthetic/generate_synthetic.py
    python datasets/synthetic/generate_synthetic.py --output-dir datasets/synthetic
"""

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

SEED = 42


def generate_classification(output_dir: Path) -> None:
    """Synthetic tabular classification dataset."""
    np.random.seed(SEED)
    X, y = make_classification(
        n_samples=2000,
        n_features=15,
        n_informative=8,
        n_redundant=3,
        n_classes=2,
        weights=[0.6, 0.4],
        random_state=SEED,
    )
    df = pd.DataFrame(X, columns=[f"feature_{i:02d}" for i in range(X.shape[1])])
    df["target"] = y

    out = output_dir / "tabular" / "tabular-synthetic-classification-v1.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)

    dist = df["target"].value_counts().to_dict()
    log.info(f"Classification → {out.name} | shape={df.shape} | dist={dist}")


def generate_conjoint(output_dir: Path) -> None:
    """Synthetic conjoint analysis survey dataset."""
    np.random.seed(SEED)
    n = 1200
    brands = ["BrandA", "BrandB", "BrandC"]

    df = pd.DataFrame({
        "respondent_id":  [f"R{i:04d}" for i in range(n)],
        "task_id":        np.random.randint(1, 9, n),
        "profile_id":     np.random.randint(1, 4, n),
        "price_level":    np.random.randint(1, 6, n),
        "brand":          np.random.choice(brands, n),
        "quality":        np.random.randint(1, 6, n),
        "delivery_days":  np.random.randint(1, 8, n),
        "utility_score":  np.clip(np.random.normal(0.5, 0.18, n), 0, 1).round(4),
        "purchase_intent": np.random.binomial(1, 0.55, n),
    })

    out = output_dir / "marketing" / "marketing-synthetic-conjoint-v1.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)

    dist = df["purchase_intent"].value_counts().to_dict()
    log.info(f"Conjoint      → {out.name} | shape={df.shape} | dist={dist}")


def generate_user_item(output_dir: Path) -> None:
    """Synthetic user-item interaction dataset for recommendation."""
    np.random.seed(SEED)
    n_users, n_items, n_interactions = 500, 200, 5000

    df = pd.DataFrame({
        "user_id":   [f"U{np.random.randint(0, n_users):04d}" for _ in range(n_interactions)],
        "item_id":   [f"I{np.random.randint(0, n_items):04d}" for _ in range(n_interactions)],
        "rating":    np.random.choice(
            [1.0, 2.0, 3.0, 4.0, 5.0], n_interactions,
            p=[0.05, 0.10, 0.20, 0.35, 0.30]
        ),
        "timestamp": np.sort(np.random.randint(1700000000, 1710000000, n_interactions)),
    })
    before = len(df)
    df = df.drop_duplicates(subset=["user_id", "item_id"]).reset_index(drop=True)
    log.info(f"Removed {before - len(df)} duplicate interactions")

    sparsity = 1 - len(df) / (n_users * n_items)

    out = output_dir / "recommendation" / "recommendation-synthetic-user-item-v1.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)

    log.info(f"User-Item     → {out.name} | shape={df.shape} | sparsity={sparsity:.4f}")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate synthetic datasets.")
    parser.add_argument(
        "--output-dir", type=str, default="datasets/synthetic",
        help="Root output directory (default: datasets/synthetic)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_dir = Path(args.output_dir)

    log.info(f"Generating synthetic datasets → {output_dir.resolve()}")
    generate_classification(output_dir)
    generate_conjoint(output_dir)
    generate_user_item(output_dir)
    log.info("Done.")
