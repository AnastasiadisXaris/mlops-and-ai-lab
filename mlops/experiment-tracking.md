# 🧪 Experiment Tracking

Experiment tracking is the process of recording all information related to ML experiments.

---

## Why It Matters

Without experiment tracking, ML development becomes chaotic.

You need to know:
- which dataset was used
- which parameters were tested
- which model performed best
- which metrics were achieved
- which code version produced the result

---

## What to Track

### Parameters
- learning rate
- batch size
- model type
- number of epochs
- train/test split
- preprocessing method

### Metrics
- accuracy
- precision
- recall
- F1-score
- RMSE
- MAE
- AUC
- log loss

### Artifacts
- trained model
- confusion matrix
- plots
- evaluation reports
- feature importance
- datasets metadata

---

## Recommended Tool: MLflow

MLflow can track:
- experiments
- parameters
- metrics
- artifacts
- models

---

## Example Workflow

```text
Train model
    ↓
Log parameters
    ↓
Log metrics
    ↓
Log artifacts
    ↓
Compare experiments
    ↓
Select best model
