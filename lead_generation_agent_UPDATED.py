#!/usr/bin/env python3
"""
GMAB Lead Generation Agent - UPDATED WITH EU COMPLIANCE INTEGRATION
Replaces mock data with real EEA database + emission compliance checking

Changes from original:
1. Imports emission_compliance_checker module
2. query_database() now uses REAL CSV data instead of mock
3. score_lead() integrates EU compliance violations from restrictions.md
4. Detailed compliance reasons in scoring output
"""

import asyncio
import os
import sys
import json
import pandas as pd
from datetime import datetime
from claude_agent_sdk import query, tool, create_sdk_mcp_server, ClaudeAgentOptions

# IMPORT EU COMPLIANCE CHECKER
from emission_compliance_checker import EmissionComplianceChecker, ComplianceStatus, RegulatoryUrgency

# Initialize compliance checker
compliance_checker = EmissionComplianceChecker()

# Agent prompt (same as original, but now with real compliance data)
AGENT_PROMPT = """
You are a lead generation AI agent for GMAB (www.SPIG-GMAB.com), specializing in waste-to-energy plant optimization.

Company: GMAB - Global leader in industrial waste-to-energy efficiency solutions
Tagline: "TOGETHER WE SUCCEED, TOGETHER WE GO GREEN"
Focus: Maximize energy recovery while meeting strict emission standards

YOUR MISSION:
Generate qualified B2B leads for waste-to-energy plant optimization projects by analyzing:
- EU Industrial Emissions Database (34,000+ facilities)
- Emission compliance violations (NOW CHECKING AGAINST EU STANDARDS from restrictions.md)
- Energy efficiency improvement opportunities
- Waste heat recovery potential

TARGET CUSTOMERS:
1. Municipal Solid Waste (MSW) incinerators
2. Refuse-Derived Fuel (RDF) facilities
3. Biomass energy plants
4. Sewage sludge incineration
5. Industrial waste energy recovery facilities

LEAD SCORING CRITERIA (0-100 points):
1. **EMISSION COMPLIANCE PROBLEMS (0-50 points)** - HIGHEST PRIORITY
   - 50 pts: CRITICAL VIOLATION - Exceeding EU limits, enforcement action, facility shutdown risk
   - 40 pts: IMMINENT VIOLATION - <90 days to compliance deadline
   - 30 pts: AT RISK - Within 20% of BAT-AEL limits
   - 20 pts: Approaching limits, compliance improvement plan required
   - 0 pts: Fully compliant

2. **Low Current Efficiency (0-25 points)**
   - 25 pts: <20% efficiency (critical waste of energy)
   - 20 pts: 20-25% efficiency (well below BAT)
   - 15 pts: 25-28% efficiency (below industry average)
   - 10 pts: 28-30% efficiency (marginal)

3. **Waste Heat Recovery Potential (0-15 points)**
   - Based on flue gas temperature, facility size, thermal energy wasted

4. **Large Waste Throughput (0-10 points)**
   - Larger plants = larger ROI opportunities
   - 10 pts: >500,000 tonnes/year
   - 5 pts: 200,000-500,000 tonnes/year

OUTPUT ALL LEADS to Excel with priority tiers:
- Priority 1 (CRITICAL): 80-100 points - Immediate action (emission violations, urgent compliance)
- Priority 2 (HIGH VALUE): 65-79 points - Active pursuit
- Priority 3 (QUALIFIED): 50-64 points - Qualified pipeline
- Priority 4 (NURTURE): 35-49 points - Long-term relationship
- Priority 5 (MONITOR): <35 points - Monitor for future opportunities

TOOLS AVAILABLE:
1. query_database - Query EEA database (NOW USES REAL DATA WITH COMPLIANCE CHECKS)
2. score_lead - Score leads (INTEGRATES EU EMISSION STANDARDS)
3. export_leads - Export to Excel

YOUR PROCESS:
1. Query database for waste-to-energy facilities
2. For each facility, check EU emission compliance (Euro 7, BAT-AEL, IED standards)
3. Score based on compliance violations + efficiency + size
4. Export ALL leads to Excel with detailed compliance context

Begin lead generation now.
"""

