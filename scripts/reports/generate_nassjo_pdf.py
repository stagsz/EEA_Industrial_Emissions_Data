"""Generate a printable PDF for Nassjo Affarsverk AB deep dive."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "Nassjo_Affarsverk_Deep_Dive.pdf")

# Colors
DARK_BLUE = HexColor("#1a3a5c")
MID_BLUE = HexColor("#2c5f8a")
LIGHT_BLUE = HexColor("#e8f0f8")
ACCENT_GREEN = HexColor("#2d7d46")
ACCENT_RED = HexColor("#c0392b")
LIGHT_GRAY = HexColor("#f5f5f5")
WHITE = HexColor("#ffffff")
BLACK = HexColor("#222222")
BORDER_GRAY = HexColor("#cccccc")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "DocTitle", fontName="Helvetica-Bold", fontSize=18,
        textColor=DARK_BLUE, spaceAfter=2*mm, leading=22
    ))
    styles.add(ParagraphStyle(
        "DocSubtitle", fontName="Helvetica", fontSize=11,
        textColor=MID_BLUE, spaceAfter=6*mm, leading=14
    ))
    styles.add(ParagraphStyle(
        "SectionHead", fontName="Helvetica-Bold", fontSize=13,
        textColor=DARK_BLUE, spaceBefore=6*mm, spaceAfter=3*mm, leading=16
    ))
    styles.add(ParagraphStyle(
        "SubHead", fontName="Helvetica-Bold", fontSize=10.5,
        textColor=MID_BLUE, spaceBefore=4*mm, spaceAfter=2*mm, leading=13
    ))
    styles.add(ParagraphStyle(
        "BodyText2", fontName="Helvetica", fontSize=9,
        textColor=BLACK, spaceAfter=2*mm, leading=12
    ))
    styles.add(ParagraphStyle(
        "BoldBody", fontName="Helvetica-Bold", fontSize=9,
        textColor=BLACK, spaceAfter=2*mm, leading=12
    ))
    styles.add(ParagraphStyle(
        "BulletItem", fontName="Helvetica", fontSize=9,
        textColor=BLACK, spaceAfter=1*mm, leading=12,
        leftIndent=10*mm, bulletIndent=5*mm
    ))
    styles.add(ParagraphStyle(
        "SmallNote", fontName="Helvetica-Oblique", fontSize=7.5,
        textColor=HexColor("#666666"), spaceAfter=1*mm, leading=10
    ))
    styles.add(ParagraphStyle(
        "TableCell", fontName="Helvetica", fontSize=8.5,
        textColor=BLACK, leading=11
    ))
    styles.add(ParagraphStyle(
        "TableCellBold", fontName="Helvetica-Bold", fontSize=8.5,
        textColor=BLACK, leading=11
    ))
    styles.add(ParagraphStyle(
        "AlertBox", fontName="Helvetica-Bold", fontSize=9,
        textColor=ACCENT_RED, spaceAfter=2*mm, leading=12,
        backColor=HexColor("#fdecea"), borderPadding=4
    ))
    return styles


def make_table(data, col_widths=None, header=True):
    """Create a styled table."""
    style_cmds = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR", (0, 0), (-1, -1), BLACK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
    ]
    if header:
        style_cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), DARK_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ]
    # Alternate row shading
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))

    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style_cmds))
    return t


def make_kv_table(pairs, label_width=45*mm, value_width=120*mm):
    """Key-value style table (no header row)."""
    data = []
    for k, v in pairs:
        data.append([Paragraph(f"<b>{k}</b>", ParagraphStyle("kv", fontName="Helvetica-Bold", fontSize=8.5, leading=11)),
                      Paragraph(str(v), ParagraphStyle("kv2", fontName="Helvetica", fontSize=8.5, leading=11))])
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
    ]
    t = Table(data, colWidths=[label_width, value_width])
    t.setStyle(TableStyle(style_cmds))
    return t


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER_GRAY, spaceBefore=3*mm, spaceAfter=3*mm)


def build_pdf():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )
    s = build_styles()
    story = []

    # Title
    story.append(Paragraph("Nassjo Affarsverk AB", s["DocTitle"]))
    story.append(Paragraph("Deep Dive &amp; Tender AC18444  |  Compiled 2026-03-04", s["DocSubtitle"]))
    story.append(hr())

    # ── Company Overview ──
    story.append(Paragraph("Company Overview", s["SectionHead"]))
    story.append(make_kv_table([
        ("Company", "Nassjo Affarsverk Aktiebolag (NAV)"),
        ("Org.nr", "556038-7044"),
        ("Founded", "1939"),
        ("Ownership", "100% Nassjo kommun (via Ornen i Nassjo AB)"),
        ("CEO (VD)", "Patrik Cantby  |  0380-51 71 01"),
        ("CFO / Vice VD", "Christian Skenberg  |  0380-51 70 20"),
        ("Energy Manager", "Maria Lund  |  0380-51 70 51"),
        ("Employees", "~140 (2021)"),
        ("Revenue", "376.8 MSEK (2021)"),
        ("Profit (after fin.)", "69.4 MSEK (2021)"),
        ("Investments", "106.4 MSEK (2021)"),
        ("Long-term debt", "289.8 MSEK"),
        ("Website", "nav.se"),
        ("Address", "Blockgatan 8, Nassjo"),
    ]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Business Areas", s["SubHead"]))
    for area in [
        "District heating (fjarrvarme) - Nassjo, Bodafors, Anneberg",
        "Electricity production (CHP + Ramsjoholms hydropower)",
        "Electricity distribution (Nassjo Affarsverk Elnat AB)",
        "Water and wastewater",
        "Waste management / renhallning",
        "Fiber network (Citynaetet)",
        "Street and park maintenance",
    ]:
        story.append(Paragraph(f"&bull;  {area}", s["BulletItem"]))

    # ── Management Team ──
    story.append(Paragraph("Full Management Team (Ledningsgrupp)", s["SectionHead"]))
    mgmt_data = [
        ["Name", "Role", "Phone"],
        ["Patrik Cantby", "VD (CEO) NAV, Elnat AB & Citynaetet", "0380-51 71 01"],
        ["Christian Skenberg", "Ekonomichef / Vice VD", "0380-51 70 20"],
        ["Maria Lund", "Energichef (Energy Manager)", "0380-51 70 51"],
        ["Karl-Johan Mannerback", "Elnatschef (Power Grid)", "0380-51 70 55"],
        ["Peter Arlbrandt", "Renhallningschef (Waste)", "0380-51 70 70"],
        ["Alexander Bjorkegren", "VA-chef (Water/WW)", "0380-51 71 37"],
        ["Johan Klintbo Falk", "Entreprenadchef (Contracting)", "0380-51 70 10"],
        ["Johanna Lofstrom", "Kommunikation & Marknad", "0380-51 71 10"],
        ["Helene Axelsson", "HR-chef", "0380-51 70 80"],
        ["Thommie Motin", "Affarsutveckling & IT", "0380-51 70 37"],
        ["Bjorn Wenstrom", "Verksamhetschef Citynaetet", "0380-55 78 83"],
    ]
    story.append(make_table(mgmt_data, col_widths=[42*mm, 62*mm, 32*mm]))
    story.append(Paragraph("Board Chair: Tommy Broholm  |  Email format: firstname.lastname@nav.se", s["SmallNote"]))

    story.append(hr())

    # ── Tender AC18444 ──
    story.append(Paragraph("Tender AC18444", s["SectionHead"]))
    story.append(Paragraph(
        "<b>DEADLINE: 2026-03-30</b>  --  Access via Clira procurement platform",
        s["AlertBox"]
    ))
    story.append(make_kv_table([
        ("Tender number", "AC18444"),
        ("Period", "2026-03-02 -- 2026-03-30"),
        ("Contact person", "Emilie Wikstand (may also be Wikstrand)"),
        ("Platform", "Clira (NAV's official tender portal)"),
        ("Backup platform", "eSource (Nassjo kommun)"),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "No public profile found for Emilie Wikstand. Likely in procurement/inkop at NAV. "
        "Maria Lund (Energy Manager, 0380-51 70 51) is the technical counterpart for energy equipment tenders.",
        s["SmallNote"]
    ))

    story.append(PageBreak())

    # ── CHP Plant Technical Details ──
    story.append(Paragraph("Nassjo Kraftvarmeverk (CHP Plant) - Technical Details", s["SectionHead"]))

    story.append(Paragraph("EEA Registered Facilities", s["SubHead"]))
    fac_data = [
        ["Facility", "EEA ID", "Activity", "Start"],
        ["Nassjo Kraftvarmeverk", "SE.CAED/10015637", "1(c) Thermal >=50 MW", "1900"],
        ["Boda avfallsanlaggning", "SE.CAED/10015633", "5(d) Landfills", "1965"],
    ]
    story.append(make_table(fac_data, col_widths=[42*mm, 38*mm, 52*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "IED Classification: 1.1 - Combustion >=50 MW  |  EU ETS ID: SE000000000000202",
        s["BoldBody"]
    ))

    story.append(Paragraph("Production Data (2021)", s["SubHead"]))
    story.append(make_kv_table([
        ("Heat delivery", "168.3 GWh"),
        ("Connected thermal cap.", "90.6 MW"),
        ("Electricity from CHP", "26.7 GWh"),
        ("Electricity from hydro", "3.6 GWh (Ramsjoholms)"),
        ("Total elec. production", "30.3 GWh"),
        ("DH customers", "~1,956"),
        ("Main fuel", "Forest residues (skogsbrансle)"),
        ("Oil share", "2.0% (at target)"),
        ("CO2 rights allocated", "7,249 tonnes"),
        ("CO2 rights sold", "6,600 (3.4 MSEK revenue)"),
    ]))

    story.append(Paragraph("Boiler Equipment", s["SubHead"]))
    story.append(Paragraph(
        "At least one hot water boiler type <b>VEA UNIVEX HVV120PD H-16</b> (confirmed via tube replacement "
        "order of 560 tubes from VEA AB).",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        "An <b>infrasound cleaning system</b> (from Heat Management) was installed because existing compressed "
        "air soot blowing was ineffective due to valve positioning.",
        s["BodyText2"]
    ))
    story.append(Paragraph(
        '<b>Key insight:</b> Boiler technology "requires replacement by 2045" per 2021 annual report. '
        "Multi-decade planning cycle for major boiler investments.",
        s["AlertBox"]
    ))

    story.append(Paragraph("Waste Transfers (E-PRTR Data 2008-2021)", s["SubHead"]))
    waste_data = [
        ["Year", "Haz. Waste (t)", "Non-Haz (t)"],
        ["2008", "8.9", "-"],
        ["2009", "25.4", "-"],
        ["2010", "22.6", "2,140"],
        ["2011", "16.5", "-"],
        ["2012", "10.0", "2,010"],
        ["2013", "3.6", "-"],
        ["2014", "5.8", "-"],
        ["2015", "7.7", "-"],
        ["2016", "10.3", "2,220"],
        ["2017", "12.2", "2,090"],
        ["2018", "6.4", "-"],
        ["2019", "10.2", "-"],
        ["2020", "15.2", "-"],
        ["2021", "6.4", "-"],
    ]
    story.append(make_table(waste_data, col_widths=[25*mm, 40*mm, 40*mm]))
    story.append(Paragraph(
        "No E-PRTR pollutant releases to air/water reported (below thresholds). "
        "Non-haz waste (~2,000+ t) is likely bottom ash from biomass combustion.",
        s["SmallNote"]
    ))

    story.append(hr())

    # ── Recent Investments ──
    story.append(Paragraph("Recent Investments and Signals", s["SectionHead"]))
    signals = [
        "<b>2024 price increases:</b> DH price raised 25% (Apr 2024), then +3% more. "
        'Reason: "large investments and new environmental requirements"',
        "<b>VEA tube replacement:</b> 560 tubes for boiler VEA UNIVEX HVV120PD H-16",
        "<b>Infrasound soot cleaning:</b> Replaced ineffective compressed air soot blowing",
        "<b>Fleet electrification:</b> 10 EVs, 24 gas vehicles, 26 HVO vehicles",
        "<b>Wastewater upgrade:</b> Major rebuild of Nassjo ARV underway, pharma removal planned",
        "<b>Biogas:</b> Exploring food waste-based biogas production",
    ]
    for sig in signals:
        story.append(Paragraph(f"&bull;  {sig}", s["BulletItem"]))

    story.append(PageBreak())

    # ── GMAB Sales Relevance ──
    story.append(Paragraph("GMAB Sales Relevance", s["SectionHead"]))

    story.append(Paragraph("Opportunity Assessment", s["SubHead"]))
    reasons = [
        "<b>Active tender (AC18444)</b> - procurement window closes 2026-03-30",
        "<b>90.6 MW connected thermal capacity</b> - significant mid-sized CHP",
        "<b>IED-classified (>=50 MW)</b> - subject to BREF/BAT requirements",
        "<b>Boiler replacement horizon to 2045</b> - planning next-gen technology",
        '<b>"New environmental requirements"</b> cited as investment driver (2024)',
        "<b>Existing flue gas cleaning challenges</b> - soot blowing was ineffective",
        "<b>Municipal utility</b> with stable finances (377 MSEK revenue, 69 MSEK profit)",
        "<b>Biomass-fired</b> - relevant for GMAB product range",
    ]
    for i, r in enumerate(reasons, 1):
        story.append(Paragraph(f"{i}.  {r}", s["BulletItem"]))

    story.append(Paragraph("Potential GMAB Products", s["SubHead"]))
    products = [
        "Flue gas cleaning equipment/upgrades",
        "Filter systems for biomass combustion",
        "SCR/SNCR for NOx reduction (IED BAT compliance)",
        "Ash handling systems (~2,000+ tonnes/year produced)",
        "Monitoring/measurement equipment",
    ]
    for p in products:
        story.append(Paragraph(f"&bull;  {p}", s["BulletItem"]))

    story.append(Paragraph("Key Contacts for Approach", s["SubHead"]))
    contact_data = [
        ["Priority", "Name", "Role", "Rationale"],
        ["1", "Emilie Wikstand", "Tender contact AC18444", "Direct procurement contact"],
        ["2", "Maria Lund", "Energichef", "Technical decision maker"],
        ["3", "Patrik Cantby", "VD", "Final decision authority"],
        ["4", "Johan Klintbo Falk", "Entreprenadchef", "Contracting/suppliers"],
    ]
    story.append(make_table(contact_data, col_widths=[18*mm, 35*mm, 40*mm, 55*mm]))

    story.append(Paragraph("Action Items", s["SubHead"]))
    actions = [
        "Access tender AC18444 via Clira before 2026-03-30 deadline",
        "Determine tender scope (emissions equipment, boiler maintenance, or other?)",
        "Contact Maria Lund (Energy Manager) to discuss technical requirements",
        "Review NAV's latest miljorapport via Naturvardsverket's SMP portal",
        "Check if tender fits GMAB's product/service categories",
    ]
    for a in actions:
        story.append(Paragraph(f"&#9744;  {a}", s["BulletItem"]))

    story.append(hr())
    story.append(Paragraph(
        "Sources: EEA Industrial Emissions Database (E-PRTR/IED), nav.se, allabolag.se, "
        "hejafjarrvarme.se, pabliq.se, NAV Arsredovisning 2021, VEA AB, Heat Management case study",
        s["SmallNote"]
    ))

    doc.build(story)
    print(f"PDF saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
