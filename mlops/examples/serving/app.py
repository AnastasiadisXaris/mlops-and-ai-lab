"""
app.py — Realistic FastAPI inference service.

Patterns demonstrated:
    - Lifespan model loading (startup/shutdown)
    - MLflow Model Registry integration
    - Pydantic v2 request/response validation
    - /health and /ready endpoints
    - Structured logging
    - Global exception handling
    - Batch prediction support
"""

import logging
import os
import time
from contextlib import asynccontextmanager
from typing import List

import mlflow.sklearn
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

# --- Config ---
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
MODEL_NAME = os.getenv("MODEL_NAME", "production-classifier")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Staging")
N_FEATURES = int(os.getenv("N_FEATURES", "15"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
log = logging.getLogger("inference-api")

# --- Global model state ---
model_store: dict = {"model": None, "model_uri": None, "loaded_at": None}


# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, release on shutdown."""
    model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
    log.info(f"Loading model from: {model_uri}")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    try:
        model_store["model"] = mlflow.sklearn.load_model(model_uri)
        model_store["model_uri"] = model_uri
        model_store["loaded_at"] = time.time()
        log.info("Model loaded successfully")
    except Exception as e:
        log.warning(f"Model load failed: {e} — /predict will return 503")
    yield
    log.info("Shutting down inference service")
    model_store["model"] = None


# --- App ---
app = FastAPI(
    title="ML Inference API",
    description="Production-pattern FastAPI inference service with MLflow Model Registry.",
    version="1.0.0",
    lifespan=lifespan,
)


# --- Exception handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error(f"Unhandled error on {request.url}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# --- Schemas ---
class PredictRequest(BaseModel):
    features: List[float] = Field(
        ...,
        description=f"Feature vector of length {N_FEATURES}",
        examples=[[0.1, -0.5, 1.2, 0.3, -1.1, 0.8, 0.0, -0.2, 0.6, 1.0, 0.4, -0.7, 0.9, -0.3, 0.5]],
    )

    @field_validator("features")
    @classmethod
    def check_feature_length(cls, v):
        if len(v) != N_FEATURES:
            raise ValueError(f"Expected {N_FEATURES} features, got {len(v)}")
        return v


class BatchPredictRequest(BaseModel):
    instances: List[List[float]] = Field(
        ..., description="List of feature vectors", min_length=1, max_length=100
    )

    @field_validator("instances")
    @classmethod
    def check_instances(cls, v):
        for i, row in enumerate(v):
            if len(row) != N_FEATURES:
                raise ValueError(f"Instance {i}: expected {N_FEATURES} features, got {len(row)}")
        return v


class PredictResponse(BaseModel):
    prediction: int
    probability: float
    model_uri: str


class BatchPredictResponse(BaseModel):
    predictions: List[int]
    probabilities: List[float]
    model_uri: str
    count: int


# --- Endpoints ---
@app.get("/health", tags=["ops"])
def health():
    """Liveness probe — always returns 200 if the process is alive."""
    return {"status": "ok"}


@app.get("/ready", tags=["ops"])
def ready():
    """Readiness probe — returns 503 if model is not loaded."""
    if model_store["model"] is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "status": "ready",
        "model_uri": model_store["model_uri"],
        "loaded_at": model_store["loaded_at"],
    }


@app.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict(request: PredictRequest):
    """Single-instance prediction."""
    if model_store["model"] is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    start = time.perf_counter()
    X = np.array(request.features).reshape(1, -1)
    prediction = int(model_store["model"].predict(X)[0])
    probability = float(model_store["model"].predict_proba(X)[0][prediction])
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    log.info(f"predict | class={prediction} prob={probability:.4f} latency={elapsed_ms}ms")

    return PredictResponse(
        prediction=prediction,
        probability=round(probability, 4),
        model_uri=model_store["model_uri"],
    )


@app.post("/predict/batch", response_model=BatchPredictResponse, tags=["inference"])
def predict_batch(request: BatchPredictRequest):
    """Batch prediction — up to 100 instances."""
    if model_store["model"] is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    start = time.perf_counter()
    X = np.array(request.instances)
    predictions = model_store["model"].predict(X).tolist()
    probabilities = [
        round(float(model_store["model"].predict_proba(X[i:i+1])[0][pred]), 4)
        for i, pred in enumerate(predictions)
    ]
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    log.info(f"predict_batch | n={len(predictions)} latency={elapsed_ms}ms")

    return BatchPredictResponse(
        predictions=predictions,
        probabilities=probabilities,
        model_uri=model_store["model_uri"],
        count=len(predictions),
    )
