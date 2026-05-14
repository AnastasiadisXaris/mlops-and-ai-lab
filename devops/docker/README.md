# Docker Compose — MLOps Stack

Production-pattern Docker Compose stack for local MLOps development and testing.

## Services

| Service | Port | Purpose |
|---|---|---|
| `api` | 8000 | FastAPI inference service |
| `mlflow` | 5000 | Experiment tracking + Model Registry |
| `postgres` | 5432 | Backend store for MLflow + app data |
| `redis` | 6379 | Cache + task queue |
| `prometheus` | 9090 | Metrics collection |
| `grafana` | 3000 | Dashboards (`admin` / `admin`) |

## Architecture

```text
Client
    ↓
FastAPI (port 8000)
    ├── MLflow Model Registry (port 5000)
    ├── PostgreSQL (port 5432)
    └── Redis cache (port 6379)

Prometheus (port 9090) ← scrapes API + MLflow
Grafana (port 3000)    ← queries Prometheus
```

## Quickstart

```bash
# 1. Start the full stack
docker compose up -d

# 2. Check service health
docker compose ps

# 3. Train and register a model
docker compose run --rm api python ml/train_and_track.py

# 4. View MLflow UI
open http://localhost:5000

# 5. Test inference
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.1,-0.5,1.2,0.3,-1.1,0.8,0.0,-0.2,0.6,1.0,0.4,-0.7,0.9,-0.3,0.5]}'

# 6. View Grafana dashboards
open http://localhost:3000  # admin / admin

# 7. Tear down
docker compose down
docker compose down -v  # also removes volumes
```

## File Structure

```text
devops/docker/
│
├── docker-compose.yml          # full stack definition
├── Dockerfile.api              # FastAPI inference service
├── init/
│   └── postgres-init.sh        # creates mlops + mlflow databases
└── monitoring/
    ├── prometheus.yml           # scrape config
    └── grafana/
        └── provisioning/
            └── datasources/
                └── prometheus.yml
```

## Environment Variables

Override defaults via a `.env` file in this directory:

```env
POSTGRES_USER=mlops
POSTGRES_PASSWORD=mlops
MLFLOW_TRACKING_URI=http://mlflow:5000
MODEL_NAME=production-classifier
MODEL_STAGE=Staging
GF_SECURITY_ADMIN_PASSWORD=your-secure-password
```

## Common Operations

```bash
# View logs for a specific service
docker compose logs -f api
docker compose logs -f mlflow

# Restart a single service
docker compose restart api

# Scale the API (multiple workers)
docker compose up -d --scale api=3

# Connect to PostgreSQL
docker compose exec postgres psql -U mlops -d mlops

# Connect to Redis
docker compose exec redis redis-cli
```

## Notes

- MLflow uses PostgreSQL as backend store — more reliable than SQLite for concurrent access
- Redis is configured with LRU eviction (256 MB limit) — suitable for response caching
- Prometheus scrapes metrics every 15s — adjust `scrape_interval` for production
- Grafana auto-provisions Prometheus as default datasource on startup
