
---

# `mlops/retraining-strategy.md`

```markdown
# 🔁 Retraining Strategy

Retraining is the process of updating an ML model with new data.

---

## Why Retraining Is Needed

Models degrade because:
- user behavior changes
- markets change
- data distributions shift
- new products appear
- external events affect decisions

In marketing and consumer analytics, drift is not a bug. It is almost guaranteed.

---

## Retraining Types

## 1. Manual Retraining

A developer or researcher decides when to retrain.

### Good For
- early-stage projects
- academic experiments
- low-risk models

---

## 2. Scheduled Retraining

The model is retrained at fixed intervals.

```text
Daily
Weekly
Monthly
Quarterly
