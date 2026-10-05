import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Sets internal padding (margins) for a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_border(cell, top="CBD5E1", bottom="CBD5E1", left=None, right=None, sz="4"):
    """Sets specific borders on a cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    borders_xml = f'<w:tcBorders {nsdecls("w")}>'
    borders_xml += f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{top}"/>' if top else '<w:top w:val="none"/>'
    borders_xml += f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{bottom}"/>' if bottom else '<w:bottom w:val="none"/>'
    borders_xml += f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{left}"/>' if left else '<w:left w:val="none"/>'
    borders_xml += f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{right}"/>' if right else '<w:right w:val="none"/>'
    borders_xml += '</w:tcBorders>'
    tcPr.append(parse_xml(borders_xml))

def add_callout(doc, title, text, border_color="0284C7", bg_color="F0F9FF"):
    """Creates a modern executive callout banner box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders_xml = f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>'
    tcPr.append(parse_xml(borders_xml))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"■ {title}\n")
    run_title.bold = True
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(11)
    run_title.font.color.rgb = RGBColor.from_string(border_color)
    
    run_text = p.add_run(text)
    run_text.font.name = "Calibri"
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def style_heading(p, font_name="Calibri", size_pt=14, bold=True, color_rgb=(15, 41, 74), space_before=12, space_after=6):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    for r in p.runs:
        r.font.name = font_name
        r.font.size = Pt(size_pt)
        r.bold = bold
        r.font.color.rgb = RGBColor(*color_rgb)

