# Processed Datasets

## Purpose

This folder stores cleaned, transformed, and feature-engineered datasets ready for training, analytics, experimentation, and deployment. Processed datasets are derived from raw data — never the other way around.

---

## Naming Convention

```text
<domain>-<description>-<version>.<ext>

# Examples:
marketing-consumer-conjoint-v1.parquet
nlp-product-reviews-cleaned-v2.parquet
recommendation-movielens-features-v1.parquet
time-series-sales-normalized-v1.parquet
```

---

## Folder Structure

```text
processed/
│
├── marketing/            # processed marketing and survey data
├── nlp/                  # cleaned and tokenized text datasets
├── recommendation/       # user-item interaction matrices
├── time-series/          # normalized sequential data
├── research/             # thesis and academic datasets
└── features/             # engineered feature sets
```

---

## Processing Pipeline

```text
Raw Data (immutable)
    ↓
Validation (schema, types, ranges)
    ↓
Cleaning (duplicates, missing values, outliers)
    ↓
Encoding (categoricals, ordinals)
    ↓
Normalization / Scaling
    ↓
Feature Engineering
    ↓
Train / Val / Test Split
    ↓
Processed Dataset (versioned)
```

**Core rule:** raw data is never modified. All transformations produce new files in `processed/`.

---

## Versioning Strategy

| Change | Version Bump | Example |
|---|---|---|
| Minor cleaning fix | patch | `v1.0 → v1.1` |
| New features added | minor | `v1.1 → v1.2` |
| Schema change | major | `v1.x → v2.0` |
| Source data changed | major | `v1.x → v2.0` |

Always keep previous versions — downstream models may depend on them.

---

## Processing Script Template

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# 1. Load raw
df = pd.read_csv("datasets/raw/consumer-conjoint-raw.csv")
print(f"Raw shape: {df.shape}")

# 2. Drop duplicates and nulls
df = df.drop_duplicates()
before = len(df)
df = df.dropna(subset=["target_column"])
print(f"Dropped {before - len(df)} rows with missing target")

# 3. Encode categoricals
le = LabelEncoder()
df["brand_encoded"] = le.fit_transform(df["brand"])

# 4. Scale numerics
scaler = StandardScaler()
numeric_cols = ["price_level", "quality", "utility_score"]
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# 5. Split
train, temp = train_test_split(df, test_size=0.3, random_state=42, stratify=df["target"])
val, test = train_test_split(temp, test_size=0.5, random_state=42, stratify=temp["target"])

print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")

# 6. Save
train.to_parquet("datasets/processed/marketing/consumer-conjoint-train-v1.parquet", index=False)
val.to_parquet("datasets/processed/marketing/consumer-conjoint-val-v1.parquet", index=False)
test.to_parquet("datasets/processed/marketing/consumer-conjoint-test-v1.parquet", index=False)

print("Saved processed datasets.")
```

---

## Recommended Formats

| Format | Use Case |
|---|---|
| Parquet | analytics, ML pipelines — preferred |
| Feather | fast local read/write |
| CSV | portability, small datasets |
| SQLite | lightweight relational queries |
| Arrow | in-memory ML frameworks |

---

## Split Naming Convention

```text
<dataset>-train-<version>.parquet
<dataset>-val-<version>.parquet
<dataset>-test-<version>.parquet
```

Store splits as separate files — never shuffle and re-split after the initial split is created.

---

## Documentation Requirements

For every processed dataset, create:

- a **dataset card** in `datasets/dataset-cards/`
- a **metadata file** in `datasets/metadata/`
- a **schema file** in `datasets/schemas/`

---

## Best Practices

- document every transformation step in the processing script
- log row counts before and after each step
- fit scalers and encoders on train only — transform val/test separately
- store fitted scalers as artifacts for inference reuse
- never re-split after the initial split is frozen

**Common pitfalls:** fitting scaler on full dataset before splitting (data leakage) · overwriting raw files · missing version tracking · undocumented dropped rows · re-shuffling splits between experiments
