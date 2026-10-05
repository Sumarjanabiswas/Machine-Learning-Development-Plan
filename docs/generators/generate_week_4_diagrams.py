"""
generate_week_4_diagrams.py
===========================
Generates 3 high-resolution (2400 x 1350/1400 px) publication-grade diagrams for
Week 4: Comprehensive Data Science Report and Insights Presentation Plan.

Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
Repository: https://github.com/Sumarjanabiswas/Machine-Learning-Development-Plan
"""

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
    if x1 > x0 and y1 == y0:
        draw.polygon([(x1, y1), (x1 - head_size, y1 - head_size // 2), (x1 - head_size, y1 + head_size // 2)], fill=color)
    elif x1 == x0 and y1 > y0:
        draw.polygon([(x1, y1), (x1 - head_size // 2, y1 - head_size), (x1 + head_size // 2, y1 - head_size)], fill=color)


# ==============================================================================
# DIAGRAM 1: Executive Insights & Churn Anomaly Diagnostic Mock-Up
# ==============================================================================
def create_insights_mockup_diagram(output_path):
    width, height = 2400, 1350
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(38, bold=True)
    f_sub = get_font(20, bold=False)
    f_header = get_font(21, bold=True)
    f_card_title = get_font(18, bold=True)
    f_body = get_font(14, bold=False)
    f_mono = get_font(14, bold=True)
    f_badge = get_font(13, bold=True)
    f_footer = get_font(15, bold=False)

    # 1. Header Banner
    draw_rounded_rect(draw, [50, 40, width - 50, 155], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "Executive Insights & Churn Anomaly Diagnostic Mock-Up", fill="#FFFFFF", font=f_title)
    draw.text((90, 112), "Synthesizing Complex Telemetry Trends, Behavioral Anomalies & Statistical Multi-Metric Evidence into Board-Level Insights", fill="#94A3B8", font=f_sub)

    # 3 Main Analytical Panels
    panels = [
        {
            "col": 0,
            "badge": "BEHAVIORAL VELOCITY TREND",
            "title": "Insight 1: 60-Day Disengagement Cliff",
            "stat": "4.8x",
            "stat_lbl": "Higher Churn Rate when Velocity < 0.60x",
            "color": "#0284C7",
            "findings": [
                "• Anomaly Detection: A 40%+ drop in 30d login frequency relative to 90d baseline marks the point of no return.",
                "• Statistical Evidence: Log-rank test p < 0.001 confirms disengagement begins 60 days before contract expiry.",
                "• Churn Rate Impact: Baseline 11.4% surges to 54.7% for accounts exhibiting activity velocity ratio < 0.60x.",
                "• Executive Rationale: Proactive CSM re-engagement must trigger at Day 45 to protect renewal cycles."
            ],
            "metrics": [
                ("Baseline Churn", "11.4%"),
                ("Post-Cliff Churn", "54.7%"),
                ("Detection Lead Time", "60 Days"),
                ("Action Window", "Day 30-45")
            ]
        },
        {
            "col": 1,
            "badge": "PRODUCT ADOPTION THRESHOLD",
            "title": "Insight 2: The 40% Seat Saturation Cliff",
            "stat": "81.4%",
            "stat_lbl": "Renewal Failure Rate Below 40% Seat Utilization",
            "color": "#F43F5E",
            "findings": [
                "• Critical Threshold: Enterprise contracts with active seats / licensed seats < 0.40 face near-total renewal failure.",
                "• Contraction Precedes Churn: Downsizing licenses at mid-term strongly signals full contract termination.",
                "• Financial Vulnerability: High ARR accounts ($18k-$72k) with low seat usage represent 64% of gross dollar loss.",
                "• Executive Rationale: Shift CSM incentives from license upsell to active monthly user seat saturation."
            ],
            "metrics": [
                ("Healthy Saturation", "> 75%"),
                ("Warning Band", "40% - 75%"),
                ("Critical Cliff", "< 40%"),
                ("ARR at Risk", "$6.13M")
            ]
        },
        {
            "col": 2,
            "badge": "OPERATIONAL FRICTION ANOMALY",
            "title": "Insight 3: Support Escalation Lag Multiplier",
            "stat": "62.0%",
            "stat_lbl": "Churn Propensity for Escalations >= 2 & Hours > 48",
            "color": "#F59E0B",
            "findings": [
                "• Compounding Interaction: Escalations alone mildly impact churn, but resolution lag > 48h triggers catastrophic decay.",
                "• CSAT Erosion: Average CSAT rating falls from 4.6 to 1.4 when ticket resolution exceeds 48 hours.",
                "• Root Cause Analysis: Platform bugs unresolved within SLA cause executive sponsor loss.",
                "• Executive Rationale: Institute an automated Tier-3 escalation bridge with guaranteed 12-hour executive turnaround."
            ],
            "metrics": [
                ("Standard Resolution", "12.4 Hours"),
                ("Critical SLA Lag", "> 48 Hours"),
                ("CSAT Penalty", "-3.2 Points"),
                ("Intervention Priority", "Immediate (24h)")
            ]
        }
    ]

    panel_w = 720
    panel_gap = 40
    start_x = 70
    start_y = 185
    panel_h = 870

    for p in panels:
        px0 = start_x + p["col"] * (panel_w + panel_gap)
        px1 = px0 + panel_w
        py0 = start_y
        py1 = py0 + panel_h

        # Panel Card
        draw_rounded_rect(draw, [px0, py0, px1, py1], radius=14, fill="#FFFFFF", outline="#E2E8F0", width=2)

        # Header Pill
        draw_rounded_rect(draw, [px0 + 24, py0 + 24, px0 + 360, py0 + 60], radius=8, fill=p["color"])
        draw.text((px0 + 36, py0 + 32), p["badge"], fill="#FFFFFF", font=f_badge)

        # Panel Title
        draw.text((px0 + 24, py0 + 78), p["title"], fill="#0F172A", font=f_card_title)

        # Stat Callout Box
        draw_rounded_rect(draw, [px0 + 24, py0 + 120, px1 - 24, py0 + 225], radius=10, fill="#F8FAFC", outline=p["color"], width=2)
        draw.text((px0 + 44, py0 + 130), p["stat"], fill=p["color"], font=get_font(42, bold=True))
        draw.text((px0 + 44, py0 + 185), p["stat_lbl"], fill="#475569", font=get_font(15, bold=True))

        # Core Findings Header
        draw.text((px0 + 24, py0 + 250), "Empirical Findings & Diagnostic Analysis:", fill="#1E293B", font=f_header)

        # Bullet Items
        cur_y = py0 + 290
        for f in p["findings"]:
            words = f.split(" ")
            line = ""
            for w in words:
                test_line = line + w + " "
                if len(test_line) > 58:
                    draw.text((px0 + 24, cur_y), line, fill="#334155", font=f_body)
                    cur_y += 24
                    line = "  " + w + " "
                else:
                    line = test_line
            if line:
                draw.text((px0 + 24, cur_y), line, fill="#334155", font=f_body)
                cur_y += 32

        # Metric Grid Box
        grid_y = py1 - 240
        draw_rounded_rect(draw, [px0 + 24, grid_y, px1 - 24, py1 - 24], radius=10, fill="#F1F5F9", outline="#CBD5E1", width=1)
        draw.text((px0 + 40, grid_y + 16), "Key Diagnostic Metrics & Benchmarks:", fill="#0F172A", font=get_font(15, bold=True))

        gy = grid_y + 48
        for k, v in p["metrics"]:
            draw.text((px0 + 40, gy), k, fill="#64748B", font=f_body)
            draw.text((px1 - 220, gy), v, fill="#0F172A", font=f_mono)
            draw.line([px0 + 40, gy + 26, px1 - 40, gy + 26], fill="#E2E8F0", width=1)
            gy += 38

    # 4. Bottom Executive Impact Banner
    by0 = start_y + panel_h + 30
    by1 = height - 40
    draw_rounded_rect(draw, [50, by0, width - 50, by1], radius=14, fill="#0F172A", outline="#10B981", width=2)

    draw.text((90, by0 + 22), "BOARD-LEVEL FINANCIAL CONCLUSION & ROI IMPACT", fill="#34D399", font=get_font(18, bold=True))
    draw.text((90, by0 + 58), "Total Addressable Churn Risk: $9,580,000 ARR across 25,000 enterprise accounts (11.4% prevalence).", fill="#FFFFFF", font=get_font(16, bold=True))
    draw.text((90, by0 + 90), "Deploying ChurnGuard-ML at optimal cutoff (t* = 0.35) recovers $464,520 gross ARR per 6,250-account cohort, delivering +$412,170 in net profit (787% ROI) after Customer Success outreach costs.", fill="#94A3B8", font=f_sub)

    # Metadata & Repository Footer
    draw.text((width - 780, by0 + 24), "Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)", fill="#94A3B8", font=f_footer)
    draw.text((width - 780, by0 + 54), "Repository: https://github.com/Sumarjanabiswas/Machine-Learning-Development-Plan", fill="#38BDF8", font=f_footer)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"[SUCCESS] Generated: {output_path}")


# ==============================================================================
# DIAGRAM 2: Non-Technical Strategic Communication & Storytelling Framework
# ==============================================================================
def create_storytelling_framework_diagram(output_path):
    width, height = 2400, 1350
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(38, bold=True)
    f_sub = get_font(20, bold=False)
    f_header = get_font(21, bold=True)
    f_card_title = get_font(18, bold=True)
    f_body = get_font(14, bold=False)
    f_mono = get_font(14, bold=True)
    f_badge = get_font(13, bold=True)
    f_footer = get_font(15, bold=False)

    # 1. Header Banner
    draw_rounded_rect(draw, [50, 40, width - 50, 155], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "Non-Technical Strategic Communication & Storytelling Framework", fill="#FFFFFF", font=f_title)
    draw.text((90, 112), "Bridging Data Science & Executive Decision-Making via SCQA Narrative Architecture & Technical-to-Business Translation", fill="#94A3B8", font=f_sub)

    col_w = 720
    col_gap = 40
    start_x = 70
    start_y = 185
    col_h = 1080

    # -----------------------------
    # Column 1: SCQA Narrative Architecture
    # -----------------------------
    c1_x0 = start_x
    c1_x1 = c1_x0 + col_w
    draw_rounded_rect(draw, [c1_x0, start_y, c1_x1, start_y + col_h], radius=14, fill="#FFFFFF", outline="#CBD5E1", width=2)

    draw_rounded_rect(draw, [c1_x0 + 24, start_y + 24, c1_x0 + 400, start_y + 60], radius=8, fill="#6366F1")
    draw.text((c1_x0 + 36, start_y + 32), "EXECUTIVE STORYTELLING PYRAMID", fill="#FFFFFF", font=f_badge)
    draw.text((c1_x0 + 24, start_y + 78), "The SCQA Narrative Structure", fill="#0F172A", font=f_card_title)

    scqa_blocks = [
        ("SITUATION (Status Quo)", "#0284C7", [
            "• Enterprise SaaS platform generates $84M ARR across 25,000 enterprise accounts.",
            "• Healthy top-of-funnel customer acquisition with 18% annual new customer growth.",
            "• High contract values: Growth ($18k ARR) and Enterprise ($54k ARR) tiers."
        ]),
        ("COMPLICATION (The Threat)", "#F43F5E", [
            "• Silent enterprise attrition: 11.4% annual churn bleeds $9.58M ARR silently.",
            "• Disengagement is hidden: Standard billing shows active status until non-renewal.",
            "• CSM teams are reactive: Reaching out 14 days before renewal is too late."
        ]),
        ("QUESTION (The Core Decision)", "#F59E0B", [
            "• How can Leadership identify at-risk enterprise accounts 60 days early?",
            "• How do we prioritize limited Customer Success bandwidth on high-ROI saves?",
            "• What is the optimal balance between intervention outreach cost and rescued ARR?"
        ]),
        ("ANSWER (The ChurnGuard-ML Solution)", "#10B981", [
            "• Deploy calibrated machine learning scoring identifying flight risk at Day 45.",
            "• Optimize decision cutoff to t* = 0.35, generating +$412,170 net profit per cohort.",
            "• Route automated tactical playbooks to Customer Success managers via Salesforce."
        ])
    ]

    sy = start_y + 125
    for title, color, points in scqa_blocks:
        draw_rounded_rect(draw, [c1_x0 + 20, sy, c1_x1 - 20, sy + 215], radius=10, fill="#F8FAFC", outline=color, width=2)
        draw_rounded_rect(draw, [c1_x0 + 32, sy + 14, c1_x0 + 280, sy + 44], radius=6, fill=color)
        draw.text((c1_x0 + 42, sy + 20), title, fill="#FFFFFF", font=get_font(12, bold=True))

        py = sy + 58
        for pt in points:
            words = pt.split(" ")
            line = ""
            for w in words:
                test_line = line + w + " "
                if len(test_line) > 52:
                    draw.text((c1_x0 + 32, py), line, fill="#334155", font=f_body)
                    py += 22
                    line = "  " + w + " "
                else:
                    line = test_line
            if line:
                draw.text((c1_x0 + 32, py), line, fill="#334155", font=f_body)
                py += 28
        sy += 230

    # -----------------------------
    # Column 2: Technical-to-Business Translation Matrix
    # -----------------------------
    c2_x0 = start_x + col_w + col_gap
    c2_x1 = c2_x0 + col_w
    draw_rounded_rect(draw, [c2_x0, start_y, c2_x1, start_y + col_h], radius=14, fill="#FFFFFF", outline="#CBD5E1", width=2)

    draw_rounded_rect(draw, [c2_x0 + 24, start_y + 24, c2_x0 + 390, start_y + 60], radius=8, fill="#0284C7")
    draw.text((c2_x0 + 36, start_y + 32), "COMMUNICATION TRANSLATION MATRIX", fill="#FFFFFF", font=f_badge)
    draw.text((c2_x0 + 24, start_y + 78), "Jargon-Free Executive Translations", fill="#0F172A", font=f_card_title)

    translations = [
        ("Technical Metric: PR-AUC = 0.3322", "Business Value: 3.0x Precision Lift", "#0284C7",
         "Rather than calling accounts blindly (where only 11% churn), 1 in every 2.2 accounts flagged by the model is an actual churning client, tripling team productivity."),
        ("Technical Metric: Brier Score = 0.0891 (ECE = 0.0106)", "Business Value: True Probability Honesty", "#10B981",
         "When the model outputs a 70% churn risk, exactly 7 out of 10 clients cancel without intervention. Executives can budget retention dollars with actuarial confidence."),
        ("Technical Metric: Specificity = 96.55%", "Business Value: Zero Client Harassment", "#0284C7",
         "Protects 5,348 healthy enterprise accounts from annoying, unnecessary check-in emails, preserving customer relationship capital and executive goodwill."),
        ("Technical Metric: Threshold Cutoff t* = 0.35", "Business Value: +$220,140 Net Profit Lift", "#10B981",
         "Shifting from standard 50% cutoff to the cost-optimal 35% captures 86 additional churning accounts, generating an extra +$220k in net revenue after outreach costs."),
        ("Technical Metric: RobustScaler & VIF < 5.0", "Business Value: Bulletproof Data Stability", "#F59E0B",
         "Eliminates volatile seasonal distortions and data redundancy, guaranteeing that executive reports reflect genuine customer health rather than tracking noise.")
    ]

    ty = start_y + 125
    for tech, biz, color, desc in translations:
        draw_rounded_rect(draw, [c2_x0 + 20, ty, c2_x1 - 20, ty + 172], radius=10, fill="#F8FAFC", outline=color, width=2)
        draw.text((c2_x0 + 32, ty + 14), tech, fill="#64748B", font=f_mono)
        draw.text((c2_x0 + 32, ty + 42), biz, fill=color, font=get_font(17, bold=True))

        words = desc.split(" ")
        line = ""
        dy = ty + 78
        for w in words:
            test_line = line + w + " "
            if len(test_line) > 54:
                draw.text((c2_x0 + 32, dy), line, fill="#334155", font=f_body)
                dy += 22
                line = "" + w + " "
            else:
                line = test_line
        if line:
            draw.text((c2_x0 + 32, dy), line, fill="#334155", font=f_body)

        ty += 185

    # -----------------------------
    # Column 3: 10-Slide Board Deck Walkthrough & Objections
    # -----------------------------
    c3_x0 = start_x + (col_w + col_gap) * 2
    c3_x1 = c3_x0 + col_w
    draw_rounded_rect(draw, [c3_x0, start_y, c3_x1, start_y + col_h], radius=14, fill="#FFFFFF", outline="#CBD5E1", width=2)

    draw_rounded_rect(draw, [c3_x0 + 24, start_y + 24, c3_x0 + 370, start_y + 60], radius=8, fill="#F59E0B")
    draw.text((c3_x0 + 36, start_y + 32), "EXECUTIVE PRESENTATION BLUEPRINT", fill="#FFFFFF", font=f_badge)
    draw.text((c3_x0 + 24, start_y + 78), "10-Slide Deck Flow & Objections", fill="#0F172A", font=f_card_title)

    slides = [
        ("Slide 1-2: Context & Financial Exposure", "Establish $9.58M ARR at risk; align on retention economics."),
        ("Slide 3-4: The 3 Core Telemetry Discoveries", "Present the Velocity Cliff, Seat Cliff, and Escalation Lag."),
        ("Slide 5-6: The Predictive Decision Engine", "Demonstrate 3x precision lift and honest calibrated risk meter."),
        ("Slide 7-8: Business ROI & Cost-Utility Matrix", "Show +$412,170 net profit and 787% ROI at t* = 0.35."),
        ("Slide 9-10: 90-Day Rollout & Action Plan", "CRM workflow integration and CS playbook governance.")
    ]

    sly = start_y + 125
    for stitle, sdesc in slides:
        draw_rounded_rect(draw, [c3_x0 + 20, sly, c3_x1 - 20, sly + 85], radius=8, fill="#F8FAFC", outline="#E2E8F0", width=1)
        draw.text((c3_x0 + 32, sly + 14), stitle, fill="#0F172A", font=get_font(15, bold=True))
        draw.text((c3_x0 + 32, sly + 46), sdesc, fill="#475569", font=f_body)
        sly += 98

    # Executive Objection Handling Card
    obj_y = sly + 15
    draw_rounded_rect(draw, [c3_x0 + 20, obj_y, c3_x1 - 20, start_y + col_h - 24], radius=10, fill="#0F172A", outline="#38BDF8", width=2)
    draw.text((c3_x0 + 36, obj_y + 20), "EXECUTIVE OBJECTION HANDLING STRATEGY", fill="#38BDF8", font=get_font(16, bold=True))

    objections = [
        ("Q: 'Is our team going to chase false alarms?'",
         "A: No. Specificity is 96.55%, meaning 97 out of 100 healthy clients are never contacted unnecessarily."),
        ("Q: 'Why not just target all expiring contracts?'",
         "A: Expiring accounts are already decided. ChurnGuard-ML intervenes at Day 45 when behavior can still be saved."),
        ("Q: 'What if customer usage patterns shift?'",
         "A: Automated Population Stability Index (PSI) tracking retrains the pipeline whenever drift exceeds 0.20.")
    ]

    oy = obj_y + 55
    for q, a in objections:
        draw.text((c3_x0 + 36, oy), q, fill="#FCD34D", font=get_font(13.5, bold=True))
        oy += 24
        words = a.split(" ")
        line = ""
        for w in words:
            test_line = line + w + " "
            if len(test_line) > 52:
                draw.text((c3_x0 + 36, oy), line, fill="#E2E8F0", font=get_font(13, bold=False))
                oy += 20
                line = "" + w + " "
            else:
                line = test_line
        if line:
            draw.text((c3_x0 + 36, oy), line, fill="#E2E8F0", font=get_font(13, bold=False))
            oy += 32

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"[SUCCESS] Generated: {output_path}")


# ==============================================================================
# DIAGRAM 3: Week 4 Implementation Timeline & 90-Day Operational Rollout
# ==============================================================================
def create_timeline_and_rollout_diagram(output_path):
    width, height = 2400, 1350
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(38, bold=True)
    f_sub = get_font(20, bold=False)
    f_header = get_font(21, bold=True)
    f_card_title = get_font(18, bold=True)
    f_body = get_font(14, bold=False)
    f_mono = get_font(14, bold=True)
    f_badge = get_font(13, bold=True)
    f_footer = get_font(15, bold=False)

    # 1. Header Banner
    draw_rounded_rect(draw, [50, 40, width - 50, 155], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "Executive Project Timeline & 90-Day Strategic Rollout Roadmap", fill="#FFFFFF", font=f_title)
    draw.text((90, 112), "32.5-Hour Professional Document Preparation Schedule & Phased Post-Presentation CRM Integration Plan", fill="#94A3B8", font=f_sub)

    # -----------------------------
    # Top Half: 32.5-Hour Week 4 Preparation Timeline
    # -----------------------------
    draw_rounded_rect(draw, [50, 180, width - 50, 680], radius=14, fill="#FFFFFF", outline="#CBD5E1", width=2)
    draw_rounded_rect(draw, [74, 204, 520, 240], radius=8, fill="#0284C7")
    draw.text((86, 212), "WEEK 4 PREPARATION SCHEDULE (32.5 HOURS)", fill="#FFFFFF", font=f_badge)
    draw.text((74, 256), "5-Day Workstream Allocation & Critical Path Delivery", fill="#0F172A", font=f_card_title)

    days = [
        {
            "day": "Day 1 (Mon)",
            "hours": "6.5h",
            "title": "Phase 1: Scoping & Alignment",
            "tasks": [
                "• Executive narrative charter & objectives",
                "• SCQA storytelling framework blueprint",
                "• Target audience & persona mapping"
            ],
            "color": "#0284C7"
        },
        {
            "day": "Day 2 (Tue)",
            "hours": "6.5h",
            "title": "Phase 2: Insights Synthesis",
            "tasks": [
                "• Anomaly threshold verification (velocity < 0.60x)",
                "• Seat utilization cliff statistical proof",
                "• Escalation latency interaction modeling"
            ],
            "color": "#0284C7"
        },
        {
            "day": "Day 3 (Wed)",
            "hours": "6.5h",
            "title": "Phase 3: Visual Design & Mock-ups",
            "tasks": [
                "• High-resolution diagnostic visuals (2400x1350)",
                "• Storytelling & translation matrix diagram",
                "• Executive presentation deck architecture"
            ],
            "color": "#6366F1"
        },
        {
            "day": "Day 4 (Thu)",
            "hours": "6.5h",
            "title": "Phase 4: Non-Technical Translation",
            "tasks": [
                "• Jargon-free translation matrix formulation",
                "• Slide-by-slide executive briefing script",
                "• Executive objection handling playbook"
            ],
            "color": "#F59E0B"
        },
        {
            "day": "Day 5 (Fri)",
            "hours": "6.0h + 2.5h",
            "title": "Phase 5: Recommendations & Review",
            "tasks": [
                "• Financial cost-utility ROI confirmation",
                "• 90-day operational roadmap specification",
                "• Final DOCX formatting & buffer review"
            ],
            "color": "#10B981"
        }
    ]

    card_w = 425
    card_gap = 25
    start_cx = 74
    start_cy = 300

    for i, d in enumerate(days):
        cx0 = start_cx + i * (card_w + card_gap)
        cx1 = cx0 + card_w
        cy0 = start_cy
        cy1 = cy0 + 340

        draw_rounded_rect(draw, [cx0, cy0, cx1, cy1], radius=10, fill="#F8FAFC", outline=d["color"], width=2)
        draw_rounded_rect(draw, [cx0 + 16, cy0 + 16, cx0 + 170, cy0 + 46], radius=6, fill=d["color"])
        draw.text((cx0 + 24, cy0 + 22), d["day"] + " • " + d["hours"], fill="#FFFFFF", font=get_font(12, bold=True))

        draw.text((cx0 + 16, cy0 + 60), d["title"], fill="#0F172A", font=get_font(15, bold=True))

        ty = cy0 + 105
        for t in d["tasks"]:
            draw.text((cx0 + 16, ty), t, fill="#334155", font=get_font(13.5, bold=False))
            ty += 38

    # -----------------------------
    # Bottom Half: 90-Day Post-Presentation Operational Roadmap
    # -----------------------------
    draw_rounded_rect(draw, [50, 710, width - 50, height - 40], radius=14, fill="#FFFFFF", outline="#CBD5E1", width=2)
    draw_rounded_rect(draw, [74, 734, 460, 770], radius=8, fill="#10B981")
    draw.text((86, 742), "POST-PRESENTATION OPERATIONAL ROADMAP", fill="#FFFFFF", font=f_badge)
    draw.text((74, 786), "90-Day Implementation & Cross-Functional Rollout Phases", fill="#0F172A", font=f_card_title)

    roadmap_phases = [
        {
            "phase": "Month 1 (Days 1–30)",
            "title": "CRM Systems Integration & Live Scoring",
            "desc": "Embed real-time inference API into Salesforce/HubSpot headers; pilot batch scoring on 5,000 accounts.",
            "kpi": "Deliverable: Live CRM API Widget (< 40ms latency)"
        },
        {
            "phase": "Month 2 (Days 31–60)",
            "title": "CSM Tactical Playbook Enablement",
            "desc": "Train 40 enterprise CSMs on tiered playbooks (Executive sponsor bridge for high risk; tutorials for medium).",
            "kpi": "Deliverable: 100% CSM Enablement & Response SLA < 24h"
        },
        {
            "phase": "Month 3 (Days 61–90)",
            "title": "Governance, Drift Auditing & Full Rollout",
            "desc": "Deploy automated PSI drift monitoring (> 0.20 triggers retrain); perform quarterly financial save audit.",
            "kpi": "Deliverable: +$412k Verified Net ARR Preservation"
        }
    ]

    r_w = 720
    r_gap = 40
    r_start_x = 74
    r_start_y = 830

    for i, rp in enumerate(roadmap_phases):
        rx0 = r_start_x + i * (r_w + r_gap)
        rx1 = rx0 + r_w
        ry0 = r_start_y
        ry1 = ry0 + 440

        draw_rounded_rect(draw, [rx0, ry0, rx1, ry1], radius=10, fill="#F8FAFC", outline="#E2E8F0", width=2)
        draw_rounded_rect(draw, [rx0 + 20, ry0 + 20, rx0 + 260, ry0 + 52], radius=6, fill="#0F172A")
        draw.text((rx0 + 32, ry0 + 26), rp["phase"], fill="#38BDF8", font=get_font(13, bold=True))

        draw.text((rx0 + 20, ry0 + 72), rp["title"], fill="#0F172A", font=get_font(18, bold=True))

        words = rp["desc"].split(" ")
        line = ""
        dy = ry0 + 120
        for w in words:
            test_line = line + w + " "
            if len(test_line) > 52:
                draw.text((rx0 + 20, dy), line, fill="#334155", font=get_font(15, bold=False))
                dy += 26
                line = "" + w + " "
            else:
                line = test_line
        if line:
            draw.text((rx0 + 20, dy), line, fill="#334155", font=get_font(15, bold=False))

        # KPI Box
        draw_rounded_rect(draw, [rx0 + 20, ry1 - 100, rx1 - 20, ry1 - 24], radius=8, fill="#ECFDF5", outline="#10B981", width=1)
        draw.text((rx0 + 36, ry1 - 70), rp["kpi"], fill="#065F46", font=get_font(14, bold=True))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"[SUCCESS] Generated: {output_path}")


if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
    create_insights_mockup_diagram(os.path.join(assets_dir, "presentation_diagram_1_insights.png"))
    create_storytelling_framework_diagram(os.path.join(assets_dir, "presentation_diagram_2_storytelling.png"))
    create_timeline_and_rollout_diagram(os.path.join(assets_dir, "presentation_diagram_3_timeline.png"))
