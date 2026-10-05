"""
src/dataset.py
==============
Enterprise Telemetry Dataset Generator for ChurnGuard-ML.

Generates realistic, high-dimensional multi-modal tabular customer telemetry
matching the specifications defined in the Week 3 Machine Learning Plan.

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Project: Machine Learning Model Development & Evaluation Plan (Week 3)
Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3
"""

import os
import numpy as np
import pandas as pd
from typing import Tuple


def generate_synthetic_telemetry(n_samples: int = 25000, random_state: int = 42) -> pd.DataFrame:
    """
    Generates synthetic enterprise B2B SaaS customer telemetry data.
    
    Parameters:
        n_samples (int): Number of customer account records to synthesize.
        random_state (int): Seed for deterministic reproducibility.
        
    Returns:
        pd.DataFrame: High-fidelity telemetry DataFrame with ~12% churn prevalence.
    """
    rng = np.random.default_rng(random_state)
    
    # 1. Account Identifiers & Metadata
    account_ids = [f"ACC-{10000 + i}" for i in range(n_samples)]
    
    # 2. Structural Account Attributes
    tenure_months = rng.integers(1, 61, size=n_samples)
    
    contract_tiers = rng.choice(
        ['Starter', 'Growth', 'Enterprise'],
        size=n_samples,
        p=[0.45, 0.35, 0.20]
    )
    
    industries = rng.choice(
        ['Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing'],
        size=n_samples,
        p=[0.30, 0.25, 0.15, 0.15, 0.15]
    )
    
    billing_cycles = rng.choice(
        ['Monthly', 'Annual'],
        size=n_samples,
        p=[0.40, 0.60]
    )
    
    # Contract ARR ($) conditional on tier
    tier_base_arr = {'Starter': 2400.0, 'Growth': 12000.0, 'Enterprise': 48000.0}
    tier_scale_arr = {'Starter': 1200.0, 'Growth': 4000.0, 'Enterprise': 18000.0}
    
    contract_arr = np.array([
        max(1200.0, rng.normal(tier_base_arr[t], tier_scale_arr[t]))
        for t in contract_tiers
    ])
    
    # Licensed vs Active Seats
    tier_licensed_seats = {'Starter': 10, 'Growth': 45, 'Enterprise': 150}
    licensed_seats = np.array([
        max(2, int(rng.poisson(tier_licensed_seats[t])))
        for t in contract_tiers
    ])
    
    seat_utilization = rng.uniform(0.30, 1.00, size=n_samples)
    active_seats = np.maximum(1, (licensed_seats * seat_utilization).astype(int))
    
    # 3. Behavioral Telemetry (Trailing 30d & 90d Usage)
    trailing_90d_logins = rng.negative_binomial(n=8, p=0.08, size=n_samples) + 15
    
    # Activity momentum factor (1.0 = stable, < 0.70 = decaying engagement)
    momentum_factor = rng.beta(a=4.0, b=2.0, size=n_samples)
    trailing_30d_logins = np.maximum(0, (trailing_90d_logins / 3.0 * momentum_factor + rng.normal(0, 3, size=n_samples)).astype(int))
    
    api_calls_30d = np.maximum(0, rng.exponential(scale=2500, size=n_samples).astype(int))
    feature_exports_30d = np.maximum(0, rng.poisson(lam=12, size=n_samples))
    storage_used_gb = np.round(np.maximum(1.0, rng.gamma(shape=2.5, scale=18.0, size=n_samples)), 2)
    
    # 4. Support Interactions & Friction Metrics
    open_escalated_tickets = rng.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.75, 0.15, 0.06, 0.03, 0.01])
    avg_resolution_hours = np.round(np.maximum(2.0, rng.exponential(scale=18.0, size=n_samples) + open_escalated_tickets * 14.0), 1)
    
    # Support ticket duration with power-user outliers for Tukey IQR capping demonstration
    monthly_ticket_minutes = np.maximum(0.0, rng.exponential(scale=240.0, size=n_samples))
    # Inject 0.5% extreme outliers (automated script friction / power users)
    outlier_idx = rng.choice(n_samples, size=int(n_samples * 0.005), replace=False)
    monthly_ticket_minutes[outlier_idx] += rng.uniform(1500.0, 4500.0, size=len(outlier_idx))
    
    # CSAT score (1 to 5), with ~4% missingness (MCAR/MAR)
    csat_score = rng.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.06, 0.10, 0.22, 0.40, 0.22]).astype(float)
    missing_csat_idx = rng.choice(n_samples, size=int(n_samples * 0.04), replace=False)
    csat_score[missing_csat_idx] = np.nan
    
    # 5. Latent Churn Propensity Generation
    # Ground truth reflects behavioral contraction, support friction, billing type, and tenure
    clean_csat = np.where(np.isnan(csat_score), 3.5, csat_score)
    activity_ratio = trailing_30d_logins / ((trailing_90d_logins / 3.0) + 1e-4)
    
    logit = (
        - 2.80                                       # Base log-odds (calibrates to ~12% churn rate)
        - 1.40 * (activity_ratio - 1.0)              # Contraction in login activity triggers high risk
        + 0.55 * open_escalated_tickets              # Open escalated tickets increase churn odds
        + 0.018 * (avg_resolution_hours - 20.0)      # Prolonged ticket resolution increases churn odds
        - 0.45 * (clean_csat - 3.0)                  # Low CSAT increases churn odds
        - 0.025 * (tenure_months - 18.0)             # Mature tenure dampens churn propensity
        + 0.40 * (billing_cycles == 'Monthly')       # Monthly contracts exhibit higher flight risk
        - 0.35 * (contract_tiers == 'Enterprise')    # Enterprise accounts exhibit higher lock-in
        - 0.50 * (seat_utilization - 0.70)           # Underutilized seats indicate abandonment
        + rng.normal(0.0, 0.45, size=n_samples)      # Stochastic unobserved variance
    )
    
    churn_prob = 1.0 / (1.0 + np.exp(-logit))
    churn = (rng.uniform(0.0, 1.0, size=n_samples) < churn_prob).astype(int)
    
    df = pd.DataFrame({
        'account_id': account_ids,
        'tenure_months': tenure_months,
        'contract_arr': np.round(contract_arr, 2),
        'contract_tier': contract_tiers,
        'industry': industries,
        'billing_cycle': billing_cycles,
        'licensed_seats': licensed_seats,
        'active_seats': active_seats,
        'trailing_30d_logins': trailing_30d_logins,
        'trailing_90d_logins': trailing_90d_logins,
        'api_calls_30d': api_calls_30d,
        'feature_exports_30d': feature_exports_30d,
        'storage_used_gb': storage_used_gb,
        'open_escalated_tickets': open_escalated_tickets,
        'avg_resolution_hours': avg_resolution_hours,
        'monthly_ticket_minutes': np.round(monthly_ticket_minutes, 1),
        'csat_score': csat_score,
        'churn': churn
    })
    
    return df


def load_or_generate_data(
    data_path: str = "data/customer_telemetry.csv",
    n_samples: int = 25000,
    force_regenerate: bool = False,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Loads existing telemetry dataset or generates and saves a fresh one.
    """
    if os.path.exists(data_path) and not force_regenerate:
        print(f"[*] Loading existing telemetry data from: {data_path}")
        df = pd.read_csv(data_path)
    else:
        print(f"[*] Generating {n_samples} synthetic enterprise telemetry records (seed={random_state})...")
        os.makedirs(os.path.dirname(data_path) or ".", exist_ok=True)
        df = generate_synthetic_telemetry(n_samples=n_samples, random_state=random_state)
        df.to_csv(data_path, index=False)
        print(f"[+] Successfully saved dataset to: {data_path}")
        
    churn_count = int(df['churn'].sum())
    churn_rate = (churn_count / len(df)) * 100.0
    print(f"[i] Dataset shape: {df.shape} | Churn count: {churn_count} ({churn_rate:.2f}%)")
    return df


if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "customer_telemetry.csv")
    df = load_or_generate_data(data_path=data_file, n_samples=25000, force_regenerate=True)
    print("\nSample records:")
    print(df.head(3).T)
