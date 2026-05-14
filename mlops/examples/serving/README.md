# ML Inference API — Example

Realistic FastAPI inference service with MLflow Model Registry integration, production-pattern error handling, and a full pytest suite.

## What It Demonstrates

- lifespan model loading (startup/shutdown) via `@asynccontextmanager`
- MLflow Model Registry integration — loads model by name + stage
- `/health` (liveness) and `/ready` (readiness) endpoints
- single-instance `/predict` and batch `/predict/batch`
- Pydantic v2 request/response validation with field validators
- structured logging with latency tracking
- global exception handler
- pytest suite with mock model — runs without MLflow

## Pipeline

```text
Startup → Load model from MLflow Registry
    ↓
POST /predict → Validate → Inference → Response
POST /predict/batch → Validate → Batch Inference → Response
GET  /health  → 200 OK (always)
GET  /ready   → 200 if model loaded, 503 if not
```

## Usage

```bash
pip install -r requirements.txt

# Start server (requires MLflow with a registered model)
MLFLOW_TRACKING_URI=http://localhost:5000 uvicorn app:app --reload

# Or with Docker Compose (full stack):
cd devops/docker && docker compose up -d
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | liveness probe — always 200 |
| GET | `/ready` | readiness probe — 503 if model absent |
| POST | `/predict` | single instance prediction |
| POST | `/predict/batch` | batch prediction (max 100) |

## Example Requests

```bash
# Health check
curl http://localhost:8000/health

# Single prediction (15 features)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.1,-0.5,1.2,0.3,-1.1,0.8,0.0,-0.2,0.6,1.0,0.4,-0.7,0.9,-0.3,0.5]}'

# Batch prediction
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"instances": [[0.1,-0.5,1.2,0.3,-1.1,0.8,0.0,-0.2,0.6,1.0,0.4,-0.7,0.9,-0.3,0.5]]}'

# Interactive API docs
open http://localhost:8000/docs
```

## Run Tests

```bash
# Tests use a mock model — no MLflow connection needed
pytest test_app.py -v
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MLFLOW_TRACKING_URI` | `sqlite:///mlflow.db` | MLflow server URL |
| `MODEL_NAME` | `production-classifier` | registered model name |
| `MODEL_STAGE` | `Staging` | model stage to load |
| `N_FEATURES` | `15` | expected feature vector length |

## Key Design Decisions

- **Lifespan over `@app.on_event`** — recommended pattern in FastAPI 0.93+
- **Separate `/health` and `/ready`** — liveness and readiness are distinct concerns in Kubernetes
- **`model_store` dict** — avoids global mutable state, easier to mock in tests
- **Batch endpoint** — capped at 100 instances to prevent memory exhaustion
- **Latency logging** — every prediction logs inference time in ms
