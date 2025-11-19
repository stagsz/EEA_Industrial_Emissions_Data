"""
SPIG-GMAB Lead Generation Agent
Target: WASTE-TO-ENERGY PLANTS - Dioxin Reduction & Energy Recovery Optimization

Company: SPIG-GMAB (www.SPIG-GMAB.com)
Mission: "TOGETHER WE SUCCEED, TOGETHER WE GO GREEN"
Solutions: GMAB – Advanced Emission Control & Energy Recovery Technologies
- APCD (Air Pollution Control Device) systems for dioxin/PCDD/PCDF reduction
- De novo synthesis prevention in flue gas treatment
- Memory effect mitigation strategies
- I-TEQ/TEQ dioxin toxicity equivalent compliance
- Advanced energy recovery systems for waste incineration plants
- Flue gas heat recovery with integrated emission control
- Steam cycle efficiency improvements with clean emissions
- Thermal energy maximization from waste combustion

This agent finds WASTE-TO-ENERGY facilities needing:
- Municipal solid waste (MSW) incineration plants with dioxin issues
- Industrial waste treatment facilities with emission violations
- Biomass/RDF (refuse-derived fuel) combustion plants
- Hazardous waste thermal treatment facilities
- Sewage sludge incineration facilities
- Any WtE facility with PCDD/PCDF compliance challenges

Focus: Eliminate dioxin/PCDD/PCDF emissions while maximizing energy recovery
"""
import asyncio
import json
from claude_agent_sdk import query, tool, create_sdk_mcp_server, ClaudeAgentOptions


