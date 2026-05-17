"""
detect_drift.py — Data and model drift detection.

Implements:
    - PSI  (Population Stability Index)  — feature distribution drift
    - KS   (Kolmogorov-Smirnov test)     — statistical distribution shift
    - CUSUM (Cumulative Sum)             — performance degradation tracking

Usage:
    python mlops/examples/monitoring/detect_drift.py

    # With custom data paths:
    python mlops/examples/monitoring/detect_drift.py \\
        --reference datasets/processed/marketing/consumer-conjoint-train-v1.parquet \\
        --current   datasets/processed/marketing/consumer-conjoint-val-v1.parquet
"""

import argparse
import logging
import warnings
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────
# Thresholds
# ─────────────────────────────────────────
PSI_THRESHOLDS = {"stable": 0.10, "warning": 0.20}  # > 0.20 = significant drift
KS_ALPHA = 0.05  # p-value threshold
CUSUM_THRESHOLD = 5.0  # cumulative sum alert threshold
CUSUM_SLACK = 0.1  # slack parameter


# ─────────────────────────────────────────
# Results
# ─────────────────────────────────────────
@dataclass
class DriftResult:
    feature: str
    method: str
    statistic: float
    threshold: float
    drifted: bool
    details: dict = field(default_factory=dict)

    def status(self) -> str:
        return "🔴 DRIFT" if self.drifted else "✅ STABLE"


