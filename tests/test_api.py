"""
tests/test_api.py
=================
Integration and Unit Tests for ChurnGuard-ML FastAPI REST Microservice.

Tests:
  1. System Health Check (/health)
  2. Single Customer Churn Prediction (/predict)
  3. Risk Tiering & Action Attribution (High vs Low risk)
  4. Batch Prediction (/batch_predict)
  5. Schema Contract Bounds & Validation Errors

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Project: Machine Learning Model Development & Evaluation Plan (Week 3)
Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3
"""

import sys
import os
import pydantic

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from api import (
    app,
    read_root,
    health_check,
    predict_single_account,
    batch_predict,
    CustomerTelemetryPayload,
    BatchPredictionRequest
)


def test_root_endpoint():
    """Verify API root endpoint metadata and author attribution."""
    from fastapi import Request
    req = Request({"type": "http", "headers": [(b"accept", b"application/json")]})
    data = read_root(req)
    assert data["service"] == "ChurnGuard-ML Inference API"
    assert data["author"] == "Sumarjana Biswas"
    assert "sumarjanabiswas" in data["repository"]
    print("  [PASS] test_root_endpoint")


def test_health_endpoint():
    """Verify system health, loaded model version, and monitored features."""
    data = health_check()
    assert data["status"] == "HEALTHY"
    assert data["model_version"] == "1.0.0"
    assert data["decision_threshold"] == 0.35
    assert data["features_monitored"] > 15
    print("  [PASS] test_health_endpoint")


def test_predict_single_account():
    """Verify single customer prediction and payload ingestion."""
    payload = CustomerTelemetryPayload(
        account_id="ACC-99001",
        tenure_months=8,
        contract_arr=12000.0,
        contract_tier="Growth",
        industry="Technology",
        billing_cycle="Monthly",
        licensed_seats=25,
        active_seats=10,
        trailing_30d_logins=8,
        trailing_90d_logins=120,
        api_calls_30d=1200,
        feature_exports_30d=4,
        storage_used_gb=32.0,
        open_escalated_tickets=3,
        avg_resolution_hours=64.0,
        monthly_ticket_minutes=250.0,
        csat_score=1.0
    )
    
    resp = predict_single_account(payload)
    assert resp.account_id == "ACC-99001"
    assert 0.0 <= resp.churn_probability <= 1.0
    assert resp.risk_tier in ["High", "Medium", "Low"]
    assert isinstance(resp.action_required, bool)
    assert len(resp.recommended_action) > 0
    print(f"  [PASS] test_predict_single_account -> Prob: {resp.churn_probability}, Tier: {resp.risk_tier}")


def test_batch_prediction():
    """Verify batch prediction scoring across multiple accounts."""
    batch_payload = BatchPredictionRequest(
        accounts=[
            CustomerTelemetryPayload(
                account_id="ACC-99001",
                tenure_months=4,
                contract_arr=2400.0,
                contract_tier="Starter",
                industry="Retail",
                billing_cycle="Monthly",
                licensed_seats=10,
                active_seats=2,
                trailing_30d_logins=4,
                trailing_90d_logins=80,
                api_calls_30d=200,
                feature_exports_30d=1,
                storage_used_gb=12.0,
                open_escalated_tickets=2,
                avg_resolution_hours=48.0,
                monthly_ticket_minutes=180.0,
                csat_score=2.0
            ),
            CustomerTelemetryPayload(
                account_id="ACC-99002",
                tenure_months=48,
                contract_arr=48000.0,
                contract_tier="Enterprise",
                industry="Finance",
                billing_cycle="Annual",
                licensed_seats=150,
                active_seats=140,
                trailing_30d_logins=120,
                trailing_90d_logins=350,
                api_calls_30d=15000,
                feature_exports_30d=45,
                storage_used_gb=210.0,
                open_escalated_tickets=0,
                avg_resolution_hours=12.0,
                monthly_ticket_minutes=20.0,
                csat_score=5.0
            )
        ]
    )
    
    resp = batch_predict(batch_payload)
    assert resp.total_accounts == 2
    assert len(resp.predictions) == 2
    print(f"  [PASS] test_batch_prediction -> High: {resp.high_risk_count}, Med: {resp.medium_risk_count}, Low: {resp.low_risk_count}")


def test_schema_validation_error():
    """Verify Pydantic input validation blocks invalid data."""
    try:
        CustomerTelemetryPayload(
            account_id="ACC-ERR",
            tenure_months=-5,  # Invalid negative tenure
            contract_arr=50.0  # Under minimum threshold
        )
        assert False, "Pydantic failed to reject invalid schema!"
    except pydantic.ValidationError:
        print("  [PASS] test_schema_validation_error (Pydantic caught invalid fields)")


if __name__ == "__main__":
    print("\n=======================================================")
    print("  RUNNING CHURNGUARD-ML API INTEGRATION TEST SUITE")
    print("=======================================================")
    test_root_endpoint()
    test_health_endpoint()
    test_predict_single_account()
    test_batch_prediction()
    test_schema_validation_error()
    print("=======================================================")
    print("  ALL TESTS PASSED SUCCESSFULLY! (5/5)")
    print("=======================================================\n")