# Define custom tools for database access
@tool(
    name="query_database",
    description="Query the leads database for waste-to-energy and dioxin emissions",
    input_schema={  # Change from inputSchema
        "query_type": {
            "type": "string",
            "enum": ["sql", "filter"],
            "description": "Type of query to run"
        },
        "query": {
            "type": "string",
            "description": "SQL query or filter criteria as JSON"
        },
        "dioxin_focus": {
            "type": "boolean",
            "description": "Filter for facilities with dioxin/PCDD/PCDF emissions"
        }
    }
)
async def query_database(args, extra):
    """
    Query EEA Industrial Emissions Database for dioxin-emitting waste-to-energy facilities

    DIOXIN-FOCUSED SEARCH: Priority on facilities with PCDD/PCDF/Dioxin emissions

    Uses actual CSV files from: converted_csv/
    - 4d_EnergyInput.csv (energy consumption data)
    - 4e_EmissionsToAir.csv (dioxin/PCDD/PCDF emissions data - KEY)
    - 2_ProductionFacility.csv (facility information)
    - 2e_ProductionVolume.csv (production levels)
    - 3d_BATConclusions.csv (Best Available Techniques - APCD compliance)

    DIOXIN SEARCH FILTERS:
    - Look for: PCDD, PCDF, Dioxin (including I-TEQ, TEQ equivalents)
    - Match facilities with:
      * Exceeding I-TEQ/TEQ limits
      * At-risk of exceeding limits
      * Memory effect indicators
      * De novo synthesis issues
    """
    # IMPLEMENTATION NOTE: Replace mock with actual data
    # import pandas as pd
    # energy_df = pd.read_csv('converted_csv/4d_EnergyInput.csv')
    # emissions_df = pd.read_csv('converted_csv/4e_EmissionsToAir.csv')
    # facilities_df = pd.read_csv('converted_csv/2_ProductionFacility.csv')

    # Mock results showing WASTE-TO-ENERGY plant opportunities
    mock_results = [
        {
            "facility": "Amsterdam Waste Energy Center (AEB)",
            "facility_type": "Municipal Solid Waste Incinerator",
            "country": "Netherlands",
            "waste_throughput_tonnes_year": 550000,
            "waste_type": "Mixed municipal solid waste (MSW)",
            "current_electricity_output_MW": 62,
            "current_heat_output_MW": 85,
            "current_efficiency_percent": 68,
            "flue_gas_temp_post_boiler": "185°C",
            "waste_heat_potential": "VERY HIGH - Additional 25 MW thermal recoverable from flue gas",
            "current_recovery": "Basic steam boiler + turbine, NO flue gas condenser",
            "energy_revenue_million_euro": 42,
            "improvement_potential": "€8-12M/year via advanced heat recovery",
            "emission_levels": "NOx: 85 mg/Nm³, Dioxins: compliant",
            "compliance_status": "Compliant but optimizable",
            "contact": "Plant Manager / Technical Director",
            "urgency": "HIGH - Plant upgrade planned 2025-2026"
        },
        {
            "facility": "SYSAV Waste-to-Energy Plant",
            "facility_type": "MSW + RDF Incineration",
            "country": "Sweden (Malmö)",
            "waste_throughput_tonnes_year": 650000,
            "waste_type": "MSW + Refuse-Derived Fuel (RDF)",
            "current_electricity_output_MW": 75,
            "current_heat_output_MW": 180,
            "current_efficiency_percent": 72,
            "flue_gas_temp_post_boiler": "140°C",
            "waste_heat_potential": "HIGH - 18 MW thermal from low-temp flue gas",
            "current_recovery": "Modern CHP, but low-grade heat unutilized",
            "energy_revenue_million_euro": 68,
            "improvement_potential": "€5-7M/year + district heating expansion",
            "emission_levels": "Best-in-class, carbon neutral certified",
            "contact": "Energy Optimization Manager",
            "urgency": "MEDIUM - Seeking to maximize energy output"
        },
        {
            "facility": "Brescia Waste Incinerator",
            "facility_type": "Municipal Waste-to-Energy",
            "country": "Italy",
            "waste_throughput_tonnes_year": 750000,
            "waste_type": "Municipal solid waste",
            "current_electricity_output_MW": 85,
            "current_heat_output_MW": 95,
            "current_efficiency_percent": 65,
            "flue_gas_temp_post_boiler": "220°C",
            "waste_heat_potential": "VERY HIGH - 35 MW thermal potential (old technology)",
            "current_recovery": "Aging boiler system, inefficient heat recovery",
            "energy_revenue_million_euro": 52,
            "improvement_potential": "€12-18M/year via boiler retrofit + advanced recovery",
            "emission_levels": "APPROACHING EU limits, warning issued (<90 days to improve NOx)",
            "compliance_status": "At risk - NOx approaching 200 mg/Nm³ limit",
            "contact": "Plant Director / Sustainability Officer",
            "urgency": "CRITICAL - Boiler end-of-life, replacement 2025"
        },
        {
            "facility": "Berlin-Ruhleben Waste Incineration Plant",
            "facility_type": "MSW Thermal Treatment",
            "country": "Germany",
            "waste_throughput_tonnes_year": 520000,
            "waste_type": "Municipal waste + commercial waste",
            "current_electricity_output_MW": 60,
            "current_heat_output_MW": 110,
            "current_efficiency_percent": 70,
            "flue_gas_temp_post_boiler": "165°C",
            "waste_heat_potential": "HIGH - 22 MW thermal via ORC or heat pump integration",
            "current_recovery": "Standard steam cycle, NO advanced systems",
            "energy_revenue_million_euro": 48,
            "improvement_potential": "€7-10M/year + 15% efficiency boost",
            "emission_levels": "Compliant, but seeking optimization",
            "contact": "Technical Operations Manager",
            "urgency": "HIGH - Energy prices driving efficiency push"
        },
        {
            "facility": "Warsaw-Targówek Waste Thermal Treatment",
            "facility_type": "MSW Incineration + Biomass",
            "country": "Poland",
            "waste_throughput_tonnes_year": 480000,
            "waste_type": "MSW + sewage sludge + biomass",
            "current_electricity_output_MW": 52,
            "current_heat_output_MW": 125,
            "current_efficiency_percent": 66,
            "flue_gas_temp_post_boiler": "195°C",
            "waste_heat_potential": "VERY HIGH - 28 MW thermal (multi-fuel optimization needed)",
            "current_recovery": "Basic boiler, NO flue gas condensation",
            "energy_revenue_million_euro": 38,
            "improvement_potential": "€9-14M/year + carbon credit bonus",
            "emission_levels": "Recent violation (6 months ago) - dioxin exceedance, corrective action implemented",
            "compliance_status": "Currently compliant, but history of issues",
            "contact": "Plant Manager / Energy Engineer",
            "urgency": "HIGH - Expansion project 2026 - ideal timing for upgrade"
        }
    ]

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(mock_results, indent=2)
            }
        ]
    }


