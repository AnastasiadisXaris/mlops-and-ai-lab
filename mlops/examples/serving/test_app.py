"""
test_app.py — Tests for the inference API.

Covers:
    - /health always returns 200
    - /ready returns 503 when model absent, 200 when loaded
    - /predict returns valid prediction when model loaded
    - /predict returns 503 when model absent
    - /predict returns 422 on wrong feature count
    - /predict/batch handles multiple instances
    - /predict/batch returns 422 on malformed instances
"""

import numpy as np
import pytest
from fastapi.testclient import TestClient
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import app as serving_app
from app import app

N = serving_app.N_FEATURES


@pytest.fixture(autouse=True)
def mock_model():
    """Inject a locally trained mock model — no MLflow needed."""
    X, y = make_classification(n_samples=300, n_features=N, random_state=42)
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(n_estimators=10, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    serving_app.model_store["model"] = pipeline
    serving_app.model_store["model_uri"] = "mock://local"
    serving_app.model_store["loaded_at"] = 1234567890.0
    yield
    serving_app.model_store["model"] = None
    serving_app.model_store["model_uri"] = None
    serving_app.model_store["loaded_at"] = None


@pytest.fixture
def client():
    return TestClient(app)


def valid_features():
    return [float(x) for x in np.random.randn(N)]


# --- /health ---
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# --- /ready ---
def test_ready_with_model(client):
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_ready_without_model(client):
    serving_app.model_store["model"] = None
    r = client.get("/ready")
    assert r.status_code == 503


# --- /predict ---
def test_predict_valid(client):
    r = client.post("/predict", json={"features": valid_features()})
    assert r.status_code == 200
    data = r.json()
    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
    assert data["model_uri"] == "mock://local"


def test_predict_no_model(client):
    serving_app.model_store["model"] = None
    r = client.post("/predict", json={"features": valid_features()})
    assert r.status_code == 503


def test_predict_wrong_feature_count(client):
    r = client.post("/predict", json={"features": [0.1, 0.2, 0.3]})
    assert r.status_code == 422


# --- /predict/batch ---
def test_predict_batch_valid(client):
    instances = [valid_features() for _ in range(5)]
    r = client.post("/predict/batch", json={"instances": instances})
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 5
    assert len(data["predictions"]) == 5
    assert len(data["probabilities"]) == 5
    assert all(p in [0, 1] for p in data["predictions"])


def test_predict_batch_wrong_features(client):
    instances = [[0.1, 0.2], [0.3, 0.4]]  # wrong length
    r = client.post("/predict/batch", json={"instances": instances})
    assert r.status_code == 422


def test_predict_batch_no_model(client):
    serving_app.model_store["model"] = None
    instances = [valid_features() for _ in range(3)]
    r = client.post("/predict/batch", json={"instances": instances})
    assert r.status_code == 503
