# Drift Detection — Example

Realistic drift detection implementation using PSI, KS test, and CUSUM — no external dependencies beyond scipy and numpy.

## What It Demonstrates

| Method | Detects | Trigger |
|---|---|---|
| PSI (Population Stability Index) | feature distribution shift | PSI ≥ 0.20 |
| KS Test (Kolmogorov-Smirnov) | statistical distribution change | p-value < 0.05 |
| CUSUM (Cumulative Sum) | sustained performance degradation | cumulative sum > 5.0 |

## Usage

```bash
pip install -r requirements.txt

# Run with synthetic data (stable)
python detect_drift.py

# Run with injected drift (demonstrates alerts)
python detect_drift.py --inject-drift

# Run with real datasets
python detect_drift.py \
    --reference datasets/processed/marketing/consumer-conjoint-train-v1.parquet \
    --current   datasets/processed/marketing/consumer-conjoint-val-v1.parquet
```

## Example Output

```
=================================================================
  DRIFT DETECTION REPORT
=================================================================

  Total checks : 17
  Drifted      : 4
  Stable       : 13

-----------------------------------------------------------------
  Feature                   Method   Statistic  Threshold  Status
-----------------------------------------------------------------
  feature_00                PSI         0.3821     0.2000  🔴 DRIFT
    └─ psi_warning: 0.2
  feature_00                KS          0.4120     0.0500  🔴 DRIFT
    └─ p_value: 0.0
  model_performance         CUSUM       8.2300     5.0000  🔴 DRIFT
    └─ alert_at_step: 14
  ...
=================================================================

  ⚠️  ACTION REQUIRED: 4 feature(s) show significant drift.
  Consider: data pipeline check · feature re-engineering · model retraining
```

## Run Tests

```bash
pytest test_detect_drift.py -v
```

## PSI Interpretation

| PSI Value | Meaning | Action |
|---|---|---|
| < 0.10 | stable | none |
| 0.10 – 0.20 | slight shift | monitor |
| ≥ 0.20 | significant drift | investigate / retrain |

## Key Design Decisions

- **No MLflow dependency** — runs standalone against any parquet dataset
- **CUSUM target** — set to expected production baseline (e.g. accuracy = 0.85)
- **Synthetic drift injection** — `--inject-drift` shifts 3 features for demonstration
- **Exit code** — returns 0 (stable) or 1 (drift detected) for CI/CD integration