@tool(
    name="score_lead",
    description="Score a lead based on qualification criteria",
    input_schema={  # Change from inputSchema
        "lead_data": {
            "type": "object",
            "description": "Lead information to score"
        },
        "criteria": {
            "type": "object",
            "description": "Scoring criteria and weights"
        }
    }
)
async def score_lead(args, extra):
    """Calculate lead score based on DIOXIN REDUCTION & waste-to-energy plant optimization"""
    lead = args.get('lead_data', {})
    criteria = args.get('criteria', {})

    # GMAB scoring logic - PRIORITY FOCUS: DIOXIN/PCDD/PCDF REDUCTION
    score = 0
    reasons = []

    # 1. DIOXIN/PCDD/PCDF EMISSIONS (40 points - HIGHEST PRIORITY) - Regulatory & health driver
    emission_status = lead.get('emission_levels', '').lower()
    compliance = lead.get('compliance_status', '').lower()

    # DIOXIN-SPECIFIC VIOLATIONS - Highest Priority
    has_dioxin_issue = 'dioxin' in emission_status or 'pcdd' in emission_status or 'pcdf' in emission_status

    if has_dioxin_issue and ('exceed' in emission_status or 'violation' in emission_status or 'critical' in compliance):
        score += 40
        reasons.append("🚨 CRITICAL DIOXIN/PCDD/PCDF VIOLATION - HIGHEST PRIORITY (APCD technology needed)")
    elif has_dioxin_issue and ('approaching' in emission_status or 'warning' in emission_status or '<90 days' in emission_status):
        score += 35
        reasons.append("⚠️ DIOXIN emissions APPROACHING limits - urgent APCD installation needed")
    elif has_dioxin_issue and ('recent violation' in emission_status or 'within 12 months' in emission_status):
        score += 30
        reasons.append("Recent DIOXIN violations - APCD retrofit needed to prevent recurrence")
    elif has_dioxin_issue and 'at risk' in emission_status:
        score += 25
        reasons.append("At risk of DIOXIN violations - proactive APCD system recommended")

    # General emission violations (lower priority than dioxin-specific)
    elif 'exceed' in emission_status or 'violation' in emission_status or 'critical' in compliance or 'enforcement' in emission_status:
        score += 20
        reasons.append("🚨 EMISSION VIOLATION - exceeding limits, enforcement action")
    elif 'approaching' in emission_status or 'warning' in emission_status or '<90 days' in emission_status:
        score += 15
        reasons.append("⚠️ APPROACHING emission limits - compliance deadline imminent")
    elif 'recent violation' in emission_status or 'within 12 months' in emission_status:
        score += 10
        reasons.append("Recent emission violations - upgrade needed to ensure compliance")
    elif 'at risk' in emission_status or 'within 20%' in emission_status:
        score += 5
        reasons.append("At risk of violations - proactive upgrade recommended")

    # 2. Low current efficiency (25 points) - More room for improvement
    efficiency = lead.get('current_efficiency_percent', 75)
    if efficiency < 67:
        score += 25
        reasons.append(f"🔥 LOW efficiency ({efficiency}%) - huge improvement potential via GMAB systems")
    elif efficiency < 70:
        score += 20
        reasons.append(f"MEDIUM efficiency ({efficiency}%) - good improvement opportunity")
    elif efficiency < 73:
        score += 15
        reasons.append(f"Moderate efficiency ({efficiency}%) - optimization possible")

    # 3. Waste heat recovery potential (20 points)
    waste_heat = lead.get('waste_heat_potential', '').lower()
    if 'very high' in waste_heat or '25 mw' in waste_heat or '28 mw' in waste_heat or '35 mw' in waste_heat:
        score += 20
        reasons.append("VERY HIGH waste heat potential from flue gas - advanced GMAB recovery systems ideal")
    elif 'high' in waste_heat or '18 mw' in waste_heat or '22 mw' in waste_heat:
        score += 15
        reasons.append("HIGH waste heat potential - excellent for GMAB ORC/heat recovery")

    # 4. Large waste throughput (15 points) - Economy of scale
    throughput = lead.get('waste_throughput_tonnes_year', 0)
    if throughput > 600000:
        score += 15
        reasons.append(f"Large facility ({throughput:,} tonnes/year) - economy of scale for GMAB systems")
    elif throughput > 500000:
        score += 12
        reasons.append(f"Medium-large facility ({throughput:,} tonnes/year) - good project size")

    # 5. Urgency/Timing (15 points) - Planned upgrades = perfect opportunity
    urgency = lead.get('urgency', '').lower()
    current_recovery = lead.get('current_recovery', '').lower()

    if 'critical' in urgency or 'end-of-life' in current_recovery or 'replacement' in urgency:
        score += 15
        reasons.append("CRITICAL timing - boiler replacement/major upgrade planned (ideal for GMAB integration)")
    elif 'high' in urgency or 'upgrade planned' in urgency or 'expansion' in urgency:
        score += 10
        reasons.append("HIGH urgency - plant upgrade or expansion planned (good timing)")

    result = {
        "facility": lead.get('facility'),
        "facility_type": lead.get('facility_type'),
        "country": lead.get('country'),
        "waste_throughput": lead.get('waste_throughput_tonnes_year'),
        "current_efficiency": lead.get('current_efficiency_percent'),
        "total_score": score,
        "qualification": "🔥 HOT LEAD" if score >= 70 else "⚠️ WARM" if score >= 50 else "COLD",
        "waste_heat_potential": lead.get('waste_heat_potential'),
        "improvement_potential": lead.get('improvement_potential'),
        "reasons": reasons
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result, indent=2)
            }
        ]
    }


