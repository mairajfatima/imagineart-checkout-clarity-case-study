"""
04_ab_test_sample_size.py

Calculates the sample size needed for the proposed A/B test in
03_experiment_design.md (clearer checkout + separate Cancel
Subscription button), and includes the analysis function you'd
run on the results IF this test were actually launched.

This is the real statistical method behind the experiment design —
runnable on your own machine, and reusable on any future A/B test
with real numbers plugged in.

HOW TO RUN:
    pip install scipy
    python 04_ab_test_sample_size.py
"""

import numpy as np
from scipy import stats

ALPHA = 0.05   # significance level (two-sided)
POWER = 0.80   # statistical power


def required_sample_size(baseline_rate: float, relative_mde: float,
                          alpha: float = ALPHA, power: float = POWER) -> int:
    """
    baseline_rate: current rate of the primary metric (e.g. 0.03 = 3% of
                   subscribers open a billing ticket)
    relative_mde:  smallest relative change worth detecting (e.g. 0.20 = 20%)
    """
    p1 = baseline_rate
    p2 = baseline_rate * (1 - relative_mde)  # we want this metric to go DOWN
    za = stats.norm.ppf(1 - alpha / 2)
    zb = stats.norm.ppf(power)
    pooled_var = p1 * (1 - p1) + p2 * (1 - p2)
    n = ((za + zb) ** 2 * pooled_var) / (p2 - p1) ** 2
    return int(np.ceil(n))


def analyze_two_proportion_test(x1, n1, x2, n2):
    """
    x1, n1: successes/total in control
    x2, n2: successes/total in variant
    Returns a two-proportion z-test result (use this ONCE you have real
    results from a launched test).
    """
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)
    se_pooled = np.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se_pooled
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    ci_low = (p2 - p1) - 1.96 * se
    ci_high = (p2 - p1) + 1.96 * se

    return {
        "control_rate": round(p1, 4),
        "variant_rate": round(p2, 4),
        "absolute_diff": round(p2 - p1, 4),
        "relative_diff_pct": round((p2 / p1 - 1) * 100, 2),
        "95pct_CI": (round(ci_low, 4), round(ci_high, 4)),
        "z": round(z, 3),
        "p_value": round(p_value, 5),
        "significant_at_0.05": p_value < 0.05,
    }


if __name__ == "__main__":
    # EXAMPLE assumed baseline (placeholder — replace with real ticket-rate
    # data if ImagineArt ever shares it, or your own product's real number).
    baseline = 0.03     # e.g. 3% of subscribers open a billing-related ticket
    mde = 0.20           # want to detect a 20% relative reduction

    n_per_arm = required_sample_size(baseline, mde)
    print(f"Assumed baseline billing-ticket rate: {baseline*100}%")
    print(f"Target relative reduction: {mde*100}%")
    print(f"Required sample size per arm: {n_per_arm:,}")
    print()

    print("Example analysis call (plug in real numbers once a test runs):")
    example = analyze_two_proportion_test(x1=90, n1=3000, x2=65, n2=3000)
    for k, v in example.items():
        print(f"  {k}: {v}")