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
# DIAGRAM 1: 5-Stage Universal EDA Lifecycle & Decision Flowchart
# ==============================================================================
def create_eda_lifecycle_diagram(output_path):
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
    draw.text((90, 60), "OmniEDA: The 5-Stage Universal Exploratory Data Analysis Lifecycle", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "A Rigorous, Dataset-Agnostic Blueprint: Ingestion & Integrity -> Structural Profiling -> Univariate Exploration -> Bivariate & Multivariate -> Synthesis", fill="#94A3B8", font=f_subtitle)

    pillars = [
        {
            "num": "01",
            "title": "Ingestion & Sanity",
            "sub": "Data hygiene & validation",
            "color": "#0284C7",
            "bg": "#F0F9FF",
            "border": "#BAE6FD",
            "cards": [
                ("Schema & Shape Audit", "Pandas & Great Expectations\nVerify dimensions, column types, duplicate primary keys"),
                ("Missingness Diagnostics", "Missingno Matrix & Heatmaps\nCategorize mechanisms: MCAR, MAR, or MNAR"),
                ("Extreme Value Scans", "Tukey IQR & Robust Z-Scores\nFlag measurement errors vs. legitimate black swans"),
                ("Data Dictionary Mapping", "Automated Metadata Registry\nClassify numeric, categorical, temporal, and text types")
            ]
        },
        {
            "num": "02",
            "title": "Univariate Profiling",
            "sub": "Individual variable dynamics",
            "color": "#0D9488",
            "bg": "#F0FDFA",
            "border": "#99F6E4",
            "cards": [
                ("Continuous Distributions", "Histograms, KDE & Box Plots\nCentral tendency, spread, skewness, and heavy tails"),
                ("Normality & Goodness-of-Fit", "Shapiro-Wilk & Q-Q Plots\nDetermine transformation needs (Log, Box-Cox, Yeo-Johnson)"),
                ("Categorical Frequencies", "Count Plots & Pareto Analysis\nCardinals, class imbalance, and rare label clustering"),
                ("Temporal & Trend Check", "Time-series line & rollings\nSeasonality, stationarity checks, and interval gaps")
            ]
        },
        {
            "num": "03",
            "title": "Bivariate Exploration",
            "sub": "Pairwise interactions & tests",
            "color": "#4F46E5",
            "bg": "#EEF2FF",
            "border": "#C7D2FE",
            "cards": [
                ("Numeric vs. Numeric", "Scatter Plots & Spearmans\nLinear vs monotonic correlation, non-linear curvature"),
                ("Numeric vs. Categorical", "Violin Plots, Box Grids, ANOVA\nAssess subgroup variance differences and median shifts"),
                ("Categorical vs. Categorical", "Contingency Tables & Heatmaps\nChi-Square tests of independence and Cramer V metrics"),
                ("Target Association Audit", "Feature-to-Target Sorting\nIdentify early predictive power and prospective drivers")
            ]
        },
        {
            "num": "04",
            "title": "Multivariate Analysis",
            "sub": "High-dimensional patterns",
            "color": "#9333EA",
            "bg": "#FAF5FF",
            "border": "#E9D5FF",
            "cards": [
                ("Collinearity & VIF Auditing", "Variance Inflation Factor\nPrune redundant features with high multi-collinearity"),
                ("Dimensionality Reduction", "PCA & t-SNE / UMAP Projections\nDecompose variance and visualize hidden latent clusters"),
                ("Faceted Interaction Grids", "Seaborn FacetGrid & PairGrid\nCondition relationships across 3 to 4 dimensions simultaneously"),
                ("Subgroup Segmentation", "Hierarchical Dendrograms\nDiscover natural customer/data sub-populations")
            ]
        },
        {
            "num": "05",
            "title": "Synthesis & Handoff",
            "sub": "Actionable modeling readiness",
            "color": "#E11D48",
            "bg": "#FFF1F2",
            "border": "#FECDD3",
            "cards": [
                ("Data Quality Scorecard", "Executive Health Summary\nQuantify data usability, missingness impact, and risks"),
                ("Feature Roadmap Spec", "Transform & Encoding Blueprints\nImputation rules, scaling choices, and interaction ideas"),
                ("Modeling Guardrails", "Leakage & Bias Documentation\nTime cutoffs, class re-balancing strategy, baseline targets"),
                ("Interactive Stakeholder Deck", "Plotly / Quarto Dashboard\nCommunicate insights cleanly to technical and business teams")
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
    draw.text((80, height - 52), "Figure 1: OmniEDA Universal 5-Stage Exploratory Data Analysis & Analytical Decision Lifecycle (Sumarjana Biswas - Week 2 Framework)", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved Diagram 1 to {output_path}")

# ==============================================================================
# DIAGRAM 2: Statistical Visualization Taxonomy & Plot Selection Decision Matrix
# ==============================================================================
def create_eda_taxonomy_diagram(output_path):
    width, height = 2400, 1400
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(40, bold=True)
    f_subtitle = get_font(21, bold=False)
    f_card_title = get_font(20, bold=True)
    f_card_sub = get_font(16, bold=True)
    f_card_body = get_font(15, bold=False)
    f_footer = get_font(16, bold=False)

    draw_rounded_rect(draw, [50, 40, width - 50, 160], radius=16, fill="#0F172A", outline="#1E293B", width=2)
    draw.text((90, 60), "OmniEDA: Diagnostic Visualization Taxonomy & Plot Selection Matrix", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "Systematic Mapping of Data Types & Analytical Questions to Optimal Plot Architectures in Python (Matplotlib, Seaborn, Plotly)", fill="#94A3B8", font=f_subtitle)

    # 4 Quadrants / Categories of Visualization Strategy:
    # 1. Distribution & Spread (Top-Left)
    # 2. Association & Relationships (Top-Right)
    # 3. Categorical Comparisons & Rankings (Bottom-Left)
    # 4. Temporal, High-Dimensional & Compositional (Bottom-Right)

    quads = [
        {
            "bbox": [70, 200, 1170, 680],
            "title": "1. Distribution, Spread & Outlier Profiling",
            "color": "#0284C7",
            "bg": "#F0F9FF",
            "border": "#BAE6FD",
            "purpose": "Primary Goal: Assess shape, symmetry, central tendency, multimodality, and tail heaviness",
            "items": [
                ("Histogram + KDE Curve", "Seaborn histplot(kde=True) | Matplotlib", "Reveals unimodal vs bimodal distribution, skewness, and peak concentration zones."),
                ("Box Plot & Whiskers", "Seaborn boxplot() | Plotly express.box()", "Highlights median, 25th/75th percentiles, and points exceeding 1.5x IQR boundaries."),
                ("Violin Plot (KDE + Box)", "Seaborn violinplot(inner='quartile')", "Combines box plot summary metrics with full probability density width profiles."),
                ("Empirical CDF (ECDF)", "Statsmodels / Seaborn ecdfplot()", "Strictly step-wise cumulative probability avoiding arbitrary binning bandwidth artifacts.")
            ]
        },
        {
            "bbox": [1230, 200, 2330, 680],
            "title": "2. Correlation, Association & Relationship Mapping",
            "color": "#0D9488",
            "bg": "#F0FDFA",
            "border": "#99F6E4",
            "purpose": "Primary Goal: Detect linear, monotonic, and complex non-linear co-movements between features",
            "items": [
                ("Scatter Plot + Rug Plots", "Seaborn scatterplot() with rugplot()", "Fine-grained pairwise observation inspection with marginal distribution densities."),
                ("2D Hexbin / Contour Map", "Matplotlib hexbin() | Seaborn kdeplot(2D)", "Resolves severe visual overplotting across 100k+ observations via density pooling."),
                ("Correlation Heatmap", "Seaborn heatmap(annot=True, cmap='vlag')", "Visual matrix of Pearson/Spearman coefficients with hierarchical dendrogram clustering."),
                ("Pairplot / SPLOM Matrix", "Seaborn pairplot() | Plotly express.scatter_matrix()", "Simultaneous multi-variable pairwise scatter grid colored by categorical class/target.")
            ]
        },
        {
            "bbox": [70, 720, 1170, 1200],
            "title": "3. Categorical Comparisons, Proportions & Disparity",
            "color": "#6366F1",
            "bg": "#EEF2FF",
            "border": "#C7D2FE",
            "purpose": "Primary Goal: Compare group aggregates, detect category imbalance, and evaluate disparities",
            "items": [
                ("Faceted Bar Chart with CIs", "Seaborn barplot(errorbar='ci')", "Displays group means/medians with bootstrapped 95% confidence intervals."),
                ("Cleveland Dot Plot", "Matplotlib / Seaborn stripplot()", "High data-ink ratio chart ideal for ranking categories without bulky vertical bar ink."),
                ("Mosaic & Contingency Plots", "Statsmodels.graphics.mosaicplot", "Visualizes contingency tables where area represents joint categorical frequency."),
                ("Treemap / Sunburst Chart", "Plotly express.treemap()", "Hierarchical nested categorical proportions with interactive drill-down zoom capabilities.")
            ]
        },
        {
            "bbox": [1230, 720, 2330, 1200],
            "title": "4. Temporal Trends, High-Dimensional Manifolds & Interactions",
            "color": "#9333EA",
            "bg": "#FAF5FF",
            "border": "#E9D5FF",
            "purpose": "Primary Goal: Uncover longitudinal momentum, cyclical patterns, and multi-variable interaction clusters",
            "items": [
                ("Time-Series Rolling Envelopes", "Pandas rolling() + Matplotlib fill_between", "Tracks moving averages alongside standard deviation volatility bands over time."),
                ("Parallel Coordinates Plot", "Plotly express.parallel_coordinates()", "Projects high-dimensional continuous features onto parallel vertical axes per sample."),
                ("t-SNE & UMAP Projections", "UMAP-learn / Scikit-Learn manifold", "Non-linear dimensionality reduction projecting high-dimensional clusters onto 2D space."),
                ("Faceted Multiples (FacetGrid)", "Seaborn FacetGrid(col='Category', row='Tier')", "Small-multiple visualization stratifying complex relationships across 3 to 4 dimensions.")
            ]
        }
    ]

    for q in quads:
        x0, y0, x1, y1 = q["bbox"]
        draw_rounded_rect(draw, [x0, y0, x1, y1], radius=12, fill="#FFFFFF", outline=q["color"], width=2)
        draw_rounded_rect(draw, [x0, y0, x1, y0 + 60], radius=10, fill=q["color"])
        draw.text((x0 + 25, y0 + 15), q["title"], fill="#FFFFFF", font=f_card_title)
        draw.text((x0 + 25, y0 + 75), q["purpose"], fill=q["color"], font=f_card_sub)

        curr_y = y0 + 115
        item_h = 75
        for p_name, p_lib, p_desc in q["items"]:
            draw_rounded_rect(draw, [x0 + 20, curr_y, x1 - 20, curr_y + item_h], radius=8, fill=q["bg"], outline=q["border"], width=1)
            draw_rounded_rect(draw, [x0 + 20, curr_y, x0 + 26, curr_y + item_h], radius=3, fill=q["color"])
            
            draw.text((x0 + 38, curr_y + 10), p_name, fill="#0F172A", font=get_font(17, bold=True))
            draw.text((x0 + 400, curr_y + 12), f"Tool: {p_lib}", fill=q["color"], font=get_font(14, bold=True))
            draw.text((x0 + 38, curr_y + 38), p_desc, fill="#475569", font=f_card_body)
            curr_y += item_h + 15

    # Footer note
    draw_rounded_rect(draw, [50, height - 70, width - 50, height - 20], radius=8, fill="#0F172A")
    draw.text((80, height - 52), "Figure 2: OmniEDA Statistical Visualization Taxonomy & Plot Selection Decision Matrix (Sumarjana Biswas - Week 2 Framework)", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved Diagram 2 to {output_path}")

# ==============================================================================
# DIAGRAM 3: 32.5-Hour Week 2 Implementation Timeline & Gantt Schedule
# ==============================================================================
def create_eda_gantt_diagram(output_path):
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
    draw.text((90, 60), "OmniEDA: Week 2 Implementation Timeline & Resource Allocation (32.5 Hours)", fill="#FFFFFF", font=f_title)
    draw.text((90, 115), "Detailed Work Breakdown Structure: 6 Phased Workstreams across 5 Working Days (Author: Sumarjana Biswas)", fill="#94A3B8", font=f_subtitle)

    left_x = 60
    table_w = 750
    timeline_x = left_x + table_w + 40
    timeline_w = width - timeline_x - 60
    start_y = 200
    row_h = 150
    total_hours = 35.0

    days = [
        ("Day 1: Scope & Data Hygiene", 0, 7),
        ("Day 2: Cleaning & Univariate", 7, 14),
        ("Day 3: Bivariate Interactions", 14, 21),
        ("Day 4: Multivariate & Charts", 21, 28),
        ("Day 5: Synthesis & Reporting", 28, 35)
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
            "name": "Scope, Architecture & Structural Profiling",
            "sub": "Taxonomy mapping, memory profiling, automated summary dictionaries",
            "start": 0.0,
            "duration": 4.5,
            "color": "#0284C7",
            "milestone": "Structural Data Profile Approved"
        },
        {
            "code": "Phase 2",
            "name": "Data Hygiene, Missingness & Anomaly Auditing",
            "sub": "MCAR/MAR/MNAR matrix scans, Tukey IQR outliers, Isolation Forest",
            "start": 4.5,
            "duration": 5.5,
            "color": "#0D9488",
            "milestone": "Hygiene & Anomaly Matrix Validated"
        },
        {
            "code": "Phase 3",
            "name": "Univariate & Bivariate Statistical Exploration",
            "sub": "KDE distributions, skewness testing, Spearmans, ANOVA & Chi-Square",
            "start": 10.0,
            "duration": 7.0,
            "color": "#F59E0B",
            "milestone": "Feature Association Catalog Complete"
        },
        {
            "code": "Phase 4",
            "name": "Multivariate Analysis, Dimensionality & Clustering",
            "sub": "Collinearity VIF checks, PCA variance decomposition, t-SNE / UMAP",
            "start": 17.0,
            "duration": 7.5,
            "color": "#6366F1",
            "milestone": "High-Dimensional Cluster Map Ready"
        },
        {
            "code": "Phase 5",
            "name": "Interactive Dashboards & Visualization Engine",
            "sub": "Plotly interactive widgets, FacetGrid multiples, styling consistency",
            "start": 24.5,
            "duration": 4.5,
            "color": "#8B5CF6",
            "milestone": "Interactive Visualization Suite Deployed"
        },
        {
            "code": "Phase 6",
            "name": "Findings Documentation & Stakeholder Synthesis",
            "sub": "Data health scorecard, modeling recommendations, executive presentation",
            "start": 29.0,
            "duration": 3.5,
            "color": "#EC4899",
            "milestone": "Final OmniEDA Report & Handoff Signed Off"
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
    draw.text((80, height - 44), "Figure 3: OmniEDA Week 2 Implementation Timeline, Phase Allocations & Critical Path Gantt Schedule (Total: 32.5 Hours)", fill="#E2E8F0", font=f_footer)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Saved Diagram 3 to {output_path}")

if __name__ == "__main__":
    out_dir = r"e:\Code Playground\Sumu\assets"
    os.makedirs(out_dir, exist_ok=True)
    create_eda_lifecycle_diagram(os.path.join(out_dir, "eda_diagram_1_lifecycle.png"))
    create_eda_taxonomy_diagram(os.path.join(out_dir, "eda_diagram_2_taxonomy.png"))
    create_eda_gantt_diagram(os.path.join(out_dir, "eda_diagram_3_timeline.png"))
    print("All Week 2 EDA diagrams generated successfully.")