@tool(
    name="export_leads",
    description="Export qualified leads to Excel file with multiple priority sheets",
    input_schema={  # Change from inputSchema
        "leads": {
            "type": "array",
            "description": "List of leads to export"
        },
        "format": {
            "type": "string",
            "enum": ["csv", "json", "excel"],
            "description": "Export format"
        },
        "filename": {
            "type": "string",
            "description": "Output filename"
        }
    }
)
async def export_leads(args, extra):
    """
    Export leads to Excel file with multiple priority sheets

    Creates separate sheets for:
    - PRIORITY 1: CRITICAL & URGENT (High value + High urgency + High need)
    - PRIORITY 2: HIGH VALUE (High value + Good possibility)
    - PRIORITY 3: HIGH NEED (Strong need + Medium value)
    - PRIORITY 4: GOOD OPPORTUNITIES (Medium value + Medium need)
    - PRIORITY 5: LONG TERM (Lower priority but qualified)
    - ALL LEADS: Complete list
    """
    # Implementation with pandas and openpyxl
    # import pandas as pd
    # leads_data = args.get('leads', [])
    #
    # # Categorize leads into priority groups
    # priority_1 = [l for l in leads_data if l.get('priority') == 1]
    # priority_2 = [l for l in leads_data if l.get('priority') == 2]
    # ...
    #
    # with pd.ExcelWriter(args.get('filename'), engine='openpyxl') as writer:
    #     pd.DataFrame(priority_1).to_excel(writer, sheet_name='PRIORITY 1 - CRITICAL', index=False)
    #     pd.DataFrame(priority_2).to_excel(writer, sheet_name='PRIORITY 2 - HIGH VALUE', index=False)
    #     ...

    leads_count = len(args.get('leads', []))
    filename = args.get('filename', 'GMAB_waste_to_energy_leads.xlsx')

    # Mock response showing multi-sheet export
    export_summary = {
        "total_leads": leads_count,
        "filename": filename,
        "sheets_created": [
            "PRIORITY 1 - CRITICAL & URGENT",
            "PRIORITY 2 - HIGH VALUE",
            "PRIORITY 3 - HIGH NEED",
            "PRIORITY 4 - GOOD OPPORTUNITIES",
            "PRIORITY 5 - LONG TERM",
            "ALL LEADS - MASTER LIST"
        ],
        "priority_breakdown": {
            "priority_1_critical": "High urgency + High value + Low efficiency",
            "priority_2_high_value": "Revenue potential >€10M/year",
            "priority_3_high_need": "Very low efficiency or aging equipment",
            "priority_4_good": "Medium value + Medium need",
            "priority_5_long_term": "Qualified but lower priority"
        }
    }

    return {
        "content": [
            {
                "type": "text",
                "text": f"✅ Exported {leads_count} leads to {filename} with {len(export_summary['sheets_created'])} priority sheets:\n" +
                       json.dumps(export_summary, indent=2)
            }
        ]
    }


