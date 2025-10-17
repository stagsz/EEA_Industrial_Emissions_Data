# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **three-agent AI system** for GMAB (www.SPIG-GMAB.com) that automates lead generation, evaluation, and proposal creation for waste-to-energy (WtE) plant optimization projects. The system analyzes the European Environment Agency's industrial emissions database (~34,000 facilities) to find waste-to-energy plants needing efficiency improvements and compliance solutions.

### Three-Agent Architecture

1. **Lead Generation Agent** (`lead_generation_agent.py`)
   - Scans EEA database for WtE plants (MSW incinerators, RDF, biomass, sewage sludge)
   - Scores leads 0-100 based on: emission violations (25pts), low efficiency (25pts), waste heat potential (20pts), plant size (15pts), urgency (15pts)
   - Outputs ALL leads to Excel with 6 sheets: Priority 1-5 + Master List
   - Priority 1 = Critical (emission violations, urgent upgrades), Priority 5 = Long-term nurture

2. **Lead Evaluation Agent** (`lead_evaluation_agent.py`)
   - Deep analysis of Priority 1-2 leads from lead generation
   - Tools: technical_feasibility_analysis, detailed_roi_calculation, competitive_analysis, sales_action_plan
   - Outputs qualified leads with complete business cases

3. **Proposal Generation Agent** (`proposal_generation_agent.py`)
   - Automatically generates complete proposal packages for qualified leads
   - Tools: generate_executive_proposal, build_financial_model, create_stakeholder_presentations, enrich_lead_data, generate_compliance_documentation
   - Creates folder per lead with 6-7 documents (PDF proposal, Excel model, PowerPoint decks, compliance reports)

## Running the Agents

### Sequential Workflow (Recommended)

```bash
# Step 1: Generate all leads with priority ranking
python lead_generation_agent.py
# Output: GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx (6 sheets)

# Step 2: Evaluate Priority 1-2 leads
python lead_evaluation_agent.py
# Output: GMAB_Evaluated_Leads_YYYYMMDD.xlsx

# Step 3: Generate proposal packages for top qualified leads
python proposal_generation_agent.py
# Output: C:\GMAB_Proposals\[Facility_Name]\ (complete package per lead)
```

### Specialized Analysis Functions

Each agent has alternative analysis modes (see bottom of each file):

**Lead Generation:**
- `asyncio.run(aging_plants_boiler_replacement())` - Target plants needing immediate boiler replacement
- `asyncio.run(facility_type_analysis())` - Segment by WtE technology type (MSW, RDF, biomass)
- `asyncio.run(geographic_wte_market_priority())` - Country-by-country market analysis

**Lead Evaluation:**
- `asyncio.run(quick_screening())` - Filter out low-probability leads (saves time)
- `asyncio.run(deep_dive_top_10())` - Ultra-detailed analysis for best 10 leads
- `asyncio.run(market_intelligence_report())` - Strategic market insights from all leads

**Proposal Generation:**
- `asyncio.run(generate_urgent_only())` - Only create packages for emission violation leads
- `asyncio.run(update_existing_proposals())` - Refresh proposals with new data

## Data Architecture

### Input Data Flow
```
EEA Database (Access DB)
  ↓ convert_access_db.py
SQLite DB (converted_database.db)
  ↓ (also exported to)
CSV Files (converted_csv/)
  ↓ lead_generation_agent.py (reads CSVs)
Prioritized Excel Leads
  ↓ lead_evaluation_agent.py
Qualified Leads
  ↓ proposal_generation_agent.py
Complete Proposal Packages
```

### Key Data Files

- `1215_Public_Product_Full Access_v8.accdb` - Original EEA Access database (1.2GB)
- `converted_database.db` - Converted SQLite database (771MB)
- `converted_csv/` - 30+ CSV tables exported from database
- Critical CSVs for agents:
  - `2_ProductionFacility.csv` - Facility names, locations, sectors
  - `2f_PollutantRelease.csv` - Emission levels by pollutant/year
  - `3_ProductionInstallation.csv` - Equipment and process details
  - `3d_BATConclusions.csv` - Best Available Techniques compliance

## Agent Technology Stack

### Claude Agent SDK
All agents use the Python Claude Agent SDK:

```python
from claude_agent_sdk import query, tool, create_sdk_mcp_server, ClaudeAgentOptions

# Tools are defined with @tool decorator
@tool(
    name="tool_name",
    description="What this tool does",
    input_schema={"param": {"type": "object", "description": "..."}}
)
async def tool_name(args, extra):
    # Tool implementation
    return {"content": [{"type": "text", "text": json.dumps(result)}]}

# MCP server bundles tools
mcp_server = create_sdk_mcp_server(
    name="server-name",
    version="1.0.0",
    tools=[tool1, tool2, tool3]
)

# Query agent with prompt and tools
async for message in query(
    prompt="Your detailed agent instructions...",
    options=ClaudeAgentOptions(
        cwd="C:\\Users\\staff\\anthropicFun\\EEA_Industrial_Emissions_Data",
        max_turns=40,
        model="sonnet",
        mcp_servers={"server-name": mcp_server}
    )
):
    # Process agent responses
```

### Key Dependencies
```bash
pip install claude-agent-sdk  # Core agent framework
pip install pandas openpyxl   # Data processing and Excel export
pip install python-docx python-pptx  # Document generation (for proposals)
pip install beautifulsoup4 selenium  # Web scraping (for lead enrichment)
```