# ─────────────────────────────────────────
# PSI
# ─────────────────────────────────────────
def compute_psi(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """
    Population Stability Index.
    PSI < 0.10  → stable
    PSI < 0.20  → slight drift (monitor)
    PSI >= 0.20 → significant drift (action required)
    """
    ref_min = reference.min()
    ref_max = reference.max()
    breakpoints = np.linspace(ref_min, ref_max, bins + 1)
    breakpoints[0] -= 1e-6
    breakpoints[-1] += 1e-6

    ref_counts = np.histogram(reference, bins=breakpoints)[0]
    cur_counts = np.histogram(current, bins=breakpoints)[0]

    # Avoid zero proportions
    ref_pct = np.where(ref_counts == 0, 1e-4, ref_counts / len(reference))
    cur_pct = np.where(cur_counts == 0, 1e-4, cur_counts / len(current))

    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return float(psi)


def run_psi(
    reference: pd.DataFrame, current: pd.DataFrame, features: List[str]
) -> List[DriftResult]:
    results = []
    for feat in features:
        ref_vals = reference[feat].dropna().values
        cur_vals = current[feat].dropna().values
        psi = compute_psi(ref_vals, cur_vals)
        drifted = psi >= PSI_THRESHOLDS["warning"]
        results.append(
            DriftResult(
                feature=feat,
                method="PSI",
                statistic=round(psi, 4),
                threshold=PSI_THRESHOLDS["warning"],
                drifted=drifted,
                details={
                    "psi_warning": PSI_THRESHOLDS["warning"],
                    "psi_stable": PSI_THRESHOLDS["stable"],
                },
            )
        )
    return results


# ─────────────────────────────────────────
# KS Test
# ─────────────────────────────────────────
def run_ks(
    reference: pd.DataFrame, current: pd.DataFrame, features: List[str]
) -> List[DriftResult]:
    results = []
    for feat in features:
        ref_vals = reference[feat].dropna().values
        cur_vals = current[feat].dropna().values
        ks_stat, p_value = stats.ks_2samp(ref_vals, cur_vals)
        drifted = p_value < KS_ALPHA
        results.append(
            DriftResult(
                feature=feat,
                method="KS",
                statistic=round(ks_stat, 4),
                threshold=KS_ALPHA,
                drifted=drifted,
                details={"p_value": round(p_value, 6), "alpha": KS_ALPHA},
            )
        )
    return results


# ─────────────────────────────────────────
# CUSUM
# ─────────────────────────────────────────
def run_cusum(
    performance_series: List[float],
    target: float,
    threshold: float = CUSUM_THRESHOLD,
    slack: float = CUSUM_SLACK,
) -> DriftResult:
    """
    CUSUM for detecting sustained performance degradation.
    Tracks cumulative deviation from target accuracy/F1.
    """
    cusum_pos = 0.0
    cusum_neg = 0.0
    cusum_values = []
    alert_idx: Optional[int] = None

    for i, val in enumerate(performance_series):
        deviation = val - target
        cusum_pos = max(0, cusum_pos + deviation - slack)
        cusum_neg = max(0, cusum_neg - deviation - slack)
        cusum_values.append(cusum_pos + cusum_neg)

        if (cusum_pos > threshold or cusum_neg > threshold) and alert_idx is None:
            alert_idx = i

    final_cusum = cusum_values[-1] if cusum_values else 0.0
    drifted = alert_idx is not None

    return DriftResult(
        feature="model_performance",
        method="CUSUM",
        statistic=round(final_cusum, 4),
        threshold=threshold,
        drifted=drifted,
        details={
            "alert_at_step": alert_idx,
            "target_metric": target,
            "n_steps": len(performance_series),
        },
    )


# ─────────────────────────────────────────
# Report
# ─────────────────────────────────────────
def print_report(results: List[DriftResult]) -> None:
    print("\n" + "=" * 65)
    print("  DRIFT DETECTION REPORT")
    print("=" * 65)

    drifted = [r for r in results if r.drifted]
    stable = [r for r in results if not r.drifted]

    print(f"\n  Total checks : {len(results)}")
    print(f"  Drifted      : {len(drifted)}")
    print(f"  Stable       : {len(stable)}")

    print("\n" + "-" * 65)
    print(
        f"  {'Feature':<25} {'Method':<8} {'Statistic':>10} {'Threshold':>10}  Status"
    )
    print("-" * 65)

    for r in sorted(results, key=lambda x: (not x.drifted, x.method, x.feature)):
        print(
            f"  {r.feature:<25} {r.method:<8} {r.statistic:>10.4f} "
            f"{r.threshold:>10.4f}  {r.status()}"
        )
        if r.drifted and r.details:
            for k, v in r.details.items():
                print(f"    └─ {k}: {v}")

    print("=" * 65)

    if drifted:
        print(
            f"\n  ⚠️  ACTION REQUIRED: {len(drifted)} feature(s) show significant drift."
        )
        print(
            "  Consider: data pipeline check · feature re-engineering · model retraining\n"
        )
    else:
        print("\n  ✅ All features stable. No action required.\n")


# ─────────────────────────────────────────
# Synthetic Data Generator
# ─────────────────────────────────────────
def generate_data(drift: bool = False, seed: int = 42):
    """Generate reference and current datasets with optional synthetic drift."""
    np.random.seed(seed)
    X, y = make_classification(
        n_samples=2000, n_features=8, n_informative=5, random_state=seed
    )
    cols = [f"feature_{i:02d}" for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=cols)
    df["target"] = y

    reference, current = train_test_split(df, test_size=0.3, random_state=seed)

    if drift:
        # Simulate distribution shift on 3 features
        log.info("Injecting synthetic drift into feature_00, feature_01, feature_02")
        current = current.copy()
        current["feature_00"] += np.random.normal(2.5, 0.5, len(current))
        current["feature_01"] *= -1.5
        current["feature_02"] += np.random.exponential(2.0, len(current))

    return reference.reset_index(drop=True), current.reset_index(drop=True)


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
def run(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    performance_series: Optional[List[float]] = None,
) -> List[DriftResult]:

    numeric_cols = reference.select_dtypes(include=[np.number]).columns.tolist()
    if "target" in numeric_cols:
        numeric_cols.remove("target")

    log.info(f"Reference: {reference.shape} | Current: {current.shape}")
    log.info(f"Features to check: {numeric_cols}")

    results: List[DriftResult] = []
    results += run_psi(reference, current, numeric_cols)
    results += run_ks(reference, current, numeric_cols)

    # CUSUM on simulated performance series if not provided
    if performance_series is None:
        np.random.seed(42)
        # Simulate gradual accuracy degradation
        performance_series = (
            list(np.random.normal(0.88, 0.01, 10))  # stable
            + list(np.random.normal(0.80, 0.02, 10))  # degrading
            + list(np.random.normal(0.72, 0.03, 10))  # degraded
        )
    results.append(run_cusum(performance_series, target=0.85))

    print_report(results)
    return results


def parse_args():
    parser = argparse.ArgumentParser(description="Detect data and model drift.")
    parser.add_argument(
        "--reference", type=str, default=None, help="Path to reference parquet dataset"
    )
    parser.add_argument(
        "--current", type=str, default=None, help="Path to current parquet dataset"
    )
    parser.add_argument(
        "--inject-drift",
        action="store_true",
        help="Inject synthetic drift for demonstration",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.reference and args.current:
        log.info("Loading datasets from disk...")
        reference = pd.read_parquet(args.reference)
        current = pd.read_parquet(args.current)
    else:
        log.info("No datasets provided — using synthetic data.")
        log.info(f"Drift injection: {args.inject_drift}")
        reference, current = generate_data(drift=args.inject_drift)

    run(reference, current)
