
---

# `mlops/model-serving.md`

```markdown
# 🌐 Model Serving

Model serving is the process of exposing a trained ML model so that applications can use it for predictions.

---

## Serving Types

## 1. Batch Inference

Predictions are generated periodically.

### Use Cases
- monthly customer segmentation
- daily recommendation updates
- scheduled churn prediction

```text
Data Batch
    ↓
Model
    ↓
Predictions File
    ↓
Database / Dashboard