## Critical Scoring Logic

### Lead Prioritization (0-100 points)

The lead generation agent uses weighted scoring:

1. **EMISSION COMPLIANCE PROBLEMS (25 points)** - Highest priority
   - 25 pts: Exceeding limits, enforcement action, critical violations
   - 20 pts: Approaching limits, compliance deadline <90 days
   - 10 pts: Historical compliance issues
   - 0 pts: Full compliance

2. **Low Current Efficiency (25 points)**
   - 25 pts: <20% efficiency (critical waste of energy)
   - 20 pts: 20-25% efficiency (well below BAT)
   - 15 pts: 25-28% efficiency (below industry average)
   - 10 pts: 28-30% efficiency (marginal)

3. **Waste Heat Recovery Potential (20 points)**
   - Based on thermal energy that could be recovered

4. **Large Waste Throughput (15 points)**
   - Larger plants = larger ROI opportunities

5. **Urgency/Timing Factors (15 points)**
   - Boiler replacement planned, major maintenance, regulatory deadlines

**Priority Thresholds:**
- Priority 1 (Critical): 80-100 points OR emission violations - Immediate action required
- Priority 2 (High Value): 65-79 points - Active pursuit, Q1-Q2 close
- Priority 3 (High Need): 50-64 points - Qualified pipeline, Q3-Q4 close
- Priority 4 (Good): 35-49 points - Nurture, close in 12 months
- Priority 5 (Long-term): <35 points - Long-term relationship building

## Mock Data vs Real Data

**Current state:** All agents use mock data for demonstration.

**To switch to real EEA data:**

1. Ensure EEA database is converted: `python convert_access_db.py`
2. In each agent file, locate the mock tool functions (e.g., `query_eea_database`)
3. Replace mock implementations with actual CSV/database queries:

```python
# MOCK (current):
mock_facilities = [
    {"facility": "Amsterdam AEB", "efficiency": 22, ...},
    # ...
]

# REAL (replace with):
import pandas as pd
facilities_df = pd.read_csv('converted_csv/2_ProductionFacility.csv')
emissions_df = pd.read_csv('converted_csv/2f_PollutantRelease.csv')
# Then filter and score based on actual data
```

## Output File Naming Convention

All agents use timestamped outputs to avoid overwriting:

- Lead Generation: `GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx`
- Lead Evaluation: `GMAB_Evaluated_Leads_YYYYMMDD.xlsx`
- Proposals: `C:\GMAB_Proposals\[FacilityName]\` folder structure

Excel files always have consistent sheet structure:
- Lead Gen: 6 sheets (Priority 1, Priority 2, Priority 3, Priority 4, Priority 5, ALL LEADS)
- Lead Eval: 3 sheets (PRIORITY LIST, DETAILED ANALYSIS, SALES ACTIONS)

## Important Context for Modifications

### When customizing Lead Generation Agent:

- **Target market:** Specifically waste-to-energy plants (MSW incinerators, RDF facilities, biomass plants, sewage sludge incineration, industrial waste energy recovery)
- **DO NOT target:** General industrial facilities, steel plants, cement plants unless they have WtE components
- **Emission compliance is critical:** Always prioritize facilities with emission violations (regulatory driver for sales)
- **Output ALL leads:** Do not limit to "top 30" or similar - sales team wants complete funnel with priorities

### When customizing Evaluation Agent:

- **Focus on Priority 1-2 only:** These are the actionable leads
- **ROI calculations must include:** CAPEX, annual savings (energy + carbon credits), OPEX, payback, NPV, IRR
- **Competitive analysis is key:** GMAB's advantage is specialized WtE experience (50+ installations) and advanced ORC technology
- **Sales action plans need:** Target contacts (Energy Manager, Plant Director, CFO), engagement sequence, objection handling

### When customizing Proposal Agent:

- **Document generation is currently mock:** Actual implementation needs python-docx, openpyxl, python-pptx libraries
- **Each proposal package must be customized:** No generic templates - use facility-specific data
- **Compliance documentation is critical:** EU Industrial Emissions Directive, BAT requirements, emission reduction projections
- **Financial models need interactivity:** Excel with sensitivity analysis, scenario planning

## Troubleshooting

### "No leads found" from Lead Generation
- Check that converted CSV files exist in `converted_csv/`
- Verify mock data is populated (if CSVs missing, agent uses mock)
- Lower scoring thresholds if needed (currently requires 35+ for Priority 5)

### "File not found" errors
- All agents assume working directory: `C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data`
- Update paths in ClaudeAgentOptions if running from different location
- Ensure relative paths use forward slashes or escaped backslashes

### Agent hangs or times out
- Increase `max_turns` in ClaudeAgentOptions (currently 40)
- Use specialized functions instead of main functions (e.g., quick_screening instead of full evaluation)
- Process in smaller batches (e.g., only Priority 1 leads)

### Excel files have encoding issues
- All Excel exports use openpyxl with UTF-8 encoding
- If special characters display incorrectly, check system locale settings

## Related Documentation

- `AGENT_WORKFLOW_GUIDE.md` - Comprehensive workflow guide for all three agents
- `lead_prompting_guide.md` - Templates for customizing agent prompts
- `Industrial_Emissions_Data_Guide.md` - Deep dive into EEA database structure
- `README.md` - Quick start for EEA data analysis
- `QUICK_SUMMARY.md` - Overview of EEA database and capabilities