# TOOL 1: Query Database (UPDATED WITH REAL DATA)
@tool(
    name="query_database",
    description="Query the EEA Industrial Emissions Database with REAL DATA + EU compliance checking",
    input_schema={
        "query_type": {
            "type": "string",
            "enum": ["waste_incineration", "all_facilities", "country_filter"],
            "description": "Type of facilities to query"
        },
        "filters": {
            "type": "object",
            "description": "Optional filters (country, min_energy, etc.)"
        }
    }
)
async def query_database(args, extra):
    """
    Query EEA Database for waste-to-energy facilities
    NOW USING REAL CSV DATA + EU COMPLIANCE CHECKING
    """
    query_type = args.get("query_type", "waste_incineration")
    filters = args.get("filters", {})

    # Load REAL EEA data
    print("📂 Loading EEA Industrial Emissions Data...")
    facilities_df = pd.read_csv('converted_csv/2_ProductionFacility.csv', low_memory=False)
    energy_df = pd.read_csv('converted_csv/4d_EnergyInput.csv', low_memory=False)
    emissions_df = pd.read_csv('converted_csv/4e_EmissionsToAir.csv', low_memory=False)
    pollutant_releases_df = pd.read_csv('converted_csv/2f_PollutantRelease.csv', low_memory=False)
    installations_df = pd.read_csv('converted_csv/3_ProductionInstallation.csv', low_memory=False)

    # Filter for waste incineration facilities
    if query_type == "waste_incineration":
        facilities = facilities_df[
            facilities_df['mainActivityName'].str.contains('incineration', case=False, na=False)
        ]
    else:
        facilities = facilities_df

    # Apply country filter if specified
    if filters.get('country'):
        facilities = facilities[facilities['countryCode'] == filters['country']]

    # Get latest year
    latest_year = energy_df['reportingYear'].max()

    # Merge with installations
    merged = facilities.merge(
        installations_df,
        left_on='Facility_INSPIRE_ID',
        right_on='Parent_Facility_INSPIRE_ID',
        how='left'
    )

    # Merge with energy data
    merged = merged.merge(
        energy_df[energy_df['reportingYear'] == latest_year],
        left_on='Installation_INSPIRE_ID',
        right_on='Installation_Part_INSPIRE_ID',
        how='left'
    )

    # Limit to first 50 facilities for performance
    merged = merged.head(50)

    # Process each facility with COMPLIANCE CHECKING
    results = []
    print(f"🔍 Checking {len(merged)} facilities against EU emission standards...")

    for idx, row in merged.iterrows():
        facility_id = row.get('Facility_INSPIRE_ID')

        # Get pollutant data for this facility
        facility_pollutants = pollutant_releases_df[
            pollutant_releases_df['Parent_Facility_INSPIRE_ID'] == facility_id
        ]

        # Prepare facility data
        facility_data = {
            'nameOfFeature': row.get('nameOfFeature', 'Unknown'),
            'countryCode': row.get('countryCode', 'EU'),
            'mainActivityName': row.get('mainActivityName', ''),
            'energyInputTJ': row.get('energyInputTJ', 0)
        }

        # CHECK EU COMPLIANCE
        compliance_status = "UNKNOWN"
        compliance_score = 0
        compliance_detail = "No emission data available"

        if not facility_pollutants.empty:
            try:
                status, violations, comp_score, detailed_reason = compliance_checker.check_facility_compliance(
                    facility_data,
                    facility_pollutants
                )
                compliance_status = status.value
                compliance_score = comp_score
                compliance_detail = detailed_reason
            except Exception as e:
                compliance_detail = f"Compliance check error: {str(e)}"

        # Build result
        result = {
            "facility": row.get('nameOfFeature', 'Unknown'),
            "facility_type": row.get('mainActivityName', 'Unknown'),
            "country": row.get('countryCode', 'EU'),
            "city": row.get('city', 'Unknown'),
            "parent_company": row.get('parentCompanyName', 'Unknown'),
            "energy_input_TJ": row.get('energyInputTJ', 0),
            "compliance_status": compliance_status,
            "compliance_score": compliance_score,
            "compliance_detail": compliance_detail,
            "facility_id": facility_id
        }

        results.append(result)

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "total_facilities": len(results),
                "facilities": results,
                "data_source": "EEA Industrial Emissions Database (REAL DATA)",
                "compliance_check": "EU standards from restrictions.md (Euro 7, BAT-AEL, IED)"
            }, indent=2)
        }]
    }


