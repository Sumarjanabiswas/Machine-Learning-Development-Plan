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
# DIAGRAM 1: End-to-End System Architecture & Lifecycle
# ==============================================================================
def create_architecture_diagram(output_path):
    width, height = 2400, 1350
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    # Fonts
    f_title = get_font(42, bold=True)
    f_subtitle = get_font(22, bold=False)
    f_col_header = get_font(24, bold=True)
    f_col_sub = get_font(16, bold=False)
    f_card_title = get_font(20, bold=True)
    f_card_text = get_font(16, bold=False)
    f_badge = get_font(14, bold=True)
    f_footer = get_font(16, bold=False)

    # Header Banner
    draw_rounded_rect(draw, [50, 40, width - 50, 160], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "ChurnGuard AI: End-to-End Predictive Architecture & Data Lifecycle", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "Holistic System Flow: Multi-Modal Ingestion -> Feature Store -> ML Pipeline -> SHAP Explainability -> Actionable CRM Interventions", fill="#94A3B8", font=f_subtitle)

    # 5 Main Lifecycle Pillars
    pillars = [
        {
            "num": "01",
            "title": "Data Ingestion & Lake",
            "sub": "Multi-source raw streams",
            "color": "#0284C7",
            "bg": "#F0F9FF",
            "border": "#BAE6FD",
            "cards": [
                ("CRM & Profiles", "PostgreSQL / Snowflake\nAccount age, plan tier, ARR, seats, contract terms"),
                ("Behavioral Telemetry", "Clickstream & Events (Kafka/JSON)\nDaily logins, feature usage, API calls, drop-offs"),
                ("Billing & Transactions", "Stripe / Chargebee\nInvoice history, failed payments, credit card expiry"),
                ("Customer Support Logs", "Zendesk API / Freshdesk\nTicket counts, resolution time, CSAT, sentiment tags")
            ]
        },
        {
            "num": "02",
            "title": "Data Wrangling & Features",
            "sub": "Curated feature engineering",
            "color": "#0D9488",
            "bg": "#F0FDFA",
            "border": "#99F6E4",
            "cards": [
                ("Data Quality & Cleaning", "Pandas & Great Expectations\nNull imputation (KNN), outlier mitigation, deduplication"),
                ("Temporal Consistency", "Point-in-time joins\nStrict time-travel auditing, zero lookahead leakage"),
                ("Behavioral Aggregations", "Recency, Frequency, Monetary (RFM)\n30/60/90-day rolling deltas, activity velocity ratios"),
                ("Offline Feature Store", "Feast / Parquet Staging\nStandardized train/test splits & schema validation")
            ]
        },
        {
            "num": "03",
            "title": "Model Training & Tuning",
            "sub": "Ensemble experimentation",
            "color": "#4F46E5",
            "bg": "#EEF2FF",
            "border": "#C7D2FE",
            "cards": [
                ("Data Partitioning", "Time-based Train/Val/Test\nStratified 5-Fold TimeSeriesSplit preserving class ratios"),
                ("Imbalance Correction", "Cost-sensitive loss functions\nSMOTE-NC oversampling on training folds only"),
                ("Model Benchmarking", "Scikit-Learn, LightGBM, XGBoost\nBaseline: Penalized Logistic Reg; Champion: LightGBM"),
                ("Hyperparameter Tuning", "Optuna Bayesian Optimization\nOptimizing PR-AUC, Brier score, and expected value")
            ]
        },
        {
            "num": "04",
            "title": "Inference & Explainability",
            "sub": "Transparent predictions",
            "color": "#9333EA",
            "bg": "#FAF5FF",
            "border": "#E9D5FF",
            "cards": [
                ("Probability Calibration", "Isotonic Regression & Platt Scaling\nCalibrated risk scores representing actual churn rates"),
                ("TreeSHAP Explainability", "Global feature attributions\nLocal waterfall plots for every at-risk customer profile"),
                ("Cost-Sensitive Thresholding", "Business Utility Maximization\nThreshold tuned on Retention Net Lift vs. Outreach Cost"),
                ("Model Artifact Registry", "MLflow & Joblib Versioning\nStrict semantic versioning, lineage, and audit trails")
            ]
        },
        {
            "num": "05",
            "title": "Operational Activation",
            "sub": "Business value delivery",
            "color": "#E11D48",
            "bg": "#FFF1F2",
            "border": "#FECDD3",
            "cards": [
                ("Batch Inference Service", "FastAPI / Scheduled Worker\nWeekly batch scoring generating Churn Risk Tiers"),
                ("CSM Dashboard Alerts", "Salesforce / HubSpot Integration\nTop churn drivers & customized intervention playbooks"),
                ("Automated Campaigns", "Marketing Automation (Braze)\nTargeted loyalty incentives, discount offers, onboarding re-engagement"),
                ("Drift Monitoring", "Evidently AI / MLflow Metrics\nPopulation Stability Index (PSI) & Concept Drift Alerts")
            ]
        }
    ]

    col_w = 420
    col_gap = 40
    start_x = 65
    start_y = 190

    for i, p in enumerate(pillars):
        cx = start_x + i * (col_w + col_gap)
        
        # Pillar Header Box
        draw_rounded_rect(draw, [cx, start_y, cx + col_w, start_y + 110], radius=12, fill=p["bg"], outline=p["border"], width=2)
        
        # Badge
        draw_rounded_rect(draw, [cx + 15, start_y + 15, cx + 60, start_y + 45], radius=6, fill=p["color"])
        draw.text((cx + 24, start_y + 20), p["num"], fill="#FFFFFF", font=f_badge)
        
        draw.text((cx + 72, start_y + 20), p["title"], fill="#0F172A", font=f_col_header)
        draw.text((cx + 72, start_y + 55), p["sub"], fill="#64748B", font=f_col_sub)

        # Cards inside Pillar
        card_y = start_y + 130
        card_h = 220
        card_gap = 20

        for title, desc in p["cards"]:
            draw_rounded_rect(draw, [cx, card_y, cx + col_w, card_y + card_h], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
            # Left accent bar
            draw_rounded_rect(draw, [cx, card_y, cx + 8, card_y + card_h], radius=4, fill=p["color"])
            
            draw.text((cx + 25, card_y + 18), title, fill="#1E293B", font=f_card_title)
            
            lines = desc.split("\n")
            draw.text((cx + 25, card_y + 55), lines[0], fill=p["color"], font=f_card_text)
            if len(lines) > 1:
                draw.text((cx + 25, card_y + 85), lines[1], fill="#64748B", font=f_card_text)

            card_y += card_h + card_gap

        # Connector Arrow between pillars
        if i < len(pillars) - 1:
            arrow_x0 = cx + col_w + 5
            arrow_x1 = cx + col_w + col_gap - 5
            arrow_y = start_y + 55
            draw_arrow(draw, (arrow_x0, arrow_y), (arrow_x1, arrow_y), color="#94A3B8", width=3, head_size=10)

    # Footer note
    draw_rounded_rect(draw, [50, height - 70, width - 50, height - 20], radius=8, fill="#0F172A")
    draw.text((80, height - 52), "Figure 1: Comprehensive End-to-End Predictive Analytics Architecture for ChurnGuard AI (Data Science Strategy - Week 1 Deliverable)", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved Diagram 1 to {output_path}")

# ==============================================================================
# DIAGRAM 2: 32.5-Hour Project Timeline & Milestones (Gantt Chart)
# ==============================================================================
def create_gantt_diagram(output_path):
    width, height = 2400, 1350
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(42, bold=True)
    f_subtitle = get_font(22, bold=False)
    f_head = get_font(20, bold=True)
    f_task_name = get_font(20, bold=True)
    f_task_desc = get_font(16, bold=False)
    f_bar_label = get_font(18, bold=True)
    f_footer = get_font(16, bold=False)

    # Header Banner
    draw_rounded_rect(draw, [50, 40, width - 50, 160], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "ChurnGuard AI: Project Implementation Timeline & Resource Allocation (32.5 Hours)", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "Detailed Work Breakdown Structure: 6 Structured Phases across 5 Working Days (Target Allocation: 30-35 Hours)", fill="#94A3B8", font=f_subtitle)

    # Table & Timeline Geometry
    left_x = 60
    table_w = 750
    timeline_x = left_x + table_w + 40
    timeline_w = width - timeline_x - 60
    start_y = 200
    row_h = 150
    total_hours = 35.0  # scale across 35h

    # Timeline Column Headers (Hours 0 to 35, grouped by Day)
    days = [
        ("Day 1: Inception & Setup", 0, 7),
        ("Day 2: Ingestion & EDA", 7, 14),
        ("Day 3: Features & Baselines", 14, 21),
        ("Day 4: Ensembles & Tuning", 21, 28),
        ("Day 5: Synthesis & Reporting", 28, 35)
    ]

    # Draw Day Header Bands
    for d_name, h_start, h_end in days:
        bx0 = timeline_x + int((h_start / total_hours) * timeline_w)
        bx1 = timeline_x + int((h_end / total_hours) * timeline_w)
        draw_rounded_rect(draw, [bx0 + 2, start_y, bx1 - 2, start_y + 45], radius=6, fill="#E2E8F0", outline="#CBD5E1", width=1)
        draw.text((bx0 + 15, start_y + 12), d_name, fill="#334155", font=f_head)

    # Gridlines
    grid_y_start = start_y + 55
    grid_y_end = start_y + 6 * row_h + 80
    for h in range(0, 36, 5):
        gx = timeline_x + int((h / total_hours) * timeline_w)
        draw.line([gx, grid_y_start, gx, grid_y_end], fill="#E2E8F0", width=1)
        draw.text((gx - 15, start_y + 50), f"{h}h", fill="#94A3B8", font=get_font(14, bold=True))

    phases = [
        {
            "code": "Phase 1",
            "name": "Project Scoping & Problem Formulation",
            "sub": "Stakeholder alignment, KPI definition, data source discovery",
            "start": 0.0,
            "duration": 4.5,
            "color": "#0284C7",
            "milestone": "Project Charter & Schema Spec Approved"
        },
        {
            "code": "Phase 2",
            "name": "Data Ingestion, Auditing & Cleansing",
            "sub": "Synthetic pipeline generation, missing data audit, pipeline build",
            "start": 4.5,
            "duration": 5.0,
            "color": "#0D9488",
            "milestone": "Cleaned Master Dataset Verified"
        },
        {
            "code": "Phase 3",
            "name": "Exploratory Data Analysis & Feature Engineering",
            "sub": "Univariate/Bivariate stats, RFM features, behavioral deltas",
            "start": 9.5,
            "duration": 6.5,
            "color": "#F59E0B",
            "milestone": "Feature Store Matrix Ready (65+ Features)"
        },
        {
            "code": "Phase 4",
            "name": "Model Exploration & Advanced Ensembles",
            "sub": "Stratified CV, Logistic baseline, Random Forest, LightGBM, XGBoost",
            "start": 16.0,
            "duration": 7.5,
            "color": "#6366F1",
            "milestone": "Champion Model Selected (PR-AUC >= 0.70)"
        },
        {
            "code": "Phase 5",
            "name": "Model Calibration, SHAP & Cost Tuning",
            "sub": "TreeSHAP explainability, threshold tuning via cost matrix, packaging",
            "start": 23.5,
            "duration": 5.0,
            "color": "#8B5CF6",
            "milestone": "Explainability Engine & Cost Policy Locked"
        },
        {
            "code": "Phase 6",
            "name": "Strategic Synthesis & Project Documentation",
            "sub": "DOC report generation, executive summary, stakeholder presentation",
            "start": 28.5,
            "duration": 4.0,
            "color": "#EC4899",
            "milestone": "Comprehensive Deliverables Finalized"
        }
    ]

    curr_y = start_y + 80
    for idx, p in enumerate(phases):
        # Table Row (Left)
        draw_rounded_rect(draw, [left_x, curr_y, left_x + table_w, curr_y + row_h - 20], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
        # Color tag
        draw_rounded_rect(draw, [left_x, curr_y, left_x + 10, curr_y + row_h - 20], radius=4, fill=p["color"])
        
        # Text in Table
        draw.text((left_x + 25, curr_y + 15), f"{p['code']}: {p['name']}", fill="#0F172A", font=f_task_name)
        draw.text((left_x + 25, curr_y + 45), p["sub"], fill="#64748B", font=f_task_desc)
        draw.text((left_x + 25, curr_y + 75), f"Milestone: {p['milestone']}", fill=p["color"], font=get_font(15, bold=True))
        draw.text((left_x + 25, curr_y + 98), f"Effort Allocation: {p['duration']} Hours", fill="#0284C7", font=get_font(15, bold=True))

        # Gantt Bar (Right)
        bx0 = timeline_x + int((p["start"] / total_hours) * timeline_w)
        bx1 = timeline_x + int(((p["start"] + p["duration"]) / total_hours) * timeline_w)
        bar_y0 = curr_y + 20
        bar_y1 = curr_y + row_h - 40

        # Bar Shadow / Fill
        draw_rounded_rect(draw, [bx0, bar_y0, bx1, bar_y1], radius=8, fill=p["color"], outline="#1E293B", width=1)
        
        # Bar Text
        bar_txt = f"{p['code']} ({p['duration']}h)"
        draw.text((bx0 + 15, bar_y0 + 18), bar_txt, fill="#FFFFFF", font=f_bar_label)

        # Milestone Diamond at end of bar
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

    # Total Hours Badge & Summary Box
    summary_y = curr_y + 10
    draw_rounded_rect(draw, [left_x, summary_y, width - 60, summary_y + 80], radius=12, fill="#0F172A")
    draw.text((90, summary_y + 25), "Total Estimated Effort: 32.5 Hours", fill="#38BDF8", font=get_font(24, bold=True))
    draw.text((550, summary_y + 28), "|   Pacing: 6.5 Hours / Day (5 Days)   |   Contingency Buffer: 2.5 Hours remaining to cap   |   Status: On Track", fill="#CBD5E1", font=get_font(18, bold=False))

    # Footer note
    draw_rounded_rect(draw, [50, height - 60, width - 50, height - 15], radius=8, fill="#1E293B")
    draw.text((80, height - 44), "Figure 2: Week 1 Project Timeline, Phase Allocations & Critical Path Gantt Schedule (Total: 32.5 Hours)", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved Diagram 2 to {output_path}")

# ==============================================================================
# DIAGRAM 3: ML Modeling, Validation & Cost-Sensitive Strategy Flowchart
# ==============================================================================
def create_ml_pipeline_diagram(output_path):
    width, height = 2400, 1400
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(42, bold=True)
    f_subtitle = get_font(22, bold=False)
    f_card_title = get_font(20, bold=True)
    f_card_sub = get_font(16, bold=True)
    f_card_body = get_font(15, bold=False)
    f_footer = get_font(16, bold=False)

    # Header Banner
    draw_rounded_rect(draw, [50, 40, width - 50, 160], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "ChurnGuard AI: Machine Learning Pipeline, Validation & Decision Framework", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "Step-by-step rigorous modeling logic: Temporal Partitioning -> Cross-Validation -> Cost-Sensitive Gating -> SHAP Explanations", fill="#94A3B8", font=f_subtitle)

    # ROW 1 (Y: 200 - 450)
    draw_rounded_rect(draw, [70, 200, 580, 440], radius=12, fill="#FFFFFF", outline="#0284C7", width=2)
    draw_rounded_rect(draw, [70, 200, 580, 250], radius=10, fill="#0284C7")
    draw.text((90, 215), "1. Master Feature Matrix (X, y)", fill="#FFFFFF", font=f_card_title)
    draw.text((90, 265), "Feature Count: 65+ Engineered Attributes", fill="#0369A1", font=f_card_sub)
    draw.text((90, 295), "- Behavioral telemetry & RFM metrics\n- Rolling 30d/60d activity decay scores\n- Billing status & payment delinquency\n- Support ticket volume & NLP sentiment\n- Plan tier, tenure, and contractual terms", fill="#475569", font=f_card_body)

    draw_arrow(draw, (580, 320), (660, 320), color="#0284C7", width=4, head_size=12)

    draw_rounded_rect(draw, [660, 200, 1180, 440], radius=12, fill="#FFFFFF", outline="#0D9488", width=2)
    draw_rounded_rect(draw, [660, 200, 1180, 250], radius=10, fill="#0D9488")
    draw.text((680, 215), "2. Temporal Split (Leakage Prevention)", fill="#FFFFFF", font=f_card_title)
    draw.text((680, 265), "Time-Based Cutoff Protocol", fill="#0F766E", font=f_card_sub)
    draw.text((680, 295), "- Historical Cohort (Months 1-9): Training Set (70%)\n- Holdout Interim (Months 10-11): Validation Set (15%)\n- Future Cutoff (Month 12): Out-of-Time Test Set (15%)\n- Ensures zero forward-looking data leakage\n- Mimics real-world production deployment conditions", fill="#475569", font=f_card_body)

    draw_arrow(draw, (1180, 320), (1260, 320), color="#0D9488", width=4, head_size=12)

    draw_rounded_rect(draw, [1260, 200, 1780, 440], radius=12, fill="#FFFFFF", outline="#4F46E5", width=2)
    draw_rounded_rect(draw, [1260, 200, 1780, 250], radius=10, fill="#4F46E5")
    draw.text((1280, 215), "3. Stratified K-Fold Cross-Validation", fill="#FFFFFF", font=f_card_title)
    draw.text((1280, 265), "5-Fold Stratified Validation within Train", fill="#4338CA", font=f_card_sub)
    draw.text((1280, 295), "- Preserves class imbalance ratio (12% churners)\n- SMOTE-NC applied strictly inside training folds\n- Prevents data leakage between validation folds\n- Establishes robust confidence intervals for metrics\n- Tracks fold variance to identify unstable models", fill="#475569", font=f_card_body)

    draw_arrow(draw, (1780, 320), (1860, 320), color="#4F46E5", width=4, head_size=12)

    draw_rounded_rect(draw, [1860, 200, 2330, 440], radius=12, fill="#FFFFFF", outline="#9333EA", width=2)
    draw_rounded_rect(draw, [1860, 200, 2330, 250], radius=10, fill="#9333EA")
    draw.text((1880, 215), "4. Preprocessing Pipeline", fill="#FFFFFF", font=f_card_title)
    draw.text((1880, 265), "Scikit-Learn Pipeline Serialization", fill="#7E22CE", font=f_card_sub)
    draw.text((1880, 295), "- Median/KNN Imputation for missing values\n- Target Encoding with smoothing for high-cardinality\n- RobustScaler for non-normal continuous features\n- Strict fit_transform(train) and transform(test)\n- Exported as monolithic repeatable pipeline artifact", fill="#475569", font=f_card_body)

    # Down arrow from Row 1 to Row 2
    draw_arrow(draw, (2095, 440), (2095, 520), color="#9333EA", width=4, head_size=12)

    # ROW 2 (Y: 520 - 760)
    draw_rounded_rect(draw, [70, 520, 580, 760], radius=12, fill="#FFFFFF", outline="#6366F1", width=2)
    draw_rounded_rect(draw, [70, 520, 580, 570], radius=10, fill="#6366F1")
    draw.text((90, 535), "5. Model Selection & Exploration", fill="#FFFFFF", font=f_card_title)
    draw.text((90, 585), "Competitive Multi-Model Benchmark", fill="#4338CA", font=f_card_sub)
    draw.text((90, 615), "- Baseline 1: L1/L2 Penalized Logistic Regression\n- Baseline 2: Pruned CART Decision Tree\n- Ensemble 1: Balanced Random Forest Classifier\n- Ensemble 2: LightGBM (Gradient Boosting)\n- Ensemble 3: CatBoost (Categorical optimization)", fill="#475569", font=f_card_body)

    draw_arrow(draw, (1260, 640), (580, 640), color="#6366F1", width=4, head_size=12)

    draw_rounded_rect(draw, [660, 520, 1260, 760], radius=12, fill="#FFFFFF", outline="#0284C7", width=2)
    draw_rounded_rect(draw, [660, 520, 1260, 570], radius=10, fill="#0284C7")
    draw.text((680, 535), "6. Bayesian Hyperparameter Search", fill="#FFFFFF", font=f_card_title)
    draw.text((680, 585), "Optuna Optimization Framework", fill="#0369A1", font=f_card_sub)
    draw.text((680, 615), "- 150 trials optimizing PR-AUC & Brier Score\n- LightGBM params: learning_rate, max_depth, num_leaves\n- Regularization: colsample_bytree, subsample, reg_alpha\n- Early stopping on validation fold (patience = 25)\n- Automated pruning of unpromising hyperparameter trials", fill="#475569", font=f_card_body)

    draw_arrow(draw, (1860, 640), (1260, 640), color="#0284C7", width=4, head_size=12)

    draw_rounded_rect(draw, [1340, 520, 2330, 760], radius=12, fill="#FFFFFF", outline="#10B981", width=2)
    draw_rounded_rect(draw, [1340, 520, 2330, 570], radius=10, fill="#10B981")
    draw.text((1360, 535), "7. Model Calibration & Probability Reliability", fill="#FFFFFF", font=f_card_title)
    draw.text((1360, 585), "Raw Score to True Probability Mapping", fill="#047857", font=f_card_sub)
    draw.text((1360, 615), "- Calibration curve analysis & Expected Calibration Error (ECE)\n- Isotonic Regression vs. Sigmoid (Platt) scaling\n- Essential for financial decisions: a score of 0.8 must equal an exact 80% empirical risk\n- Brier score minimized to verify predictive probability reliability across cohorts", fill="#475569", font=f_card_body)

    # Down arrow from Row 2 to Row 3
    draw_arrow(draw, (325, 760), (325, 840), color="#6366F1", width=4, head_size=12)

    # ROW 3 (Y: 840 - 1080)
    draw_rounded_rect(draw, [70, 840, 680, 1080], radius=12, fill="#FFFFFF", outline="#F59E0B", width=2)
    draw_rounded_rect(draw, [70, 840, 680, 890], radius=10, fill="#F59E0B")
    draw.text((90, 855), "8. Cost-Sensitive Threshold Engine", fill="#FFFFFF", font=f_card_title)
    draw.text((90, 905), "Financial Utility Function Optimization", fill="#B45309", font=f_card_sub)
    draw.text((90, 935), "- Abandon standard 0.5 arbitrary probability cutoff\n- Utility Matrix: Net Value = TP*(CLV*P_succ - C_out) - FP*C_out\n- Evaluates true cost of false negatives ($8,400 churn loss)\n- Determines optimal threshold (e.g. t* = 0.38) for max ROI\n- Stratifies accounts into High, Medium, and Low risk tiers", fill="#475569", font=f_card_body)

    draw_arrow(draw, (680, 960), (760, 960), color="#F59E0B", width=4, head_size=12)

    draw_rounded_rect(draw, [760, 840, 1420, 1080], radius=12, fill="#FFFFFF", outline="#8B5CF6", width=2)
    draw_rounded_rect(draw, [760, 840, 1420, 890], radius=10, fill="#8B5CF6")
    draw.text((780, 855), "9. Explainability & Interpretability", fill="#FFFFFF", font=f_card_title)
    draw.text((780, 905), "SHAP (SHapley Additive exPlanations)", fill="#6D28D9", font=f_card_sub)
    draw.text((780, 935), "- Global Feature Importance: TreeSHAP beeswarm summary\n- Local Attribution: Force plots & waterfall charts per user\n- Empowers Customer Success with exact reasons for risk\n- Actionable diagnosis: e.g. '+32% risk due to zero logins in 14d'\n- Complies with AI transparency & regulatory governance", fill="#475569", font=f_card_body)

    draw_arrow(draw, (1420, 960), (1500, 960), color="#8B5CF6", width=4, head_size=12)

    draw_rounded_rect(draw, [1500, 840, 2330, 1080], radius=12, fill="#FFFFFF", outline="#EF4444", width=2)
    draw_rounded_rect(draw, [1500, 840, 2330, 890], radius=10, fill="#EF4444")
    draw.text((1520, 855), "10. Production Deployment Gating Check", fill="#FFFFFF", font=f_card_title)
    draw.text((1520, 905), "Strict Acceptance Criteria & Governance", fill="#B91C1C", font=f_card_sub)
    draw.text((1520, 935), "[CRITERION 1] Discrimination: ROC-AUC >= 0.86 AND PR-AUC >= 0.65\n[CRITERION 2] Financial Net ROI: Campaign Net Value >= +$120,000/quarter\n[CRITERION 3] Calibration Quality: Brier Score < 0.12, ECE < 0.05\n[CRITERION 4] Latency & Stability: Batch run < 30 min, Inference < 50ms\n[PASS] -> MLflow Registry & Deployment  |  [FAIL] -> Feature Loop", fill="#475569", font=f_card_body)

    # ROW 4 (Y: 1120 - 1280) - Downstream Activation
    draw_rounded_rect(draw, [70, 1120, width - 70, 1280], radius=12, fill="#0F172A", outline="#334155", width=2)
    draw.text((95, 1140), "Downstream Operational Impact: Automated Retention Action Engine", fill="#38BDF8", font=get_font(22, bold=True))
    draw.text((95, 1180), "High Risk Tier (Score > 0.65): Dedicated CSM outreach call, tailored QBR, executive sponsor check-in, discount lock-in", fill="#E2E8F0", font=get_font(16, bold=False))
    draw.text((95, 1215), "Medium Risk Tier (0.38 - 0.65): Automated in-app re-engagement, targeted feature walkthroughs, automated training webinars", fill="#E2E8F0", font=get_font(16, bold=False))
    draw.text((95, 1250), "Continuous Telemetry: Daily Population Stability Index (PSI) tracking & concept drift monitoring with automated re-training triggers", fill="#94A3B8", font=get_font(15, bold=False))

    # Footer note
    draw_rounded_rect(draw, [50, height - 60, width - 50, height - 15], radius=8, fill="#1E293B")
    draw.text((80, height - 44), "Figure 3: Comprehensive Machine Learning Validation, Calibration, Cost Optimization & Governance Strategy Flowchart", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved Diagram 3 to {output_path}")

if __name__ == "__main__":
    out_dir = r"e:\Code Playground\Sumu\assets"
    os.makedirs(out_dir, exist_ok=True)
    create_architecture_diagram(os.path.join(out_dir, "diagram_1_architecture.png"))
    create_gantt_diagram(os.path.join(out_dir, "diagram_2_gantt_timeline.png"))
    create_ml_pipeline_diagram(os.path.join(out_dir, "diagram_3_ml_pipeline.png"))
    print("All diagrams generated successfully.")
