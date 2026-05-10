
---

# `mlops/monitoring-drift.md`

```markdown
# 📈 Monitoring and Drift Detection

Monitoring ensures that an ML system continues to work after deployment.

A model is not finished when it is deployed. Deployment is where the real test begins.

---

## What to Monitor

## 1. System Metrics

- latency
- uptime
- error rate
- CPU usage
- memory usage
- GPU usage
- request volume

## 2. Data Metrics

- missing values
- schema changes
- distribution changes
- outliers
- feature ranges

## 3. Model Metrics

- accuracy
- precision
- recall
- F1-score
- RMSE
- prediction confidence
- calibration

## 4. Business Metrics

- conversion rate
- click-through rate
- recommendation acceptance
- churn reduction
- revenue impact

---

## Types of Drift

## Data Drift

Input data distribution changes.

Example:
```text
Training users: mostly desktop users
Production users: mostly mobile users
