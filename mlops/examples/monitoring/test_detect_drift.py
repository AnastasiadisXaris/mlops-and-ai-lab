"""
test_detect_drift.py — Tests for the drift detection module.

Covers:
    - PSI returns 0 for identical distributions
    - PSI detects large distribution shift
    - KS test passes for same distribution
    - KS test flags different distributions
    - CUSUM stable on flat performance series
    - CUSUM triggers on degrading performance
    - run() returns results for all features
"""

import numpy as np
import pandas as pd

from mlops.examples.monitoring.detect_drift import (
    CUSUM_THRESHOLD,
    KS_ALPHA,
    PSI_THRESHOLDS,
    compute_psi,
    generate_data,
    run,
    run_cusum,
    run_ks,
    run_psi,
)


# ─── PSI ───
def test_psi_identical_distributions():
    data = np.random.normal(0, 1, 1000)
    psi = compute_psi(data, data)
    assert psi < PSI_THRESHOLDS["stable"], f"Expected PSI near 0, got {psi}"


def test_psi_detects_large_shift():
    reference = np.random.normal(0, 1, 1000)
    current = np.random.normal(5, 1, 1000)  # large shift
    psi = compute_psi(reference, current)
    assert psi >= PSI_THRESHOLDS["warning"], f"Expected PSI >= 0.20, got {psi}"


def test_run_psi_returns_results_per_feature():
    df = pd.DataFrame(
        {"f1": np.random.normal(0, 1, 500), "f2": np.random.normal(0, 1, 500)}
    )
    results = run_psi(df, df, ["f1", "f2"])
    assert len(results) == 2
    assert all(r.method == "PSI" for r in results)
    assert all(not r.drifted for r in results)


def test_run_psi_flags_drift():
    reference = pd.DataFrame({"f1": np.random.normal(0, 1, 1000)})
    current = pd.DataFrame({"f1": np.random.normal(5, 1, 1000)})
    results = run_psi(reference, current, ["f1"])
    assert results[0].drifted


# ─── KS ───
def test_ks_same_distribution_no_drift():
    np.random.seed(42)
    data = pd.DataFrame({"f1": np.random.normal(0, 1, 500)})
    results = run_ks(data, data, ["f1"])
    assert not results[0].drifted


def test_ks_different_distribution_drift():
    reference = pd.DataFrame({"f1": np.random.normal(0, 1, 1000)})
    current = pd.DataFrame({"f1": np.random.normal(4, 1, 1000)})
    results = run_ks(reference, current, ["f1"])
    assert results[0].drifted
    assert results[0].details["p_value"] < KS_ALPHA


# ─── CUSUM ───
def test_cusum_stable_performance():
    stable_series = list(np.random.normal(0.90, 0.005, 30))
    result = run_cusum(stable_series, target=0.85, threshold=CUSUM_THRESHOLD)
    assert not result.drifted


def test_cusum_detects_degradation():
    degraded = list(np.random.normal(0.90, 0.005, 10)) + list(
        np.random.normal(0.50, 0.01, 20)
    )  # very large drop - well below target of 0.85
    result = run_cusum(degraded, target=0.85, threshold=CUSUM_THRESHOLD)
    assert result.drifted
    assert result.details["alert_at_step"] is not None


# ─── Full run ───
def test_run_stable_returns_all_results():
    reference, current = generate_data(drift=False, seed=0)
    results = run(reference, current)
    numeric_cols = reference.select_dtypes(include=[np.number]).columns.tolist()
    if "target" in numeric_cols:
        numeric_cols.remove("target")
    # PSI + KS per feature + 1 CUSUM
    assert len(results) == len(numeric_cols) * 2 + 1


def test_run_with_drift_detects_drift():
    reference, current = generate_data(drift=True, seed=42)
    results = run(reference, current)
    drifted = [r for r in results if r.drifted]
    assert len(drifted) > 0, "Expected at least one drift detection with injected drift"