async def find_qualified_leads():
    """
    Main function to find qualified leads

    Customize the prompt based on your specific needs:
    - Your product/service
    - Ideal customer profile (ICP)
    - Geographic preferences
    - Industry focus
    - Budget requirements
    """

    # Create MCP server with database tools
    mcp_server = create_sdk_mcp_server(
        name="lead-tools",
        version="1.0.0",
        tools=[query_database, score_lead, export_leads]
    )

    # GMAB DIOXIN REDUCTION & WASTE-TO-ENERGY PLANT OPTIMIZATION LEAD FINDER
    prompt = """
    Find WASTE-TO-ENERGY PLANTS with DIOXIN/PCDD/PCDF EMISSIONS and energy efficiency opportunities from the EEA Industrial Emissions Database.

    Company: SPIG-GMAB (www.SPIG-GMAB.com)
    Mission: "TOGETHER WE SUCCEED, TOGETHER WE GO GREEN"

    PRIMARY FOCUS: DIOXIN/PCDD/PCDF EMISSION REDUCTION with ADVANCED APCD TECHNOLOGY

    Our Core Solutions for Waste-to-Energy Plants:
    1. APCD (Air Pollution Control Device) Systems for Dioxin Elimination:
       - Advanced flue gas treatment systems (activated carbon injection, fabric filters)
       - De novo synthesis prevention (cooling to <200°C post-treatment)
       - Memory effect mitigation through optimized residence times
       - I-TEQ/TEQ toxicity equivalent compliance systems

    2. Dioxin-Integrated Energy Recovery:
       - Flue gas heat recovery with integrated APCD (economizers + clean treatment)
       - ORC systems for low-temperature heat conversion (post-dioxin treatment)
       - Steam cycle optimization with clean emissions baseline
       - Heat pump integration with dioxin-free heat source
       - Combined heat and power (CHP) with emission compliance

    3. Supporting Systems:
       - Boiler retrofit for emission control integration
       - Advanced monitoring and I-TEQ measurement systems
       - Continuous emission monitoring (CEM) for dioxins

    TARGET FACILITIES (Ideal Customer Profile):
    - Facility Types (DIOXIN PRIORITY):
      * Municipal Solid Waste (MSW) incinerators WITH DIOXIN ISSUES
      * Refuse-Derived Fuel (RDF) combustion plants with PCDD/PCDF emissions
      * Biomass waste-to-energy facilities with emission violations
      * Industrial waste thermal treatment (hazardous waste high dioxin risk)
      * Sewage sludge incineration plants (HIGH dioxin emission risk)
      * Hazardous waste thermal treatment (CRITICAL dioxin concern)

    - Location: European Union (focus: Germany, Netherlands, Italy, Sweden, Poland, France, Spain, Denmark)
    - Plant Size: >300,000 tonnes/year waste throughput (sufficient for APCD ROI)
    - Dioxin Status: CRITICAL (any recent violations, approaching limits, or at-risk)
    - Current Efficiency: LOW to MEDIUM (<73%) - secondary priority vs dioxin control
    - Flue Gas Temperature: >120°C post-boiler (for heat recovery + dioxin treatment)
    - Current Status: Aging equipment, poor emission control, planned upgrades, or enforcement pressure
    - Regulatory Pressure: Recent enforcement actions, compliance deadlines, EU BAT requirements
    - Decision Makers: Plant Manager, Environmental/HSE Director, Technical Director, Municipal Authority, Regulatory Affairs

    LEAD SCORING CRITERIA (0-100+ points - DIOXIN-FOCUSED):

    *** PRIMARY: DIOXIN/PCDD/PCDF EMISSIONS (40+ points - HIGHEST PRIORITY) ***
    1. DIOXIN/PCDD/PCDF VIOLATIONS (40 points - CRITICAL)
       - CRITICAL dioxin violations (exceeding I-TEQ/TEQ limits): 40 points
       - Recent dioxin violation history (within 24 months): 35 points
       - Approaching dioxin limits (<90 days warning): 35 points
       - At risk of dioxin exceedance (>80% of I-TEQ limit): 30 points
       - Memory effect indicators in flue gas treatment: 25 points
       - De novo synthesis risk (post-treatment temps >200°C): 25 points
    [BONUS] Dioxin-specific APCD need identified: +10 points

    2. General Emission Violations (Secondary Priority)
       - Other violations (NOx, SO2, particulates): 15-20 points
       - At risk of other emission violations: 10 points

    3. Low Current Efficiency = 20 points (Supports APCD ROI)
       - <67% efficiency: 20 points (ideal for integrated solution)
       - 67-70% efficiency: 15 points
       - 70-73% efficiency: 10 points

    4. Waste Heat Recovery Potential = 15 points (Secondary benefit after dioxin control)
       - VERY HIGH (>25 MW thermal): 15 points
       - HIGH (18-25 MW thermal): 12 points
       - MEDIUM (10-18 MW thermal): 8 points

    5. Plant Size/Throughput = 10 points (Economy of scale for APCD)
       - >600,000 tonnes/year: 10 points
       - 500,000-600,000 tonnes/year: 8 points
       - 300,000-500,000 tonnes/year: 6 points

    6. Regulatory Pressure/Urgency = 15 points (APCD drivers)
       - Enforcement action, compliance deadline <6 months: 15 points
       - EU BAT compliance deadline approaching: 12 points
       - Planned upgrade/retrofit: 10 points
       - Seeking proactive compliance: 5 points

    QUALIFICATION LEVELS (DIOXIN-FOCUSED):
    - 🔥 CRITICAL (40+ points with dioxin issue): IMMEDIATE APCD outreach - compliance & health critical
    - 🔥 HOT (70+ points): IMMEDIATE outreach - major opportunity
    - ⚠️ WARM (50-69 points): Priority outreach - good business case
    - COLD (<50 points): Long-term nurture

    PRIORITY CATEGORIZATION (for Excel export - DIOXIN-FOCUSED):

    📌 PRIORITY 1 - DIOXIN CRITICAL & URGENT (Highest Value & Regulatory Risk)
    - Score: 40+ points with DIOXIN/PCDD/PCDF violation OR 80-100 overall
    - Criteria:
      * DIOXIN VIOLATIONS/approaching I-TEQ/TEQ limits (CRITICAL health & regulatory driver)
      * Memory effect or de novo synthesis issues
      * Recent dioxin violation history + no effective APCD
      * Enforcement action with dioxin focus
    - Action: IMMEDIATE executive outreach within 48 hours (regulatory crisis)
    - APCD Solution: Urgent APCD retrofit + continuous emission monitoring
    - Example: Plant exceeding dioxin limits, health emergency potential, compliance deadline <3 months

    📌 PRIORITY 2 - DIOXIN FOCUSED HIGH VALUE (APCD + Energy ROI)
    - Score: 70+ points with dioxin issues OR 70-79 overall + PCDD/PCDF emissions
    - Criteria:
      * Dioxin at-risk status + High heat recovery potential (integrated APCD+energy solution)
      * Approaching dioxin limits + Planned upgrade (perfect timing)
      * High compliance cost drivers + Energy savings upside
    - Action: Priority outreach within 1-2 weeks
    - APCD Solution: Integrated APCD + waste heat recovery system
    - Example: Large plant with dioxin issues + efficiency opportunity, planned upgrade

    📌 PRIORITY 3 - DIOXIN AT-RISK (Proactive APCD Opportunity)
    - Score: 30-39 with dioxin indicators OR 60-75 with low efficiency + dioxin risk
    - Criteria:
      * At risk of dioxin violations (>80% limit)
      * Aging equipment with dioxin risk + LOW efficiency
      * Future compliance deadline 6-12 months
    - Action: Outreach within 2-3 weeks (proactive positioning)
    - Example: Plant approaching dioxin limits, proactive facility management

    📌 PRIORITY 4 - GENERAL EMISSION + ENERGY OPPORTUNITY
    - Score: 50-69 with non-dioxin emissions OR good energy but any dioxin concern
    - Criteria: Medium value + Medium emission need + Good energy recovery
    - Action: Outreach within 1 month
    - Example: Plant with NOx/PM issues but also heat recovery potential

    📌 PRIORITY 5 - COMPLIANCE MONITORING (Future APCD Need)
    - Score: 30-49 with minor dioxin indicators OR <50 general
    - Criteria: Qualified for future engagement, monitoring for dioxin trends
    - Action: Quarterly compliance check-in, position as thought leader
    - Example: Small plants, currently compliant but in dioxin-emitting sectors

    TASKS:
    1. Query the EEA database for ALL WASTE-TO-ENERGY facilities (waste management sector)
       ** CRITICAL: FILTER FOR DIOXIN/PCDD/PCDF EMISSIONS FIRST **

    2. Identify ALL plants with dioxin/PCDD/PCDF emissions:
       - Municipal waste incineration WITH dioxin data/violations
       - RDF/SRF combustion WITH dioxin risks
       - Biomass waste processing WITH dioxin profile analysis
       - Industrial waste thermal treatment (HIGHEST dioxin risk)
       - Sewage sludge incineration (HIGH dioxin risk)
       - Look for: PCDD, PCDF, Dioxin, I-TEQ, TEQ columns in emissions data
       - Flag: Memory effect history, de novo synthesis indicators, APCD status

    3. Filter for plants with current dioxin issues:
       - Exceeding I-TEQ/TEQ limits
       - Approaching dioxin limits (<90 days warning)
       - Recent violation history (within 24 months)
       - At-risk status (>80% of limit)
       - NO adequate APCD system in place

    4. Score EVERY facility using GMAB DIOXIN-FOCUSED criteria above (no limit - find all)
       - DIOXIN violations = TOP priority (40+ points)
       - Other factors secondary to dioxin control need

    5. DO NOT filter to "top 30" - include ALL qualified leads (score >30 with dioxin concern, >50 without)

    6. Categorize each lead into Priority 1-5 based on dioxin-focused criteria above

    7. Create detailed report with:
       - Facility name, type (MSW/RDF/biomass), country
       - Waste throughput (tonnes/year) and waste type
       - Current energy output (electricity MW, heat MW)
       - Current overall efficiency (%)
       - **DIOXIN/PCDD/PCDF EMISSION DATA** (I-TEQ mg/m³ or ng I-TEQ/Nm³)
       - **DIOXIN COMPLIANCE STATUS** (violations, warnings, at-risk, compliant)
       - Flue gas temperature post-boiler
       - Current emission control systems (APCD status, fabric filters, etc.)
       - Memory effect or de novo synthesis indicators
       - Waste heat potential (MW thermal) - secondary to dioxin control
       - Total score and qualification level
       - Priority categorization (1-5)
       - Specific GMAB APCD solution recommendations:
         * APCD system type for dioxin elimination
         * De novo synthesis prevention temperature targets
         * Memory effect mitigation strategy
         * I-TEQ/TEQ monitoring & compliance assurance
         * Integrated heat recovery + dioxin control system
         * Boiler retrofit for clean combustion support
       - Annual APCD cost potential (€M CAPEX for compliance)
       - Energy recovery value (€M/year) - secondary benefit
       - Payback analysis: APCD ROI + Energy savings
       - Regulatory risk if dioxin not addressed

    8. Export to 'GMAB_Dioxin_Control_Leads.xlsx' (Excel with 6 sheets):
       - Sheet 1: PRIORITY 1 - DIOXIN CRITICAL & URGENT (violations, <3 months compliance deadline)
       - Sheet 2: PRIORITY 2 - DIOXIN HIGH VALUE (APCD+Energy combined ROI)
       - Sheet 3: PRIORITY 3 - DIOXIN AT-RISK (proactive APCD opportunity)
       - Sheet 4: PRIORITY 4 - GENERAL EMISSION + ENERGY
       - Sheet 5: PRIORITY 5 - COMPLIANCE MONITORING
       - Sheet 6: ALL LEADS - DIOXIN FOCUS MASTER LIST

    Data Location: C:\\Users\\staff\\anthropicFun\\EEA_Industrial_Emissions_Data\\converted_csv\\
    Key Files:
    - 2_ProductionFacility.csv (facility info)
    - 4d_EnergyInput.csv (waste input, energy consumption)
    - 4e_EmissionsToAir.csv (combustion data)
    - 2e_ProductionVolume.csv (waste throughput)

    Analyze the database and identify WASTE-TO-ENERGY plants with MAXIMUM efficiency improvement potential!
    """

    print("[HOT] GMAB Waste-to-Energy Plant Optimization Lead Finder")
    print("   Finding WtE plants with efficiency improvement opportunities...\n")

    qualified_leads = []

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            cwd="C:\\Users\\staff\\anthropicFun\\EEA_Industrial_Emissions_Data",
            max_turns=30,
            model="sonnet",
            mcp_servers={
                "leads": mcp_server
            }
        )
    ):
        if message.type == "assistant":
            for content in message.message.content:
                if hasattr(content, 'text') and content.text:
                    print(f"\n{content.text}")
                elif hasattr(content, 'name'):
                    print(f"\n[TOOL] Using tool: {content.name}")

        elif message.type == "result":
            print(f"\n\n[DONE] Analysis Complete!")
            print(f"   Duration: {message.duration_ms/1000:.2f} seconds")
            print(f"   Cost: ${message.total_cost_usd:.4f}")
            print(f"   Turns: {message.num_turns}")


