"""
src/api.py
==========
FastAPI Production REST Serving Microservice for ChurnGuard-ML.

Implements:
  1. Low-latency synchronous single-account inference (/predict).
  2. Bulk batch scoring for CRM synchronization (/batch_predict).
  3. System health check and model version auditing (/health).
  4. Pydantic payload validation with bounded schema contracts.

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Project: Machine Learning Model Development & Evaluation Plan (Week 3)
Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3
"""

import os
import joblib
import pandas as pd
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from features import engineer_domain_features

# -----------------------------------------------------------------------------
# FastAPI Application & Model Initialization
# -----------------------------------------------------------------------------
app = FastAPI(
    title="ChurnGuard-ML Inference API",
    description="Production REST microservice for Enterprise Customer Churn Prediction & Risk Mitigation",
    version="1.0.0",
    contact={
        "name": "Sumarjana Biswas",
        "email": "sumarjanabiswas690@gmail.com",
        "url": "https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3"
    }
)

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "champion_pipeline.joblib")
_model_artifact: Optional[Dict[str, Any]] = None


def get_model():
    """Lazy loader for serialized champion pipeline artifact."""
    global _model_artifact
    if _model_artifact is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(
                f"Model artifact not found at '{MODEL_PATH}'. "
                f"Please run 'python src/train.py' before launching the API."
            )
        _model_artifact = joblib.load(MODEL_PATH)
    return _model_artifact


# -----------------------------------------------------------------------------
# Pydantic Request & Response Schemas
# -----------------------------------------------------------------------------
class CustomerTelemetryPayload(BaseModel):
    account_id: str = Field(..., examples=["ACC-10492"], description="Unique customer account identifier")
    tenure_months: int = Field(..., ge=1, le=120, examples=[14], description="Account age in active subscription months")
    contract_arr: float = Field(..., ge=100.0, examples=[12000.0], description="Annual Recurring Revenue in USD")
    contract_tier: str = Field(..., examples=["Growth"], description="Contract tier: 'Starter', 'Growth', or 'Enterprise'")
    industry: str = Field(..., examples=["Technology"], description="Customer commercial sector")
    billing_cycle: str = Field(..., examples=["Annual"], description="Billing frequency: 'Monthly' or 'Annual'")
    licensed_seats: int = Field(..., ge=1, examples=[25], description="Total contracted team seat licenses")
    active_seats: int = Field(..., ge=0, examples=[20], description="Active user seats engaged in trailing 30 days")
    trailing_30d_logins: int = Field(..., ge=0, examples=[45], description="Platform logins during trailing 30 days")
    trailing_90d_logins: int = Field(..., ge=0, examples=[180], description="Platform logins during trailing 90 days")
    api_calls_30d: int = Field(0, ge=0, examples=[3500], description="API invocation count in last 30 days")
    feature_exports_30d: int = Field(0, ge=0, examples=[12], description="Data reports/exports generated in last 30 days")
    storage_used_gb: float = Field(1.0, ge=0.0, examples=[42.5], description="Cloud storage consumed in GB")
    open_escalated_tickets: int = Field(0, ge=0, examples=[1], description="Active unresolved tier-2/3 support escalations")
    avg_resolution_hours: float = Field(12.0, ge=0.0, examples=[36.5], description="Average support ticket resolution time in hours")
    monthly_ticket_minutes: float = Field(60.0, ge=0.0, examples=[180.0], description="Total time spent on customer support interactions")
    csat_score: Optional[float] = Field(None, ge=1.0, le=5.0, examples=[3.0], description="Customer satisfaction rating (1-5, or null if unrated)")


class PredictionResponse(BaseModel):
    account_id: str
    churn_probability: float
    risk_tier: str
    action_required: bool
    recommended_action: str


class BatchPredictionRequest(BaseModel):
    accounts: List[CustomerTelemetryPayload]


class BatchPredictionResponse(BaseModel):
    total_accounts: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    predictions: List[PredictionResponse]