def add_h1(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    style_heading(p, "Calibri", 17, True, (15, 41, 74), space_before=16, space_after=6)
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    style_heading(p, "Calibri", 13, True, (13, 148, 136), space_before=12, space_after=4)
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    style_heading(p, "Calibri", 11, True, (79, 70, 229), space_before=8, space_after=3)
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_bullet_item(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + ": ")
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_image_box(doc, image_path, caption_title, caption_text, width_inches=6.4):
    if not os.path.exists(image_path):
        print(f"Warning: Image {image_path} not found!")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    r = p_img.add_run()
    r.add_picture(image_path, width=Inches(width_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    
    r_cap_title = p_cap.add_run(f"{caption_title}: ")
    r_cap_title.bold = True
    r_cap_title.font.name = "Calibri"
    r_cap_title.font.size = Pt(9.5)
    r_cap_title.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    
    r_cap_text = p_cap.add_run(caption_text)
    r_cap_text.italic = True
    r_cap_text.font.name = "Calibri"
    r_cap_text.font.size = Pt(9.5)
    r_cap_text.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

def build_project_plan_document(output_path):
    print("Initializing humanized document generation...")
    doc = Document()

    # Margins: 0.8 inches
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
        # Header & Footer
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("ChurnGuard AI | Data Science Project Plan & Technical Strategy (Week 1)")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
        
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com) — Data Science Strategy Roadmap")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # -------------------------------------------------------------------------
    # COVER / HEADER BANNER BLOCK
    # -------------------------------------------------------------------------
    cover_table = doc.add_table(rows=1, cols=1)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_table.autofit = False
    c_cell = cover_table.cell(0, 0)
    c_cell.width = Inches(6.9)
    set_cell_background(c_cell, "0F172A")
    set_cell_margins(c_cell, top=260, bottom=260, left=260, right=260)
    
    cp = c_cell.paragraphs[0]
    cp.paragraph_format.space_after = Pt(6)
    r_tag = cp.add_run("DATA SCIENCE PROJECT CHARTER & ARCHITECTURAL STRATEGY\n")
    r_tag.bold = True
    r_tag.font.name = "Calibri"
    r_tag.font.size = Pt(11)
    r_tag.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)
    
    r_main_title = cp.add_run("ChurnGuard AI: Predictive Customer Churn Intelligence & Proactive Retention Engine\n")
    r_main_title.bold = True
    r_main_title.font.name = "Calibri"
    r_main_title.font.size = Pt(21)
    r_main_title.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    
    r_desc = cp.add_run("A Practical, Practitioner-Focused Architectural Blueprint, Machine Learning Strategy, 32.5-Hour Implementation Schedule, and Risk Mitigation Plan for Subscription Platforms\n\n")
    r_desc.font.name = "Calibri"
    r_desc.font.size = Pt(10.5)
    r_desc.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    r_author = cp.add_run("Prepared by: Sumarjana Biswas\n")
    r_author.bold = True
    r_author.font.name = "Calibri"
    r_author.font.size = Pt(11)
    r_author.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)

    r_meta = cp.add_run("Email: sumarjanabiswas690@gmail.com  |  Role: Lead Data Science Architect  |  Milestone: Week 1 Deliverable  |  Effort: 32.5 Hours")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # EXECUTIVE SUMMARY & METADATA TABLE
    # -------------------------------------------------------------------------
    add_callout(doc, "PROJECT VISION & PRACTITIONER NOTE", 
                "When subscription businesses lose customers, the default reaction is usually reactive panic: marketing teams fire off "
                "last-minute discounts, and Customer Success scrambles to save relationships at the eleventh hour. In reality, customers "
                "rarely churn overnight—they quietly disengage weeks in advance. ChurnGuard AI is designed to catch those subtle behavioral drop-offs "
                "60 to 90 days before renewal deadlines. Our goal isn't just to produce a model that outputs an abstract probability; "
                "it's to deliver calibrated risk scores, explainable drivers via SHAP, and an actionable pipeline that gives teams the clarity "
                "they need to intervene effectively—all designed to be built within a focused 32.5-hour development schedule.", 
                border_color="0284C7", bg_color="F0F9FF")

    # Metadata Summary Table
    meta_tbl = doc.add_table(rows=6, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    meta_widths = [Inches(2.2), Inches(4.7)]
    meta_data = [
        ("Project Author & Lead", "Sumarjana Biswas (sumarjanabiswas690@gmail.com)"),
        ("Project Codename", "ChurnGuard AI (Enterprise Customer Retention & Lifetime Value Optimization)"),
        ("Core Mission", "Detect high-risk churn signals 60-90 days before contract renewal and arm Customer Success with clear root causes"),
        ("Primary Stakeholders", "VP of Customer Success, Chief Revenue Officer (CRO), Retention Marketing, CRM Operations"),
        ("Core Python Stack", "Python 3.12, Pandas, Scikit-Learn, LightGBM, XGBoost, Optuna, SHAP, Great Expectations, MLflow"),
        ("Timeline & Effort", "32.5 Hours structured across 6 phases over 5 working days (Week 1 Milestone)")
    ]
    for row_idx, (lbl, val) in enumerate(meta_data):
        row = meta_tbl.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = meta_widths[0], meta_widths[1]
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=70, bottom=70, left=120, right=120)
        set_cell_margins(c1, top=70, bottom=70, left=120, right=120)
        set_cell_border(c0, top="E2E8F0", bottom="E2E8F0", left="CBD5E1", right="E2E8F0")
        set_cell_border(c1, top="E2E8F0", bottom="E2E8F0", left="E2E8F0", right="CBD5E1")
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(lbl)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # SECTION 1: PROJECT BACKGROUND, MOTIVATION & PROBLEM JUSTIFICATION
    # -------------------------------------------------------------------------
    add_h1(doc, "1. Project Background, Motivation & Problem Justification")
    
    add_h2(doc, "1.1 The Real-World Problem: The Leaky Bucket in Subscription Businesses")
    add_body_p(doc, 
               "Every subscription-based business—whether B2B SaaS, developer tooling, or consumer cloud services—faces the fundamental challenge "
               "of customer attrition. Companies routinely pour enormous budgets into sales, paid marketing, and brand awareness to attract new accounts. "
               "Yet, if customers leave after a few months, that acquisition spend is largely wasted. This creates what operators call the 'leaky bucket' "
               "syndrome: you have to run faster and spend more money just to keep revenue flat.")
    
    add_body_p(doc,
               "In our analysis, customer churn breaks down into two distinct categories, each requiring a completely different response:")
    add_bullet_item(doc, "Voluntary Churn", 
                    "This happens when a customer actively decides to cancel or downgrade. They might feel they aren't getting enough value, "
                    "their internal team stopped using the product, they encountered too many bugs, or a competitor offered a better deal. "
                    "This is the most critical segment to address because behavioral signals almost always precede the decision by weeks or months.")
    add_bullet_item(doc, "Involuntary Churn", 
                    "This happens passively due to billing friction—expired corporate credit cards, failed payment gateway retries, or invoicing "
                    "delays. These accounts don't actually want to leave, but poor dunning processes push them out.")

    add_body_p(doc,
               "The core problem today isn't that companies lack data. Modern applications track everything: logins, clicks, billing receipts, "
               "and support tickets. The breakdown happens because this data sits in isolated silos. By the time a customer reaches out to cancel, "
               "their mind is already made up. What Customer Success teams need is a dependable, automated heads-up—an early detection radar that "
               "flags dropping engagement while there is still plenty of time to fix the relationship.")

    add_h2(doc, "1.2 Why Focus on Retention? The Compelling Business Math")
    add_body_p(doc,
               "From a pure return-on-investment perspective, retention is one of the highest-leverage areas a data science team can tackle:")
    
    add_bullet_item(doc, "Acquiring vs. Retaining Costs",
                    "Extensive industry studies from Bain & Company, Harvard Business Review, and SaaS Capital confirm that acquiring a new customer "
                    "costs roughly 5 to 7 times more than keeping an existing one. For enterprise accounts with 14 to 18-month payback windows, "
                    "early churn guarantees that the business loses money on the customer.")
    add_bullet_item(doc, "The Power of Compound Retention",
                    "A modest 5% improvement in customer retention can boost lifetime customer value and cumulative operating profits by 25% to 95%. "
                    "Retained customers expand their seats, adopt higher tiers, and require significantly lower onboarding support.")
    add_bullet_item(doc, "Sufficient Lead Time to Act",
                    "A machine learning model that alerts teams only 3 days before cancellation is almost useless. By framing our prediction target "
                    "around a 60-to-90-day forward-looking horizon, we provide account managers with realistic lead time to schedule reviews, address "
                    "product pain points, and offer customized incentives.")

    add_h2(doc, "1.3 Understanding Our Users & Stakeholders")
    add_body_p(doc,
               "A data science project only succeeds if the people on the front lines actually use its outputs. Here is how ChurnGuard AI serves each team:")
    
    add_bullet_item(doc, "Customer Success Managers (CSMs)",
                    "CSMs are our primary everyday users. They don't need confusing model probability decimals; they need prioritized risk lists and "
                    "clear reasons why an account is at risk (e.g., 'Weekly active users dropped by 60%' or 'Two unresolved priority tickets').")
    add_bullet_item(doc, "Retention & Lifecycle Marketing",
                    "Marketing needs automated risk tiering to trigger targeted re-engagement campaigns—such as onboarding refresher webinars, feature "
                    "walkthroughs, or timely promotional check-ins.")
    add_bullet_item(doc, "Executive Leadership (CRO / CFO)",
                    "Leadership requires clear visibility into net revenue retention (NRR) trajectories and high-risk ARR exposure to forecast quarterly renewals accurately.")
    add_bullet_item(doc, "Data Engineering & MLOps",
                    "Engineering needs clean, maintainable Python pipelines with reproducible transformations, clear data validation checks, and low-latency inference.")

    # -------------------------------------------------------------------------
    # SECTION 2: PROJECT OBJECTIVES, SCOPE DEFINITION & SUCCESS CRITERIA
    # -------------------------------------------------------------------------
    add_h1(doc, "2. Project Objectives, Scope Definition & Success Criteria")
    
    add_h2(doc, "2.1 Clear Technical & Business Objectives")
    add_body_p(doc,
               "We have defined concrete, realistic goals to ensure the project remains focused and achievable within our 32.5-hour timeline:")
    
    add_bullet_item(doc, "Predictive Discrimination",
                    "Train and validate a supervised classification pipeline that achieves an Area Under the ROC Curve (ROC-AUC) >= 0.86 and a "
                    "Precision-Recall AUC (PR-AUC) >= 0.65 on out-of-time test cohorts exhibiting realistic class imbalance (~12% churn rate).")
    add_bullet_item(doc, "Model Explainability (XAI)",
                    "Ensure 100% of flagged accounts include local TreeSHAP feature attributions so account managers immediately understand "
                    "the specific drivers behind every risk score.")
    add_bullet_item(doc, "Cost-Sensitive Thresholding",
                    "Replace naive 0.5 probability cutoffs with a financial utility framework that optimizes net retention ROI, factoring in real outreach "
                    "costs (C_outreach), customer lifetime value (CLV), and expected recovery rates (P_success).")
    add_bullet_item(doc, "Production-Ready Modular Code",
                    "Package the complete pipeline using standard Scikit-Learn transformers and modular Python best practices for seamless serialization.")

    add_h2(doc, "2.2 In-Scope Commitments vs. Out-of-Scope Boundaries")
    add_body_p(doc,
               "Scope creep is the number one reason data science projects run over budget and miss deadlines. "
               "To deliver high-impact results in 32.5 hours, we have clearly defined what we are building and what we are deliberately setting aside for later:")

    # Scope Table
    scope_tbl = doc.add_table(rows=6, cols=3)
    scope_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    scope_tbl.autofit = False
    col_w = [Inches(1.8), Inches(2.6), Inches(2.5)]
    
    headers = ["Functional Domain", "In-Scope Commitments (Week 1)", "Out-of-Scope Exclusions (Future Iterations)"]
    hdr_row = scope_tbl.rows[0]
    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        cell.width = col_w[c_idx]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    scope_data = [
        ("Data Ingestion & Synthesis", 
         "Multi-source historical batch ingestion, robust synthetic schema generator, missing value auditing, and point-in-time joins.",
         "Real-time streaming broker operations (Kafka cluster administration) and production database DDL schema migrations."),
        ("Feature Engineering",
         "RFM indicators, 30/60/90-day rolling activity velocity ratios, support ticket sentiment tags, and categorical target encoding.",
         "Complex unstructured video/voice call transcript NLP processing and computer vision analysis."),
        ("Modeling & Algorithms",
         "Penalized Logistic Regression, CART Decision Trees, Balanced Random Forest, LightGBM, XGBoost, and Optuna Bayesian tuning.",
         "Deep reinforcement learning agents, LLM fine-tuning, and compute-heavy neural architecture search (NAS)."),
        ("Evaluation & Explainability",
         "Time-based cross-validation, PR-AUC, Brier score calibration, TreeSHAP global/local attribution, and financial cost-utility matrix.",
         "Live multi-month customer A/B testing and automated execution of unapproved contract discounts without human review."),
        ("Deployment & Packaging",
         "Joblib pipeline serialization, containerized batch scoring module, and modular REST inference schema (FastAPI).",
         "Full custom frontend UI development from scratch, multi-region Kubernetes deployments, and 24/7 on-call rotation setup.")
    ]

    for r_idx, (dom, inc, exc) in enumerate(scope_data, start=1):
        row = scope_tbl.rows[r_idx]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate([dom, inc, exc]):
            cell = row.cells[c_idx]
            cell.width = col_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            set_cell_border(cell, top="E2E8F0", bottom="E2E8F0", left="E2E8F0", right="E2E8F0")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            else:
                r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_h2(doc, "2.3 How We Measure Success: Core KPIs")
    add_body_p(doc,
               "We evaluate our system on both scientific quality and practical business utility:")
    
    add_bullet_item(doc, "ROC-AUC Score >= 0.86", "Measures our model's ability to rank churners above non-churners across all possible decision thresholds.")
    add_bullet_item(doc, "PR-AUC Score >= 0.65", "Our primary metric for imbalanced data (~12% churn rate), ensuring high precision when recalling high-risk accounts.")
    add_bullet_item(doc, "Brier Calibration Score <= 0.12", "Confirms that a predicted probability of 0.70 translates to an actual 70% churn rate in practice.")
    add_bullet_item(doc, "Top-Decile Lift >= 3.5x", "Ensures the top 10% highest-risk accounts identified by the model have at least 3.5x higher churn frequency than average.")
    add_bullet_item(doc, "Net Retention Uplift", "Targeting a 2.0% to 3.5% reduction in annual gross revenue churn across pilot enterprise cohorts.")

    # -------------------------------------------------------------------------
    # SECTION 3: END-TO-END METHODOLOGY & TECHNICAL STRATEGY
    # -------------------------------------------------------------------------
    add_h1(doc, "3. End-to-End Technical Methodology & Data Science Strategy")
    
    add_h2(doc, "3.1 Data Sources: Bringing Disparate Signals Together")
    add_body_p(doc,
               "Customer churn cannot be understood from a single table. A customer might have an active subscription on paper, but their actual "
               "usage might have collapsed weeks ago. ChurnGuard AI unites four core data streams:")
    
    add_bullet_item(doc, "Account & Profile Metadata (CRM / Data Warehouse)",
                    "Basic account characteristics: account tenure, business size (Enterprise, Mid-Market, SMB), contract type (Annual vs. Monthly), "
                    "total licensed seats, annual recurring revenue (ARR), industry vertical, and geographic region.")
    add_bullet_item(doc, "Product Engagement & Telemetry Logs",
                    "The heartbeat of user behavior: daily and weekly active users (DAU/WAU), session counts, core feature adoption, API call volume, "
                    "and export activity. Dropping activity here is our earliest warning indicator.")
    add_bullet_item(doc, "Billing, Invoicing & Payment History",
                    "Financial touchpoints: historical payment failures, credit card expiration proximity, invoice payment delays, applied credits, "
                    "and refund requests.")
    add_bullet_item(doc, "Customer Support & Feedback Logs",
                    "Customer frustration signals: support ticket frequency, escalation counts, resolution duration, Customer Satisfaction (CSAT) scores, "
                    "and NLP sentiment tags from customer tickets.")

    add_h2(doc, "3.2 Data Cleaning & Preprocessing: Avoiding Common Pitfalls")
    add_body_p(doc,
               "In data science, bad data produces deceptive models. We apply thoughtful, battle-tested cleaning strategies:")
    
    add_bullet_item(doc, "Context-Aware Missing Value Imputation",
                    "Naive mean imputation ruins feature distributions. For behavioral metrics (like logins or exports), missing data usually means the user did nothing—so we impute with 0. "
                    "For structural profile features, we use K-Nearest Neighbors (KNN) or grouped medians based on account tier. Missing categoricals are kept as 'Unknown' "
                    "to preserve informative missingness.")
    add_bullet_item(doc, "Handling Extreme Outliers (Power Users vs. Bots)",
                    "API usage and event counts often have massive right tails (e.g., an automated script generating 50,000 requests). "
                    "We use 1st and 99th percentile winsorization (clipping) alongside robust scaling transforms to keep gradients stable during training.")
    add_bullet_item(doc, "Data Contracts & Schema Validation",
                    "We use Great Expectations to enforce data contracts: verifying account IDs are unique, timestamps are normalized to UTC ISO-8601, "
                    "and currencies are converted into standard USD equivalents before feeding into the modeling pipeline.")

    add_h2(doc, "3.3 Exploratory Data Analysis (EDA): Uncovering the Story in the Data")
    add_body_p(doc,
               "Before jumping into training, we take time to understand the underlying behavioral distributions:")
    
    add_bullet_item(doc, "Survival Analysis (Kaplan-Meier Curves)",
                    "Survival curves model customer retention over time, revealing natural danger zones—such as the 'Onboarding Cliff' (Days 14 to 30) "
                    "and the 'Renewal Hesitation Window' (Months 10 to 12). This guides when retention interventions should be triggered.")
    add_bullet_item(doc, "Multicollinearity Checks (VIF & Heatmaps)",
                    "Highly redundant features confuse models and dilute feature importance. We check correlation matrices and Variance Inflation Factor (VIF) "
                    "scores to consolidate collinear metrics (such as daily logins and total session minutes).")
    add_bullet_item(doc, "Bivariate Risk Cohort Analysis",
                    "Examining churn rates conditioned on contract length, payment method, and feature usage to identify strong non-linear relationships.")

    add_h2(doc, "3.4 Feature Engineering: Building Real Predictive Signals")
    add_body_p(doc,
               "In tabular machine learning, feature engineering is where models are won or lost. We craft 65+ specialized signals, focusing on behavioral momentum:")
    
    add_bullet_item(doc, "Strict Point-in-Time Joins (Zero Data Leakage)",
                    "Data leakage is the single most common mistake in churn modeling. If a feature includes data from after the prediction cutoff date, "
                    "your validation score will look amazing, but your model will collapse in production. All features for observation date T use data strictly "
                    "prior to T, while the target label (churned within next 60 days) is calculated strictly in the forward-looking evaluation window [T to T + 60 days].")
    add_bullet_item(doc, "RFM Behavioral Indicators",
                    "Recency (days since last admin login), Frequency (active days in the last 30 days), and Monetary (MRR per active seat).")
    add_bullet_item(doc, "Velocity & Acceleration Ratios (The Engagement Drop-Off Signal)",
                    "A static number of logins doesn't tell the full story; what matters is the direction of travel. We compute an Activity Velocity Ratio: "
                    "Activity Velocity Ratio = (Trailing 30-Day Activity) / [(Trailing 90-Day Activity / 3) + epsilon]. "
                    "A ratio below 0.60 indicates that user engagement has dropped by 40%+ compared to their quarterly baseline—one of our strongest churn indicators.")
    add_bullet_item(doc, "Support Ticket Friction Index",
                    "A combined index tracking ticket escalation frequency, long resolution delays, and negative sentiment flags.")

    add_h2(doc, "3.5 Machine Learning Modeling: Why We Chose Tree Ensembles")
    add_body_p(doc,
               "We compare transparent linear baselines against state-of-the-art gradient boosted trees:")
    
    add_bullet_item(doc, "Why Not Deep Learning or LLMs?",
               "While neural networks and LLMs are powerful for text and images, gradient boosted decision trees (GBDTs) like LightGBM and XGBoost "
               "consistently outperform deep learning on structured tabular business data. They handle mixed feature types naturally, train in minutes, "
               "require vastly less compute, and allow direct, exact SHAP explainability.")
    add_bullet_item(doc, "Validation Protocol (Stratified TimeSeriesSplit)",
                    "We use 5-Fold Stratified Time-Series Cross-Validation. Data rolls forward chronologically so the model is always trained on past cohorts "
                    "and validated on future ones, matching real-world deployment.")
    add_bullet_item(doc, "Handling Class Imbalance (~12% Churn Rate)",
                    "To prevent models from simply predicting that nobody churns, we apply SMOTE-NC strictly inside training folds and use class-weighted "
                    "loss functions (such as LightGBM's scale_pos_weight).")
    add_bullet_item(doc, "Benchmarked Algorithms",
                    "1. Baseline 1: L1/L2 Penalized Logistic Regression (convex, transparent baseline).\n"
                    "2. Baseline 2: Pruned CART Decision Tree (intuitive decision rules).\n"
                    "3. Balanced Random Forest (robust bagging ensemble with out-of-bag validation).\n"
                    "4. LightGBM (Histogram-based gradient boosting; champion candidate for speed and accuracy).\n"
                    "5. XGBoost (Exact second-order gradient boosting with robust regularization).\n"
                    "6. CatBoost (Specialized categorical split optimization).")
    add_bullet_item(doc, "Bayesian Hyperparameter Tuning (Optuna)",
                    "We use Optuna to run 150 automated Bayesian trials optimizing PR-AUC and Brier calibration score, intelligently pruning unpromising configurations.")

    add_h2(doc, "3.6 Probability Calibration & Financial Cost-Utility Matrix")
    add_body_p(doc,
               "Raw model scores from boosted trees are often uncalibrated rankings rather than true probabilities. If a model says an account has a 0.70 risk score, "
               "we need that to mean that exactly 70 out of 100 such accounts actually churn. We calibrate raw outputs using Isotonic Regression and evaluate Brier scores.")
    
    add_body_p(doc,
               "Furthermore, standard classification defaults to an arbitrary 0.50 probability cutoff. In business, that makes no sense: saving an $8,400 enterprise account "
               "is worth spending $150 of a CSM's time on, even if the churn risk is only 35%. We calculate an optimal decision threshold (t*) using a net financial utility equation:")
    add_body_p(doc,
               "Net Economic Utility(t) = Sum over True Positives [ P_success * CLV - C_outreach ] - Sum over False Positives [ C_outreach ] - Sum over False Negatives [ CLV ]\n"
               "Where C_outreach is the intervention cost (e.g., $150 CSM review), CLV is the customer lifetime value (e.g., $8,400), and P_success is the expected save rate (e.g., 35%).",
               bold_prefix="Decision Formula: ")

    add_h2(doc, "3.7 Explainable AI (XAI): Turning Predictions into Action")
    add_body_p(doc,
               "A prediction without an explanation is useless to an account manager. If an alert just says 'Account #8192 has an 84% churn risk', "
               "the CSM won't know what to say. ChurnGuard AI integrates TreeSHAP:")
    
    add_bullet_item(doc, "Global Model Transparency",
                    "Global SHAP beeswarm plots show the top systemic churn drivers across the entire business (e.g., 30-day login contraction, payment failure streaks).")
    add_bullet_item(doc, "Individual Account Waterfall Charts",
                    "For every account flagged in the weekly report, we produce a local breakdown showing exactly what drove the score: "
                    "'Baseline Risk: 12% | +28% due to 65% drop in active seats | +18% due to 3 open support tickets | -6% due to 2-year tenure | Total Risk: 52%'. "
                    "Now the CSM can call the client with specific solutions ready.")

    # -------------------------------------------------------------------------
    # SECTION 4: STRATEGIC ARCHITECTURE & LIFECYCLE DIAGRAMS
    # -------------------------------------------------------------------------
    add_h1(doc, "4. Strategic Architecture & Lifecycle Diagrams")
    add_body_p(doc,
               "To make the planning and system design tangible, we developed three comprehensive visual diagrams:")

    # Diagram 1
    add_h2(doc, "4.1 End-to-End System Architecture & Data Lifecycle")
    add_body_p(doc,
               "Figure 1 illustrates how raw multi-source data travels through ingestion, feature stores, modeling, and downstream CRM tools:")
    add_image_box(doc, r"e:\Code Playground\Sumu\assets\diagram_1_architecture.png", 
                  "Figure 1", 
                  "End-to-End Predictive Analytics Architecture for ChurnGuard AI (Ingestion -> Feature Store -> ML Pipeline -> Explainability -> Operational CRM)")
    add_body_p(doc,
               "How the Architecture Functions: Disparate operational databases feed the raw staging layer. The wrangling pipeline enforces point-in-time "
               "temporal joins to eliminate leakage. The modeling engine evaluates candidates and performs Bayesian hyperparameter optimization. "
               "Calibrated probabilities and SHAP attributions are generated, and weekly batch jobs deliver prioritized alerts directly into Salesforce/HubSpot.")

    # Diagram 3
    add_h2(doc, "4.2 Machine Learning Validation, Calibration & Decision Pipeline")
    add_body_p(doc,
               "Figure 2 details the step-by-step modeling logic, temporal cross-validation boundaries, cost-sensitive thresholding, and production gating criteria:")
    add_image_box(doc, r"e:\Code Playground\Sumu\assets\diagram_3_ml_pipeline.png", 
                  "Figure 2", 
                  "Machine Learning Validation, Probability Calibration & Decision Framework")
    add_body_p(doc,
               "How the Modeling Pipeline Functions: The master feature matrix is strictly partitioned chronologically. Stratified 5-fold cross-validation "
               "benchmarks linear baselines against tree ensembles. Hyperparameter tuning targets PR-AUC and Brier scores. Finally, the calibrated model "
               "must pass four strict gating criteria (discrimination, financial ROI, calibration quality, and inference latency) before deployment.")

    # -------------------------------------------------------------------------
    # SECTION 5: PROJECT IMPLEMENTATION TIMELINE & RESOURCE ALLOCATION
    # -------------------------------------------------------------------------
    add_h1(doc, "5. Project Implementation Timeline & Resource Allocation (32.5 Hours)")
    
    add_h2(doc, "5.1 Realistic Work Breakdown: Why 32.5 Hours?")
    add_body_p(doc,
               "Any seasoned data scientist knows that training a model is only about 20% of the job. In real projects, the vast majority of time "
               "is spent understanding business requirements, hunting down data quirks, auditing quality, and engineering meaningful features. "
               "We have mapped out a 32.5-hour schedule (at 6.5 hours/day over 5 days), leaving a 2.5-hour buffer within our 35-hour ceiling:")

    # WBS Table
    wbs_tbl = doc.add_table(rows=7, cols=5)
    wbs_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    wbs_tbl.autofit = False
    wbs_col_w = [Inches(1.1), Inches(2.2), Inches(0.9), Inches(1.0), Inches(1.7)]
    wbs_headers = ["Phase", "Phase Name & Scope", "Hours", "Days", "Core Deliverable & Milestone"]
    
    w_hdr_row = wbs_tbl.rows[0]
    for c_idx, h_text in enumerate(wbs_headers):
        cell = w_hdr_row.cells[c_idx]
        cell.width = wbs_col_w[c_idx]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    wbs_data = [
        ("Phase 1", "Project Scoping, Problem Formulation & Architecture", "4.5 h", "Day 1", "Project Charter, Schema Spec & Architecture Blueprint"),
        ("Phase 2", "Data Ingestion, Auditing & Cleansing Pipeline", "5.0 h", "Day 1-2", "Cleaned Master Dataset & Great Expectations Suite"),
        ("Phase 3", "Exploratory Data Analysis & Feature Engineering Store", "6.5 h", "Day 2-3", "65+ Feature Store Matrix & Survival Curve Analysis"),
        ("Phase 4", "Model Exploration, Baseline & Advanced Ensembles", "7.5 h", "Day 3-4", "Benchmark Comparison Matrix & Tuned Champion Model"),
        ("Phase 5", "Calibration, SHAP Explainability & Cost-Sensitive Tuning", "5.0 h", "Day 4-5", "Calibrated Pipeline, SHAP Explainer & Cost Policy"),
        ("Phase 6", "Strategic Synthesis, Packaging & Final Documentation", "4.0 h", "Day 5", "Comprehensive DOCX Report, Code Artifacts & Pitch")
    ]

    for r_idx, row_vals in enumerate(wbs_data, start=1):
        row = wbs_tbl.rows[r_idx]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = wbs_col_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            set_cell_border(cell, top="E2E8F0", bottom="E2E8F0", left="E2E8F0", right="E2E8F0")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            elif c_idx == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
            else:
                r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Detailed Phase Breakdown
    add_h2(doc, "5.2 Day-by-Day Task Execution Plan")
    
    add_bullet_item(doc, "Phase 1: Project Scoping & Architecture (4.5 Hours — Day 1)",
                    "Align with Customer Success and Sales stakeholders on target churn horizons (1.5h); audit raw database schemas and data availability (1.5h); "
                    "scaffold project directory and define repository structure (1.5h).")
    add_bullet_item(doc, "Phase 2: Ingestion, Auditing & Cleansing (5.0 Hours — Day 1 to 2)",
                    "Build data ingestion pipelines and synthetic test generators (1.5h); profile data for missing values and anomalies (1.5h); "
                    "construct KNN/median imputation transformers and Great Expectations test suites (2.0h).")
    add_bullet_item(doc, "Phase 3: Exploratory Data Analysis & Feature Engineering (6.5 Hours — Day 2 to 3)",
                    "Compute univariate/bivariate distributions and cohort churn rates (1.5h); plot Kaplan-Meier survival curves and analyze VIF collinearity (1.5h); "
                    "engineer point-in-time RFM indicators (2.0h); construct 30-day activity velocity ratios and support friction indices (1.5h).")
    add_bullet_item(doc, "Phase 4: Model Exploration & Ensembles (7.5 Hours — Day 3 to 4)",
                    "Implement 5-Fold Stratified TimeSeriesSplit validation (1.0h); build Penalized Logistic Regression and Decision Tree baselines (1.5h); "
                    "train Random Forest, LightGBM, and XGBoost models (2.5h); run 150 Bayesian hyperparameter optimization trials using Optuna (2.5h).")
    add_bullet_item(doc, "Phase 5: Calibration, SHAP & Cost Tuning (5.0 Hours — Day 4 to 5)",
                    "Fit Isotonic Regression probability calibration curves and minimize Brier score (1.5h); calculate optimal decision threshold (t*) via cost-utility matrix (1.5h); "
                    "build TreeSHAP explainer to produce global beeswarm plots and local waterfall charts (2.0h).")
    add_bullet_item(doc, "Phase 6: Synthesis, Packaging & Final Documentation (4.0 Hours — Day 5)",
                    "Serialize the end-to-end pipeline into `pipeline.joblib` (1.0h); compile comprehensive technical documentation and model cards (2.0h); "
                    "synthesize executive summary and present findings to leadership (1.0h).")

    # Diagram 2 (Gantt Chart)
    add_h2(doc, "5.3 Critical Path Analysis & Resource Gantt Schedule")
    add_body_p(doc,
               "Figure 3 illustrates our Gantt schedule across the 5 working days, highlighting phase boundaries and milestone checkpoints:")
    add_image_box(doc, r"e:\Code Playground\Sumu\assets\diagram_2_gantt_timeline.png", 
                  "Figure 3", 
                  "Project Implementation Timeline, Phase Allocations & Critical Path Gantt Schedule (32.5 Hours Total Effort)")
    add_body_p(doc,
               "Pacing & Resilience: With 6.5 working hours allocated per day, the schedule is rigorous yet sustainable. The remaining 2.5-hour contingency "
               "buffer protects against unexpected data schema issues or extra hyperparameter search iterations without putting deadlines at risk.")

    # -------------------------------------------------------------------------
    # SECTION 6: PYTHON ECOSYSTEM & TECHNICAL TOOLING STACK
    # -------------------------------------------------------------------------
    add_h1(doc, "6. Python Ecosystem & Technical Tooling Stack")
    add_body_p(doc,
               "Python 3.12+ was selected as our core environment because it offers the most mature, high-performance ecosystem for tabular machine learning. "
               "Each library in our stack was chosen for stability, developer speed, and enterprise reliability:")

    # Tooling Table
    tool_tbl = doc.add_table(rows=8, cols=4)
    tool_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tool_tbl.autofit = False
    tool_col_w = [Inches(1.5), Inches(1.4), Inches(0.8), Inches(3.2)]
    tool_headers = ["Functional Layer", "Library / Framework", "Version", "Technical Justification & Purpose"]
    
    t_hdr_row = tool_tbl.rows[0]
    for c_idx, h_text in enumerate(tool_headers):
        cell = t_hdr_row.cells[c_idx]
        cell.width = tool_col_w[c_idx]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tool_data = [
        ("Data Manipulation & Ingestion", "pandas\nnumpy", ">= 2.2.0\n>= 1.26.0", "Vectorized table operations, temporal joins, rolling window calculations, and fast numeric arrays."),
        ("Data Quality & Auditing", "great-expectations\npydantic", ">= 0.18.0\n>= 2.6.0", "Declarative schema validation, missing data boundary testing, and strict data type enforcement."),
        ("Exploratory Data Analysis", "matplotlib\nseaborn\nlifelines", ">= 3.8.0\n>= 0.13.0\n>= 0.28.0", "Statistical data visualization, correlation heatmaps, distribution plots, and Kaplan-Meier survival analysis."),
        ("Feature Engineering & Imbalance", "scikit-learn\nimbalanced-learn", ">= 1.4.0\n>= 0.12.0", "Custom Transformer pipelines, RobustScaler, TargetEncoder, and SMOTE-NC minority oversampling."),
        ("Machine Learning Algorithms", "lightgbm\nxgboost\ncatboost", ">= 4.3.0\n>= 2.0.0\n>= 1.2.0", "State-of-the-art gradient boosted decision trees optimized for speed, memory efficiency, and tabular accuracy."),
        ("Hyperparameter Optimization", "optuna", ">= 3.5.0", "Bayesian hyperparameter optimization using Tree-structured Parzen Estimator (TPE) algorithm with automated pruning."),
        ("Explainability & MLOps", "shap\nmlflow\njoblib", ">= 0.44.0\n>= 2.10.0\n>= 1.3.0", "Game-theoretic TreeSHAP feature attributions, experiment parameter tracking, and pipeline serialization.")
    ]

    for r_idx, row_vals in enumerate(tool_data, start=1):
        row = tool_tbl.rows[r_idx]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = tool_col_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            set_cell_border(cell, top="E2E8F0", bottom="E2E8F0", left="E2E8F0", right="E2E8F0")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            elif c_idx == 1:
                r.bold = True
                r.font.color.rgb = RGBColor(0x0D, 0x94, 0x88)
            else:
                r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_h2(doc, "6.2 Reproducibility & Engineering Hygiene")
    add_body_p(doc,
               "We maintain professional software engineering standards throughout the project:")
    
    add_bullet_item(doc, "Deterministic Random Seeds",
                    "A global seed (`RANDOM_STATE = 42`) is pinned across NumPy, Scikit-Learn, LightGBM, and XGBoost to ensure identical results across runs.")
    add_bullet_item(doc, "Isolated Virtual Environments",
                    "All dependencies are managed via `venv` or `poetry` with fully pinned versions in `requirements.txt`.")
    add_bullet_item(doc, "Automated Unit Tests with PyTest",
                    "Automated tests verify that data transformations produce zero NaNs, preserve row counts, and contain zero lookahead leakage.")

    # -------------------------------------------------------------------------
    # SECTION 7: ANTICIPATED OUTCOMES, BUSINESS VALUE & COMPREHENSIVE RISK MATRIX
    # -------------------------------------------------------------------------
    add_h1(doc, "7. Anticipated Outcomes, Business Value & Comprehensive Risk Matrix")
    
    add_h2(doc, "7.1 Tangible Deliverables Handed Over to the Business")
    add_body_p(doc,
               "Upon completion of this initiative, the organization receives concrete, production-ready assets:")
    
    add_bullet_item(doc, "Serialized Inference Pipeline (`pipeline.joblib`)",
                    "A single, modular artifact bundling missing value imputation, robust scaling, categorical encoding, the calibrated LightGBM model, and the SHAP explainer.")
    add_bullet_item(doc, "Automated Batch Scoring Worker",
                    "A Python script that runs weekly to score the customer base, segment accounts into High/Medium/Low risk tiers, and update CRM tables.")
    add_bullet_item(doc, "Executive Model Card & Report",
                    "Complete documentation covering model performance, discrimination curves, calibration diagnostics, and fairness checks.")

    add_h2(doc, "7.2 Practical Risk Assessment & Mitigation Matrix")
    add_body_p(doc,
               "In production data science, things rarely go 100% as planned. We have cataloged 10 common failure modes and built defensive strategies for each:")

    # Risk Table
    risk_tbl = doc.add_table(rows=11, cols=6)
    risk_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    risk_tbl.autofit = False
    risk_col_w = [Inches(0.6), Inches(1.4), Inches(1.8), Inches(0.7), Inches(0.7), Inches(1.7)]
    risk_headers = ["ID", "Risk Category", "Risk Description & Threat", "Severity", "Prob.", "Mitigation Strategy & Contingency Protocol"]
    
    r_hdr_row = risk_tbl.rows[0]
    for c_idx, h_text in enumerate(risk_headers):
        cell = r_hdr_row.cells[c_idx]
        cell.width = risk_col_w[c_idx]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, top=100, bottom=100, left=60, right=60)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    risk_data = [
        ("R-01", "Data Leakage", "Future activity signals inadvertently included in historical training features.", "CRITICAL", "MED", "Enforce strict point-in-time joins; automated unit tests verify feature timestamps strictly precede label window."),
        ("R-02", "Class Imbalance", "Churn rate is ~12%, causing naive models to predict majority non-churn.", "HIGH", "HIGH", "Optimize PR-AUC and cost-sensitive loss; apply SMOTE-NC strictly inside training cross-validation folds."),
        ("R-03", "Concept Drift", "Customer behavior shifts due to product updates or market conditions.", "HIGH", "MED", "Track Population Stability Index (PSI) monthly; trigger retraining alerts if PSI exceeds 0.20."),
        ("R-04", "Uncalibrated Scores", "Raw model probabilities overestimate or underestimate true empirical churn rate.", "HIGH", "HIGH", "Apply Isotonic Regression calibration; evaluate Brier score and Expected Calibration Error (ECE < 0.05)."),
        ("R-05", "Cold-Start Accounts", "New accounts (< 30 days) lack historical telemetry for reliable model inference.", "MED", "HIGH", "Deploy fallback onboarding heuristic rules based on setup completion and first-week login frequency."),
        ("R-06", "High-Cardinality Features", "Categorical features (e.g. zip code, marketing campaign ID) cause overfitting.", "MED", "MED", "Deploy smoothed target encoding with cross-validation regularization and frequency capping."),
        ("R-07", "Overfitting / Optimism", "Model captures historical noise without generalizing to new cohorts.", "HIGH", "MED", "Enforce 5-Fold Stratified TimeSeriesSplit with strict out-of-time test set (Month 12 holdout)."),
        ("R-08", "Actionability Gap", "Predictions are accurate but lack causal levers for CSMs to intervene effectively.", "HIGH", "MED", "Generate local TreeSHAP waterfall charts; map top negative features to specific CSM playbook actions."),
        ("R-09", "Data Privacy (GDPR/CCPA)", "Inference features expose Personally Identifiable Information (PII) inappropriately.", "HIGH", "LOW", "Hash/strip all PII (names, emails) at ingestion; utilize anonymous account UUIDs throughout modeling."),
        ("R-10", "Pipeline Execution Failure", "Missing upstream API payloads cause batch scoring script to crash unexpectedly.", "MED", "MED", "Wrap scoring script in try-except fallbacks; log missing telemetry; generate alert emails to engineering.")
    ]

    for r_idx, row_vals in enumerate(risk_data, start=1):
        row = risk_tbl.rows[r_idx]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = risk_col_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            set_cell_border(cell, top="E2E8F0", bottom="E2E8F0", left="E2E8F0", right="E2E8F0")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            elif c_idx == 3:
                r.bold = True
                if val == "CRITICAL":
                    r.font.color.rgb = RGBColor(0xDC, 0x26, 0x26)
                elif val == "HIGH":
                    r.font.color.rgb = RGBColor(0xEA, 0x58, 0x0C)
                else:
                    r.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
            else:
                r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # SECTION 8: TRANSITION ROADMAP & NEXT STEPS FOR WEEK 2
    # -------------------------------------------------------------------------
    add_h1(doc, "8. Transition Roadmap & Next Steps for Technical Execution")
    add_body_p(doc,
               "With this strategy and architecture locked in Week 1, we are fully prepared to begin hands-on technical execution in Week 2. "
               "The immediate next steps are:")
    
    add_bullet_item(doc, "Step 1: Environment Provisioning",
                    "Set up virtual environment (`venv`) and install pinned dependencies from `requirements.txt`.")
    add_bullet_item(doc, "Step 2: Synthetic Data & Schema Pipeline",
                    "Execute the data generation script to synthesize 100,000 multi-table customer records with 12 months of realistic telemetry.")
    add_bullet_item(doc, "Step 3: Baseline Notebook Execution",
                    "Run `notebooks/01_eda_and_feature_engineering.ipynb` and `notebooks/02_model_benchmarking.ipynb` to establish benchmark metrics.")
    add_bullet_item(doc, "Step 4: Stakeholder Review",
                    "Review validation metrics and SHAP explanations with Customer Success leadership to calibrate risk tier cutoffs.")

    # Formal Approval Block
    add_h2(doc, "8.1 Strategy Sign-Off & Project Governance Registry")
    
    appr_tbl = doc.add_table(rows=4, cols=4)
    appr_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    appr_tbl.autofit = False
    appr_col_w = [Inches(1.8), Inches(1.8), Inches(1.5), Inches(1.8)]
    appr_headers = ["Project Role", "Name & Contact", "Approval Status", "Sign-Off Date"]
    
    a_hdr_row = appr_tbl.rows[0]
    for c_idx, h_text in enumerate(appr_headers):
        cell = a_hdr_row.cells[c_idx]
        cell.width = appr_col_w[c_idx]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    appr_data = [
        ("Lead Data Science Architect", "Sumarjana Biswas (sumarjanabiswas690@gmail.com)", "APPROVED (Strategy Locked)", "2026-09-17"),
        ("VP of Customer Success", "Stakeholder Review Board", "PENDING PILOT LAUNCH", "Tentative Week 2"),
        ("Chief Revenue Officer (CRO)", "Executive Sponsor", "CHARTER ENDORSED", "2026-09-17")
    ]

    for r_idx, row_vals in enumerate(appr_data, start=1):
        row = appr_tbl.rows[r_idx]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = appr_col_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            set_cell_border(cell, top="E2E8F0", bottom="E2E8F0", left="E2E8F0", right="E2E8F0")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            elif c_idx == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(0x05, 0x96, 0x69) if "APPROVED" in val or "ENDORSED" in val else RGBColor(0xD9, 0x77, 0x06)
            else:
                r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # Save the document
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Save candidate paths
    dir_name = os.path.dirname(os.path.abspath(output_path))
    candidates = [
        os.path.join(dir_name, "Data_Science_Project_Plan_Week_1_Sumarjana_Biswas.docx"),
        os.path.join(dir_name, "Data_Science_Project_Plan_Week_1_Final.docx"),
        os.path.join(dir_name, "Data_Science_Project_Plan_Week_1_Updated.docx"),
        os.path.join(dir_name, "Data_Science_Project_Plan_Week_1.docx"),
    ]
    
    saved_paths = []
    for path in candidates:
        try:
            doc.save(path)
            saved_paths.append(path)
            print(f"[SUCCESS] Saved to: {path}")
        except PermissionError:
            print(f"[LOCKED] File currently open in Word: {path}")
    
    if not saved_paths:
        raise PermissionError("All candidate file paths are currently locked by Word. Please close Word and retry.")

if __name__ == "__main__":
    output_docx = r"e:\Code Playground\Sumu\Data_Science_Project_Plan_Week_1.docx"
    build_project_plan_document(output_docx)
