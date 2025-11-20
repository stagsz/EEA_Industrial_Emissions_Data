# CLAUDE.md - Project Guide

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **three-agent AI system** for GMAB (www.SPIG-GMAB.com) that automates lead generation, evaluation, and proposal creation for waste-to-energy (WtE) plant optimization projects. The system analyzes the European Environment Agency's industrial emissions database (~34,000 facilities) to find waste-to-energy plants needing efficiency improvements and compliance solutions.

**Last Updated:** November 19, 2025

### Three-Agent Architecture

1. **Lead Generation Agent** (`agents/lead_generation_agent.py`)
   - Scans EEA database for WtE plants (MSW incinerators, RDF, biomass, sewage sludge)
   - Scores leads 0-100 based on: emission violations (25pts), low efficiency (25pts), waste heat potential (20pts), plant size (15pts), urgency (15pts)
   - Outputs ALL leads to Excel with 6 sheets: Priority 1-5 + Master List
   - Priority 1 = Critical (emission violations, urgent upgrades), Priority 5 = Long-term nurture

2. **Lead Evaluation Agent** (`agents/lead_evaluation_agent.py`)
   - Deep analysis of Priority 1-2 leads from lead generation
   - Tools: technical_feasibility_analysis, detailed_roi_calculation, competitive_analysis, sales_action_plan
   - Outputs qualified leads with complete business cases

3. **Proposal Generation Agent** (`agents/proposal_generation_agent.py`)
   - Automatically generates complete proposal packages for qualified leads
   - Tools: generate_executive_proposal, build_financial_model, create_stakeholder_presentations, enrich_lead_data, generate_compliance_documentation
   - Creates folder per lead with 6-7 documents (PDF proposal, Excel model, PowerPoint decks, compliance reports)

## Directory Structure

```
EEA_Industrial_Emissions_Data/
 agents/                          # Agent implementations
    lead_generation_agent.py
    lead_evaluation_agent.py
    proposal_generation_agent.py
    run_agents_demo.py
 scripts/                         # Utility scripts and data processors
    analyze_data_structure.py
    eea_emissions_analyzer.py
    industrial_emissions_lead_finder.py
    waste_to_energy_lead_finder.py
    ... (data processing utilities)
 data/                            # All data files
    raw/                        # Source data (original EEA database)
       1215_Public_Product_Full Access_v8.accdb    # Original EEA Access DB (1.2GB)
       downloaded_data/        # Downloaded EEA datasets
    processed/                  # Converted/cleaned data
       converted_database.db   # SQLite version (771MB)
       converted_csv/          # 30+ CSV tables from EEA database
           2_ProductionFacility.csv       # Facility names, locations, sectors
           2f_PollutantRelease.csv        # Emission levels by pollutant/year
           3_ProductionInstallation.csv   # Equipment and process details
           ... (25+ other CSV files)
    market/                     # Market analysis and reference data
        Active Plants Global WtE market 2024-2033.csv
        Market outlook Global WtE market 2024-2033.csv
        Projects Global WtE market 2024-2033.csv
        ... (PDF, analysis documents)
 docs/                            # Documentation (all updated November 2025)
    guides/                     # Quick start and overview
       README.md               # Quick start guide
       CLAUDE.md              # This file - project guidance
       QUICK_SUMMARY.md       # Database overview and capabilities
    agents/                     # Agent-specific documentation
       AGENT_WORKFLOW_GUIDE.md # Step-by-step workflow for all agents
       lead_prompting_guide.md # Templates for agent customization
    data_structure/             # Database and data documentation
       Industrial_Emissions_Data_Guide.md  # Deep dive into EEA structure
       DATA_INSIGHTS_ANALYSIS.md          # Data insights and patterns
    market_analysis/            # Market intelligence documentation
       WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md      # Current market analysis
       WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md # 2024-2025 market trends
    technical_reference/        # Technical reference and deep dives
       DIOXIN_APCD_REFERENCE_GUIDE.md   # Dioxin and APCD analysis
       DIOXIN_CHANGES_SUMMARY.md        # Dioxin regulatory changes
       EXTERNAL_DATA_CORRELATION_STRATEGY.md
    GIT_WORKTREES_GUIDE.md     # Git workflow guidance
    restrictions.md             # Data usage restrictions
    TASK_COMPLETION_SUMMARY.md # Completed implementation tasks
    IMPLEMENTATION_COMPLETE.md  # Implementation status
 outputs/                         # Generated proposal packages and outputs
 .git/                           # Version control with worktrees
 .venv/ & venv/                  # Python virtual environments
 .gitignore, .claude/            # Configuration files
```

## Running the Agents

### Sequential Workflow (Recommended)

