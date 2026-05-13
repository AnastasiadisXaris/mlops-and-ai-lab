# MLflow Experiment Tracking — Example

Realistic MLflow tracking example: train a model, log params/metrics/artifacts, register in Model Registry, and transition to Staging.

## What It Demonstrates

- `mlflow.set_experiment()` — experiment isolation
- `mlflow.start_run()` — run context manager
- `mlflow.log_params()` — hyperparameter logging
- `mlflow.log_metrics()` — metric logging (accuracy, F1, ROC-AUC, CV scores)
- `mlflow.set_tags()` — run metadata
- `mlflow.sklearn.log_model()` — model artifact + auto-registration
- `MlflowClient.transition_model_version_stage()` — promote to Staging
- `sklearn.Pipeline` — scaler + classifier as a single artifact

## Pipeline

```text
Data Generation → Train/Test Split → Pipeline (Scaler + RandomForest)
    ↓
Cross-Validation → Evaluation → MLflow Logging → Model Registry → Staging
```

## Usage

```bash
pip install -r requirements.txt

# Local run (SQLite backend, no server needed)
python train_and_track.py

# With MLflow Tracking Server
MLFLOW_TRACKING_URI=http://localhost:5000 python train_and_track.py
```

## View Results

```bash
# Launch MLflow UI
mlflow ui --backend-store-uri sqlite:///mlflow.db

# Open http://localhost:5000
```

## Key Design Decisions

- **Pipeline artifact:** scaler and classifier are packaged together — the served model handles its own preprocessing
- **Cross-validation:** `cv_roc_auc_mean` and `cv_roc_auc_std` are logged alongside test metrics for generalization assessment
- **Tags:** model type, dataset, stage, and author are tagged for experiment filtering
- **Auto-staging:** new versions automatically transition to Staging — production promotion requires explicit approval
