"""
src/evaluate.py
===============
Diagnostic Evaluation Suite, Confusion Matrix Arithmetic, and Financial Cost-Utility Matrix.

Generates:
  1. Complete Confusion Matrix breakdown (TP, FP, FN, TN).
  2. Step-by-step evaluation metrics (Precision, Recall, Specificity, F1, Balanced Accuracy, ROC-AUC, PR-AUC).
  3. Probability Calibration diagnostics (Brier Score, Expected Calibration Error).
  4. Economic Cost-Utility Matrix comparing decision thresholds (t=0.50, t*=0.35, t=0.20).
  5. JSON summary export to 'reports/evaluation_metrics.json'.

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Project: Machine Learning Model Development & Evaluation Plan (Week 3)
Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any
from sklearn.metrics import (
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from features import engineer_domain_features


def compute_expected_calibration_error(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """
    Computes Expected Calibration Error (ECE) across n_bins equal-width bins.
    ECE = Sum_b ( (N_b / N) * |acc(b) - conf(b)| )
    """
    bin_limits = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n_samples = len(y_true)
    
    for i in range(n_bins):
        bin_lower = bin_limits[i]
        bin_upper = bin_limits[i + 1]
        
        in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper if i < n_bins - 1 else y_prob <= bin_upper)
        bin_count = np.sum(in_bin)
        
        if bin_count > 0:
            bin_acc = np.mean(y_true[in_bin])
            bin_conf = np.mean(y_prob[in_bin])
            ece += (bin_count / n_samples) * np.abs(bin_acc - bin_conf)
            
    return float(ece)


def evaluate_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float,
    clv: float = 8400.0,
    outreach_cost: float = 150.0,
    rescue_rate: float = 0.35
) -> Dict[str, Any]:
    """
    Evaluates classification performance and financial ROI at a designated decision cutoff.
    """
    y_pred = (y_prob >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    
    total = len(y_true)
    acc = (tp + tn) / total
    prec = tp / max(tp + fp, 1)
    rec = tp / max(tp + fn, 1)
    spec = tn / max(tn + fp, 1)
    f1 = 2 * (prec * rec) / max(prec + rec, 1e-6)
    bal_acc = (rec + spec) / 2.0
    
    # Financial metrics (Section 4.6)
    contacted_accounts = tp + fp
    campaign_outreach_cost = contacted_accounts * outreach_cost
    rescued_accounts = tp * rescue_rate
    gross_arr_retained = rescued_accounts * clv
    net_campaign_profit = gross_arr_retained - campaign_outreach_cost
    roi_pct = (net_campaign_profit / max(campaign_outreach_cost, 1.0)) * 100.0
    
    return {
        'threshold': threshold,
        'TP': int(tp),
        'FP': int(fp),
        'FN': int(fn),
        'TN': int(tn),
        'accuracy': round(float(acc), 4),
        'precision': round(float(prec), 4),
        'recall': round(float(rec), 4),
        'specificity': round(float(spec), 4),
        'f1_score': round(float(f1), 4),
        'balanced_accuracy': round(float(bal_acc), 4),
        'contacted_accounts': int(contacted_accounts),
        'campaign_outreach_cost': round(float(campaign_outreach_cost), 2),
        'rescued_accounts': round(float(rescued_accounts), 1),
        'gross_arr_retained': round(float(gross_arr_retained), 2),
        'net_campaign_profit': round(float(net_campaign_profit), 2),
        'roi_percentage': round(float(roi_pct), 2)
    }


def run_evaluation_suite(
    model_path: str = "models/champion_pipeline.joblib",
    test_path: str = "data/test_holdout.csv",
    report_output_path: str = "reports/evaluation_metrics.json"
):
    """
    Executes complete multi-metric diagnostic audit and financial cost-utility analysis.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at '{model_path}'. Please run 'python src/train.py' first.")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Test holdout data not found at '{test_path}'. Please run 'python src/train.py' first.")
        
    print(f"[*] Loading model artifact: {model_path}")
    artifact = joblib.load(model_path)
    model = artifact['model']
    feature_cols = artifact['feature_cols']
    
    print(f"[*] Loading test holdout cohort: {test_path}")
    test_df = pd.read_csv(test_path)
    if 'activity_velocity' not in test_df.columns:
        test_df = engineer_domain_features(test_df)
        
    X_test = test_df[feature_cols]
    y_test = test_df['churn'].values
    
    print(f"[i] Evaluating {len(y_test)} test accounts (Actual Churners: {int(np.sum(y_test))}, Rate: {np.mean(y_test)*100:.2f}%)...")
    y_probs = model.predict_proba(X_test)[:, 1]
    
    # Global Discrimination & Calibration Metrics
    roc_auc = float(roc_auc_score(y_test, y_probs))
    pr_auc = float(average_precision_score(y_test, y_probs))
    brier = float(brier_score_loss(y_test, y_probs))
    ece = float(compute_expected_calibration_error(y_test, y_probs))
    
    # Threshold Analyses: Naive (0.50), Tuned Optimal (0.35), Aggressive (0.20)
    eval_50 = evaluate_threshold(y_test, y_probs, threshold=0.50)
    eval_35 = evaluate_threshold(y_test, y_probs, threshold=0.35)
    eval_20 = evaluate_threshold(y_test, y_probs, threshold=0.20)
    
    # Terminal Display
    print("\n" + "=" * 78)
    print("        CHURNGUARD-ML MODEL EVALUATION SCORECARD & FINANCIAL MATRIX")
    print("=" * 78)
    print(f" Author: {artifact.get('author', 'Sumarjana Biswas')} | Artifact Version: {artifact.get('version', '1.0.0')}")
    print(f" Test Cohort Size: {len(y_test):,} accounts | True Churn Prevalence: {np.mean(y_test)*100:.2f}%\n")
    
    print("--- [1] GLOBAL DISCRIMINATION & CALIBRATION METRICS ---")
    print(f" Area Under ROC Curve (ROC-AUC):        {roc_auc:.4f}  (Baseline Random: 0.500)")
    print(f" Area Under Precision-Recall (PR-AUC):  {pr_auc:.4f}  (Baseline Random: {np.mean(y_test):.4f})")
    print(f" Brier Score:                          {brier:.4f}  (Lower is better, ideal: < 0.10)")
    print(f" Expected Calibration Error (ECE):      {ece:.4f}  (Acceptance gate: < 0.05)\n")
    
    print("--- [2] WORKED-OUT CONFUSION MATRIX AT OPTIMAL CUTOFF (t* = 0.35) ---")
    print(f"  +-------------------------------+-------------------------------+")
    print(f"  | Predicted Churn (Positive)    | Predicted Active (Negative)   |")
    print(f"  +-------------------------------+-------------------------------+")
    print(f"  | True Positive  (TP) = {eval_35['TP']:<7} | False Negative (FN) = {eval_35['FN']:<7} |  Actual Churn:  {eval_35['TP'] + eval_35['FN']:,}")
    print(f"  | False Positive (FP) = {eval_35['FP']:<7} | True Negative  (TN) = {eval_35['TN']:<7} |  Actual Active: {eval_35['FP'] + eval_35['TN']:,}")
    print(f"  +-------------------------------+-------------------------------+\n")
    
    print("--- [3] DETAILED METRIC ARITHMETIC (t* = 0.35) ---")
    print(f"  * Accuracy:           {eval_35['accuracy']*100:.2f}%  ((TP+TN)/Total)")
    print(f"  * Precision:          {eval_35['precision']*100:.2f}%  (TP / (TP + FP))")
    print(f"  * Recall/Sensitivity: {eval_35['recall']*100:.2f}%  (TP / (TP + FN))")
    print(f"  * Specificity (TNR):  {eval_35['specificity']*100:.2f}%  (TN / (TN + FP))")
    print(f"  * F1-Score:           {eval_35['f1_score']*100:.2f}%  (Harmonic mean of Prec & Rec)")
    print(f"  * Balanced Accuracy:  {eval_35['balanced_accuracy']*100:.2f}%  ((Recall + Specificity)/2)\n")
    
    print("--- [4] FINANCIAL COST-UTILITY MATRIX ACROSS DECISION CUTOFFS ---")
    print(f" {'Cutoff':<8} | {'TP / FP':<12} | {'Outreach Cost':<14} | {'Gross ARR Saved':<16} | {'Net Profit':<14} | {'ROI %':<8}")
    print(f" {'-'*8}-+-{'-'*12}-+-{'-'*14}-+-{'-'*16}-+-{'-'*14}-+-{'-'*8}")
    for item in [eval_50, eval_35, eval_20]:
        t_str = f"t = {item['threshold']:.2f}"
        if item['threshold'] == 0.35:
            t_str += " *"
        counts_str = f"{item['TP']} / {item['FP']}"
        cost_str = f"${item['campaign_outreach_cost']:,.0f}"
        gross_str = f"${item['gross_arr_retained']:,.0f}"
        net_str = f"${item['net_campaign_profit']:,.0f}"
        roi_str = f"{item['roi_percentage']:.1f}%"
        print(f" {t_str:<8} | {counts_str:<12} | {cost_str:<14} | {gross_str:<16} | {net_str:<14} | {roi_str:<8}")
        
    lift = eval_35['net_campaign_profit'] - eval_50['net_campaign_profit']
    print(f"\n [+] Financial Decision Conclusion:")
    print(f"     Threshold tuning from default 0.50 to optimal t*=0.35 yields +${lift:,.0f} net profit lift per campaign!\n")
    print("=" * 78)
    
    # Save Report
    report = {
        'metadata': {
            'author': artifact.get('author', 'Sumarjana Biswas'),
            'email': 'sumarjanabiswas690@gmail.com',
            'version': artifact.get('version', '1.0.0'),
            'repository': 'https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3',
            'sample_count': int(len(y_test)),
            'churn_prevalence': round(float(np.mean(y_test)), 4)
        },
        'global_metrics': {
            'roc_auc': round(roc_auc, 4),
            'pr_auc': round(pr_auc, 4),
            'brier_score': round(brier, 4),
            'expected_calibration_error': round(ece, 4)
        },
        'threshold_evaluations': {
            'default_0_50': eval_50,
            'optimal_0_35': eval_35,
            'aggressive_0_20': eval_20
        },
        'financial_assumptions': {
            'customer_lifetime_value_usd': 8400.0,
            'csm_outreach_cost_usd': 150.0,
            'intervention_rescue_success_rate': 0.35,
            'net_profit_lift_from_tuning_usd': round(float(lift), 2)
        }
    }
    
    os.makedirs(os.path.dirname(report_output_path) or ".", exist_ok=True)
    with open(report_output_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"[+] Diagnostic evaluation report successfully saved to: {report_output_path}")


if __name__ == "__main__":
    run_evaluation_suite()