# TOOL 2: Score Lead (UPDATED WITH COMPLIANCE INTEGRATION)
@tool(
    name="score_lead",
    description="Score a lead based on EU compliance violations + efficiency + size",
    input_schema={
        "lead_data": {
            "type": "object",
            "description": "Lead data including compliance info"
        }
    }
)
async def score_lead(args, extra):
    """
    Score lead with COMPLIANCE-FIRST approach
    """
    lead = args.get("lead_data", {})

    # COMPLIANCE SCORE (0-50 points) - HIGHEST PRIORITY
    compliance_score = lead.get("compliance_score", 0)

    # Cap compliance contribution at 50 points
    compliance_points = min(compliance_score // 2, 50)

    # EFFICIENCY SCORE (0-25 points)
    efficiency = lead.get("current_efficiency_percent", 30)
    if efficiency < 20:
        efficiency_points = 25
    elif efficiency < 25:
        efficiency_points = 20
    elif efficiency < 28:
        efficiency_points = 15
    elif efficiency < 30:
        efficiency_points = 10
    else:
        efficiency_points = 5

    # SIZE SCORE (0-15 points)
    energy_input = lead.get("energy_input_TJ", 0)
    if energy_input > 5000:
        size_points = 15
    elif energy_input > 2000:
        size_points = 10
    elif energy_input > 1000:
        size_points = 5
    else:
        size_points = 0

    # URGENCY BONUS (0-10 points)
    urgency = lead.get("urgency", "").upper()
    if "CRITICAL" in urgency or "IMMEDIATE" in urgency:
        urgency_points = 10
    elif "HIGH" in urgency:
        urgency_points = 7
    elif "MEDIUM" in urgency:
        urgency_points = 5
    else:
        urgency_points = 0

    # TOTAL SCORE
    total_score = compliance_points + efficiency_points + size_points + urgency_points

    # DETERMINE PRIORITY
    if total_score >= 80:
        priority = 1
        priority_label = "CRITICAL"
        action = "IMMEDIATE - Contact within 24 hours, technical assessment within 48 hours"
    elif total_score >= 65:
        priority = 2
        priority_label = "HIGH VALUE"
        action = "Contact within 3 days, proposal within 2 weeks"
    elif total_score >= 50:
        priority = 3
        priority_label = "QUALIFIED"
        action = "Contact within 2 weeks, nurture for Q3-Q4 close"
    elif total_score >= 35:
        priority = 4
        priority_label = "NURTURE"
        action = "Add to nurture campaign, contact within 30 days"
    else:
        priority = 5
        priority_label = "MONITOR"
        action = "Monitor for future opportunities, quarterly check-in"

    # BUILD DETAILED SCORING REASON
    compliance_detail = lead.get("compliance_detail", "No compliance data")

    scoring_breakdown = f"""
LEAD SCORE: {total_score}/100 | PRIORITY {priority}: {priority_label}

SCORING BREAKDOWN:
  • EU Compliance Violations: {compliance_points}/50 points
  • Energy Efficiency Gap: {efficiency_points}/25 points
  • Facility Size/Revenue Potential: {size_points}/15 points
  • Regulatory Urgency: {urgency_points}/10 points

EU COMPLIANCE ANALYSIS:
{compliance_detail}

RECOMMENDED SALES ACTION:
{action}

GMAB VALUE PROPOSITION:
  • 50+ waste-to-energy installations worldwide
  • Proven emission control solutions (NOx, SO₂, particulates)
  • Advanced heat recovery systems (ORC turbines)
  • Typical ROI: 2-4 years
  • Compliance guarantee: Meet all EU BAT-AEL standards
"""

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "facility": lead.get("facility"),
                "total_score": total_score,
                "priority": priority,
                "priority_label": priority_label,
                "scoring_breakdown": {
                    "compliance": compliance_points,
                    "efficiency": efficiency_points,
                    "size": size_points,
                    "urgency": urgency_points
                },
                "detailed_reason": scoring_breakdown,
                "sales_action": action
            }, indent=2)
        }]
    }