# GMAB Waste-to-Energy Specialized Analysis Functions

async def aging_plants_boiler_replacement():
    """Find WtE plants with CRITICAL boiler replacement needs - URGENT"""
    prompt = """
    Find WASTE-TO-ENERGY plants with aging boilers needing IMMEDIATE replacement for GMAB.

    Focus ONLY on:
    - Boiler age >20 years or end-of-life status
    - Plant efficiency <68% (old technology)
    - Major maintenance issues or reliability problems
    - Replacement/retrofit planned 2025-2026
    - Plant size >400,000 tonnes/year (economic viability)

    For each CRITICAL plant:
    - Exact boiler age and condition assessment
    - Current vs. achievable efficiency with GMAB modern boiler
    - Waste throughput and energy potential
    - GMAB boiler solution sizing and technology
    - Total CAPEX estimate
    - Revenue improvement (€M/year) from efficiency gain
    - Payback period (target: 3-5 years)
    - Environmental benefits (emissions reduction, carbon credits)
    - Financing options (EU funds, municipal bonds)

    Export to 'WTE_BOILER_REPLACEMENT_URGENT.csv' for immediate project pursuit.
    """


async def facility_type_analysis():
    """Analyze waste-to-energy opportunities by facility type"""
    prompt = """
    Segment waste-to-energy leads by facility type for GMAB:

    Facility Types:
    1. Municipal Solid Waste (MSW) Incinerators
       - Typical throughput: 200,000-800,000 tonnes/year
       - Current efficiency range: 60-75%
       - GMAB opportunity: Flue gas condensers, CHP optimization

    2. RDF/SRF (Refuse-Derived Fuel) Plants
       - Higher heating value than MSW
       - Efficiency potential: up to 85%
       - GMAB opportunity: Advanced steam cycles, ORC integration

    3. Biomass/Wood Waste Plants
       - Clean combustion (lower emissions)
       - District heating focus
       - GMAB opportunity: Heat pump integration, efficiency upgrades

    4. Industrial Waste Treatment
       - High-temperature processes
       - Hazardous waste handling
       - GMAB opportunity: Specialized heat recovery, emission control

    5. Sewage Sludge Incineration
       - Integrated with wastewater treatment
       - Lower efficiency (50-65%)
       - GMAB opportunity: Major efficiency improvement potential

    For each type:
    - Total number of facilities in EU
    - Average current efficiency
    - Typical GMAB solution fit
    - Market size (€M opportunity)
    - Top 10 facilities per type
    - Success stories and reference accounts

    Recommend which facility type to prioritize for WtE campaign.
    """


