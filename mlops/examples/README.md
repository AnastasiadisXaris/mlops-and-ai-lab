# MLOps Examples

Realistic, runnable MLOps examples demonstrating production patterns for experiment tracking, model serving, and drift detection.

Each example is self-contained with its own `requirements.txt`, tests, and README.

---

## Examples

### [tracking/](./tracking/) — Experiment Tracking with MLflow

Train a model and track everything: hyperparameters, metrics, artifacts, cross-validation scores. Registers the model in MLflow Model Registry and transitions to Staging.

```bash
cd mlops/examples/tracking
pip install -r requirements.txt
python train_and_track.py
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

**Demonstrates:** `mlflow.start_run` · `log_params` · `log_metrics` · `log_model` · Model Registry · Staging transition · sklearn Pipeline artifact

---

### [serving/](./serving/) — FastAPI Inference Service

Production-pattern FastAPI inference API with MLflow Model Registry integration, liveness/readiness probes, single and batch prediction, structured logging, and a full pytest suite.

```bash
cd mlops/examples/serving
pip install -r requirements.txt
pytest test_app.py -v
MLFLOW_TRACKING_URI=http://localhost:5000 uvicorn app:app --reload
```

**Demonstrates:** lifespan model loading · `/health` + `/ready` · `/predict` + `/predict/batch` · Pydantic v2 validation · latency logging · mock model tests

---

### [monitoring/](./monitoring/) — Drift Detection

Data and model drift detection using PSI, KS test, and CUSUM — no external MLOps dependencies. Runs standalone against any parquet dataset or with built-in synthetic data.

```bash
cd mlops/examples/monitoring
pip install -r requirements.txt

python detect_drift.py                  # stable data
python detect_drift.py --inject-drift   # with synthetic drift
pytest test_detect_drift.py -v
```

**Demonstrates:** PSI · KS test · CUSUM performance tracking · drift alerts · injectable synthetic drift · CI/CD-friendly exit codes

---

## End-to-End Flow

The three examples form a complete MLOps cycle:

```text
train_and_track.py          →  experiment logged to MLflow
    ↓
app.py (serving)            →  model loaded from Registry, served via API
    ↓
detect_drift.py (monitoring) →  input drift and performance degradation detected
```

For the full stack with Docker (API + MLflow + PostgreSQL + Redis + Prometheus + Grafana):

```bash
cd devops/docker
docker compose up -d
```

---

## Requirements

| Example | Key Dependencies |
|---|---|
| tracking | `mlflow` · `scikit-learn` |
| serving | `fastapi` · `mlflow` · `scikit-learn` · `pydantic` |
| monitoring | `scipy` · `scikit-learn` · `numpy` · `pandas` |