# TOOL 3: Export Leads (same as original, but with compliance context)
@tool(
    name="export_leads",
    description="Export qualified leads to Excel file with compliance-based priority sheets",
    input_schema={
        "leads": {
            "type": "array",
            "description": "Array of scored lead objects"
        },
        "filename": {
            "type": "string",
            "description": "Output filename"
        }
    }
)
async def export_leads(args, extra):
    """Export leads to Excel with compliance prioritization"""
    leads = args.get("leads", [])
    filename = args.get("filename", f"GMAB_WtE_Leads_EU_Compliance_{datetime.now().strftime('%Y%m%d')}.xlsx")

    if not leads:
        return {"content": [{"type": "text", "text": "No leads to export"}]}

    # Convert to DataFrame
    df = pd.DataFrame(leads)

    # Create Excel with priority sheets
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Priority 1: CRITICAL (80-100)
        priority1 = df[df['total_score'] >= 80]
        if len(priority1) > 0:
            priority1.to_excel(writer, sheet_name='Priority 1 CRITICAL', index=False)

        # Priority 2: HIGH VALUE (65-79)
        priority2 = df[(df['total_score'] >= 65) & (df['total_score'] < 80)]
        if len(priority2) > 0:
            priority2.to_excel(writer, sheet_name='Priority 2 HIGH VALUE', index=False)

        # Priority 3: QUALIFIED (50-64)
        priority3 = df[(df['total_score'] >= 50) & (df['total_score'] < 65)]
        if len(priority3) > 0:
            priority3.to_excel(writer, sheet_name='Priority 3 QUALIFIED', index=False)

        # Priority 4: NURTURE (35-49)
        priority4 = df[(df['total_score'] >= 35) & (df['total_score'] < 50)]
        if len(priority4) > 0:
            priority4.to_excel(writer, sheet_name='Priority 4 NURTURE', index=False)

        # Priority 5: MONITOR (<35)
        priority5 = df[df['total_score'] < 35]
        if len(priority5) > 0:
            priority5.to_excel(writer, sheet_name='Priority 5 MONITOR', index=False)

        # ALL LEADS
        df.to_excel(writer, sheet_name='ALL LEADS', index=False)

    summary = f"""
✅ Exported {len(leads)} leads to: {filename}

PRIORITY BREAKDOWN:
  • Priority 1 (CRITICAL): {len(df[df['total_score'] >= 80])} leads
  • Priority 2 (HIGH VALUE): {len(df[(df['total_score'] >= 65) & (df['total_score'] < 80)])} leads
  • Priority 3 (QUALIFIED): {len(df[(df['total_score'] >= 50) & (df['total_score'] < 65)])} leads
  • Priority 4 (NURTURE): {len(df[(df['total_score'] >= 35) & (df['total_score'] < 50)])} leads
  • Priority 5 (MONITOR): {len(df[df['total_score'] < 35])} leads

🚨 Leads prioritized by EU EMISSION COMPLIANCE VIOLATIONS (restrictions.md)
"""

    return {"content": [{"type": "text", "text": summary}]}


# Create MCP server with tools
mcp_server = create_sdk_mcp_server(
    name="gmab-lead-generation-compliance",
    version="2.0.0",
    tools=[query_database, score_lead, export_leads]
)


# Main agent execution
async def run_lead_generation():
    """Run the lead generation agent with EU compliance integration"""
    print("=" * 80)
    print("   GMAB WASTE-TO-ENERGY LEAD GENERATION AGENT")
    print("   NOW WITH EU EMISSION COMPLIANCE CHECKING")
    print("   Based on restrictions.md: Euro 7, BAT-AEL, IED Standards")
    print("=" * 80)

    async for message in query(
        prompt=AGENT_PROMPT,
        options=ClaudeAgentOptions(
            cwd=os.getcwd(),
            max_turns=40,
            model="sonnet",
            mcp_servers={"gmab-lead-gen": mcp_server}
        )
    ):
        # Print agent messages
        if hasattr(message, 'content'):
            for content in message.content:
                if hasattr(content, 'text'):
                    print(content.text)
                elif hasattr(content, 'tool_use'):
                    print(f"\n🔧 Using tool: {content.tool_use.name}")

    print("\n" + "=" * 80)
    print("✅ Lead generation complete!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(run_lead_generation())