async def geographic_wte_market_priority():
    """Prioritize EU countries by waste-to-energy market opportunity"""
    prompt = """
    Rank European countries by GMAB waste-to-energy market opportunity:

    Analyze (WtE-specific focus):
    - Germany (100+ WtE plants, high environmental standards)
    - Netherlands (MSW leaders, district heating integration)
    - Sweden (Advanced CHP systems, carbon neutral goals)
    - Italy (Growing WtE sector, aging infrastructure)
    - Poland (New WtE construction, EU funding available)
    - France (Modernization wave, efficiency targets)
    - Denmark (District heating champions, high energy prices)
    - Spain (MSW treatment expansion, EU compliance)

    For each country:
    - Number of waste-to-energy plants (MSW, RDF, biomass)
    - Total waste treatment capacity (tonnes/year)
    - Average plant age (older = more GMAB opportunities)
    - National waste management strategy (landfill bans, circular economy)
    - Energy prices (electricity, district heating) - higher = better ROI
    - Government subsidies for WtE efficiency improvements
    - Renewable energy targets (WtE as renewable)
    - Market maturity and competition level
    - Estimated WtE optimization market size (€M)

    Export top 30 WtE facilities per country with:
    - Localized business case
    - National incentives mapping
    - Reference accounts in that country
    - Cultural considerations for sales approach
    """


