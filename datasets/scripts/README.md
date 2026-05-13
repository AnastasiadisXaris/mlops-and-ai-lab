# Dataset Scripts

## Purpose

This folder stores Python scripts for dataset ingestion, cleaning, preprocessing, validation, feature engineering, and export. Scripts here are the executable layer of the data pipeline — reproducible, versioned, and documented.

---

## Naming Convention

```text
<action>_<dataset>_<description>.py

# Examples:
ingest_movielens_100k.py
clean_consumer_conjoint.py
validate_product_reviews.py
features_rfm_engineering.py
export_processed_parquet.py
split_train_val_test.py
```

---

## Folder Structure

```text
scripts/
│
├── ingestion/            # download and store raw datasets
├── cleaning/             # deduplication, missing values, outliers
├── validation/           # schema and quality checks
├── preprocessing/        # encoding, normalization, transformation
├── feature-engineering/  # feature creation and selection
├── splitting/            # train / val / test splits
└── export/               # format conversion and export
```

---

## Script Template

Every script should follow this structure:

```python
"""
script_name.py — One-line description.

Input:  datasets/raw/<domain>/filename.csv
Output: datasets/processed/<domain>/filename.parquet

Usage:
    python scripts/<action>/<script_name>.py
    python scripts/<action>/<script_name>.py --input path --output path
"""

import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Script description.")
    parser.add_argument("--input", type=str,
                        default="datasets/raw/domain/filename.csv")
    parser.add_argument("--output", type=str,
                        default="datasets/processed/domain/filename.parquet")
    return parser.parse_args()


def run(input_path: str, output_path: str) -> None:
    log.info(f"Loading: {input_path}")
    df = pd.read_csv(input_path)
    log.info(f"Shape: {df.shape}")

    # --- Processing steps ---
    before = len(df)
    df = df.drop_duplicates()
    log.info(f"Removed {before - len(df)} duplicates")

    # ... additional steps ...

    # --- Save ---
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    log.info(f"Saved: {output_path} ({len(df)} rows)")


if __name__ == "__main__":
    args = parse_args()
    run(args.input, args.output)
```

---

## Cleaning Script Example

```python
"""
clean_consumer_conjoint.py — Clean raw conjoint survey data.

Input:  datasets/raw/surveys/consumer-conjoint-2026-01-10.csv
Output: datasets/processed/marketing/consumer-conjoint-cleaned-v1.parquet
"""

import logging
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

log = logging.getLogger(__name__)

def clean(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)
    log.info(f"Raw shape: {df.shape}")

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["respondent_id", "task_id"])
    log.info(f"Dropped {before - len(df)} duplicate rows")

    # Drop incomplete responses
    before = len(df)
    df = df.dropna(subset=["purchase_intent", "utility_score"])
    log.info(f"Dropped {before - len(df)} rows with missing target")

    # Encode brand
    le = LabelEncoder()
    df["brand_encoded"] = le.fit_transform(df["brand"])
    log.info(f"Encoded brand: {list(le.classes_)}")

    # Normalize utility scores
    df["utility_score"] = (df["utility_score"] - df["utility_score"].min()) / \
                          (df["utility_score"].max() - df["utility_score"].min())

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    log.info(f"Saved: {output_path} ({len(df)} rows, {df.shape[1]} columns)")
```

---

## Validation Script Example

```python
"""
validate_schema.py — Validate a processed dataset against its schema.
"""

import json
import pandas as pd
import pandera as pa

def validate(parquet_path: str, schema_path: str) -> bool:
    df = pd.read_parquet(parquet_path)
    with open(schema_path) as f:
        schema_def = json.load(f)

    checks = {}
    for col in schema_def["columns"]:
        c = col.get("constraints", {})
        col_checks = []
        if c.get("min") is not None:
            col_checks.append(pa.Check.greater_than_or_equal_to(c["min"]))
        if c.get("max") is not None:
            col_checks.append(pa.Check.less_than_or_equal_to(c["max"]))
        if c.get("allowed_values"):
            col_checks.append(pa.Check.isin(c["allowed_values"]))
        checks[col["name"]] = pa.Column(nullable=col.get("nullable", True),
                                         checks=col_checks)

    schema = pa.DataFrameSchema(checks)
    try:
        schema.validate(df, lazy=True)
        print(f"✓ Validation passed: {parquet_path}")
        return True
    except pa.errors.SchemaErrors as e:
        print(f"✗ Validation failed:\n{e.failure_cases}")
        return False
```

---

## Recommended Libraries

| Library | Purpose |
|---|---|
| Pandas | data manipulation |
| Polars | high-performance processing |
| Pandera | schema validation |
| Great Expectations | data quality suites |
| Scikit-learn | preprocessing utilities |
| Pathlib | path management |
| argparse | CLI arguments |

---

## Best Practices

- use `argparse` for all input/output paths — no hardcoded paths
- log row counts before and after every transformation step
- save outputs to `processed/` — never overwrite raw files
- make scripts idempotent — running twice should produce the same result
- add a docstring with input, output, and usage at the top of every script

**Common pitfalls:** hardcoded paths · missing logging · scripts that only run in a specific working directory · no error handling on missing files · silent data loss without logging counts
