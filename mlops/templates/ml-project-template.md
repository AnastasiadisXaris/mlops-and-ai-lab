
---

# `mlops/templates/ml-project-template.md`

```markdown
# ML Project Template

## Project Name

`project-name`

---

## Problem Statement

Describe the problem this model solves.

Example:

The goal is to predict customer churn based on behavioral, demographic, and transactional features.

---

## Business / Research Objective

Explain why this model matters.

Examples:
- improve customer retention
- personalize recommendations
- estimate consumer preferences
- automate decision support

---

## Dataset

| Item | Description |
|---|---|
| Source | |
| Size | |
| Features | |
| Target Variable | |
| Data Type | |
| Update Frequency | |

---

## ML Task Type

- Classification
- Regression
- Ranking
- Clustering
- Recommendation
- NLP
- Forecasting

---

## Baseline Model

Describe the simplest model used as baseline.

Example:
- Logistic Regression
- Decision Tree
- Mean predictor
- Rule-based system

---

## Candidate Models

- Random Forest
- XGBoost
- Neural Network
- Transformer
- Recommender model

---

## Evaluation Metrics

| Metric | Purpose |
|---|---|
| Accuracy | |
| Precision | |
| Recall | |
| F1-score | |
| RMSE | |
| AUC | |

---

## Experiment Tracking

Tool:
- MLflow

Track:
- parameters
- metrics
- artifacts
- dataset version
- model version

---

## Deployment Plan

Serving type:
- Batch
- Real-time API
- Streaming

Stack:
- FastAPI
- Docker
- Kubernetes

---

## Monitoring Plan

Monitor:
- latency
- error rate
- data drift
- prediction drift
- business KPIs

---

## Retraining Plan

Retraining strategy:
- manual
- scheduled
- trigger-based
- continuous

---

## Risks

- data leakage
- bias
- overfitting
- concept drift
- poor generalization
- infrastructure cost

---

## Next Steps

- [ ] Clean dataset
- [ ] Build baseline model
- [ ] Track experiments
- [ ] Register best model
- [ ] Build API
- [ ] Dockerize service
- [ ] Add monitoring
