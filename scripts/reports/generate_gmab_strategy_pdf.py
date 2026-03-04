"""
Generate GMAB Strategic Analysis PDF — ecoprog WtE Market Study 2024/2025
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import date

OUTPUT_PATH = "C:/Users/staff/ObsidianVaults/WET knowledgebase/60-Assets/GMAB Strategic Analysis - ecoprog WtE 2024-2025.pdf"

DARK_BLUE  = colors.HexColor("#0D2B4E")
MID_BLUE   = colors.HexColor("#1565C0")
LIGHT_BLUE = colors.HexColor("#E3F0FB")
ACCENT_RED = colors.HexColor("#C62828")
ACCENT_AMB = colors.HexColor("#E65100")
GREEN      = colors.HexColor("#1B5E20")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
MID_GRAY   = colors.HexColor("#9E9E9E")
DARK_GRAY  = colors.HexColor("#424242")
WHITE      = colors.white
TEAL       = colors.HexColor("#00695C")


def S():
    s = {}
    s["cover_title"] = ParagraphStyle("ct", fontSize=24, fontName="Helvetica-Bold",
        textColor=WHITE, leading=30, spaceAfter=3)
    s["cover_sub"] = ParagraphStyle("cs", fontSize=13, fontName="Helvetica",
        textColor=colors.HexColor("#BFD7F5"), leading=18, spaceAfter=2)
    s["cover_meta"] = ParagraphStyle("cm", fontSize=8.5, fontName="Helvetica",
        textColor=colors.HexColor("#90B9DC"), leading=12)
    s["section"] = ParagraphStyle("sec", fontSize=13, fontName="Helvetica-Bold",
        textColor=WHITE, leading=17, spaceBefore=4, spaceAfter=3, leftIndent=4)
    s["h2"] = ParagraphStyle("h2", fontSize=11, fontName="Helvetica-Bold",
        textColor=DARK_BLUE, leading=15, spaceBefore=10, spaceAfter=3)
    s["h3"] = ParagraphStyle("h3", fontSize=9.5, fontName="Helvetica-Bold",
        textColor=MID_BLUE, leading=13, spaceBefore=7, spaceAfter=2)
    s["body"] = ParagraphStyle("body", fontSize=8.5, fontName="Helvetica",
        textColor=DARK_GRAY, leading=13, spaceAfter=4)
    s["bullet"] = ParagraphStyle("bul", fontSize=8.5, fontName="Helvetica",
        textColor=DARK_GRAY, leading=12.5, leftIndent=14, firstLineIndent=-10, spaceAfter=2)
    s["bullet_bold"] = ParagraphStyle("bulb", fontSize=8.5, fontName="Helvetica-Bold",
        textColor=DARK_BLUE, leading=12.5, leftIndent=14, firstLineIndent=-10, spaceAfter=2)
    s["risk"] = ParagraphStyle("risk", fontSize=8.5, fontName="Helvetica",
        textColor=DARK_GRAY, leading=12.5, leftIndent=14, firstLineIndent=-10, spaceAfter=2)
    s["caption"] = ParagraphStyle("cap", fontSize=7.5, fontName="Helvetica-Oblique",
        textColor=MID_GRAY, leading=10, spaceAfter=5)
    s["label"] = ParagraphStyle("lbl", fontSize=8, fontName="Helvetica-Bold",
        textColor=MID_BLUE, leading=11, spaceAfter=1)
    return s


def banner(text, styles, color=DARK_BLUE):
    W = 170*mm
    data = [[Paragraph(text, styles["section"])]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ]))
    return t


def data_table(headers, rows, col_widths, stripe=True, header_color=DARK_BLUE):
    th_style = ParagraphStyle("th", fontSize=7.5, fontName="Helvetica-Bold",
        textColor=WHITE, leading=10)
    td_style = ParagraphStyle("td", fontSize=7.5, fontName="Helvetica",
        textColor=DARK_GRAY, leading=10)

    hdr = [Paragraph(f"<b>{h}</b>", th_style) for h in headers]
    table_data = [hdr] + [
        [Paragraph(str(c), td_style) for c in row] for row in rows
    ]
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND",    (0,0),(-1,0),  header_color),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]
    if stripe:
        cmds.append(("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, LIGHT_BLUE]))
    t.setStyle(TableStyle(cmds))
    return t


def pill(text, bg, fg=WHITE):
    """Small coloured inline badge."""
    style = ParagraphStyle("pill", fontSize=7.5, fontName="Helvetica-Bold",
        textColor=fg, leading=10)
    data = [[Paragraph(text, style)]]
    t = Table(data, colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("TOPPADDING",    (0,0),(-1,-1), 2),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ]))
    return t


def build():
    styles = S()
    W = A4[0] - 40*mm

    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title="GMAB Strategic Analysis — ecoprog WtE Market Study 2024/2025",
        author="SPIG-GMAB / EEA Emissions Analysis",
    )
    story = []

    # ── COVER ────────────────────────────────────────────────────────────────
    for text, style_key in [
        ("GMAB Strategic Analysis", "cover_title"),
        ("ecoprog Global WtE Market Study 2024/2025 — Implications & Opportunities", "cover_sub"),
        (f"Source: ecoprog GmbH, copy SPIG SpA / Alberto Galantini  |  "
         f"Prepared: {date.today().strftime('%d %B %Y')}  |  Confidential — SPIG-GMAB internal", "cover_meta"),
    ]:
        t = Table([[Paragraph(text, styles[style_key])]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), DARK_BLUE),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("TOPPADDING",    (0,0),(-1,-1), 7 if style_key=="cover_title" else 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ]))
        story.append(t)
    story.append(Spacer(1, 5*mm))

    # ── EXEC SUMMARY ─────────────────────────────────────────────────────────
    story.append(banner("Executive Summary", styles))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "This report analyses the ecoprog Market Study Waste to Energy 2024/2025 (pages 27–50) "
        "against GMAB's product portfolio and business model. It identifies where GMAB is well-"
        "positioned, where gaps exist, and maps concrete strategic development actions across "
        "geographies and product lines.",
        styles["body"]))

    kpis = [
        ["2,869", "537", "EUR 2.2B→2.7B", "45%"],
        ["Active WtE plants\nworldwide", "Plants in Europe\n(19% of global)", "European maintenance\nmarket 2024→2033", "European boilers\n>25 years old"],
    ]
    kt = Table(kpis, colWidths=[W/4]*4)
    kt.setStyle(TableStyle([
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,0),  18),
        ("TEXTCOLOR",     (0,0),(-1,0),  MID_BLUE),
        ("FONTNAME",      (0,1),(-1,1),  "Helvetica"),
        ("FONTSIZE",      (0,1),(-1,1),  7.5),
        ("TEXTCOLOR",     (0,1),(-1,1),  DARK_GRAY),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
        ("BACKGROUND",    (0,0),(-1,-1), LIGHT_GRAY),
        ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ]))
    # highlight the retrofit percentage
    kt.setStyle(TableStyle([("TEXTCOLOR", (3,0),(3,0), ACCENT_RED)]))
    story.append(kt)
    story.append(Spacer(1, 5*mm))

    # ── SECTION 1: MARKET TRENDS ──────────────────────────────────────────────
    story.append(banner("1. Key Market Trends & Findings (ecoprog pp.27–50)", styles))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Global Market Structure", styles["h2"]))
    for b in [
        "<b>2,869 active plants</b> worldwide (end-2023); combined capacity ~576 mtpy. Projected ~726 mtpy by 2033 (CAGR ~2.7%).",
        "Asia dominates: <b>78% of plant count</b>. Europe holds 19% of plants and 19% of capacity.",
        "<b>Grate combustion = 98%</b> of all newly commissioned capacity since 2019. Gasification/pyrolysis remain marginal (17 lines total, 2014–2024).",
        "Global average plant age: <b>~19 years</b>. North America: 33–34 years. Europe: <b>45% of boilers older than 25 years</b> (=34% of EU capacity).",
        "European maintenance market: <b>EUR 2.2B (2024) → EUR 2.7B (2033)</b>.",
    ]:
        story.append(Paragraph(f"\u2022  {b}", styles["bullet"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("China — Major Market Downturn", styles["h2"]))
    for b in [
        "New plant awardings in China have <b>collapsed since 2023</b>. Eastern coastal provinces face overcapacity and forced plant shutdowns.",
        "Peak commissioning: 190 plants (2021). Expected 2024: ~55. Annual new capacity: 29.8 mtpy (2023) → 3.3 mtpy (2033).",
        "Despite the downturn, China still accounts for <b>48.7%</b> of all new global capacity 2024–2033 by tonnage.",
        "China's existing fleet averages only <b>6 years old</b> — no meaningful retrofit demand for 10–15 years.",
    ]:
        story.append(Paragraph(f"\u2022  {b}", styles["bullet"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Europe — Retrofit-Driven, Compliance-Pressured", styles["h2"]))
    for b in [
        "<b>537 WtE plants</b>, 108.2 mtpy. The UK new-build boom ended in 2023; UK nearing saturation by ~2028.",
        "<b>Germany</b> explicitly forecast to see increasing retrofit numbers over coming years — oldest active large fleet.",
        "<b>France</b>: 131 plants, high average age, many small and not in district energy systems — economically vulnerable.",
        "<b>Poland</b>: Strong near-term growth market. Landfill ban + landfill tax + existing MBT infrastructure = RDF combustion demand.",
        "Growth markets also include Czech Republic, Italy, Eastern/Southern Europe (EU compliance pressure on landfilling).",
        "Maintenance/modernisation will become the <b>dominant European WtE business model</b> by the late 2020s.",
    ]:
        story.append(Paragraph(f"\u2022  {b}", styles["bullet"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Carbon / CO\u2082 / CCS — The Defining New Challenge", styles["h2"]))
    for b in [
        "CO\u2082 pricing described as <b>the most important strategic issue</b> in the WtE industry — yet implementation remains patchy.",
        "Germany and Netherlands leading on CO\u2082 pricing. CCS/CCU projects proliferating near <b>North Sea</b> storage sites (NL, UK, NO, DK).",
        "First operational CCU installation exists in the Netherlands (CO\u2082 \u2192 greenhouse supply).",
        "Current carbon capture cost: <b>>EUR 200/tonne CO\u2082</b> — a major investment barrier, but pressure growing.",
        "Risk: CO\u2082 pricing without matching landfill taxes could make some WtE plants economically unviable, driving closure not retrofit.",
    ]:
        story.append(Paragraph(f"\u2022  {b}", styles["bullet"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Emerging / New Markets", styles["h2"]))
    rows_em = [
        ["Middle East", "UAE (2 plants), Saudi Arabia, Qatar, Kuwait, Egypt, Oman, Bahrain", "Active but immature regulation", "2026–2029"],
        ["India", "2–4 new plants/year projected through 2033", "Gate fee policy lacking", "2028–2033"],
        ["SE Asia", "Thailand, Indonesia, Malaysia, Vietnam, Philippines — growing interest", "Financially/politically fragile", "2028–2033"],
        ["Australia", "First projects under construction; ~2.5 mtpy by 2033", "EU BAT likely benchmark", "2027–2030"],
        ["South America", "First plant Brazil expected 2027; signal-effect dynamics", "Policy support lacking", "2030+"],
        ["North America", "Fleet avg 33–34 yrs; 20+ plants closed in 20 yrs", "No landfill bans; cheap energy; Trump uncertainty", "Low priority"],
    ]
    story.append(data_table(
        ["Region", "Status", "Constraint", "GMAB Window"],
        rows_em, [28*mm, 56*mm, 48*mm, 24*mm]
    ))
    story.append(Spacer(1, 5*mm))

    # ── SECTION 2: WHERE GMAB FITS ────────────────────────────────────────────
    story.append(banner("2. Where GMAB Fits — Trend-by-Trend Positioning", styles))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "GMAB core capabilities: APCD/dioxin control, de novo synthesis prevention, memory effect "
        "mitigation, flue gas heat recovery, steam cycle efficiency, thermal energy maximisation. "
        "Target facilities: MSW incineration, industrial waste, biomass/RDF, hazardous waste, sewage sludge.",
        styles["body"]))
    story.append(Spacer(1, 2*mm))

    pos_rows = [
        ["European retrofit/modernisation wave",
         "WELL POSITIONED",
         "Core business. APCD upgrades, heat recovery retrofits on 25+ yr EU plants."],
        ["EU BAT compliance / IED enforcement",
         "WELL POSITIONED",
         "GMAB's primary market driver. Dioxin/PCDD/PCDF permits, BAT reviews = sales triggers."],
        ["Flue gas heat recovery / energy efficiency",
         "WELL POSITIONED",
         "Explicitly stated GMAB capability. Aligns with EU energy recovery requirements."],
        ["Aging fleet — Germany, France, Italy, Denmark",
         "WELL POSITIONED",
         "These markets have the oldest plants. France and Italy are most under-served."],
        ["Poland / Eastern Europe RDF new builds",
         "PARTIALLY POSITIONED",
         "Strong on APCD; needs a dedicated RDF/chlorinated flue gas commercial package. New-build "
         "requires EPC supply chain access."],
        ["UK late-stage build pipeline",
         "PARTIALLY POSITIONED",
         "Depends on whether GMAB is in current EPC supply chains for projects under construction."],
        ["Middle East first-generation plants",
         "PARTIALLY POSITIONED",
         "Lower initial regulatory requirements. Entry via European EPC relationships. Upgrade "
         "contracts will follow as regulation matures."],
        ["Japan consolidation / modernisation",
         "PARTIALLY POSITIONED",
         "Strong technical fit (strict dioxin law, energy recovery emphasis). Requires local "
         "partner/agent relationship."],
        ["CO\u2082 / CCS / CCU at WtE plants",
         "NOT POSITIONED",
         "Most significant strategic gap. CCS is the #1 emerging issue in EU WtE. "
         "GMAB needs a CCS interface/pre-treatment story."],
        ["North America aging fleet",
         "PARTIALLY POSITIONED",
         "Perfect technical fit (33-yr-old plants) but structurally unfavourable market."],
        ["SE Asia / India (long-term)",
         "PARTIALLY POSITIONED",
         "Low current regulatory weight is correct. Pipeline-building posture appropriate now."],
    ]

    td = ParagraphStyle("td2", fontSize=7.5, fontName="Helvetica", textColor=DARK_GRAY, leading=10)
    th = ParagraphStyle("th2", fontSize=7.5, fontName="Helvetica-Bold", textColor=WHITE, leading=10)

    def pos_color(txt):
        if "WELL" in txt: return GREEN
        if "NOT" in txt:  return ACCENT_RED
        return ACCENT_AMB

    hdr_row = [Paragraph(h, th) for h in ["Trend", "GMAB Position", "Commentary"]]
    tdata = [hdr_row]
    for trend, pos, comment in pos_rows:
        bg = pos_color(pos)
        pos_cell = Table([[Paragraph(f"<b>{pos}</b>", ParagraphStyle("pc",
            fontSize=7.5, fontName="Helvetica-Bold", textColor=WHITE, leading=10))]],
            colWidths=[35*mm])
        pos_cell.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), bg),
            ("TOPPADDING",    (0,0),(-1,-1), 3),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
            ("LEFTPADDING",   (0,0),(-1,-1), 4),
        ]))
        tdata.append([
            Paragraph(trend, td),
            pos_cell,
            Paragraph(comment, td),
        ])

    pos_t = Table(tdata, colWidths=[52*mm, 35*mm, 83*mm], repeatRows=1)
    pos_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  DARK_BLUE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    story.append(pos_t)
    story.append(Spacer(1, 5*mm))

    # ── SECTION 3: STRATEGIC OPPORTUNITIES ────────────────────────────────────
    story.append(banner("3. Strategic Development Opportunities", styles))
    story.append(Spacer(1, 3*mm))

    opps = [
        ("A", DARK_BLUE, "Double Down on European Retrofit — Priority Geographies",
         [
             "<b>Germany</b> (98 plants, 27 mtpy): Report explicitly forecasts increasing retrofits. Strictest BAT implementation in Europe. Ensure GMAB is in every relevant tender and has direct operator relationships across the German fleet.",
             "<b>France</b> (131 plants, 26.4 mtpy): Largest under-served market in Europe. High average age, small plants, many not in district heating — economically isolated and compliance-exposed. Position a cost-efficient APCD package for small municipal operators.",
             "<b>Italy</b> (37 plants, 7 mtpy): Similar profile to France. Remaining new-build potential alongside aging fleet. Combined retrofit + new-build strategy.",
             "<b>Denmark / Netherlands</b>: Mature, CO\u2082-pressured. Explore CCS-compatible flue gas treatment as an upsell angle (see Opportunity C).",
         ]),
        ("B", TEAL, "Build a Dedicated RDF Combustion Emission Control Proposition",
         [
             "Poland and Eastern Europe are transitioning from MBT to RDF combustion — the report's primary European growth story.",
             "<b>RDF has higher chlorine content than MSW</b> — increasing de novo dioxin synthesis risk. GMAB's prevention capability is directly applicable and technically differentiated.",
             "These are <b>new-build projects</b>: GMAB must get specified at the project design stage, via EPC supply chain relationships.",
             "Develop a dedicated RDF/chlorinated flue gas APCD technical paper and commercial package. Target Poland, Czech Republic, UK pipeline.",
         ]),
        ("C", ACCENT_RED, "Develop a CCS Interface / Flue Gas Pre-Treatment Offering  [CRITICAL GAP]",
         [
             "CCS/CCU is the #1 strategic trend in EU WtE. GMAB has no stated position. This needs to change.",
             "<b>Dioxin removal is a non-negotiable prerequisite for CCS</b>: dioxins contaminate CO\u2082 capture streams and poison amine solvents. GMAB's APCD is a required upstream component of any WtE CCS installation.",
             "<b>Flue gas pre-treatment for amine-based capture</b>: acid gases, HCl/HF, particulates must be removed before CO\u2082 capture — exactly GMAB's domain.",
             "Approach CCS technology providers (<b>Aker Carbon Capture, MHI, SLB, SINTEF, Linde</b>) about being named as preferred flue gas pre-treatment partner for WtE CCS projects.",
             "Geographic target: <b>North Sea cluster</b> — Netherlands, UK, Norway, Denmark — where CCS projects are most active.",
             "This reframes GMAB from compliance vendor to <b>CCS-enabling technology partner</b>.",
         ]),
        ("D", ACCENT_AMB, "Middle East — First-Mover Positioning via EPC Relationships",
         [
             "UAE, Saudi Arabia, Qatar, Kuwait, Egypt, Oman, Bahrain: actively developing first-generation WtE plants. Projects being awarded to European EPCs now.",
             "Enter via EPC subcontracting relationships before local low-cost competition establishes itself.",
             "Initial regulatory standards will be below EU BAT — but establish presence, then upgrade contracts follow as regulation matures.",
             "<b>Timing window: 2026–2029</b> for first-generation project specifications.",
         ]),
        ("E", MID_BLUE, "Develop Service & Maintenance Contract Product",
         [
             "European maintenance market grows <b>EUR 2.2B → 2.7B by 2033</b> — the most predictable and stable growth segment in the report.",
             "Formalise a recurring revenue product: <b>annual activated carbon supply agreements</b> (for dioxin injection), APCD inspection/tuning, CEM data review, compliance advisory.",
             "Service contracts deepen operator relationships and ensure GMAB is first call when capital upgrades are needed.",
             "This is directly complementary to the retrofit capital equipment business.",
         ]),
        ("F", TEAL, "Australia — Early Entry for a Building Market",
         [
             "First Australian WtE projects are under construction; ~2.5 mtpy expected by 2033. All will be permitted against EU BAT-benchmarked standards.",
             "Identify Australian project developers and EPC contractors active in Sydney, Melbourne, and Perth projects and engage as emission control supplier.",
             "<b>First-mover advantage</b>: get specified on the first Australian WtE plants and that relationship sets the standard for all that follow.",
         ]),
        ("G", DARK_GRAY, "Japan — Modernisation Market via Local Partner",
         [
             "Japan consolidating from ~1,000 small plants toward fewer, larger, energy-efficient plants. New plants built to very high energy recovery and emission standards.",
             "Japan has one of the world's <b>strictest dioxin laws</b> (enacted 2000) — GMAB's core competence is directly relevant.",
             "Market requires a local industrial partner or agent. Candidates: <b>Hitachi Zosen, JFE Engineering, Kawasaki, Kobelco</b>.",
             "<b>Timing: medium-term</b> (2027–2032).",
         ]),
    ]

    for letter, color, title, bullets in opps:
        # Header row
        hdr_data = [[
            Paragraph(f"<b>{letter}</b>", ParagraphStyle("ltr", fontSize=13,
                fontName="Helvetica-Bold", textColor=WHITE, leading=16)),
            Paragraph(title, ParagraphStyle("opp_title", fontSize=10,
                fontName="Helvetica-Bold", textColor=WHITE, leading=14)),
        ]]
        ht = Table(hdr_data, colWidths=[10*mm, 160*mm])
        ht.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), color),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 6),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ]))
        items = [ht]
        for b in bullets:
            items.append(Paragraph(f"\u2022  {b}", styles["bullet"]))
        items.append(Spacer(1, 3*mm))
        story.append(KeepTogether(items))

    story.append(Spacer(1, 3*mm))

    # ── SECTION 4: RISKS ──────────────────────────────────────────────────────
    story.append(banner("4. Key Risks & Threats to GMAB's Business", styles, color=colors.HexColor("#7B1FA2")))
    story.append(Spacer(1, 3*mm))

    risks = [
        ("1", "CO\u2082 Pricing Drives Plant Closures Rather Than Retrofits",
         "HIGH",
         "If CO\u2082 costs make WtE plants unviable in Germany/Netherlands, operators close plants rather than retrofit. "
         "GMAB's retrofit pipeline requires plants to stay in operation.\n"
         "Mitigation: Prioritise France and Italy (less advanced CO\u2082 pricing). Develop CCS interface offering "
         "to reframe GMAB as part of the CO\u2082 compliance solution."),
        ("2", "Short Municipal Contract Periods Block Capital Investment",
         "HIGH",
         "Report identifies this as 'the most severe threat' to European plant modernisation. "
         "Operators on short-term municipal contracts won't commit APCD or heat recovery capex.\n"
         "Mitigation: Target operators with confirmed long-term contracts or those bidding for new ones — "
         "procurement decisions become sales trigger events."),
        ("3", "EPC Consolidation Squeezes Specialist Suppliers",
         "MEDIUM",
         "Major EPCs (Hitachi Zosen Inova, Covanta, Babcock) have increased bargaining power. "
         "GMAB's margins and contract access depend on being indispensable.\n"
         "Mitigation: Invest in direct operator relationships and technical reputation (case studies, BAT track record) "
         "to create operator pull-through that forces EPCs to include GMAB in tenders."),
        ("4", "Chinese Market Collapse Removes New-Build Volume",
         "LOW (if limited China exposure)",
         "China's downturn removes the largest new-build pool. China's fleet averages 6 years old — "
         "no meaningful retrofit demand for 10–15 years.\n"
         "Mitigation: GMAB's scoring correctly assigns China a low regulatory weight. Maintain this position."),
        ("5", "Regulatory Lag in New Markets Delays Revenue",
         "MEDIUM",
         "Middle East, SE Asia, India, Australia, South America all hampered by regulatory immaturity. "
         "Low enforcement means price competition from lower-spec suppliers dominates.\n"
         "Mitigation: Enter early via EPC relationships, position EU BAT as the correct benchmark before "
         "local low-cost competition establishes itself."),
        ("6", "Recycling Growth Reduces WtE Throughput / Investment Headroom",
         "MEDIUM (long-term)",
         "EU Circular Economy Package prioritises recycling above thermal treatment. "
         "Declining waste calorific value reduces plant economics and capex headroom.\n"
         "Mitigation: Focus retrofit on France and Italy (lower recycling rates). RDF (concentrated stream) "
         "partially mitigates — a positive for GMAB's RDF proposition."),
        ("7", "Trump Administration Weakens US Environmental Enforcement",
         "LOW",
         "Already-marginal US WtE sector faces even less incentive to invest in emission control. "
         "Confirms North America is a low-priority market for GMAB."),
        ("8", "Advanced Thermal Technologies (Gasification/Pyrolysis) Gaining Niche Ground",
         "LOW (near-term)",
         "Currently 1–2% of capacity, but continues to receive investment for smaller modular applications. "
         "If these displace grate combustion in India/SE Asia, GMAB's grate-oriented APCD may need adaptation.\n"
         "Mitigation: Monitor advanced thermal segment; gasification syngas cleaning is an adjacent capability "
         "to consider for the longer term."),
    ]

    risk_td = ParagraphStyle("rtd", fontSize=7.5, fontName="Helvetica", textColor=DARK_GRAY, leading=10.5)
    risk_th = ParagraphStyle("rth", fontSize=7.5, fontName="Helvetica-Bold", textColor=WHITE, leading=10)

    def risk_badge_color(level):
        if "HIGH" in level:   return ACCENT_RED
        if "MEDIUM" in level: return ACCENT_AMB
        return GREEN

    r_hdr = [Paragraph(h, risk_th) for h in ["#", "Risk", "Level", "Description & Mitigation"]]
    r_data = [r_hdr]
    for num, title, level, desc in risks:
        bg = risk_badge_color(level)
        badge = Table([[Paragraph(f"<b>{level}</b>", ParagraphStyle("rb",
            fontSize=7, fontName="Helvetica-Bold", textColor=WHITE, leading=9))]],
            colWidths=[22*mm])
        badge.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), bg),
            ("TOPPADDING",    (0,0),(-1,-1), 2),
            ("BOTTOMPADDING", (0,0),(-1,-1), 2),
            ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ]))
        r_data.append([
            Paragraph(f"<b>{num}</b>", risk_td),
            Paragraph(f"<b>{title}</b>", risk_td),
            badge,
            Paragraph(desc.replace("\n", "<br/>"), risk_td),
        ])

    rt = Table(r_data, colWidths=[7*mm, 44*mm, 22*mm, 97*mm], repeatRows=1)
    rt.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  colors.HexColor("#7B1FA2")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    story.append(rt)
    story.append(Spacer(1, 5*mm))

    # ── SECTION 5: PRIORITY MATRIX ────────────────────────────────────────────
    story.append(banner("5. Strategic Priority Matrix", styles))
    story.append(Spacer(1, 3*mm))

    matrix_rows = [
        ["IMMEDIATE", "Target France — old fleet, small municipal, cost-efficient APCD packages", "Now–2027", "A"],
        ["IMMEDIATE", "Target Germany — retrofit wave, aging boilers, BAT review cycles", "Now–2030", "A"],
        ["IMMEDIATE", "Develop Poland RDF emission control proposition, engage EPC supply chain", "Now–2028", "B"],
        ["NEAR-TERM", "Build CCS interface / flue gas pre-treatment partnership narrative (Aker, MHI, SLB)", "2026–2028", "C"],
        ["NEAR-TERM", "Engage Middle East first-generation plant EPC supply chains (UAE, Saudi, Egypt)", "2026–2029", "D"],
        ["NEAR-TERM", "Develop service/maintenance contract product (carbon supply, APCD inspection, CEM)", "2026–2028", "E"],
        ["NEAR-TERM", "Australia market entry — EPC relationships on first-generation projects", "2027–2030", "F"],
        ["MEDIUM-TERM", "Japan modernisation market — identify local partner/agent", "2027–2032", "G"],
        ["MONITOR", "India and Southeast Asia — regulatory tracking, agent relationships", "2027–2033", "—"],
        ["AVOID", "China — overcapacity, young fleet (avg 6 yrs), regulatory weight low", "—", "—"],
        ["DEPRIORITISE", "North America as a primary market — structural headwinds, policy uncertainty", "—", "—"],
    ]

    def horizon_color(h):
        if h == "IMMEDIATE":    return ACCENT_RED
        if h == "NEAR-TERM":    return ACCENT_AMB
        if h == "MEDIUM-TERM":  return MID_BLUE
        if h == "MONITOR":      return TEAL
        if h in ("AVOID","DEPRIORITISE"): return MID_GRAY
        return DARK_GRAY

    m_th = ParagraphStyle("mth", fontSize=7.5, fontName="Helvetica-Bold", textColor=WHITE, leading=10)
    m_td = ParagraphStyle("mtd", fontSize=7.5, fontName="Helvetica", textColor=DARK_GRAY, leading=10)
    m_hdr_row = [Paragraph(h, m_th) for h in ["Horizon", "Action", "Timeframe", "Ref"]]
    m_data = [m_hdr_row]
    for horizon, action, timeframe, ref in matrix_rows:
        bg = horizon_color(horizon)
        badge = Table([[Paragraph(f"<b>{horizon}</b>", ParagraphStyle("mb",
            fontSize=7, fontName="Helvetica-Bold", textColor=WHITE, leading=9))]],
            colWidths=[25*mm])
        badge.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), bg),
            ("TOPPADDING",    (0,0),(-1,-1), 2),
            ("BOTTOMPADDING", (0,0),(-1,-1), 2),
            ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ]))
        m_data.append([badge, Paragraph(action, m_td),
                        Paragraph(timeframe, m_td), Paragraph(ref, m_td)])

    mt = Table(m_data, colWidths=[27*mm, 107*mm, 22*mm, 14*mm], repeatRows=1)
    mt.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  DARK_BLUE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    story.append(mt)
    story.append(Spacer(1, 5*mm))

    # ── FOOTER ────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width=W, thickness=0.5, color=MID_GRAY))
    story.append(Spacer(1, 2*mm))
    notes = [
        "Source: ecoprog GmbH, 'Market Study Waste to Energy 2024/2025', pages 27–50. Copy: SPIG SpA / Alberto Galantini. Not for forwarding or reproduction.",
        "GMAB business model source: SPIG-GMAB lead_generation_agent.py; lead_evaluation_agent.py.",
        f"Prepared: {date.today().strftime('%d %B %Y')}. Confidential — SPIG-GMAB internal use only.",
    ]
    for n in notes:
        story.append(Paragraph(f"\u2022  {n}", ParagraphStyle("fn",
            fontSize=7, fontName="Helvetica", textColor=MID_GRAY,
            leading=10, leftIndent=10, firstLineIndent=-8, spaceAfter=1)))

    doc.build(story)
    print(f"PDF saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
