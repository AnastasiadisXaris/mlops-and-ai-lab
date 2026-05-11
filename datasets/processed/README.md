# Processed Datasets

## Purpose

This folder contains cleaned and transformed datasets ready for:

- training
- analytics
- experimentation
- deployment

---

# Pipeline

```text
Raw Data
    ↓
Cleaning
    ↓
Transformation
    ↓
Feature Engineering
    ↓
Processed Dataset
```

---

# Best Practices

- never overwrite raw data
- document preprocessing steps
- version processed datasets
- store feature metadata

---

# Recommended Formats

- parquet
- feather
- csv
- sqlite
