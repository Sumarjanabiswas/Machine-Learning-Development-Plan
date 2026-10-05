"""
src/pipeline.py
===============
Zero-Leakage Scikit-Learn Pipeline and ColumnTransformer Architecture.

Encapsulates all preprocessing steps (KNN/Median Imputation, RobustScaler,
TargetEncoder / OneHotEncoder) inside a monolithic Scikit-Learn Pipeline,
preventing cross-fold data leakage and guaranteeing deployment portability.

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Project: Machine Learning Model Development & Evaluation Plan (Week 3)
Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan-Week3
"""

import warnings
from typing import List, Optional
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, TargetEncoder
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Optional import for native LightGBM if installed in environment
try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False


def build_preprocessor(
    numeric_cols: List[str],
    categorical_cols: List[str],
    use_knn_imputer: bool = False,
    categorical_encoder: str = 'target'
) -> ColumnTransformer:
    """
    Constructs the Scikit-Learn ColumnTransformer preprocessor.
    
    Parameters:
        numeric_cols: List of continuous and discrete numerical feature names.
        categorical_cols: List of categorical feature names.
        use_knn_imputer: If True, applies KNNImputer(k=5); else SimpleImputer(median).
        categorical_encoder: 'target' for TargetEncoder(cv=5), or 'onehot' for OneHotEncoder.
        
    Returns:
        ColumnTransformer: Fit-ready composite preprocessor.
    """
    if use_knn_imputer:
        num_imputer = KNNImputer(n_neighbors=5)
    else:
        num_imputer = SimpleImputer(strategy='median')
        
    numeric_transformer = Pipeline(steps=[
        ('imputer', num_imputer),
        ('scaler', RobustScaler())
    ])
    
    if categorical_encoder == 'target':
        try:
            cat_encoder = TargetEncoder(smooth='auto', cv=5, random_state=42)
        except Exception:
            cat_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    else:
        cat_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='Missing_Token')),
        ('encoder', cat_encoder)
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ],
        remainder='drop'
    )
    
    return preprocessor


def build_pipeline(
    numeric_cols: List[str],
    categorical_cols: List[str],
    model_type: str = 'champion',
    random_state: int = 42
) -> Pipeline:
    """
    Constructs an end-to-end Scikit-Learn Pipeline combining preprocessing
    and the designated classification algorithm.
    
    Parameters:
        numeric_cols: List of numeric features.
        categorical_cols: List of categorical features.
        model_type: 'champion' (LightGBM / HistGradientBoosting),
                    'random_forest', or 'logistic_regression'.
        random_state: Random seed for deterministic reproducibility.
        
    Returns:
        Pipeline: Complete Scikit-Learn Pipeline.
    """
    preprocessor = build_preprocessor(numeric_cols, categorical_cols)
    
    if model_type == 'champion':
        if HAS_LIGHTGBM:
            classifier = lgb.LGBMClassifier(
                n_estimators=350,
                learning_rate=0.035,
                num_leaves=45,
                subsample=0.82,
                colsample_bytree=0.75,
                reg_alpha=0.15,
                reg_lambda=1.85,
                scale_pos_weight=4.5,
                random_state=random_state,
                verbosity=-1
            )
        else:
            # Native Scikit-Learn histogram-based gradient booster (identical leaf-wise algorithm)
            classifier = HistGradientBoostingClassifier(
                max_iter=350,
                learning_rate=0.035,
                max_leaf_nodes=45,
                l2_regularization=1.85,
                class_weight='balanced',
                random_state=random_state
            )
    elif model_type == 'random_forest':
        classifier = RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            class_weight='balanced',
            random_state=random_state,
            n_jobs=-1
        )
    elif model_type == 'logistic_regression':
        classifier = LogisticRegression(
            penalty='l2',
            C=1.0,
            class_weight='balanced',
            max_iter=1000,
            random_state=random_state
        )
    else:
        raise ValueError(f"Unknown model_type: '{model_type}'. Choose 'champion', 'random_forest', or 'logistic_regression'.")
        
    full_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])
    
    return full_pipeline


if __name__ == "__main__":
    from dataset import generate_synthetic_telemetry
    from features import engineer_domain_features
    
    raw_df = generate_synthetic_telemetry(n_samples=500)
    df = engineer_domain_features(raw_df)
    
    num_cols = [
        'tenure_months', 'contract_arr', 'active_seats', 'trailing_30d_logins',
        'trailing_90d_logins', 'api_calls_30d', 'feature_exports_30d',
        'storage_used_gb', 'open_escalated_tickets', 'avg_resolution_hours',
        'monthly_ticket_minutes', 'csat_score', 'activity_velocity',
        'seat_utilization_ratio', 'friction_index', 'arr_per_licensed_seat'
    ]
    cat_cols = ['contract_tier', 'industry', 'billing_cycle']
    
    pipe = build_pipeline(num_cols, cat_cols, model_type='champion')
    print("[+] Successfully initialized ML pipeline:")
    print(pipe)
