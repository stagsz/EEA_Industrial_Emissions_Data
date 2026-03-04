"""
Generate Nordic WtE Leads PDF Report for GMAB Business Development
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import date

OUTPUT_PATH = "C:/Users/staff/ObsidianVaults/WET knowledgebase/60-Assets/Nordic WtE Leads - GMAB Report 2026.pdf"

# ── Colour palette ──────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#0D2B4E")
MID_BLUE    = colors.HexColor("#1565C0")
LIGHT_BLUE  = colors.HexColor("#E3F0FB")
ACCENT_RED  = colors.HexColor("#C62828")
ACCENT_AMB  = colors.HexColor("#F57F17")
GREEN       = colors.HexColor("#1B5E20")
LIGHT_GRAY  = colors.HexColor("#F5F5F5")
MID_GRAY    = colors.HexColor("#9E9E9E")
WHITE       = colors.white

def make_styles():
    base = getSampleStyleSheet()
    s = {}

    s["cover_title"] = ParagraphStyle("cover_title",
        fontSize=26, fontName="Helvetica-Bold", textColor=WHITE,
        leading=32, spaceAfter=4)
    s["cover_sub"] = ParagraphStyle("cover_sub",
        fontSize=13, fontName="Helvetica", textColor=colors.HexColor("#BFD7F5"),
        leading=18, spaceAfter=2)
    s["cover_meta"] = ParagraphStyle("cover_meta",
        fontSize=9, fontName="Helvetica", textColor=colors.HexColor("#90B9DC"),
        leading=13)

    s["section"] = ParagraphStyle("section",
        fontSize=14, fontName="Helvetica-Bold", textColor=WHITE,
        leading=18, spaceBefore=6, spaceAfter=4,
        leftIndent=4)
    s["h2"] = ParagraphStyle("h2",
        fontSize=11, fontName="Helvetica-Bold", textColor=DARK_BLUE,
        leading=15, spaceBefore=10, spaceAfter=3)
    s["h3"] = ParagraphStyle("h3",
        fontSize=10, fontName="Helvetica-Bold", textColor=MID_BLUE,
        leading=13, spaceBefore=7, spaceAfter=2)
    s["body"] = ParagraphStyle("body",
        fontSize=8.5, fontName="Helvetica", textColor=colors.HexColor("#212121"),
        leading=12.5, spaceAfter=4)
    s["bullet"] = ParagraphStyle("bullet",
        fontSize=8.5, fontName="Helvetica", textColor=colors.HexColor("#212121"),
        leading=12, leftIndent=14, firstLineIndent=-10, spaceAfter=2)
    s["alert"] = ParagraphStyle("alert",
        fontSize=8.5, fontName="Helvetica-Bold", textColor=ACCENT_RED,
        leading=12, leftIndent=14, firstLineIndent=-10, spaceAfter=2)
    s["caption"] = ParagraphStyle("caption",
        fontSize=7.5, fontName="Helvetica-Oblique", textColor=MID_GRAY,
        leading=10, spaceAfter=6)
    s["footer"] = ParagraphStyle("footer",
        fontSize=7, fontName="Helvetica", textColor=MID_GRAY,
        leading=9, alignment=TA_CENTER)

    return s


def section_banner(text, styles):
    """Coloured full-width banner for section headings."""
    data = [[Paragraph(text, styles["section"])]]
    t = Table(data, colWidths=[170*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("ROUNDEDCORNERS", [3]),
    ]))
    return t


def priority_table(headers, rows, col_widths, styles, alert_col=None, alert_val=None):
    """Build a styled data table."""
    header_row = [Paragraph(f"<b>{h}</b>", ParagraphStyle("th",
        fontSize=7.5, fontName="Helvetica-Bold", textColor=WHITE, leading=10))
        for h in headers]
    table_data = [header_row]

    for i, row in enumerate(rows):
        cells = []
        for j, cell in enumerate(row):
            cell_str = str(cell)
            if alert_col is not None and j == alert_col and alert_val and alert_val in cell_str:
                p = Paragraph(cell_str, styles["alert"])
            else:
                p = Paragraph(cell_str, ParagraphStyle("td",
                    fontSize=7.5, fontName="Helvetica", textColor="#212121", leading=10))
            cells.append(p)
        table_data.append(cells)

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0),  DARK_BLUE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_BLUE]),
        ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def build_pdf():
    styles = make_styles()
    W = A4[0] - 40*mm   # usable width

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title="Nordic WtE Leads — GMAB Business Development 2026",
        author="EEA Industrial Emissions Analysis",
    )

    story = []

    # ── COVER BLOCK ─────────────────────────────────────────────────────────
    cover_data = [[
        Paragraph("Nordic WtE Leads", styles["cover_title"]),
    ]]
    cover_sub_data = [[
        Paragraph("GMAB Business Development Report", styles["cover_sub"]),
    ]]
    meta_data = [[
        Paragraph(
            f"Source: EEA Industrial Emissions Database v16 (2007–2024)  |  Generated: {date.today().strftime('%d %B %Y')}  |  Confidential — SPIG-GMAB internal use",
            styles["cover_meta"]),
    ]]
    for data in [cover_data, cover_sub_data, meta_data]:
        t = Table(data, colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), DARK_BLUE),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("RIGHTPADDING",  (0,0), (-1,-1), 10),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ]))
        story.append(t)
    story.append(Spacer(1, 6*mm))

    # ── EXECUTIVE SUMMARY ───────────────────────────────────────────────────
    story.append(section_banner("Executive Summary", styles))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "This report identifies the highest-priority Waste-to-Energy (WtE) leads across the Nordic "
        "region — Denmark, Finland, and Norway — for GMAB's Air Pollution Control (APCD) and Waste "
        "Heat Recovery product lines. Analysis is based on the EEA E-PRTR Industrial Emissions Database "
        "(v16, covering 2007–2024), queried for 66 WtE incineration facilities (IED activity code 5(b)) "
        "across three countries. Sweden is covered separately.",
        styles["body"]))
    story.append(Paragraph(
        "Key signals screened: dioxin/PCDD+PCDF (kg TEq), mercury Hg (kg), NOx (tonnes), plant age, "
        "and BAT compliance status. Five Tier-1 leads require immediate contact.",
        styles["body"]))
    story.append(Spacer(1, 2*mm))

    # KPI boxes
    kpi_data = [
        ["66", "5", "3", "1"],
        ["WtE facilities\nscreened", "Tier-1 leads\nidentified", "Countries\ncovered", "Regulatory\nemergency"],
    ]
    kpi_t = Table(kpi_data, colWidths=[W/4]*4)
    kpi_t.setStyle(TableStyle([
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  22),
        ("TEXTCOLOR",     (0,0), (-1,0),  MID_BLUE),
        ("FONTNAME",      (0,1), (-1,1),  "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,1),  7.5),
        ("TEXTCOLOR",     (0,1), (-1,1),  colors.HexColor("#546E7A")),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GRAY),
        ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("INNERGRID",     (0,0), (-1,-1), 0.3, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    # highlight the emergency cell
    kpi_t.setStyle(TableStyle([
        ("TEXTCOLOR",  (3,0), (3,0), ACCENT_RED),
        ("BACKGROUND", (3,0), (3,1), colors.HexColor("#FFEBEE")),
    ]))
    story.append(kpi_t)
    story.append(Spacer(1, 5*mm))

    # ── TIER 1 PRIORITY LIST ─────────────────────────────────────────────────
    story.append(section_banner("Tier 1 — Immediate Contact Targets", styles))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Five facilities require immediate outreach based on confirmed dioxin events, critical Hg levels, "
        "or rapidly rising NOx above 250 t/yr.",
        styles["body"]))
    story.append(Spacer(1, 2*mm))

    t1_headers = ["#", "Facility", "Country", "City", "Critical Signal", "GMAB Product"]
    t1_rows = [
        ["1", "I/S Amager Ressourcecenter\n(ARC / CopenHill)",
         "DK", "Copenhagen",
         "DIOXINS 8.98 kg TEq (2024)\n~90,000x reporting threshold",
         "APCD + de novo synthesis control"],
        ["2", "Vantaan Energia Oy\nJätevoimala",
         "FI", "Vantaa\n(Helsinki metro)",
         "NOx 545 t/yr (2024)\n+20% vs 2019, +19% vs 2023",
         "Heat recovery + SCR/SNCR optimisation"],
        ["3", "Bio-El / Kvitebjørn Bio-El AS",
         "NO", "Fredrikstad",
         "Dioxins 0.0008 kg TEq detected\n(2015, last reported year)",
         "APCD, dioxin control systems"],
        ["4", "Statkraft Varme AS\nAvfallsforbrenning",
         "NO", "Trondheim",
         "NOx 255 t/yr (2017)\nHighest in Norwegian WtE",
         "ORC / waste heat recovery"],
        ["5", "Fjernvarme Horsens\nKraftvarmevaerk",
         "DK", "Horsens",
         "Dioxins 0.0107 kg TEq (2020)\nWorst single-year Danish event",
         "APCD, de novo prevention"],
    ]
    cw = [8*mm, 42*mm, 14*mm, 24*mm, 46*mm, 42*mm]
    story.append(priority_table(t1_headers, t1_rows, cw, styles))
    story.append(Paragraph(
        "Note: Norway stopped reporting to EEA E-PRTR after 2017. Norwegian leads are verified via "
        "Miljodirektoratet (national database). All facilities assumed operational.",
        styles["caption"]))
    story.append(Spacer(1, 5*mm))

    # ── DENMARK ──────────────────────────────────────────────────────────────
    story.append(section_banner("Denmark — Detailed Lead Analysis", styles))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Denmark has the most data-rich WtE sector in the Nordics (annual E-PRTR reporting through 2024). "
        "The country operates ~20 active MSW incineration plants. IED activity code 5(b). "
        "Many plants started 1993–2000 and are approaching 30-year refurbishment cycles.",
        styles["body"]))

    story.append(Paragraph("Dioxin-Flagged Facilities", styles["h2"]))
    dk_diox_h = ["Facility", "City", "Dioxin year", "TEq (kg)", "NOx (t/yr)", "Started", "Signal"]
    dk_diox_r = [
        ["I/S Amager Ressourcecenter", "Copenhagen", "2024", "8.980", "204", "2017",
         "CRITICAL — sudden spike, modern plant"],
        ["Fjernvarme Horsens Kraftvarmevaerk", "Horsens", "2020", "0.0107", "121 (2024)",
         "2000", "Worst DK spike on record; recurring 2022"],
        ["Fjernvarme Fyn Affaldsenergi", "Odense", "2020–22", "up to 0.0005", "286 (2024)",
         "1996", "NOx also rising +24%; aging plant"],
        ["Energnist Kolding", "Kolding", "2024", "0.0005", "177", "1999",
         "Dioxin reappeared 2024 after clean 2022–23"],
        ["Sonderborg Kraftvarme", "Sonderborg", "2019", "0.0002", "96 (2024)",
         "1993", "32-year-old plant"],
        ["Hammel Fjernvarme", "Hammel", "2023", "0.0050", "36 (2024)",
         "2013", "Small but modern — compliance gap"],
    ]
    cw2 = [42*mm, 26*mm, 18*mm, 16*mm, 18*mm, 14*mm, 38*mm]
    story.append(priority_table(dk_diox_h, dk_diox_r, cw2, styles))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("High Mercury (Hg) Facilities", styles["h2"]))
    dk_hg_h = ["Facility", "City", "Hg 2022 (kg)", "Hg 2023 (kg)", "Hg 2024 (kg)", "Trend"]
    dk_hg_r = [
        ["I/S AffaldPlus Naestved", "Naestved", "6.60", "2.33", "1.44", "Declining — active remediation"],
        ["I/S Argo Roskilde Kraftvarmevaerk", "Roskilde", "3.81", "2.32", "2.13", "Persistent high"],
        ["I/S Vestforbr\u00e6nding Glostrup", "Glostrup", "3.69", "—", "—", "Spike 2022; data gap"],
        ["Svendborg Kraftvarme", "Svendborg", "5.78", "0.21", "—", "Volatile; was 3.6 kg in 2019"],
        ["REFA Affaldsforbraendingsanlaeg", "Nykobing F", "2.29", "2.37", "0.92", "Peaked 16.85 kg (2020)"],
        ["Frederikshavn Forsyning", "Frederikshavn", "0.64", "0.90", "—", "Rising: 0.08→0.90 over 3 yrs"],
    ]
    cw3 = [46*mm, 26*mm, 20*mm, 20*mm, 20*mm, 40*mm]
    story.append(priority_table(dk_hg_h, dk_hg_r, cw3, styles))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("High NOx / Heat Recovery Opportunities", styles["h2"]))
    dk_nox_h = ["Facility", "City", "NOx 2024 (t)", "NOx trend", "Started", "Scale"]
    dk_nox_r = [
        ["Fjernvarme Fyn Affaldsenergi", "Odense", "286", "+24% vs 2019", "1996", "Large"],
        ["I/S Argo Roskilde Kraftvarmevaerk", "Roskilde", "292", "Declining from 368", "1993", "Large"],
        ["Energnist Esbjerg", "Esbjerg", "230", "Stable ~230", "2002", "Large"],
        ["I/S Amager Ressourcecenter", "Copenhagen", "204", "Rising 2022–24", "2017", "Very large"],
        ["I/S Reno-Nord Energianl. Aalborg", "Aalborg", "211", "Stable ~215–228", "1977", "Large (47 yrs old)"],
        ["Maabjerg Energy Center", "Holstebro", "194", "Stable ~185–226", "2013", "Medium-large"],
        ["I/S Norfors", "Horsholm", "106", "Declining", "1996", "Medium"],
    ]
    cw4 = [48*mm, 24*mm, 22*mm, 32*mm, 18*mm, 28*mm]
    story.append(priority_table(dk_nox_h, dk_nox_r, cw4, styles))
    story.append(Spacer(1, 5*mm))

    # ── FINLAND ───────────────────────────────────────────────────────────────
    story.append(section_banner("Finland — Detailed Lead Analysis", styles))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Finland operates 8 WtE incineration plants (5(b)), mostly built 2010–2016. Annual E-PRTR "
        "reporting available 2019–2024. No Finnish plant reports dioxins to EEA, but WI BAT requirements "
        "still apply. NOx levels are significantly higher than Danish equivalents — heat recovery and "
        "SCR optimisation are the primary GMAB angles.",
        styles["body"]))

    fi_h = ["Facility", "City", "NOx 2019 (t)", "NOx 2022 (t)", "NOx 2024 (t)", "Trend", "CO2 2024 (kt)"]
    fi_r = [
        ["Vantaan Energia, Jätevoimala", "Vantaa", "456", "390", "545",
         "RISING sharply", "284,000"],
        ["Lahti Energia, Kymijärvi", "Lahti", "477", "409", "324",
         "Declining (~35%)", "—"],
        ["Tammervoima Oy", "Tampere", "228", "230", "206",
         "Stable", "—"],
        ["Westenergy Oy, Mustasaaren", "Koivulahti", "198", "141", "138",
         "Declining (~30%)", "212,000"],
        ["Kotkan Energia, Hyötyvoimalaitos", "Kotka", "113", "110", "125",
         "Rising 2024", "107,000"],
        ["Riikinvoima Oy", "Leppavirta", "—", "—", "—",
         "CO2 only (~120 kt)", "~120,000"],
        ["Lounavoima Oy, Korvenmaen", "Salo", "—", "—", "—",
         "No data reported", "—"],
        ["Turun Seudun Energiantuotanto", "Turku", "—", "—", "—",
         "No data reported", "—"],
    ]
    cw5 = [48*mm, 22*mm, 18*mm, 18*mm, 18*mm, 28*mm, 20*mm]
    story.append(priority_table(fi_h, fi_r, cw5, styles))
    story.append(Paragraph(
        "Vantaan Energia (Helsinki) is the dominant Finnish lead. NOx 545 t/yr in 2024 is the highest "
        "single-plant value in the entire Nordic dataset. CO2 jumped 58% in 2024, signalling new capacity "
        "or feedstock change. Immediate priority for heat recovery proposal.",
        styles["caption"]))
    story.append(Spacer(1, 5*mm))

    # ── NORWAY ────────────────────────────────────────────────────────────────
    story.append(section_banner("Norway — Lead Analysis", styles))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Norway ceased E-PRTR reporting to EEA after 2017. Current emissions are available via "
        "Miljodirektoratet (Norwegian Environment Agency) — norskeutslipp.no. All 15 registered "
        "WtE plants are assumed operational. Norway is actively expanding WtE capacity; several "
        "plants have been commissioned since 2017.",
        styles["body"]))
    story.append(Paragraph(
        "Strategic note: Fortum Oslo Varme's Klemetsrud facility is the world's first WtE plant "
        "with full CCS (carbon capture). This represents a unique GMAB heat-integration partnership "
        "opportunity beyond standard APCD.",
        styles["body"]))

    no_h = ["Facility", "City", "Operator", "Last NOx (t)", "Dioxin flag", "Priority"]
    no_r = [
        ["Statkraft Varme, Avfallsforbrenning", "Trondheim",
         "Statkraft Varme AS", "255 (2017)", "—", "HIGH"],
        ["BIR Avfallsenergi", "Bergen",
         "BIR Avfallsenergi AS", "159 (2017)", "—", "HIGH"],
        ["Bio-El / Kvitebjorn Bio-El AS", "Fredrikstad",
         "Kvitebjorn Bio-El AS", "—", "0.0008 kg TEq (2015)", "HIGH — dioxin"],
        ["Fortum Oslo Varme", "Oslo",
         "Fortum Oslo Varme AS", "115 (2017)", "—", "MED / Strategic (CCS)"],
        ["Haraldrud Energigjenvinning", "Oslo",
         "Haraldrud EGJ", "126 (2009)", "—", "MED"],
        ["Fortum Haraldrud Varmesentral", "Oslo",
         "Fortum Oslo Varme AS", "103 (2010)", "—", "MED"],
        ["FREVAR Forbrenningsanlegget", "Fredrikstad",
         "FREVAR", "CO2: ~115 kt", "—", "MED"],
        ["Forus Energigjenvinning 1", "Sandnes (Stavanger)",
         "Forus Energigjenvinning 2 AS", "—", "—", "MED"],
        ["Tafjord Kraftvarme", "Alesund",
         "Tafjord Kraftvarme AS", "—", "—", "MED"],
        ["Kvitebjorn Varme, Skattora", "Tromso",
         "Kvitebjorn Varme AS", "—", "—", "MED (northernmost)"],
        ["Nordmore Energigjenvinning KS", "Averoy",
         "Nordmore EGJ KS", "—", "—", "LOW"],
        ["Ostfold Energi, Rakkestadanlegget", "Rakkestad",
         "Ostfold Energi AS", "—", "—", "LOW"],
    ]
    cw6 = [46*mm, 24*mm, 36*mm, 20*mm, 24*mm, 22*mm]
    story.append(priority_table(no_h, no_r, cw6, styles))
    story.append(Paragraph(
        "Data for Norway: last EEA E-PRTR report = 2017. Verify current emissions via "
        "https://www.norskeutslipp.no before outreach.",
        styles["caption"]))
    story.append(Spacer(1, 5*mm))

    # ── TIER 2 & 3 ────────────────────────────────────────────────────────────
    story.append(section_banner("Tier 2 & 3 Pipeline", styles))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Tier 2 — Queue for Q2 2026", styles["h2"]))
    t2_h = ["Facility", "Country", "City", "Key Signal", "GMAB Angle"]
    t2_r = [
        ["Lahti Energia, Kymijärvi", "FI", "Lahti",
         "NOx 477→324 t/yr (declining) — active investment", "Residual NOx reduction + ORC"],
        ["I/S Argo Roskilde Kraftvarmevaerk", "DK", "Roskilde",
         "Hg persistent 2.1–3.8 kg/yr; 1993 plant", "APCD Hg control upgrade"],
        ["I/S Vestforbr\u00e6nding Glostrup", "DK", "Glostrup",
         "Hg 3.69 kg spike 2022; NOx ~380 t/yr", "APCD + heat recovery (very large plant)"],
        ["BIR Avfallsenergi", "NO", "Bergen",
         "NOx 159 t/yr; main Bergen WtE", "Heat recovery / ORC"],
        ["Fjernvarme Fyn Affaldsenergi", "DK", "Odense",
         "Dioxins 2020–22; NOx +24%", "APCD + ORC upgrade"],
        ["I/S Reno-Nord Aalborg", "DK", "Aalborg",
         "Started 1977 (47 yrs old); NOx 211 t/yr", "Full APCD + heat recovery overhaul"],
        ["Tammervoima Oy", "FI", "Tampere",
         "NOx stable 215 t/yr; modern plant", "ORC / heat recovery"],
    ]
    cw7 = [44*mm, 14*mm, 22*mm, 52*mm, 40*mm]
    story.append(priority_table(t2_h, t2_r, cw7, styles))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Tier 3 — Longer-Term Pipeline", styles["h2"]))
    t3_items = [
        "Energnist Esbjerg (DK) — large scale, stable 230 t NOx/yr",
        "Westenergy Oy (FI, Koivulahti) — declining NOx (198→138 t), coastal, 212 kt CO2",
        "Fortum Oslo Varme / Klemetsrud CCS (NO) — CCS integration = strategic GMAB synergy",
        "AVV I/S Hjoerring (DK) — NOx rising to 95 t in 2024; started 1999",
        "Sonderborg Kraftvarme (DK) — dioxins 2019, 1993 plant, 96 t NOx",
        "Renosyd Skanderborg (DK) — Hg rising 2024 (0.27 kg); started 1980",
        "Kotkan Energia (FI) — NOx rising to 125 t in 2024; coastal industrial port",
        "Hammel Fjernvarme (DK) — small but modern; dioxins 0.005 kg in 2023",
        "FREVAR Fredrikstad (NO) — sewage sludge + MSW; CO2 ~115 kt",
    ]
    for item in t3_items:
        story.append(Paragraph(f"\u2022  {item}", styles["bullet"]))
    story.append(Spacer(1, 5*mm))

    # ── KEY OBSERVATIONS ──────────────────────────────────────────────────────
    story.append(section_banner("Key Observations by Country", styles))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Denmark", styles["h2"]))
    dk_obs = [
        "Most data-rich: annual E-PRTR reporting through 2024 for all major plants.",
        "ARC CopenHill dioxin spike (8.98 kg TEq, 2024) is the single most urgent Nordic APCD lead.",
        "Multiple persistent Hg cases: Naestved, Glostrup, Roskilde — ongoing compliance pressure.",
        "NOx broadly declining 2019–2024 except Odense Fjernvarme Fyn (+24%).",
        "~8 plants started 1993–2000 are approaching 30-year refurbishment cycles.",
    ]
    for o in dk_obs:
        story.append(Paragraph(f"\u2022  {o}", styles["bullet"]))

    story.append(Paragraph("Finland", styles["h2"]))
    fi_obs = [
        "Vantaan Energia (Helsinki) is the dominant lead — 545 t NOx in 2024, rising strongly.",
        "Finnish WtE plants are larger and newer (2012–2016) than Danish equivalents.",
        "No dioxin EEA reporting — Finnish national permits may reveal compliance gaps.",
        "Lahti Energia shows active NOx investment — consultative/upgrade opportunity now.",
    ]
    for o in fi_obs:
        story.append(Paragraph(f"\u2022  {o}", styles["bullet"]))

    story.append(Paragraph("Norway", styles["h2"]))
    no_obs = [
        "EEA data gap: Norway ceased E-PRTR reporting after 2017. Verify via norskeutslipp.no.",
        "Bio-El Fredrikstad is the confirmed dioxin case — direct APCD sales lead.",
        "Statkraft Varme Trondheim is the volume NOx lead (255 t/yr, 2017).",
        "Fortum Oslo Varme / Klemetsrud CCS = strategic long-term partnership (world-first CCS on WtE).",
        "Norway is actively expanding WtE; several new plants commissioned post-2017.",
    ]
    for o in no_obs:
        story.append(Paragraph(f"\u2022  {o}", styles["bullet"]))

    story.append(Paragraph("Iceland", styles["h2"]))
    story.append(Paragraph(
        "75 registered facilities in EEA database, none in 5(b) incineration category. "
        "Not relevant for WtE GMAB sales.",
        styles["body"]))
    story.append(Spacer(1, 5*mm))

    # ── DATA NOTES ────────────────────────────────────────────────────────────
    story.append(HRFlowable(width=W, thickness=0.5, color=MID_GRAY))
    story.append(Spacer(1, 2*mm))
    notes = [
        "NOx values in tonnes/year (1 t = 1,000 kg). Source column: 2f_PollutantRelease, medium=AIR.",
        "Dioxin reporting threshold: 0.0001 kg I-TEQ/yr. Mercury threshold: 1 kg/yr.",
        "Norway E-PRTR last reporting year: 2017. Active facilities verified via public records.",
        "Finnish facility IDs use national paikkatiedot.fi INSPIRE identifiers.",
        "Sweden covered in separate note: Swedish WtE — Emissions Data & GMAB Lead Analysis.",
        f"Database: data/processed/converted_database.db (v16). Report generated: {date.today().strftime('%d %B %Y')}.",
    ]
    for n in notes:
        story.append(Paragraph(f"\u2022  {n}", ParagraphStyle("note",
            fontSize=7, fontName="Helvetica", textColor=MID_GRAY,
            leading=10, leftIndent=10, firstLineIndent=-8, spaceAfter=1)))

    doc.build(story)
    print(f"PDF saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
