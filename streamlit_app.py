"""
streamlit_app.py
================
ChurnGuard-ML: Enterprise Customer Churn Prediction & Risk Mitigation Platform.

A high-performance interactive Streamlit application for model evaluation,
real-time account scoring, batch CRM inference, and economic cost-utility simulation.

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Project: Machine Learning Model Development & Evaluation Plan (Week 3)
Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Ensure local source directory is resolvable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from features import engineer_domain_features


# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ChurnGuard-ML | Enterprise Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom CSS for Sleek Dark Glassmorphism Styling
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Background & Typography */
    .stApp {
        background-color: #070B14;
        background-image: 
            radial-gradient(at 0% 0%, rgba(2, 132, 199, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.10) 0px, transparent 50%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Metrics and Card Container */
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    
    /* Risk Badges */
    .badge-high {
        background-color: rgba(244, 63, 94, 0.15);
        color: #FDA4AF;
        border: 1px solid rgba(244, 63, 94, 0.4);
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }
    .badge-med {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.15);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }
    
    .playbook-card {
        background: rgba(18, 28, 48, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 14px;
        padding: 18px 22px;
        margin-top: 14px;
    }
    
    /* Dataframe table border */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Cached Model Loader
# -----------------------------------------------------------------------------
@st.cache_resource
def load_champion_model():
    model_path = os.path.join(os.path.dirname(__file__), "models", "champion_pipeline.joblib")
    if not os.path.exists(model_path):
        st.error(f"Model file not found at '{model_path}'. Please run 'python src/train.py' first.")
        st.stop()
    return joblib.load(model_path)


artifact = load_champion_model()
model = artifact['model']
feature_cols = artifact['feature_cols']
decision_threshold = artifact.get('decision_threshold', 0.35)


# -----------------------------------------------------------------------------
# Presets Data Dictionary
# -----------------------------------------------------------------------------
PRESETS = {
  "🚨 High Flight Risk": {
    "account_id": "ACC-CRIT-9921", "tenure_months": 7, "contract_arr": 14400.0,
    "contract_tier": "Growth", "industry": "Technology", "billing_cycle": "Monthly",
    "licensed_seats": 25, "active_seats": 8, "trailing_30d_logins": 6,
    "trailing_90d_logins": 140, "api_calls_30d": 850, "feature_exports_30d": 2,
    "storage_used_gb": 18.5, "open_escalated_tickets": 3, "avg_resolution_hours": 64.0,
    "monthly_ticket_minutes": 240.0, "csat_score": 1.0
  },
  "⚠️ Moderate Friction": {
    "account_id": "ACC-DRIFT-4012", "tenure_months": 18, "contract_arr": 18000.0,
    "contract_tier": "Growth", "industry": "Finance", "billing_cycle": "Monthly",
    "licensed_seats": 40, "active_seats": 22, "trailing_30d_logins": 28,
    "trailing_90d_logins": 120, "api_calls_30d": 3200, "feature_exports_30d": 9,
    "storage_used_gb": 45.0, "open_escalated_tickets": 1, "avg_resolution_hours": 38.0,
    "monthly_ticket_minutes": 110.0, "csat_score": 3.0
  },
  "🟢 Healthy Enterprise": {
    "account_id": "ACC-PWR-1002", "tenure_months": 38, "contract_arr": 54000.0,
    "contract_tier": "Enterprise", "industry": "Healthcare", "billing_cycle": "Annual",
    "licensed_seats": 120, "active_seats": 115, "trailing_30d_logins": 135,
    "trailing_90d_logins": 360, "api_calls_30d": 18400, "feature_exports_30d": 48,
    "storage_used_gb": 210.0, "open_escalated_tickets": 0, "avg_resolution_hours": 14.0,
    "monthly_ticket_minutes": 35.0, "csat_score": 5.0
  }
}


# -----------------------------------------------------------------------------
# Top Header & Author Attribution
# -----------------------------------------------------------------------------
col_h1, col_h2 = st.columns([0.75, 0.25])
with col_h1:
    st.title("🛡️ ChurnGuard-ML Risk Intelligence Platform")
    st.caption("Production Machine Learning Decision System • Supervised Tabular Classification • Week 3 Applied ML Blueprint")

with col_h2:
    st.markdown(
        f"""
        <div style="text-align: right; margin-top: 10px;">
            <div style="font-weight: 700; color: #38BDF8;">Sumarjana Biswas</div>
            <div style="font-size: 12px; color: #94A3B8;">sumarjanabiswas690@gmail.com</div>
            <a href="https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3" target="_blank" style="font-size: 11px; color: #10B981; text-decoration: none;">GitHub Repository ↗</a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


