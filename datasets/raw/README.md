# Raw Datasets

## Purpose

This folder stores untouched original datasets.

Raw datasets should remain immutable.

---

# Why Important?

Raw data enables:

- reproducibility
- rollback
- auditing
- debugging

---

# Rules

- never modify raw files
- never clean raw datasets directly
- keep source provenance
- document ingestion date

---

# Example

```text
raw/
│
├── customer-survey-original.csv
├── kaggle-export.zip
└── amazon-reviews-raw.parquet
```