# -----------------------------------------------------------------------------
# REST API Endpoints
# -----------------------------------------------------------------------------
@app.get("/", tags=["General"])
def read_root():
    return {
        "service": "ChurnGuard-ML Inference API",
        "author": "Sumarjana Biswas",
        "email": "sumarjanabiswas690@gmail.com",
        "repository": "https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3",
        "status": "Online",
        "documentation": "/docs"
    }


@app.get("/health", tags=["Monitoring"])
def health_check():
    try:
        artifact = get_model()
        return {
            "status": "HEALTHY",
            "model_version": artifact.get("version", "1.0.0"),
            "model_author": artifact.get("author", "Sumarjana Biswas"),
            "decision_threshold": artifact.get("decision_threshold", 0.35),
            "features_monitored": len(artifact.get("feature_cols", []))
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model artifact unavailable: {str(e)}"
        )


@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
def predict_single_account(payload: CustomerTelemetryPayload):
    """
    Computes real-time calibrated churn probability and risk tier for a single customer.
    """
    try:
        artifact = get_model()
        model = artifact['model']
        feature_cols = artifact['feature_cols']
        threshold = artifact.get('decision_threshold', 0.35)
        
        # Ingest payload and calculate domain engineered features
        raw_dict = payload.model_dump()
        df_raw = pd.DataFrame([raw_dict])
        df_eng = engineer_domain_features(df_raw)
        
        X_input = df_eng[feature_cols]
        prob = float(model.predict_proba(X_input)[0, 1])
        
        if prob >= threshold:
            risk_tier = "High"
            action_required = True
            rec_action = (
                "Priority 1: Trigger CSM Executive Retention Outreach. "
                "Investigate unresolved escalations and schedule quarterly account review."
            )
        elif prob >= 0.20:
            risk_tier = "Medium"
            action_required = False
            rec_action = (
                "Priority 2: Enroll in Automated Re-engagement Flow. "
                "Send product feature tutorials and proactive satisfaction pulse."
            )
        else:
            risk_tier = "Low"
            action_required = False
            rec_action = "Standard Cadence: Account healthy. Monitor for upsell opportunities."
            
        return PredictionResponse(
            account_id=payload.account_id,
            churn_probability=round(prob, 4),
            risk_tier=risk_tier,
            action_required=action_required,
            recommended_action=rec_action
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )


@app.post("/batch_predict", response_model=BatchPredictionResponse, tags=["Inference"])
def batch_predict(batch: BatchPredictionRequest):
    """
    Scores up to 1,000 accounts simultaneously for weekly CRM and marketing synchronization.
    """
    try:
        artifact = get_model()
        model = artifact['model']
        feature_cols = artifact['feature_cols']
        threshold = artifact.get('decision_threshold', 0.35)
        
        raw_list = [acc.model_dump() for acc in batch.accounts]
        df_raw = pd.DataFrame(raw_list)
        df_eng = engineer_domain_features(df_raw)
        
        X_input = df_eng[feature_cols]
        probs = model.predict_proba(X_input)[:, 1]
        
        predictions: List[PredictionResponse] = []
        high_cnt, med_cnt, low_cnt = 0, 0, 0
        
        for acc_payload, prob_val in zip(batch.accounts, probs):
            prob = float(prob_val)
            if prob >= threshold:
                risk_tier = "High"
                action_required = True
                rec_action = "Priority 1: Immediate CSM Retention Intervention."
                high_cnt += 1
            elif prob >= 0.20:
                risk_tier = "Medium"
                action_required = False
                rec_action = "Priority 2: Re-engagement & Onboarding Check-in."
                med_cnt += 1
            else:
                risk_tier = "Low"
                action_required = False
                rec_action = "Standard Cadence: Healthy account."
                low_cnt += 1
                
            predictions.append(
                PredictionResponse(
                    account_id=acc_payload.account_id,
                    churn_probability=round(prob, 4),
                    risk_tier=risk_tier,
                    action_required=action_required,
                    recommended_action=rec_action
                )
            )
            
        return BatchPredictionResponse(
            total_accounts=len(predictions),
            high_risk_count=high_cnt,
            medium_risk_count=med_cnt,
            low_risk_count=low_cnt,
            predictions=predictions
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch inference error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
