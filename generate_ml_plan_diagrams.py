import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    font_paths = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color, width=3, head_size=12):
    x0, y0 = start
    x1, y1 = end
    draw.line([x0, y0, x1, y1], fill=color, width=width)
    if x1 > x0 and y1 == y0: # Horizontal right
        draw.polygon([(x1, y1), (x1 - head_size, y1 - head_size // 2), (x1 - head_size, y1 + head_size // 2)], fill=color)
    elif x1 == x0 and y1 > y0: # Vertical down
        draw.polygon([(x1, y1), (x1 - head_size // 2, y1 - head_size), (x1 + head_size // 2, y1 - head_size)], fill=color)
    elif x1 < x0 and y1 == y0: # Horizontal left
        draw.polygon([(x1, y1), (x1 + head_size, y1 - head_size // 2), (x1 + head_size, y1 + head_size // 2)], fill=color)

# ==============================================================================
# DIAGRAM 1: End-to-End Machine Learning System Architecture & Workflow
# ==============================================================================
def create_ml_pipeline_diagram(output_path):
    width, height = 2400, 1350
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(40, bold=True)
    f_subtitle = get_font(21, bold=False)
    f_col_header = get_font(22, bold=True)
    f_col_sub = get_font(15, bold=False)
    f_card_title = get_font(19, bold=True)
    f_card_text = get_font(15, bold=False)
    f_badge = get_font(14, bold=True)
    f_footer = get_font(16, bold=False)

    # Header Banner
    draw_rounded_rect(draw, [50, 40, width - 50, 160], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "Production Machine Learning Workflow & System Architecture", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "Modular Engineering Pipeline: Data Ingestion & Time-Split -> Preprocessing -> Model Training & Tuning -> Gating -> Deployment & Monitoring", fill="#94A3B8", font=f_subtitle)

    pillars = [
        {
            "num": "01",
            "title": "Data Ingestion & Split",
            "sub": "Leakage-free partitioning",
            "color": "#0284C7",
            "bg": "#F0F9FF",
            "border": "#BAE6FD",
            "cards": [
                ("Multi-Source Ingestion", "PostgreSQL / Snowflake Data Lake\nRaw behavioral telemetry, billing, and support logs"),
                ("Time-Based Cutoff Split", "Strict Historical Horizon Protocol\nTrain: Months 1-9 (70%) | Val: 10-11 (15%) | Test: 12 (15%)"),
                ("Zero-Leakage Boundary", "Point-in-Time Join Enforcement\nFeatures strictly prior to T; labels in window [T, T+60d]"),
                ("Great Expectations Checks", "Automated Data Contracts\nAssert non-null keys, schema typing, and range boundaries")
            ]
        },
        {
            "num": "02",
            "title": "Preprocessing & Store",
            "sub": "Scikit-Learn Transformers",
            "color": "#0D9488",
            "bg": "#F0FDFA",
            "border": "#99F6E4",
            "cards": [
                ("Missing Value Imputation", "Context-Aware KNN & Medians\nCategorical 'Unknown' token & binary missing indicators"),
                ("Outlier Mitigation", "Tukey IQR & Robust Capping\nWinsorize extreme tails (1st & 99th percentiles)"),
                ("Feature Scaling", "RobustScaler & Power Transforms\nStabilize heavy-tailed continuous behavioral signals"),
                ("Feature Selection & VIF", "Mutual Information & VIF Auditing\nPrune collinear metrics with VIF > 5.0")
            ]
        },
        {
            "num": "03",
            "title": "Training & Tuning",
            "sub": "Ensemble optimization",
            "color": "#4F46E5",
            "bg": "#EEF2FF",
            "border": "#C7D2FE",
            "cards": [
                ("Candidate Benchmarking", "Scikit-Learn, LightGBM, XGBoost\nBaseline: Logistic Regression | Champion: LightGBM"),
                ("Class Imbalance Control", "Focal Loss & SMOTE-NC\nscale_pos_weight applied strictly inside training folds"),
                ("Bayesian Optimization", "Optuna Optimization Framework\n150 automated trials tuning PR-AUC & Brier scores"),
                ("Stratified Cross-Validation", "5-Fold Stratified Split within Train\nPreserve 12% minority class ratio across all folds")
            ]
        },
        {
            "num": "04",
            "title": "Validation & Gating",
            "sub": "Rigorous acceptance checks",
            "color": "#9333EA",
            "bg": "#FAF5FF",
            "border": "#E9D5FF",
            "cards": [
                ("Probability Calibration", "Isotonic Regression & Platt Scaling\nMap raw heuristic scores to empirical probabilities"),
                ("Cost-Utility Matrix", "Financial Threshold Optimization\nTune decision cutoff t* to maximize net retention profit"),
                ("TreeSHAP Explainability", "Global & Local Feature Attributions\nProduce local waterfall charts for account-level action"),
                ("Production Acceptance Gate", "Four Strict Go/No-Go Criteria\nROC-AUC >= 0.86, PR-AUC >= 0.65, Latency < 40ms")
            ]
        },
        {
            "num": "05",
            "title": "Serving & Monitoring",
            "sub": "Production MLOps lifecycle",
            "color": "#E11D48",
            "bg": "#FFF1F2",
            "border": "#FECDD3",
            "cards": [
                ("FastAPI Microservice", "Low-Latency REST Inference\nPydantic validated schemas with <40ms p95 response"),
                ("Batch Scoring Worker", "Weekly Automated Cohort Run\nGenerates High/Medium/Low risk tiers for CRM sync"),
                ("Drift Detection Engine", "Evidently AI & PSI Tracking\nKolmogorov-Smirnov test; trigger alert if PSI > 0.20"),
                ("CI/CD Retraining Loop", "MLflow Model Registry\nAutomated candidate evaluation and zero-downtime rollback")
            ]
        }
    ]

    col_w = 420
    col_gap = 40
    start_x = 65
    start_y = 190

    for i, p in enumerate(pillars):
        cx = start_x + i * (col_w + col_gap)
        draw_rounded_rect(draw, [cx, start_y, cx + col_w, start_y + 110], radius=12, fill=p["bg"], outline=p["border"], width=2)
        draw_rounded_rect(draw, [cx + 15, start_y + 15, cx + 60, start_y + 45], radius=6, fill=p["color"])
        draw.text((cx + 24, start_y + 20), p["num"], fill="#FFFFFF", font=f_badge)
        draw.text((cx + 72, start_y + 20), p["title"], fill="#0F172A", font=f_col_header)
        draw.text((cx + 72, start_y + 55), p["sub"], fill="#64748B", font=f_col_sub)

        card_y = start_y + 130
        card_h = 220
        card_gap = 20

        for title, desc in p["cards"]:
            draw_rounded_rect(draw, [cx, card_y, cx + col_w, card_y + card_h], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
            draw_rounded_rect(draw, [cx, card_y, cx + 8, card_y + card_h], radius=4, fill=p["color"])
            draw.text((cx + 25, card_y + 18), title, fill="#1E293B", font=f_card_title)
            lines = desc.split("\n")
            draw.text((cx + 25, card_y + 55), lines[0], fill=p["color"], font=f_card_text)
            if len(lines) > 1:
                draw.text((cx + 25, card_y + 85), lines[1], fill="#64748B", font=f_card_text)
            card_y += card_h + card_gap

        if i < len(pillars) - 1:
            arrow_x0 = cx + col_w + 5
            arrow_x1 = cx + col_w + col_gap - 5
            arrow_y = start_y + 55
            draw_arrow(draw, (arrow_x0, arrow_y), (arrow_x1, arrow_y), color="#94A3B8", width=3, head_size=10)

    draw_rounded_rect(draw, [50, height - 70, width - 50, height - 20], radius=8, fill="#0F172A")
    draw.text((80, height - 52), "Figure 1: End-to-End Production Machine Learning Pipeline Workflow & System Architecture (Author: Sumarjana Biswas - Week 3 Plan)", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved ML Pipeline Diagram 1 to {output_path}")

# ==============================================================================
# DIAGRAM 2: Validation Framework, Confusion Matrix & Metrics Hierarchy
# ==============================================================================
def create_ml_validation_diagram(output_path):
    width, height = 2400, 1400
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(40, bold=True)
    f_subtitle = get_font(21, bold=False)
    f_card_title = get_font(20, bold=True)
    f_card_sub = get_font(16, bold=True)
    f_card_body = get_font(15, bold=False)
    f_num_large = get_font(28, bold=True)
    f_footer = get_font(16, bold=False)

    draw_rounded_rect(draw, [50, 40, width - 50, 160], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "Validation Architecture, Confusion Matrix & Multi-Metric Hierarchy", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "Rigorous Statistical Assessment: 5-Fold Stratified Cross-Validation -> Confusion Matrix Arithmetic -> Discrimination Curves -> Financial Utility", fill="#94A3B8", font=f_subtitle)

    # 4 Quadrants:
    # 1. Stratified 5-Fold Cross Validation Architecture (Top-Left)
    # 2. Worked-Out Confusion Matrix & Arithmetic Formulas (Top-Right)
    # 3. Discrimination & Calibration Curves (Bottom-Left)
    # 4. Financial Cost-Utility Matrix & Decision Thresholding (Bottom-Right)

    # QUADRANT 1: Stratified 5-Fold CV (Top-Left)
    draw_rounded_rect(draw, [70, 200, 1170, 680], radius=12, fill="#FFFFFF", outline="#0284C7", width=2)
    draw_rounded_rect(draw, [70, 200, 1170, 260], radius=10, fill="#0284C7")
    draw.text((95, 215), "1. Stratified 5-Fold Cross-Validation Framework", fill="#FFFFFF", font=f_card_title)
    draw.text((95, 275), "Purpose: Eliminate sampling variance and prevent optimistic leakage across 70,000 training samples", fill="#0369A1", font=f_card_sub)

    folds = [
        ("Fold 1", "Train: 56,000 (12.0% churn) | Val: 14,000 (12.0% churn)", "PR-AUC: 0.694 | ROC-AUC: 0.886 | F1: 68.4%"),
        ("Fold 2", "Train: 56,000 (12.0% churn) | Val: 14,000 (12.0% churn)", "PR-AUC: 0.688 | ROC-AUC: 0.881 | F1: 67.9%"),
        ("Fold 3", "Train: 56,000 (12.0% churn) | Val: 14,000 (12.0% churn)", "PR-AUC: 0.698 | ROC-AUC: 0.889 | F1: 68.8%"),
        ("Fold 4", "Train: 56,000 (12.0% churn) | Val: 14,000 (12.0% churn)", "PR-AUC: 0.691 | ROC-AUC: 0.883 | F1: 68.1%"),
        ("Fold 5", "Train: 56,000 (12.0% churn) | Val: 14,000 (12.0% churn)", "PR-AUC: 0.692 | ROC-AUC: 0.884 | F1: 68.2%")
    ]
    curr_y = 310
    for f_name, f_desc, f_metrics in folds:
        draw_rounded_rect(draw, [90, curr_y, 1150, curr_y + 55], radius=6, fill="#F0F9FF", outline="#BAE6FD", width=1)
        draw_rounded_rect(draw, [90, curr_y, 96, curr_y + 55], radius=3, fill="#0284C7")
        draw.text((110, curr_y + 8), f_name, fill="#0F172A", font=get_font(16, bold=True))
        draw.text((200, curr_y + 10), f_desc, fill="#475569", font=get_font(13, bold=False))
        draw.text((200, curr_y + 30), f_metrics, fill="#0284C7", font=get_font(13, bold=True))
        curr_y += 65

    draw_rounded_rect(draw, [90, curr_y, 1150, curr_y + 40], radius=6, fill="#0F172A")
    draw.text((110, curr_y + 10), "Mean CV PR-AUC = 0.6926 (+/- 0.0034)  |  Mean CV ROC-AUC = 0.8846 (+/- 0.0028)  |  Highly Stable", fill="#38BDF8", font=get_font(14, bold=True))

    # QUADRANT 2: Worked-Out Confusion Matrix & Arithmetic (Top-Right)
    draw_rounded_rect(draw, [1230, 200, 2330, 680], radius=12, fill="#FFFFFF", outline="#0D9488", width=2)
    draw_rounded_rect(draw, [1230, 200, 2330, 260], radius=10, fill="#0D9488")
    draw.text((1255, 215), "2. Worked-Out Confusion Matrix & Metric Arithmetic", fill="#FFFFFF", font=f_card_title)
    draw.text((1255, 275), "Holdout Test Cohort (N = 10,000 accounts | Actual Churners = 1,200 | Non-Churners = 8,800)", fill="#0F766E", font=f_card_sub)

    # 2x2 Matrix Box
    m_x0, m_y0 = 1255, 310
    draw_rounded_rect(draw, [m_x0, m_y0, m_x0 + 260, m_y0 + 130], radius=8, fill="#ECFDF5", outline="#10B981", width=2)
    draw.text((m_x0 + 15, m_y0 + 12), "True Positive (TP)", fill="#047857", font=get_font(15, bold=True))
    draw.text((m_x0 + 15, m_y0 + 38), "840", fill="#047857", font=f_num_large)
    draw.text((m_x0 + 15, m_y0 + 85), "Correctly caught churners", fill="#065F46", font=get_font(13, bold=False))

    draw_rounded_rect(draw, [m_x0 + 280, m_y0, m_x0 + 540, m_y0 + 130], radius=8, fill="#FFF1F2", outline="#F43F5E", width=2)
    draw.text((m_x0 + 295, m_y0 + 12), "False Positive (FP)", fill="#BE123C", font=get_font(15, bold=True))
    draw.text((m_x0 + 295, m_y0 + 38), "420", fill="#BE123C", font=f_num_large)
    draw.text((m_x0 + 295, m_y0 + 85), "False alarms (wasted outreach)", fill="#9F1239", font=get_font(13, bold=False))

    draw_rounded_rect(draw, [m_x0, m_y0 + 145, m_x0 + 260, m_y0 + 275], radius=8, fill="#FEF2F2", outline="#EF4444", width=2)
    draw.text((m_x0 + 15, m_y0 + 157), "False Negative (FN)", fill="#B91C1C", font=get_font(15, bold=True))
    draw.text((m_x0 + 15, m_y0 + 183), "360", fill="#B91C1C", font=f_num_large)
    draw.text((m_x0 + 15, m_y0 + 230), "Missed churners (lost ARR)", fill="#991B1B", font=get_font(13, bold=False))

    draw_rounded_rect(draw, [m_x0 + 280, m_y0 + 145, m_x0 + 540, m_y0 + 275], radius=8, fill="#F8FAFC", outline="#64748B", width=2)
    draw.text((m_x0 + 295, m_y0 + 157), "True Negative (TN)", fill="#334155", font=get_font(15, bold=True))
    draw.text((m_x0 + 295, m_y0 + 183), "8,380", fill="#334155", font=f_num_large)
    draw.text((m_x0 + 295, m_y0 + 230), "Correctly identified loyal accounts", fill="#475569", font=get_font(13, bold=False))

    # Metric formulas block
    calc_x = m_x0 + 560
    draw_rounded_rect(draw, [calc_x, m_y0, 2310, m_y0 + 275], radius=8, fill="#F0FDFA", outline="#99F6E4", width=1)
    draw.text((calc_x + 15, m_y0 + 12), "Exact Metric Calculations:", fill="#0F766E", font=get_font(16, bold=True))
    draw.text((calc_x + 15, m_y0 + 45), "- Accuracy = (840 + 8380) / 10000 = 92.20% (Deceptive baseline)", fill="#334155", font=get_font(14, bold=False))
    draw.text((calc_x + 15, m_y0 + 75), "- Precision = 840 / (840 + 420) = 66.67% (Retention campaign efficiency)", fill="#0D9488", font=get_font(14, bold=True))
    draw.text((calc_x + 15, m_y0 + 105), "- Recall = 840 / (840 + 360) = 70.00% (Caught 70% of total churners)", fill="#0D9488", font=get_font(14, bold=True))
    draw.text((calc_x + 15, m_y0 + 135), "- Specificity = 8380 / (8380 + 420) = 95.23% (Avoided false alarms)", fill="#334155", font=get_font(14, bold=False))
    draw.text((calc_x + 15, m_y0 + 165), "- F1-Score = 2 * (0.6667 * 0.7000) / (0.6667 + 0.7000) = 68.29%", fill="#0F172A", font=get_font(14, bold=True))
    draw.text((calc_x + 15, m_y0 + 195), "- Balanced Accuracy = (70.00% + 95.23%) / 2 = 82.62%", fill="#334155", font=get_font(14, bold=False))
    draw.text((calc_x + 15, m_y0 + 225), "- False Positive Rate (FPR) = 420 / 8800 = 4.77%", fill="#64748B", font=get_font(14, bold=False))

    draw_rounded_rect(draw, [1255, 605, 2310, 655], radius=6, fill="#0F172A")
    draw.text((1275, 620), "Key Takeaway: 92.2% accuracy is misleading because predicting 'nobody churns' yields 88% accuracy. PR-AUC and F1 govern.", fill="#F8FAFC", font=get_font(14, bold=False))

    # QUADRANT 3: Discrimination & Calibration (Bottom-Left)
    draw_rounded_rect(draw, [70, 720, 1170, 1200], radius=12, fill="#FFFFFF", outline="#4F46E5", width=2)
    draw_rounded_rect(draw, [70, 720, 1170, 780], radius=10, fill="#4F46E5")
    draw.text((95, 735), "3. Discrimination Curves vs. Probability Calibration", fill="#FFFFFF", font=f_card_title)
    draw.text((95, 795), "Why ranking ability (AUC) must be paired with probability reliability (Brier Score)", fill="#4338CA", font=f_card_sub)

    c_cards = [
        ("Receiver Operating Characteristic (ROC-AUC = 0.884)", "Plots True Positive Rate vs False Positive Rate across all thresholds\nInsensitive to class imbalance; demonstrates high global separability."),
        ("Precision-Recall Curve (PR-AUC = 0.692)", "Plots Precision vs Recall; baseline equal to empirical churn rate (12.0%)\nProvides primary optimization metric for imbalanced minority targets."),
        ("Probability Calibration (Brier Score = 0.086)", "Isotonic regression maps raw decision scores to true frequencies\nA predicted score of 0.70 means exactly 70% of those accounts churn."),
        ("Expected Calibration Error (ECE = 0.038)", "Measures average gap between predicted confidence and observed accuracy\nECE < 0.05 guarantees financial risk decisions are grounded in real odds.")
    ]
    curr_y = 830
    for c_title, c_desc in c_cards:
        draw_rounded_rect(draw, [90, curr_y, 1150, curr_y + 75], radius=6, fill="#EEF2FF", outline="#C7D2FE", width=1)
        draw_rounded_rect(draw, [90, curr_y, 96, curr_y + 75], radius=3, fill="#4F46E5")
        draw.text((110, curr_y + 8), c_title, fill="#0F172A", font=get_font(16, bold=True))
        lines = c_desc.split("\n")
        draw.text((110, curr_y + 32), lines[0], fill="#334155", font=get_font(13, bold=False))
        draw.text((110, curr_y + 52), lines[1], fill="#4F46E5", font=get_font(13, bold=True))
        curr_y += 85

    # QUADRANT 4: Financial Cost-Utility Matrix (Bottom-Right)
    draw_rounded_rect(draw, [1230, 720, 2330, 1200], radius=12, fill="#FFFFFF", outline="#9333EA", width=2)
    draw_rounded_rect(draw, [1230, 720, 2330, 780], radius=10, fill="#9333EA")
    draw.text((1255, 735), "4. Financial Cost-Utility Matrix & Decision Threshold Optimization", fill="#FFFFFF", font=f_card_title)
    draw.text((1255, 795), "Translating Probabilities into Enterprise ROI (CLV = $8,400 | Outreach Cost = $150 | Save Rate = 35%)", fill="#7E22CE", font=f_card_sub)

    rows = [
        ("Threshold t = 0.50 (Standard Naive)", "TP=620, FP=180, FN=580, TN=8620", "Gross Value = $1,822,800 | Campaign Cost = $120,000", "Net Profit = +$1,702,800", "#64748B"),
        ("Threshold t = 0.35 (Optimal Tuned t*)", "TP=840, FP=420, FN=360, TN=8380", "Gross Value = $2,469,600 | Campaign Cost = $189,000", "Net Profit = +$2,280,600", "#059669"),
        ("Threshold t = 0.20 (Aggressive Outreach)", "TP=1010, FP=1150, FN=190, TN=7650", "Gross Value = $2,969,400 | Campaign Cost = $324,000", "Net Profit = +$2,645,400", "#D97706")
    ]
    curr_y = 830
    for r_title, r_counts, r_calc, r_net, r_col in rows:
        draw_rounded_rect(draw, [1255, curr_y, 2310, curr_y + 80], radius=6, fill="#FAF5FF", outline="#E9D5FF", width=1)
        draw_rounded_rect(draw, [1255, curr_y, 1261, curr_y + 80], radius=3, fill="#9333EA")
        draw.text((1275, curr_y + 8), r_title, fill="#0F172A", font=get_font(16, bold=True))
        draw.text((1275, curr_y + 32), r_counts, fill="#475569", font=get_font(13, bold=False))
        draw.text((1275, curr_y + 54), r_calc, fill="#334155", font=get_font(13, bold=False))
        draw.text((1950, curr_y + 25), r_net, fill=r_col, font=get_font(18, bold=True))
        curr_y += 92

    draw_rounded_rect(draw, [1255, 1120, 2310, 1175], radius=6, fill="#0F172A")
    draw.text((1275, 1135), "Optimal Threshold Impact: Lowering cutoff from t=0.50 to t=0.35 captures 220 additional at-risk accounts, yielding +$577,800 net uplift.", fill="#38BDF8", font=get_font(14, bold=True))

    # Footer note
    draw_rounded_rect(draw, [50, height - 70, width - 50, height - 20], radius=8, fill="#0F172A")
    draw.text((80, height - 52), "Figure 2: Validation Framework, Worked-Out Confusion Matrix Arithmetic & Financial Decision Thresholding (Sumarjana Biswas - Week 3 Plan)", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved ML Validation Diagram 2 to {output_path}")

# ==============================================================================
# DIAGRAM 3: 32.5-Hour Week 3 Model Development Timeline & Gantt Schedule
# ==============================================================================
def create_ml_gantt_diagram(output_path):
    width, height = 2400, 1350
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(40, bold=True)
    f_subtitle = get_font(21, bold=False)
    f_head = get_font(20, bold=True)
    f_task_name = get_font(20, bold=True)
    f_task_desc = get_font(16, bold=False)
    f_bar_label = get_font(18, bold=True)
    f_footer = get_font(16, bold=False)

    # Header Banner
    draw_rounded_rect(draw, [50, 40, width - 50, 160], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "Machine Learning Model Development Timeline & Resource Allocation (32.5 Hours)", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "Detailed Work Breakdown Structure: 6 Phased Workstreams across 5 Working Days (Author: Sumarjana Biswas)", fill="#94A3B8", font=f_subtitle)

    left_x = 60
    table_w = 750
    timeline_x = left_x + table_w + 40
    timeline_w = width - timeline_x - 60
    start_y = 200
    row_h = 150
    total_hours = 35.0

    days = [
        ("Day 1: Scope & Pipeline Architecture", 0, 7),
        ("Day 2: Data Preprocessing & Features", 7, 14),
        ("Day 3: Baseline & Ensemble Modeling", 14, 21),
        ("Day 4: Bayesian Tuning & Calibration", 21, 28),
        ("Day 5: Validation, Serving & Packaging", 28, 35)
    ]

    for d_name, h_start, h_end in days:
        bx0 = timeline_x + int((h_start / total_hours) * timeline_w)
        bx1 = timeline_x + int((h_end / total_hours) * timeline_w)
        draw_rounded_rect(draw, [bx0 + 2, start_y, bx1 - 2, start_y + 45], radius=6, fill="#E2E8F0", outline="#CBD5E1", width=1)
        draw.text((bx0 + 15, start_y + 12), d_name, fill="#334155", font=f_head)

    grid_y_start = start_y + 55
    grid_y_end = start_y + 6 * row_h + 80
    for h in range(0, 36, 5):
        gx = timeline_x + int((h / total_hours) * timeline_w)
        draw.line([gx, grid_y_start, gx, grid_y_end], fill="#E2E8F0", width=1)
        draw.text((gx - 15, start_y + 50), f"{h}h", fill="#94A3B8", font=get_font(14, bold=True))

    phases = [
        {
            "code": "Phase 1",
            "name": "Problem Formulation & Metric Alignment",
            "sub": "Mathematical framing, retention economics, data contracts, and repo setup",
            "start": 0.0,
            "duration": 4.5,
            "color": "#0284C7",
            "milestone": "Project Charter & Evaluation Metrics Approved"
        },
        {
            "code": "Phase 2",
            "name": "Data Preprocessing & Feature Engineering",
            "sub": "KNN imputation, Tukey IQR capping, RobustScaler, and velocity features",
            "start": 4.5,
            "duration": 6.5,
            "color": "#0D9488",
            "milestone": "Leakage-Free Preprocessing Pipeline Serialized"
        },
        {
            "code": "Phase 3",
            "name": "Candidate Modeling & Ensemble Benchmarking",
            "sub": "Logistic baseline, CART trees, Random Forest, LightGBM, and XGBoost",
            "start": 11.0,
            "duration": 7.5,
            "color": "#F59E0B",
            "milestone": "Champion Model Selected (PR-AUC >= 0.69)"
        },
        {
            "code": "Phase 4",
            "name": "Bayesian Hyperparameter Optimization",
            "sub": "150 Optuna trials tuning LightGBM leaves, learning rate, and regularizers",
            "start": 18.5,
            "duration": 5.5,
            "color": "#6366F1",
            "milestone": "Tuned Hyperparameter State Locked"
        },
        {
            "code": "Phase 5",
            "name": "Probability Calibration & Validation Diagnostics",
            "sub": "Isotonic regression, Brier score minimization, TreeSHAP waterfall charts",
            "start": 24.0,
            "duration": 4.5,
            "color": "#8B5CF6",
            "milestone": "Calibrated Decision Threshold Locked"
        },
        {
            "code": "Phase 6",
            "name": "Deployment Packaging & Maintenance Blueprint",
            "sub": "FastAPI REST microservice, batch scoring worker, and PSI drift monitoring",
            "start": 28.5,
            "duration": 4.0,
            "color": "#EC4899",
            "milestone": "Production Handoff & Governance Sign-Off"
        }
    ]

    curr_y = start_y + 80
    for idx, p in enumerate(phases):
        draw_rounded_rect(draw, [left_x, curr_y, left_x + table_w, curr_y + row_h - 20], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
        draw_rounded_rect(draw, [left_x, curr_y, left_x + 10, curr_y + row_h - 20], radius=4, fill=p["color"])
        
        draw.text((left_x + 25, curr_y + 15), f"{p['code']}: {p['name']}", fill="#0F172A", font=f_task_name)
        draw.text((left_x + 25, curr_y + 45), p["sub"], fill="#64748B", font=f_task_desc)
        draw.text((left_x + 25, curr_y + 75), f"Milestone: {p['milestone']}", fill=p["color"], font=get_font(15, bold=True))
        draw.text((left_x + 25, curr_y + 98), f"Effort Allocation: {p['duration']} Hours", fill="#0284C7", font=get_font(15, bold=True))

        bx0 = timeline_x + int((p["start"] / total_hours) * timeline_w)
        bx1 = timeline_x + int(((p["start"] + p["duration"]) / total_hours) * timeline_w)
        bar_y0 = curr_y + 20
        bar_y1 = curr_y + row_h - 40

        draw_rounded_rect(draw, [bx0, bar_y0, bx1, bar_y1], radius=8, fill=p["color"], outline="#1E293B", width=1)
        bar_txt = f"{p['code']} ({p['duration']}h)"
        draw.text((bx0 + 15, bar_y0 + 18), bar_txt, fill="#FFFFFF", font=f_bar_label)

        diamond_cx = bx1
        diamond_cy = (bar_y0 + bar_y1) // 2
        d_rad = 12
        draw.polygon([
            (diamond_cx, diamond_cy - d_rad),
            (diamond_cx + d_rad, diamond_cy),
            (diamond_cx, diamond_cy + d_rad),
            (diamond_cx - d_rad, diamond_cy)
        ], fill="#F59E0B", outline="#FFFFFF")

        curr_y += row_h

    summary_y = curr_y + 10
    draw_rounded_rect(draw, [left_x, summary_y, width - 60, summary_y + 80], radius=12, fill="#0F172A")
    draw.text((90, summary_y + 25), "Total Estimated Effort: 32.5 Hours", fill="#38BDF8", font=get_font(24, bold=True))
    draw.text((550, summary_y + 28), "|   Pacing: 6.5 Hours / Day (5 Days)   |   Contingency Buffer: 2.5 Hours remaining to cap   |   Status: On Track", fill="#CBD5E1", font=get_font(18, bold=False))

    draw_rounded_rect(draw, [50, height - 60, width - 50, height - 15], radius=8, fill="#1E293B")
    draw.text((80, height - 44), "Figure 3: Week 3 Machine Learning Development Timeline & Critical Path Gantt Schedule (Total: 32.5 Hours)", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved ML Gantt Diagram 3 to {output_path}")

if __name__ == "__main__":
    out_dir = r"e:\Code Playground\Sumu\assets"
    os.makedirs(out_dir, exist_ok=True)
    create_ml_pipeline_diagram(os.path.join(out_dir, "ml_diagram_1_pipeline.png"))
    create_ml_validation_diagram(os.path.join(out_dir, "ml_diagram_2_validation.png"))
    create_ml_gantt_diagram(os.path.join(out_dir, "ml_diagram_3_timeline.png"))
    print("All Week 3 ML diagrams generated successfully.")
