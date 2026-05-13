# Dataset Schemas

## Purpose

This folder stores schema definitions for all datasets — column names, data types, constraints, validation rules, and expected value ranges. Schemas are the contract between data producers and data consumers.

---

## Naming Convention

```text
<dataset-name>-schema-<version>.json / .yaml

# Examples:
consumer-conjoint-schema-v1.json
product-reviews-schema-v1.yaml
movielens-ratings-schema-v1.json
user-item-interactions-schema-v1.json
```

---

## Folder Structure

```text
schemas/
│
├── marketing/            # marketing and survey schemas
├── nlp/                  # text dataset schemas
├── recommendation/       # interaction matrix schemas
├── time-series/          # sequential data schemas
└── research/             # thesis and research schemas
```

---

## JSON Schema Template

```json
{
  "name": "dataset-name",
  "version": "1.0",
  "description": "Short description of the dataset.",
  "columns": [
    {
      "name": "column_name",
      "type": "string | integer | float | boolean | date",
      "nullable": false,
      "description": "Column description.",
      "constraints": {
        "min": null,
        "max": null,
        "allowed_values": null,
        "regex": null
      },
      "example": "example_value"
    }
  ],
  "primary_key": "column_name",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

---

## Completed Example

```json
{
  "name": "consumer-conjoint-survey",
  "version": "1.0",
  "description": "Consumer conjoint analysis survey for preference modeling.",
  "columns": [
    {
      "name": "respondent_id",
      "type": "string",
      "nullable": false,
      "description": "Unique respondent identifier.",
      "constraints": {"regex": "^R[0-9]{4}$"},
      "example": "R0042"
    },
    {
      "name": "price_level",
      "type": "integer",
      "nullable": false,
      "description": "Price attribute on a 1–5 Likert scale.",
      "constraints": {"min": 1, "max": 5},
      "example": 3
    },
    {
      "name": "brand",
      "type": "string",
      "nullable": false,
      "description": "Product brand shown in the choice task.",
      "constraints": {"allowed_values": ["BrandA", "BrandB", "BrandC"]},
      "example": "BrandA"
    },
    {
      "name": "utility_score",
      "type": "float",
      "nullable": true,
      "description": "Estimated part-worth utility score, normalized to [0, 1].",
      "constraints": {"min": 0.0, "max": 1.0},
      "example": 0.73
    },
    {
      "name": "purchase_intent",
      "type": "integer",
      "nullable": false,
      "description": "Binary purchase intention label.",
      "constraints": {"allowed_values": [0, 1]},
      "example": 1
    }
  ],
  "primary_key": "respondent_id",
  "created_at": "2026-01-15",
  "updated_at": "2026-02-01"
}
```

---

## Pandera Validation

Enforce schemas programmatically with Pandera:

```python
import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check

schema = DataFrameSchema({
    "respondent_id": Column(str, Check.str_matches(r"^R[0-9]{4}$")),
    "price_level":   Column(int, Check.in_range(1, 5)),
    "brand":         Column(str, Check.isin(["BrandA", "BrandB", "BrandC"])),
    "utility_score": Column(float, Check.in_range(0.0, 1.0), nullable=True),
    "purchase_intent": Column(int, Check.isin([0, 1])),
})

df = pd.read_parquet("datasets/processed/marketing/consumer-conjoint-v1.parquet")

try:
    schema.validate(df, lazy=True)
    print("Schema validation passed.")
except pa.errors.SchemaErrors as e:
    print(f"Schema errors:\n{e.failure_cases}")
```

---

## Validation Script

```python
import json
import pandas as pd
import pandera as pa

def validate_dataset(df: pd.DataFrame, schema_path: str) -> bool:
    """Validate a DataFrame against a JSON schema definition."""
    with open(schema_path) as f:
        schema_def = json.load(f)

    checks = {}
    for col in schema_def["columns"]:
        c = col["constraints"]
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
        print(f"✓ Validation passed: {schema_def['name']} v{schema_def['version']}")
        return True
    except pa.errors.SchemaErrors as e:
        print(f"✗ Validation failed:\n{e.failure_cases}")
        return False
```

---

## Recommended Tools

| Tool | Purpose |
|---|---|
| Pandera | Python schema validation |
| Great Expectations | data quality suites |
| JSON Schema | format-agnostic schema definition |
| Pydantic | API and config validation |
| dbt | SQL-based schema testing |

---

## Best Practices

- create schemas at ingestion time, not retrospectively
- validate on every pipeline run — not just once
- version schemas alongside datasets
- fail pipelines explicitly on schema violations — do not silently skip rows
- update schemas when preprocessing changes the column structure

**Common pitfalls:** no schema enforcement in pipelines · silent type coercion masking errors · schema defined only in documentation not in code · missing nullable flags
