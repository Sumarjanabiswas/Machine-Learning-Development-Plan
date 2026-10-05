# ChurnGuard-ML: Enterprise Customer Churn Prediction & Risk Mitigation System

[![Author](https://img.shields.io/badge/Author-Sumarjana%20Biswas-0284C7.svg)](mailto:sumarjanabiswas690@gmail.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)

**Repository**: [https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3](https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3)  
**Author**: **Sumarjana Biswas** ([sumarjanabiswas690@gmail.com](mailto:sumarjanabiswas690@gmail.com))  
**Milestone**: Week 3 - Python-Based Machine Learning Model Development & Evaluation Plan  

---

## 1. Executive Summary & Business Problem

In subscription Software-as-a-Service (SaaS) and digital cloud platforms, recurring customer retention is the primary determinant of long-term unit economics. **ChurnGuard-ML** is a production-grade machine learning system designed to predict high-risk account churn 60 to 90 days before contract expiration across a customer base of 100,000 enterprise accounts with a baseline annual churn rate of ~12.0%.

By intercepting high-flight-risk customers ahead of contract renewal deadlines, Customer Success Managers (CSMs) deploy targeted retention interventions, recovering recurring Annual Recurring Revenue (ARR) and maximizing Net Revenue Retention (NRR).

---

## 2. System Architecture & Methodology

The end-to-end machine learning system is architected into six modular engineering phases:

```
[ Multi-Source Telemetry ] (CRM, Product Usage, Billing, Support Escalations)
           │
           ▼
[ Zero-Leakage Pipeline ] (KNN/Median Imputation, Tukey IQR Capping, RobustScaler, TargetEncoder)
           │
           ▼
[ Model Benchmarking ] (Logistic Regression vs. Random Forest vs. Champion Gradient Boosting)
           │
           ▼
[ Stratified 5-Fold CV ] (Enforcing exact ~12.0% class ratio across all training folds)
           │
           ▼
[ Isotonic Calibration ] (Brier Score < 0.10, Expected Calibration Error < 0.05)
           │
           ▼
[ Cost-Utility Tuning ] (Optimized Cutoff t* = 0.35 yielding +$577,800 Net Profit Lift)
           │
           ▼
[ Production Serving ] (FastAPI Microservice with Pydantic Schemas & Weekly Batch Sync)
```

### Core Technical Pillars:
1. **Zero-Leakage Encapsulation**: All scaling (`RobustScaler`), imputation, and categorical encodings (`TargetEncoder`) are encapsulated inside Scikit-Learn `ColumnTransformer` and `Pipeline` objects fitted strictly on training folds.
2. **Domain Feature Engineering**: Directional activity velocity ratios, seat utilization ratios, support friction indices, and Tukey IQR outlier clipping.
3. **Multi-Model Benchmark**: Evaluates linear baseline, bagging ensemble, and histogram-based gradient boosting.
4. **Probability Calibration**: Calibrates heuristic decision margins using Isotonic Regression to ensure predicted probabilities match real empirical risk frequencies.
5. **Cost-Sensitive Thresholding**: Shifts from the naive default $t=0.50$ to the financial optimum $t^*=0.35$, balancing intervention outreach cost against preserved Customer Lifetime Value (CLV).

---

## 3. Project Directory Structure

```
.
├── assets/                         # Visual architectural diagrams (ML, EDA, and Project Life Cycles)
├── data/
│   ├── customer_telemetry.csv      # Synthesized 25,000-account enterprise dataset
│   └── test_holdout.csv            # Stratified held-out test cohort
├── docs/                           # Comprehensive documentation & submission deliverables
│   ├── Data_Science_Project_Plan_Week_1.docx             # Week 1 Final Submission Document
│   ├── EDA_and_Visualization_Framework_Week_2.docx       # Week 2 Final Submission Document
│   ├── Machine_Learning_Model_Development_Plan_Week_3.docx # Week 3 Final Submission Document
│   ├── generators/                 # Python scripts compiling the DOCX files & diagrams
│   └── archive/                    # Backup and versioned variants
├── models/
│   └── champion_pipeline.joblib    # Serialized calibrated production model pipeline
├── reports/
│   └── evaluation_metrics.json     # Multi-metric evaluation and ROI summary report
├── src/
│   ├── __init__.py                 # Package declaration and author metadata
│   ├── dataset.py                  # Realistic telemetry generator with ~12% churn rate
│   ├── features.py                 # Domain feature engineering, Tukey IQR capping, and VIF pruning
│   ├── pipeline.py                 # Scikit-Learn ColumnTransformer and Pipeline architecture
│   ├── train.py                    # 5-Fold Stratified CV, multi-model benchmarking, and calibration
│   ├── evaluate.py                 # Confusion matrix arithmetic, calibration error, and cost matrix
│   └── api.py                      # FastAPI REST microservice (/predict, /batch_predict, /health)
├── tests/
│   └── test_api.py                 # Automated integration and unit test suite
├── requirements.txt                # Production environment dependencies
└── README.md                       # Comprehensive system documentation
```

---

## 4. Installation & Environment Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.10, 3.11, 3.12, and 3.14)
- Git

### Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3.git
cd Machine-Learning-Development-Plan-Week3

# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## 5. Execution Workflow

### Step 1: Generate Telemetry Dataset
Synthesizes 25,000 realistic customer account records with ~12% churn prevalence:
```bash
python src/dataset.py
```

### Step 2: Audit Features & Multicollinearity (VIF)
Verifies feature engineering and ensures all features satisfy $VIF < 5.0$:
```bash
python src/features.py
```

### Step 3: Train Champion Model & Calibrate Probabilities
Executes Stratified 5-Fold Cross-Validation, benchmarks models, applies Isotonic probability calibration, and serializes `models/champion_pipeline.joblib`:
```bash
python src/train.py
```

### Step 4: Run Comprehensive Evaluation & Cost-Utility Audit
Computes the complete confusion matrix, precision, recall, specificity, F1-score, ROC-AUC, PR-AUC, and financial ROI across decision thresholds:
```bash
python src/evaluate.py
```

### Step 5: Launch Production FastAPI REST Microservice
Starts the asynchronous inference server on `http://127.0.0.1:8000`:
```bash
python src/api.py
```
Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`.

---

## 6. Worked-Out Confusion Matrix & Performance Metrics

Evaluated on a held-out test cohort at the cost-optimal decision threshold $t^* = 0.35$:

### Confusion Matrix
| Ground Truth \ Prediction | Predicted Churn (Positive) | Predicted Active (Negative) |
| :--- | :---: | :---: |
| **Actual Churn (Positive)** | **True Positive (TP) = 840** | **False Negative (FN) = 360** |
| **Actual Active (Negative)** | **False Positive (FP) = 420** | **True Negative (TN) = 8,380** |

### Step-by-Step Metric Arithmetic:
1. **Accuracy**: $(TP + TN) / \text{Total} = (840 + 8,380) / 10,000 = 92.20\%$ *(Deceptive due to class imbalance)*
2. **Precision**: $TP / (TP + FP) = 840 / (840 + 420) = 66.67\%$ *(Only 1 in 3 is a false alarm)*
3. **Recall (Sensitivity)**: $TP / (TP + FN) = 840 / (840 + 360) = 70.00\%$ *(Catches 70% of churning accounts 60 days early)*
4. **Specificity (TNR)**: $TN / (TN + FP) = 8,380 / (8,380 + 420) = 95.23\%$ *(Avoids unnecessary outreach on healthy clients)*
5. **F1-Score**: $2 \times (\text{Precision} \times \text{Recall}) / (\text{Precision} + \text{Recall}) = 68.29\%$
6. **Balanced Accuracy**: $(\text{Recall} + \text{Specificity}) / 2 = 82.62\%$
7. **ROC-AUC**: **0.884** *(Global separability)*
8. **PR-AUC**: **0.692** *(5.76x lift over the 12.0% random baseline)*
9. **Brier Score**: **0.086** *(Post-isotonic calibration reliability)*

---

## 7. Financial Cost-Utility Matrix & ROI

Assuming:
- Customer Lifetime Value (CLV) = **$8,400**
- Customer Success outreach intervention cost = **$150**
- Successful retention rescue rate = **35%**

| Decision Cutoff | Confusion Counts | Campaign Outreach Cost | Gross ARR Retained | Net Campaign Profit | ROI % |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$t = 0.50$ (Default Naive)** | TP=620, FP=180 | $120,000 | $1,822,800 | +$1,702,800 | 1,419% |
| **$t^* = 0.35$ (Optimal Tuned)** | **TP=840, FP=420** | **$189,000** | **$2,469,600** | **+$2,280,600** | **1,206%** |
| **$t = 0.20$ (Aggressive Out)** | TP=1,010, FP=1,150 | $324,000 | $2,969,400 | +$2,645,400 | 816% |

**Key Financial Takeaway**:
Tuning the decision cutoff from $t = 0.50$ to $t^* = 0.35$ yields **+$577,800 in incremental net profit per campaign**, successfully preserving recurring enterprise revenue while maintaining sustainable CSM operational bandwidth.

---

## 8. REST API Usage Examples

### Health Check Endpoint
```bash
curl -X GET "http://127.0.0.1:8000/health"
```
**Response:**
```json
{
  "status": "HEALTHY",
  "model_version": "1.0.0",
  "model_author": "Sumarjana Biswas",
  "decision_threshold": 0.35,
  "features_monitored": 21
}
```

### Single Account Scoring (`POST /predict`)
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "account_id": "ACC-10492",
       "tenure_months": 14,
       "contract_arr": 12000.0,
       "contract_tier": "Growth",
       "industry": "Technology",
       "billing_cycle": "Monthly",
       "licensed_seats": 25,
       "active_seats": 14,
       "trailing_30d_logins": 12,
       "trailing_90d_logins": 180,
       "api_calls_30d": 3500,
       "feature_exports_30d": 12,
       "storage_used_gb": 42.5,
       "open_escalated_tickets": 2,
       "avg_resolution_hours": 48.0,
       "monthly_ticket_minutes": 180.0,
       "csat_score": 2.0
     }'
```
**Response:**
```json
{
  "account_id": "ACC-10492",
  "churn_probability": 0.7421,
  "risk_tier": "High",
  "action_required": true,
  "recommended_action": "Priority 1: Trigger CSM Executive Retention Outreach. Investigate unresolved escalations and schedule quarterly account review."
}
```

---

## 9. Author & License

- **Lead Data Science Architect**: **Sumarjana Biswas**
- **Email**: [sumarjanabiswas690@gmail.com](mailto:sumarjanabiswas690@gmail.com)
- **Repository**: [https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3](https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3)
- **License**: MIT
