# MLOps

This section contains notes, tools, templates, and architecture patterns for building production-ready Machine Learning systems.

MLOps combines Machine Learning, Software Engineering, DevOps, Data Engineering, Monitoring, Automation, and Reproducibility. The goal is not only to train models, but to deploy, monitor, improve, and maintain them in real-world environments.

---

## Core Topics

- ML lifecycle management
- Experiment tracking
- Model registry and versioning
- Model serving and inference
- Feature stores
- Monitoring and drift detection
- CI/CD for ML
- Retraining pipelines
- Data versioning
- Model governance

---

## Folder Contents

| File | Purpose |
|---|---|
| `mlops-roadmap.md` | Learning roadmap for MLOps |
| `experiment-tracking.md` | Tracking experiments, metrics, and artifacts |
| `model-registry.md` | Managing model versions and stages |
| `model-serving.md` | Deploying models as APIs |
| `monitoring-drift.md` | Monitoring data drift, model drift, and performance |
| `retraining-strategy.md` | Strategies for model updates and retraining |
| `feature-store.md` | Feature management and reuse |
| `mlops-tools.md` | Useful MLOps tools and platforms |
| `mlops-project-ideas.md` | Practical portfolio/research project ideas |

### Templates

| File | Purpose |
|---|---|
| `templates/ml-project-template.md` | Reusable ML project structure |
| `templates/experiment-log-template.md` | Experiment logging template |
| `templates/model-card-template.md` | Model card documentation |

---

## MLOps Lifecycle

```text
Data Collection
    ↓
Data Validation
    ↓
Feature Engineering
    ↓
Experiment Tracking
    ↓
Model Training
    ↓
Model Evaluation
    ↓
Model Registry
    ↓
Model Deployment
    ↓
Monitoring
    ↓
Retraining
```

---

## Recommended Stack

| Area | Technology |
|---|---|
| Experiment Tracking | MLflow |
| Data Versioning | DVC |
| Serving | FastAPI / BentoML |
| Drift Detection | Evidently AI |
| Monitoring | Prometheus / Grafana |
| Containerization | Docker |
| Orchestration | Kubernetes |
| CI/CD | GitHub Actions |
