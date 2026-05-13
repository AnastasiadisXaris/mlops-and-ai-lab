# Dataset Metadata

## Purpose

This folder stores metadata files that describe datasets — their origin, schema, version history, preprocessing steps, ownership, and governance information. Metadata is the documentation layer that makes datasets discoverable, auditable, and reproducible.

---

## Naming Convention

```text
<dataset-name>-metadata-<version>.json / .yaml

# Examples:
consumer-conjoint-metadata-v1.json
product-reviews-metadata-v2.yaml
movielens-100k-metadata-v1.json
```

---

## Metadata Schema

### Full JSON Template

```json
{
  "name": "dataset-name",
  "version": "1.0",
  "description": "Short description of the dataset.",
  "domain": "marketing | nlp | recommendation | time-series | images | research",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD",
  "author": "Name",
  "license": "MIT | CC BY 4.0 | proprietary",
  "source": {
    "origin": "survey | kaggle | api | synthetic | internal",
    "url": "https://...",
    "collection_date": "YYYY-MM-DD"
  },
  "schema": {
    "rows": 0,
    "columns": 0,
    "file_size_kb": 0,
    "format": "parquet | csv | jsonl",
    "path": "datasets/processed/dataset-name-v1.parquet"
  },
  "features": [
    {"name": "column_name", "type": "string | int | float | bool", "description": ""}
  ],
  "target": {
    "column": "target_column",
    "type": "binary | multiclass | continuous",
    "distribution": ""
  },
  "preprocessing": [
    "step 1 description",
    "step 2 description"
  ],
  "limitations": [
    "limitation 1",
    "limitation 2"
  ],
  "related_files": {
    "raw": "datasets/raw/",
    "processed": "datasets/processed/",
    "schema": "datasets/schemas/",
    "dataset_card": "datasets/dataset-cards/"
  },
  "tags": ["tag1", "tag2"]
}
```

---

## Completed Example

```json
{
  "name": "consumer-conjoint-survey",
  "version": "1.0",
  "description": "Consumer preference survey for conjoint analysis and utility estimation.",
  "domain": "marketing",
  "created_at": "2026-01-15",
  "updated_at": "2026-02-01",
  "author": "Anastasiadis Xaris",
  "license": "proprietary",
  "source": {
    "origin": "survey",
    "url": "internal Google Forms",
    "collection_date": "2026-01-10"
  },
  "schema": {
    "rows": 1200,
    "columns": 14,
    "file_size_kb": 420,
    "format": "parquet",
    "path": "datasets/processed/consumer-conjoint-v1.parquet"
  },
  "features": [
    {"name": "respondent_id", "type": "string", "description": "unique respondent identifier"},
    {"name": "price_level", "type": "int", "description": "price attribute, 1–5 scale"},
    {"name": "brand", "type": "string", "description": "product brand"},
    {"name": "utility_score", "type": "float", "description": "estimated part-worth utility"}
  ],
  "target": {
    "column": "purchase_intent",
    "type": "binary",
    "distribution": "58% positive, 42% negative"
  },
  "preprocessing": [
    "removed 23 incomplete responses",
    "encoded categorical variables (brand, region)",
    "normalized utility scores to [0, 1]"
  ],
  "limitations": [
    "convenience sample, not fully representative",
    "limited to Greek market respondents",
    "self-reported data subject to response bias"
  ],
  "related_files": {
    "raw": "datasets/raw/consumer-conjoint-raw.csv",
    "processed": "datasets/processed/consumer-conjoint-v1.parquet",
    "schema": "datasets/schemas/consumer-conjoint-schema.json",
    "dataset_card": "datasets/dataset-cards/marketing-consumer-conjoint-v1.md"
  },
  "tags": ["conjoint", "marketing", "preference-modeling", "tbca"]
}
```

---

## Versioning Strategy

Increment version when:

| Change | Version Bump |
|---|---|
| New rows added | `v1.0 → v1.1` |
| Schema change | `v1.x → v2.0` |
| Preprocessing updated | `v1.x → v1.x+1` |
| Source changed | `v1.x → v2.0` |

Always keep previous versions — never overwrite.

---

## Usage Example

```python
import json

with open("datasets/metadata/consumer-conjoint-metadata-v1.json") as f:
    meta = json.load(f)

print(f"Dataset: {meta['name']} v{meta['version']}")
print(f"Rows: {meta['schema']['rows']}, Columns: {meta['schema']['columns']}")
print(f"Target: {meta['target']['column']} ({meta['target']['type']})")
```

---

## Why Metadata Matters

| Benefit | Description |
|---|---|
| Discoverability | find the right dataset without opening files |
| Governance | ownership, license, and provenance tracked |
| Reproducibility | preprocessing steps documented and versioned |
| Auditability | trace decisions back to data properties |
| Collaboration | new contributors onboard without guesswork |

---

## Best Practices

- create metadata at ingestion time, not retrospectively
- update `updated_at` on every change
- store metadata in the same version control as the dataset
- link metadata to dataset cards, schemas, and raw files

**Common pitfalls:** outdated metadata · missing versioning · no link between metadata and actual files · undocumented preprocessing steps