if __name__ == "__main__":
    print("=" * 80)
    print("   GMAB DIOXIN CONTROL & Waste-to-Energy Optimization Lead Generation Agent")
    print("   PRIMARY TARGET: DIOXIN/PCDD/PCDF ELIMINATION with APCD Technology")
    print("   SECONDARY: Energy Efficiency & Heat Recovery Integration")
    print("   'TOGETHER WE SUCCEED, TOGETHER WE GO GREEN'")
    print("=" * 80)
    print()
    print("   DIOXIN FOCUS: WtE Plants with PCDD/PCDF Violations or At-Risk Status")
    print("   APCD Solutions: Activated Carbon Injection, Fabric Filters, Temperature Control")
    print("   Memory Effect & De Novo Synthesis Prevention")
    print("   I-TEQ/TEQ Toxicity Equivalent Compliance & Monitoring")
    print()
    print("   Facility Types: MSW Incinerators, RDF Plants, Sewage Sludge, Industrial Waste")
    print("   Geographic Focus: Germany, Netherlands, Italy, Poland, Sweden, France")
    print()
    print("   Data Source: EEA Industrial Emissions Database (PCDD/PCDF Emissions Data)")
    print("   Location: C:\\Users\\staff\\anthropicFun\\EEA_Industrial_Emissions_Data\\converted_csv\\")
    print()
    print("=" * 80)

    # Run the main lead finding function
    asyncio.run(find_qualified_leads())

    # Or run specialized analyses:
    # asyncio.run(aging_plants_boiler_replacement())    # URGENT: Boiler end-of-life plants
    # asyncio.run(facility_type_analysis())             # Segment by WtE facility type
    # asyncio.run(geographic_wte_market_priority())     # Prioritize EU countries for WtE