```bash
# Step 1: Generate all leads with priority ranking
cd C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data
python agents/lead_generation_agent.py
# Output: outputs/GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx (6 sheets)

# Step 2: Evaluate Priority 1-2 leads
python agents/lead_evaluation_agent.py
# Output: outputs/GMAB_Evaluated_Leads_YYYYMMDD.xlsx

# Step 3: Generate proposal packages for top qualified leads
python agents/proposal_generation_agent.py
# Output: outputs/GMAB_Proposals/[Facility_Name]/ (complete package per lead)
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
EEA Database (data/raw/1215_Public_Product_Full Access_v8.accdb)
  ↓
SQLite DB (data/processed/converted_database.db)
  ↓ (exported to)
CSV Files (data/processed/converted_csv/)
  ↓ lead_generation_agent.py (reads CSVs)
Prioritized Excel Leads (outputs/)
  ↓ lead_evaluation_agent.py
Qualified Leads (outputs/)
  ↓ proposal_generation_agent.py
Complete Proposal Packages (outputs/GMAB_Proposals/)
```

### Critical Data Files for Agents

In `data/processed/converted_csv/`:
- `2_ProductionFacility.csv` - Facility names, locations, sectors
- `2f_PollutantRelease.csv` - Emission levels by pollutant/year
- `3_ProductionInstallation.csv` - Equipment and process details
- `3d_BATConclusions.csv` - Best Available Techniques compliance status
- `2e_ProductionVolume.csv` - Waste input volumes
- `4e_EmissionsToAir.csv` - Detailed air emissions
- `3c_PermitDetails.csv` - Permit and regulatory information

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

## Current Implementation Status

 **Completed (November 2025)**
- Three-agent architecture fully implemented with Claude Agent SDK
- Lead generation with comprehensive WtE plant detection
- Lead evaluation with ROI analysis and competitive positioning
- Proposal generation framework for automated document creation
- Complete EEA database conversion (Access → SQLite → CSV)
- 2024-2025 market analysis integration
- Regulatory compliance documentation (dioxin, APCD, BAT guidelines)
- Documentation reorganization and updates

 **Current State: Mock Data**
- All agents currently use mock data for demonstration
- See "Mock Data vs Real Data" section below for switching to live EEA data

### Mock Data vs Real Data

**Current state:** All agents use mock data for demonstration.

**To switch to real EEA data:**

1. Ensure EEA database is converted: Run a data conversion script if needed
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
facilities_df = pd.read_csv('data/processed/converted_csv/2_ProductionFacility.csv')
emissions_df = pd.read_csv('data/processed/converted_csv/2f_PollutantRelease.csv')
# Then filter and score based on actual data
```

## Output File Naming Convention

All agents use timestamped outputs to avoid overwriting:

- Lead Generation: `outputs/GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx`
- Lead Evaluation: `outputs/GMAB_Evaluated_Leads_YYYYMMDD.xlsx`
- Proposals: `outputs/GMAB_Proposals/[FacilityName]/` folder structure

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
- Check that CSV files exist in `data/processed/converted_csv/`
- Verify mock data is populated (if CSVs missing, agent uses mock)
- Lower scoring thresholds if needed (currently requires 35+ for Priority 5)

### "File not found" errors
- All agents assume working directory: `C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data`
- Update paths in ClaudeAgentOptions if running from different location
- Verify all paths use correct directory structure (data/, agents/, etc.)

### Agent hangs or times out
- Increase `max_turns` in ClaudeAgentOptions (currently 40)
- Use specialized functions instead of main functions (e.g., quick_screening instead of full evaluation)
- Process in smaller batches (e.g., only Priority 1 leads)

### Excel files have encoding issues
- All Excel exports use openpyxl with UTF-8 encoding
- If special characters display incorrectly, check system locale settings

## Related Documentation

All documentation is located in `docs/`:

- `docs/guides/README.md` - Quick start for EEA data analysis
- `docs/guides/QUICK_SUMMARY.md` - Overview of EEA database and capabilities
- `docs/agents/AGENT_WORKFLOW_GUIDE.md` - Comprehensive workflow guide for all three agents
- `docs/agents/lead_prompting_guide.md` - Templates for customizing agent prompts
- `docs/data_structure/Industrial_Emissions_Data_Guide.md` - Deep dive into EEA database structure
- `docs/data_structure/DATA_INSIGHTS_ANALYSIS.md` - Data insights and analysis patterns
- `docs/market_analysis/WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md` - Current market analysis
- `docs/market_analysis/WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md` - 2024-2025 market trends
- `docs/technical_reference/DIOXIN_APCD_REFERENCE_GUIDE.md` - Dioxin and APCD regulatory reference
- `docs/technical_reference/DIOXIN_CHANGES_SUMMARY.md` - Recent regulatory changes
- `docs/GIT_WORKTREES_GUIDE.md` - Git workflow and worktrees setup
- `docs/restrictions.md` - Data usage restrictions and licensing