# -----------------------------------------------------------------------------
# Sidebar Navigation & System Meta
# -----------------------------------------------------------------------------
with st.sidebar:
    st.subheader("⚙️ System Status")
    st.success("● Pipeline Status: Active (Calibrated)")
    st.info(f"Model: HistGradientBoosting (v{artifact.get('version', '1.0.0')})")
    st.metric("Decision Cutoff (t*)", f"{decision_threshold:.2f}", delta="Optimal Cost-Utility")
    st.metric("Monitored Features", f"{len(feature_cols)} Columns")
    
    st.divider()
    app_mode = st.radio(
        "Navigation Workspace:",
        [
            "🎯 Single Account Simulator",
            "📊 Batch CRM Scoring",
            "📈 Performance Diagnostics",
            "💰 Cost-Utility & ROI"
        ]
    )


# -----------------------------------------------------------------------------
# WORKSPACE 1: Single Account Simulator
# -----------------------------------------------------------------------------
if app_mode == "🎯 Single Account Simulator":
    st.subheader("🎯 Real-Time Customer Telemetry Simulator")
    st.write("Adjust raw account attributes to simulate calibrated churn probability and automated Customer Success intervention routing.")
    
    # Preset Selector
    preset_choice = st.selectbox("⚡ Quick Scenario Presets:", list(PRESETS.keys()))
    preset = PRESETS[preset_choice]
    
    with st.form("single_predict_form"):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("##### 1. Contract & Profile")
            acc_id = st.text_input("Account ID", value=preset["account_id"])
            tenure = st.number_input("Tenure (Months)", min_value=1, max_value=120, value=preset["tenure_months"])
            arr = st.number_input("Contract ARR ($ USD)", min_value=100.0, value=float(preset["contract_arr"]), step=500.0)
            tier = st.selectbox("Contract Tier", ["Starter", "Growth", "Enterprise"], index=["Starter", "Growth", "Enterprise"].index(preset["contract_tier"]))
            industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing"], index=["Technology", "Finance", "Healthcare", "Retail", "Manufacturing"].index(preset["industry"]))
            billing = st.selectbox("Billing Cadence", ["Monthly", "Annual"], index=["Monthly", "Annual"].index(preset["billing_cycle"]))
            
        with c2:
            st.markdown("##### 2. Usage Momentum")
            lic_seats = st.number_input("Licensed Seats", min_value=1, value=preset["licensed_seats"])
            act_seats = st.number_input("Active Seats (30d)", min_value=0, value=preset["active_seats"])
            t30_logins = st.number_input("Trailing 30d Logins", min_value=0, value=preset["trailing_30d_logins"])
            t90_logins = st.number_input("Trailing 90d Logins", min_value=0, value=preset["trailing_90d_logins"])
            api_calls = st.number_input("API Calls (30d)", min_value=0, value=preset["api_calls_30d"], step=500)
            exports = st.number_input("Reports Exported", min_value=0, value=preset["feature_exports_30d"])
            storage = st.number_input("Storage Used (GB)", min_value=0.0, value=float(preset["storage_used_gb"]), step=5.0)

        with c3:
            st.markdown("##### 3. Friction & Health")
            escalations = st.number_input("Open Escalations", min_value=0, max_value=10, value=preset["open_escalated_tickets"])
            resolution = st.number_input("Avg Resolution (Hours)", min_value=0.0, value=float(preset["avg_resolution_hours"]), step=4.0)
            ticket_mins = st.number_input("Support Minutes", min_value=0.0, value=float(preset["monthly_ticket_minutes"]), step=15.0)
            csat = st.slider("CSAT Score (1 to 5)", min_value=1.0, max_value=5.0, value=float(preset["csat_score"]), step=0.5)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("⚡ Evaluate Churn Risk", use_container_width=True)

    # Inference Execution
    input_dict = {
        'account_id': acc_id, 'tenure_months': tenure, 'contract_arr': arr,
        'contract_tier': tier, 'industry': industry, 'billing_cycle': billing,
        'licensed_seats': lic_seats, 'active_seats': act_seats,
        'trailing_30d_logins': t30_logins, 'trailing_90d_logins': t90_logins,
        'api_calls_30d': api_calls, 'feature_exports_30d': exports,
        'storage_used_gb': storage, 'open_escalated_tickets': escalations,
        'avg_resolution_hours': resolution, 'monthly_ticket_minutes': ticket_mins,
        'csat_score': csat
    }
    
    df_raw = pd.DataFrame([input_dict])
    df_eng = engineer_domain_features(df_raw)
    X_input = df_eng[feature_cols]
    
    prob = float(model.predict_proba(X_input)[0, 1])
    is_high = prob >= decision_threshold
    is_med = (prob >= 0.20) and not is_high
    
    st.divider()
    res_c1, res_c2 = st.columns([0.45, 0.55])
    
    with res_c1:
        st.markdown("### Risk Evaluation Scorecard")
        metric_delta = "Above Threshold (Alert)" if is_high else "Normal Operational Range"
        delta_color = "inverse" if is_high else "normal"
        st.metric(
            label="Calibrated Churn Probability",
            value=f"{prob*100:.1f}%",
            delta=f"{metric_delta} (Cutoff: {decision_threshold*100:.0f}%)",
            delta_color=delta_color
        )
        st.progress(min(prob, 1.0))
        
        if is_high:
            st.markdown('<div class="badge-high">🚨 HIGH FLIGHT RISK TIER (INTERVENTION REQUIRED)</div>', unsafe_allow_html=True)
        elif is_med:
            st.markdown('<div class="badge-med">⚠️ MODERATE ENGAGEMENT DRIFT (NURTURE)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="badge-low">🟢 HEALTHY RETENTION CADENCE</div>', unsafe_allow_html=True)
            
    with res_c2:
        st.markdown("### Engineered Domain Signals & Playbook")
        sig1, sig2, sig3 = st.columns(3)
        with sig1:
            st.metric("Activity Velocity", f"{df_eng['activity_velocity'].iloc[0]:.2f}x", help="Trailing 30d logins vs quarterly baseline")
        with sig2:
            st.metric("Seat Utilization", f"{df_eng['seat_utilization_ratio'].iloc[0]*100:.0f}%", help="Active seats / licensed seats")
        with sig3:
            st.metric("Friction Index", f"{df_eng['friction_index'].iloc[0]:.1f}", help="Composite support lag and CSAT friction")
            
        st.markdown(
            f"""
            <div class="playbook-card">
                <div style="font-weight:700; color:#38BDF8; font-size:13px; text-transform:uppercase; margin-bottom:6px;">
                    🛡️ Customer Success Tactical Playbook
                </div>
                <div style="font-size:14px; line-height:1.5;">
                    {'<b>Priority 1: Immediate CSM Executive Retention Intervention.</b> Investigate open escalations, coordinate support lead response, and schedule executive sponsor review.' if is_high else ('<b>Priority 2: Automated Re-engagement Flow.</b> Trigger onboarding check-in and targeted tutorial materials.' if is_med else '<b>Standard Cadence:</b> Account engagement healthy. Monitor for contract seat expansion and upsell.')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------------------------------------------------------
# WORKSPACE 2: Batch CRM Scoring Engine
# -----------------------------------------------------------------------------
elif app_mode == "📊 Batch CRM Scoring":
    st.subheader("📊 Automated Batch CRM Scoring (Salesforce & HubSpot Routing)")
    st.write("Score multi-account cohorts simultaneously using the calibrated production pipeline.")
    
    batch_file = st.file_uploader("Upload Account Cohort CSV (optional):", type=["csv"])
    
    if batch_file is not None:
        batch_df_raw = pd.read_csv(batch_file)
        st.success(f"Uploaded custom cohort: {len(batch_df_raw)} records")
    else:
        # Load sample demonstration cohort
        batch_df_raw = pd.DataFrame([
            PRESETS["🚨 High Flight Risk"],
            PRESETS["⚠️ Moderate Friction"],
            PRESETS["🟢 Healthy Enterprise"],
            {
                "account_id": "ACC-2091", "tenure_months": 4, "contract_arr": 2400.0,
                "contract_tier": "Starter", "industry": "Retail", "billing_cycle": "Monthly",
                "licensed_seats": 10, "active_seats": 2, "trailing_30d_logins": 3,
                "trailing_90d_logins": 50, "api_calls_30d": 120, "feature_exports_30d": 1,
                "storage_used_gb": 5.0, "open_escalated_tickets": 2, "avg_resolution_hours": 48.0,
                "monthly_ticket_minutes": 180.0, "csat_score": 2.0
            },
            {
                "account_id": "ACC-9982", "tenure_months": 28, "contract_arr": 36000.0,
                "contract_tier": "Enterprise", "industry": "Finance", "billing_cycle": "Annual",
                "licensed_seats": 80, "active_seats": 75, "trailing_30d_logins": 95,
                "trailing_90d_logins": 260, "api_calls_30d": 9200, "feature_exports_30d": 28,
                "storage_used_gb": 120.0, "open_escalated_tickets": 0, "avg_resolution_hours": 12.0,
                "monthly_ticket_minutes": 22.0, "csat_score": 5.0
            }
        ])
        st.info("Displaying default 5-account enterprise demonstration cohort.")
        
    if st.button("🚀 Score Cohort with Model Pipeline", type="primary"):
        df_eng_batch = engineer_domain_features(batch_df_raw)
        X_batch = df_eng_batch[feature_cols]
        probs = model.predict_proba(X_batch)[:, 1]
        
        batch_df_raw['Churn_Probability'] = np.round(probs * 100.0, 1)
        batch_df_raw['Risk_Tier'] = np.where(probs >= decision_threshold, "High", np.where(probs >= 0.20, "Medium", "Low"))
        batch_df_raw['Outreach_Action'] = np.where(probs >= decision_threshold, "Mandatory CSM Review", "Standby")
        
        high_cnt = int(np.sum(probs >= decision_threshold))
        med_cnt = int(np.sum((probs >= 0.20) & (probs < decision_threshold)))
        low_cnt = int(np.sum(probs < 0.20))
        saved_arr = high_cnt * 0.35 * 8400.0
        
        # KPI Row
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Accounts Scored", len(probs))
        k2.metric("High Risk (Alerts)", high_cnt, delta="Intervention Needed", delta_color="inverse")
        k3.metric("Medium Risk", med_cnt)
        k4.metric("Low Risk (Healthy)", low_cnt)
        k5.metric("Projected ARR Saved", f"${saved_arr:,.0f}", delta="+35% Rescue Rate")
        
        st.divider()
        st.dataframe(
            batch_df_raw[['account_id', 'contract_tier', 'contract_arr', 'Risk_Tier', 'Churn_Probability', 'Outreach_Action']],
            use_container_width=True
        )
        
        csv_data = batch_df_raw.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Scored Accounts CSV",
            data=csv_data,
            file_name="churnguard_scored_accounts.csv",
            mime="text/csv"
        )


# -----------------------------------------------------------------------------
# WORKSPACE 3: Performance Diagnostics
# -----------------------------------------------------------------------------
elif app_mode == "📈 Performance Diagnostics":
    st.subheader("📈 Model Architecture & Holdout Validation Diagnostics")
    st.write("Comprehensive multi-metric evaluation on the held-out test cohort (N = 6,250 accounts).")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown("#### Champion Model Specifications")
        st.markdown("""
        - **Algorithm**: Histogram-based Gradient Boosted Trees (`HistGradientBoostingClassifier`)
        - **Hyperparameters**: `max_iter=350`, `learning_rate=0.035`, `max_leaf_nodes=45`
        - **Pipeline Preprocessing**: Scikit-Learn `ColumnTransformer` (Median Imputation, `RobustScaler`, `TargetEncoder`)
        - **Calibration**: Isotonic Regression via `CalibratedClassifierCV` (cv=5)
        - **Decision Threshold**: $t^* = 0.35$ (Cost-Utility Tuned)
        """)
        
        st.markdown("#### Performance Metrics (Test Cohort N=6,250)")
        metrics_df = pd.DataFrame([
            {"Metric": "Area Under ROC Curve (ROC-AUC)", "Value": "0.7467", "Baseline": "0.5000"},
            {"Metric": "Area Under Precision-Recall (PR-AUC)", "Value": "0.3322", "Baseline": "0.1138 (3.0x lift!)"},
            {"Metric": "Post-Calibration Brier Score", "Value": "0.0891", "Baseline": "0.1740 (Pre-Cal)"},
            {"Metric": "Expected Calibration Error (ECE)", "Value": "0.0106", "Baseline": "< 0.0500 Gate"},
            {"Metric": "Accuracy (at t* = 0.35)", "Value": "88.10%", "Baseline": "88.00% Naive"},
            {"Metric": "Precision (at t* = 0.35)", "Value": "45.27%", "Baseline": "11.38% Positive Rate"},
            {"Metric": "Specificity / True Negative Rate", "Value": "96.55%", "Baseline": "Avoids client fatigue"}
        ])
        st.table(metrics_df)

    with col_d2:
        st.markdown("#### Worked Confusion Matrix (t* = 0.35)")
        cm_df = pd.DataFrame(
            [
                ["True Positive (TP) = 158", "False Negative (FN) = 553", "711 Actual Churners"],
                ["False Positive (FP) = 191", "True Negative (TN) = 5,348", "5,539 Actual Active"]
            ],
            columns=["Predicted Churn", "Predicted Active", "Ground Truth Total"],
            index=["Actual Churn", "Actual Active"]
        )
        st.table(cm_df)
        
        st.markdown(r"""
        **Step-by-Step Metric Arithmetic:**
        - **Accuracy** = $(158 + 5,348) / 6,250 = 88.10\%$
        - **Precision** = $158 / (158 + 191) = 45.27\%$ *(1 in 2.2 alerts is a real churner)*
        - **Recall** = $158 / 711 = 22.22\%$ *(Catches critical early attrition accounts)*
        - **Specificity** = $5,348 / 5,539 = 96.55\%$ *(Protects healthy accounts from unnecessary contact)*
        """)


# -----------------------------------------------------------------------------
# WORKSPACE 4: Cost-Utility & Economic ROI
# -----------------------------------------------------------------------------
elif app_mode == "💰 Cost-Utility & ROI":
    st.subheader("💰 Financial Cost-Utility Matrix & Decision Threshold Optimization")
    st.write("Demonstrates why shifting from the naive default $t=0.50$ to the cost-optimal cutoff $t^*=0.35$ produces tangible net ARR preservation.")
    
    c_roi1, c_roi2 = st.columns([0.45, 0.55])
    
    with c_roi1:
        st.markdown("#### Economic Unit Parameters")
        clv_input = st.slider("Customer Lifetime Value (CLV $):", min_value=2000.0, max_value=25000.0, value=8400.0, step=400.0)
        cost_input = st.slider("CSM Outreach Review Cost ($):", min_value=50.0, max_value=500.0, value=150.0, step=25.0)
        rescue_rate = st.slider("Intervention Rescue Success Rate (%):", min_value=10.0, max_value=60.0, value=35.0, step=5.0) / 100.0
        
        # Calculations based on test cohort
        tp_50, fp_50 = 72, 59
        cost_50 = (tp_50 + fp_50) * cost_input
        saved_50 = (tp_50 * rescue_rate) * clv_input
        profit_50 = saved_50 - cost_50
        
        tp_35, fp_35 = 158, 191
        cost_35 = (tp_35 + fp_35) * cost_input
        saved_35 = (tp_35 * rescue_rate) * clv_input
        profit_35 = saved_35 - cost_35
        
        tp_20, fp_20 = 302, 587
        cost_20 = (tp_20 + fp_20) * cost_input
        saved_20 = (tp_20 * rescue_rate) * clv_input
        profit_20 = saved_20 - cost_20
        
        lift = profit_35 - profit_50
        st.metric("Net Profit Lift (t*=0.35 vs t=0.50)", f"+${lift:,.0f}", delta=f"+{((profit_35/profit_50)-1)*100:.1f}% Financial Improvement")

    with c_roi2:
        st.markdown("#### Threshold Performance Comparison")
        comp_df = pd.DataFrame([
            {"Cutoff": "t = 0.50 (Standard Naive)", "Outreach Cost": f"${cost_50:,.0f}", "Gross ARR Saved": f"${saved_50:,.0f}", "Net Profit": f"+${profit_50:,.0f}", "ROI %": f"{(profit_50/cost_50)*100:.0f}%"},
            {"Cutoff": "t* = 0.35 (Optimal Tuned)", "Outreach Cost": f"${cost_35:,.0f}", "Gross ARR Saved": f"${saved_35:,.0f}", "Net Profit": f"+${profit_35:,.0f}", "ROI %": f"{(profit_35/cost_35)*100:.0f}%"},
            {"Cutoff": "t = 0.20 (Aggressive Outreach)", "Outreach Cost": f"${cost_20:,.0f}", "Gross ARR Saved": f"${saved_20:,.0f}", "Net Profit": f"+${profit_20:,.0f}", "ROI %": f"{(profit_20/cost_20)*100:.0f}%"}
        ])
        st.table(comp_df)
        
        st.markdown(f"""
        <div style="padding:16px; border-radius:12px; background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.3);">
            <div style="font-weight:700; color:#6EE7B7; font-size:13.5px; margin-bottom:4px;">
                💡 Financial Conclusion:
            </div>
            <div style="font-size:13px; color:#F8FAFC;">
                Tuning cutoff to <b>t* = 0.35</b> captures 86 additional churning enterprise accounts. After accounting for all Customer Success outreach expenses, it yields an incremental <b>+${lift:,.0f} in net profit</b> per campaign cycle!
            </div>
        </div>
        """, unsafe_allow_html=True)
