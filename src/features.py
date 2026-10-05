"""
src/features.py
===============
Domain-Specific Feature Engineering, Tukey IQR Capping, and Multicollinearity Auditing.

Implements the velocity ratios, support friction indices, robust clipping,
and Variance Inflation Factor (VIF) pruning detailed in Section 2 of the Week 3 Plan.

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Project: Machine Learning Model Development & Evaluation Plan (Week 3)
Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LinearRegression


class TukeyIQRCapper(BaseEstimator, TransformerMixin):
    """
    Scikit-Learn compatible transformer that winsorizes continuous numeric
    features to [Q1 - 1.5*IQR, Q3 + 1.5*IQR], preventing gradient instability.
    """
    def __init__(self, columns: List[str] = None, factor: float = 1.5, min_val: float = 0.0):
        self.columns = columns
        self.factor = factor
        self.min_val = min_val
        self.bounds_: Dict[str, Tuple[float, float]] = {}

    def fit(self, X: pd.DataFrame, y=None):
        cols_to_fit = self.columns if self.columns else X.select_dtypes(include=[np.number]).columns
        for col in cols_to_fit:
            if col in X.columns:
                series = X[col].dropna()
                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                iqr = q3 - q1
                lower = max(self.min_val, q1 - self.factor * iqr)
                upper = q3 + self.factor * iqr
                self.bounds_[col] = (lower, upper)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_out = X.copy()
        for col, (lower, upper) in self.bounds_.items():
            if col in X_out.columns:
                X_out[col] = np.clip(X_out[col], lower, upper)
        return X_out


def engineer_domain_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes directional momentum ratios, seat saturation, and customer friction indices.
    
    Features engineered:
      1. activity_velocity: Trailing 30-day logins vs. normalized quarterly baseline.
      2. seat_utilization_ratio: Active seats divided by paid licensed seats.
      3. friction_index: Weighted composite of open escalations, resolution lag, and poor CSAT.
      4. support_burden_per_seat: Monthly support ticket minutes per active seat.
      5. arr_per_licensed_seat: Contract ARR normalized by licensed seat count.
    """
    df_out = df.copy()
    
    # 1. Activity Velocity Ratio (Section 2.4)
    # (Trailing_30d_Logins) / [ (Trailing_90d_Logins / 3) + epsilon ]
    quarterly_expected = (df_out['trailing_90d_logins'] / 3.0) + 1e-4
    df_out['activity_velocity'] = np.round(df_out['trailing_30d_logins'] / quarterly_expected, 4)
    
    # 2. Seat Utilization Ratio
    df_out['seat_utilization_ratio'] = np.round(
        df_out['active_seats'] / np.maximum(df_out['licensed_seats'], 1), 4
    )
    
    # 3. Support Escalation & Friction Index (Section 2.4)
    # Friction_Index = (Open_Escalated_Tickets * 3.0) + (Avg_Resolution_Hours / 24.0) + (1.0 if CSAT < 3 else 0.0)
    csat_imputed = df_out['csat_score'].fillna(3.5)
    csat_penalty = (csat_imputed < 3.0).astype(float)
    df_out['friction_index'] = np.round(
        (df_out['open_escalated_tickets'] * 3.0) + 
        (df_out['avg_resolution_hours'] / 24.0) + 
        csat_penalty, 3
    )
    
    # 4. Support Burden Per Seat
    df_out['support_burden_per_seat'] = np.round(
        df_out['monthly_ticket_minutes'] / np.maximum(df_out['active_seats'], 1), 3
    )
    
    # 5. Contract ARR per Licensed Seat
    df_out['arr_per_licensed_seat'] = np.round(
        df_out['contract_arr'] / np.maximum(df_out['licensed_seats'], 1), 2
    )
    
    return df_out


def calculate_vif_scorecard(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    """
    Calculates Variance Inflation Factor (VIF) across continuous features
    using OLS auxiliary regressions: VIF_i = 1 / (1 - R_i^2).
    
    Used to prune collinear features exceeding the VIF threshold (5.0).
    """
    clean_data = df[numeric_cols].dropna()
    vif_records = []
    
    for i, target_col in enumerate(numeric_cols):
        X_cols = [c for c in numeric_cols if c != target_col]
        X = clean_data[X_cols]
        y = clean_data[target_col]
        
        lr = LinearRegression()
        lr.fit(X, y)
        r2 = lr.score(X, y)
        
        # Guard against perfect collinearity division by zero
        vif = 1.0 / max(1.0 - r2, 1e-5)
        status = "Prune (>5.0)" if vif > 5.0 else "Retain (Safe)"
        
        vif_records.append({
            'Feature': target_col,
            'R_squared': round(r2, 4),
            'VIF': round(vif, 2),
            'Status': status
        })
        
    vif_df = pd.DataFrame(vif_records).sort_values(by='VIF', ascending=False)
    return vif_df


if __name__ == "__main__":
    from dataset import load_or_generate_data
    df = load_or_generate_data()
    df_eng = engineer_domain_features(df)
    
    numeric_check = [
        'tenure_months', 'contract_arr', 'active_seats',
        'trailing_30d_logins', 'api_calls_30d', 'activity_velocity',
        'friction_index', 'seat_utilization_ratio'
    ]
    vif_df = calculate_vif_scorecard(df_eng, numeric_check)
    print("\n[+] Variance Inflation Factor (VIF) Scorecard:")
    print(vif_df.to_string(index=False))
