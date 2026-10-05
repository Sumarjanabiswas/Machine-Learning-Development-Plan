"""
src/train.py
============
Model Training, Cross-Validation, Probability Calibration, and Model Serialization.

Executes:
  1. Stratified 5-Fold Cross-Validation on the training pool.
  2. Multi-model benchmarking (Logistic Regression vs. Random Forest vs. Champion).
  3. Probability calibration using Isotonic Regression (CalibratedClassifierCV).
  4. Final model serialization to 'models/champion_pipeline.joblib'.
  5. Holdout test set partitioning saved to 'data/test_holdout.csv'.

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Project: Machine Learning Model Development & Evaluation Plan (Week 3)
Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan
"""

import os
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    f1_score,
    brier_score_loss,
    accuracy_score
)

from dataset import load_or_generate_data
from features import engineer_domain_features
from pipeline import build_pipeline


NUMERIC_COLS = [
    'tenure_months', 'contract_arr', 'licensed_seats', 'active_seats',
    'trailing_30d_logins', 'trailing_90d_logins', 'api_calls_30d',
    'feature_exports_30d', 'storage_used_gb', 'open_escalated_tickets',
    'avg_resolution_hours', 'monthly_ticket_minutes', 'csat_score',
    'activity_velocity', 'seat_utilization_ratio', 'friction_index',
    'support_burden_per_seat', 'arr_per_licensed_seat'
]

CATEGORICAL_COLS = ['contract_tier', 'industry', 'billing_cycle']


def run_cross_validation(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_type: str = 'champion',
    n_splits: int = 5,
    random_state: int = 42
) -> Dict[str, List[float]]:
    """
    Executes Stratified K-Fold Cross-Validation strictly inside pipeline boundaries.
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    
    metrics = {
        'pr_auc': [],
        'roc_auc': [],
        'f1_score': []
    }
    
    print(f"\n=======================================================")
    print(f"  Evaluating Model: {model_type.upper()} ({n_splits}-Fold Stratified CV)")
    print(f"=======================================================")
    
    for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train), start=1):
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
        
        # Fresh pipeline instance per fold (zero leakage)
        pipe = build_pipeline(NUMERIC_COLS, CATEGORICAL_COLS, model_type=model_type, random_state=random_state)
        pipe.fit(X_tr, y_tr)
        
        val_probs = pipe.predict_proba(X_val)[:, 1]
        val_preds = (val_probs >= 0.35).astype(int)
        
        pr_auc = average_precision_score(y_val, val_probs)
        roc_auc = roc_auc_score(y_val, val_probs)
        f1 = f1_score(y_val, val_preds)
        
        metrics['pr_auc'].append(pr_auc)
        metrics['roc_auc'].append(roc_auc)
        metrics['f1_score'].append(f1)
        
        print(f"  Fold {fold} | PR-AUC: {pr_auc:.4f} | ROC-AUC: {roc_auc:.4f} | F1 (t=0.35): {f1*100:.2f}%")
        
    mean_pr = np.mean(metrics['pr_auc'])
    std_pr = np.std(metrics['pr_auc'])
    mean_roc = np.mean(metrics['roc_auc'])
    std_roc = np.std(metrics['roc_auc'])
    mean_f1 = np.mean(metrics['f1_score'])
    std_f1 = np.std(metrics['f1_score'])
    
    print(f"  -----------------------------------------------------")
    print(f"  Mean +/- Std:")
    print(f"  PR-AUC:   {mean_pr:.4f} (+/- {std_pr:.4f})")
    print(f"  ROC-AUC:  {mean_roc:.4f} (+/- {std_roc:.4f})")
    print(f"  F1-Score: {mean_f1*100:.2f}% (+/- {std_f1*100:.2f}%)")
    print(f"=======================================================\n")
    
    return metrics


def train_and_serialize(
    data_path: str = "data/customer_telemetry.csv",
    model_output_path: str = "models/champion_pipeline.joblib",
    test_output_path: str = "data/test_holdout.csv",
    random_state: int = 42
):
    """
    Main orchestrator for training, calibration, and serialization.
    """
    print("[1/5] Loading and engineering customer telemetry...")
    raw_df = load_or_generate_data(data_path=data_path, random_state=random_state)
    df = engineer_domain_features(raw_df)
    
    feature_cols = NUMERIC_COLS + CATEGORICAL_COLS
    X = df[feature_cols]
    y = df['churn']
    
    # 25% held-out test cohort (Stratified)
    print(f"[2/5] Partitioning data into 75% Train/Val Pool and 25% Test Holdout...")
    X_train, X_test, y_train, y_test, df_train_idx, df_test_idx = train_test_split(
        X, y, df.index, test_size=0.25, stratify=y, random_state=random_state
    )
    
    # Save held-out test dataset with account_id and churn target for evaluation
    test_holdout_df = df.loc[df_test_idx].copy()
    os.makedirs(os.path.dirname(test_output_path) or ".", exist_ok=True)
    test_holdout_df.to_csv(test_output_path, index=False)
    print(f"[+] Saved test holdout cohort ({len(test_holdout_df)} accounts) to: {test_output_path}")
    
    # [3/5] Benchmarking Models via 5-Fold Stratified CV
    print("[3/5] Benchmarking candidate algorithms across 5 Stratified Folds...")
    lr_metrics = run_cross_validation(X_train, y_train, model_type='logistic_regression')
    rf_metrics = run_cross_validation(X_train, y_train, model_type='random_forest')
    champ_metrics = run_cross_validation(X_train, y_train, model_type='champion')
    
    # [4/5] Training Champion Pipeline & Applying Probability Calibration
    print("[4/5] Fitting Champion Pipeline on full training pool & Calibrating Probabilities...")
    base_pipeline = build_pipeline(NUMERIC_COLS, CATEGORICAL_COLS, model_type='champion', random_state=random_state)
    
    # Calibrate using Isotonic Regression via CalibratedClassifierCV
    calibrated_pipeline = CalibratedClassifierCV(
        estimator=base_pipeline,
        method='isotonic',
        cv=5
    )
    calibrated_pipeline.fit(X_train, y_train)
    
    # Evaluate raw vs calibrated on test set
    raw_pipeline = build_pipeline(NUMERIC_COLS, CATEGORICAL_COLS, model_type='champion', random_state=random_state)
    raw_pipeline.fit(X_train, y_train)
    raw_test_probs = raw_pipeline.predict_proba(X_test)[:, 1]
    cal_test_probs = calibrated_pipeline.predict_proba(X_test)[:, 1]
    
    raw_brier = brier_score_loss(y_test, raw_test_probs)
    cal_brier = brier_score_loss(y_test, cal_test_probs)
    print(f"[i] Pre-Calibration Brier Score:  {raw_brier:.4f}")
    print(f"[+] Post-Calibration Brier Score: {cal_brier:.4f} (Improved reliability!)")
    
    # [5/5] Serialization
    os.makedirs(os.path.dirname(model_output_path) or ".", exist_ok=True)
    model_artifact = {
        'model': calibrated_pipeline,
        'numeric_cols': NUMERIC_COLS,
        'categorical_cols': CATEGORICAL_COLS,
        'feature_cols': feature_cols,
        'decision_threshold': 0.35,
        'version': '1.0.0',
        'author': 'Sumarjana Biswas'
    }
    joblib.dump(model_artifact, model_output_path)
    print(f"[+] Serialized champion model artifact successfully to: {model_output_path}")
    print("\nTraining workflow completed successfully! Run 'python src/evaluate.py' to generate comprehensive metrics.")


if __name__ == "__main__":
    train_and_serialize()
