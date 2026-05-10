
---

# `mlops/feature-store.md`

```markdown
# 🏪 Feature Store

A feature store is a centralized system for storing, managing, and serving ML features.

---

## What Is a Feature?

A feature is an input variable used by a model.

Examples:
- customer age
- number of purchases
- average session duration
- sentiment score
- product category preference
- previous click behavior

---

## Why Feature Stores Matter

Without a feature store:
- teams duplicate feature logic
- training and serving data may differ
- features become hard to reuse
- production bugs become likely

---

## Training-Serving Skew

One of the biggest ML production problems.

It happens when:
- training uses one feature calculation
- production uses a different calculation

Example:

```text
Training:
average_purchase_value over 12 months

Production:
average_purchase_value over 6 months
