"""
train_and_track.py — Realistic MLflow experiment tracking example.

Pipeline:
    1. Load / generate dataset
    2. Preprocess and split
    3. Train a RandomForest classifier
    4. Evaluate (accuracy, F1, ROC-AUC)
    5. Log params, metrics, tags, and model artifact to MLflow
    6. Register model in MLflow Model Registry
    7. Transition model to Staging

Usage:
    # With local MLflow (no server needed):
    python train_and_track.py

    # With MLflow Tracking Server:
    MLFLOW_TRACKING_URI=http://localhost:5000 python train_and_track.py
"""

import logging
import os

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# --- Config ---
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
EXPERIMENT_NAME = "classifier-training"
MODEL_NAME = "production-classifier"
RANDOM_STATE = 42


def load_data():
    """Generate synthetic classification dataset."""
    log.info("Generating dataset...")
    X, y = make_classification(
        n_samples=2000,
        n_features=15,
        n_informative=8,
        n_redundant=3,
        n_clusters_per_class=2,
        random_state=RANDOM_STATE,
    )
    return train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)


def build_pipeline(params: dict) -> Pipeline:
    """Build a sklearn Pipeline: scaler + classifier."""
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(**params, random_state=RANDOM_STATE)),
        ]
    )


def evaluate(model, X_test, y_test) -> dict:
    """Compute evaluation metrics."""
    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    return {
        "accuracy": round(accuracy_score(y_test, preds), 4),
        "f1_score": round(f1_score(y_test, preds), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
    }


def run_experiment():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    X_train, X_test, y_train, y_test = load_data()

    # Hyperparameters to track
    params = {
        "n_estimators": 200,
        "max_depth": 8,
        "min_samples_split": 4,
        "min_samples_leaf": 2,
        "max_features": "sqrt",
    }

    with mlflow.start_run(run_name="rf-baseline") as run:

        # --- Tags ---
        mlflow.set_tags(
            {
                "model_type": "RandomForest",
                "dataset": "synthetic-classification",
                "stage": "baseline",
                "author": "mlops-lab",
            }
        )

        # --- Train ---
        log.info("Training model...")
        pipeline = build_pipeline(params)
        pipeline.fit(X_train, y_train)

        # --- Cross-validation ---
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="roc_auc")
        cv_mean = round(float(np.mean(cv_scores)), 4)
        cv_std = round(float(np.std(cv_scores)), 4)

        # --- Evaluate ---
        metrics = evaluate(pipeline, X_test, y_test)
        metrics["cv_roc_auc_mean"] = cv_mean
        metrics["cv_roc_auc_std"] = cv_std

        log.info(f"Metrics: {metrics}")
        log.info("\n" + classification_report(y_test, pipeline.predict(X_test)))

        # --- Log to MLflow ---
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        # Log model + register
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
            registered_model_name=MODEL_NAME,
            input_example=X_test[:3],
        )

        log.info(f"Run ID: {run.info.run_id}")
        log.info(f"Experiment: {EXPERIMENT_NAME}")
        log.info(f"Model registered as: {MODEL_NAME}")

        # --- Transition to Staging ---
        client = mlflow.tracking.MlflowClient()
        latest = client.get_latest_versions(MODEL_NAME, stages=["None"])
        if latest:
            client.transition_model_version_stage(
                name=MODEL_NAME,
                version=latest[0].version,
                stage="Staging",
            )
            log.info(f"Model v{latest[0].version} transitioned to Staging")


if __name__ == "__main__":
    run_experiment()
