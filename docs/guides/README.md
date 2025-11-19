# EEA Industrial Emissions Data - GMAB Lead Generation System

Automated lead generation, evaluation, and proposal system for waste-to-energy (WtE) plant optimization using European Environment Agency industrial emissions data.

**Updated:** November 19, 2025

## 🎯 What This Project Does

This repository contains a **three-agent AI system** that:

1. **Scans 34,000+ European industrial facilities** to identify waste-to-energy plants
2. **Scores and ranks leads** based on emission compliance problems, efficiency gaps, and ROI potential
3. **Evaluates top prospects** with detailed technical feasibility and competitive analysis
4. **Generates automated proposals** with financial models and compliance documentation

**Target:** Waste-to-energy plants (MSW incinerators, RDF facilities, biomass, sewage sludge) that need:
- Emission compliance improvements
- Efficiency upgrades (ORC, waste heat recovery)
- Regulatory compliance documentation

---

## 📁 Project Structure

```
EEA_Industrial_Emissions_Data/
├── 📚 docs/                              # All documentation (organized by topic)
│   ├── guides/                          # Quick start guides
│   │   ├── README.md                    # This file - project overview
│   │   ├── CLAUDE.md                    # Project guidance for Claude Code
│   │   └── QUICK_SUMMARY.md             # EEA database capabilities
│   ├── agents/                          # Agent documentation
│   │   ├── AGENT_WORKFLOW_GUIDE.md      # Step-by-step agent execution
│   │   └── lead_prompting_guide.md      # Agent customization templates
│   ├── data_structure/                  # Data documentation
│   │   ├── Industrial_Emissions_Data_Guide.md   # EEA database deep dive
│   │   └── DATA_INSIGHTS_ANALYSIS.md            # Data insights & patterns
│   ├── market_analysis/                 # Market intelligence
│   │   ├── WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md      # 2024-2025 analysis
│   │   └── WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md
│   ├── technical_reference/             # Technical reference
│   │   ├── DIOXIN_APCD_REFERENCE_GUIDE.md
│   │   ├── DIOXIN_CHANGES_SUMMARY.md
│   │   └── EXTERNAL_DATA_CORRELATION_STRATEGY.md
│   ├── GIT_WORKTREES_GUIDE.md          # Git workflow
│   ├── restrictions.md                  # Data usage restrictions
│   ├── TASK_COMPLETION_SUMMARY.md      # Completed work
│   └── IMPLEMENTATION_COMPLETE.md       # Implementation status
│
├── 🤖 agents/                           # Agent implementations
│   ├── lead_generation_agent.py         # Scan & score facilities
│   ├── lead_evaluation_agent.py         # Deep analysis of top leads
│   ├── proposal_generation_agent.py     # Auto-generate proposals
│   └── run_agents_demo.py               # Demo execution
│
├── 🔧 scripts/                          # Utility scripts
│   ├── analyze_data_structure.py
│   ├── eea_emissions_analyzer.py        # General analysis tools
│   ├── waste_to_energy_lead_finder.py   # WtE-specific analysis
│   ├── industrial_emissions_lead_finder.py
│   ├── emission_compliance_checker.py
│   └── download_*.ps1, download_data.py # Data download utilities
│
├── 📊 data/                             # All data files (organized by type)
│   ├── raw/                            # Source data
│   │   ├── 1215_Public_Product_Full Access_v8.accdb  # Original EEA database
│   │   └── downloaded_data/            # Downloaded EEA datasets
│   ├── processed/                      # Converted/cleaned data
│   │   ├── converted_database.db       # SQLite version
│   │   └── converted_csv/              # 30+ CSV tables from database
│   └── market/                         # Market analysis & reference
│       ├── Active Plants Global WtE market 2024-2033.csv
│       ├── Projects Global WtE market 2024-2033.csv
│       ├── Waste to Energy 2024-2025.pdf
│       └── WTE_Market_Analysis_2024-2025.pptx
│
├── 📤 outputs/                          # Generated outputs
│   ├── GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx
│   ├── GMAB_Evaluated_Leads_YYYYMMDD.xlsx
│   └── GMAB_Proposals/                 # Per-facility proposal packages
│
└── 🐍 Python environments (.venv, venv), Git (.git), Config (.claude)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

```bash
# Clone or navigate to the repository
cd C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data

# Install Python dependencies
pip install claude-agent-sdk pandas openpyxl python-docx python-pptx

# Optional: for web scraping and additional analysis
pip install beautifulsoup4 selenium
```

### Running the Agents (Sequential Workflow)

```bash
# Step 1: Generate and score all leads
python agents/lead_generation_agent.py
# Output: outputs/GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx

# Step 2: Evaluate top Priority 1-2 leads
python agents/lead_evaluation_agent.py
# Output: outputs/GMAB_Evaluated_Leads_YYYYMMDD.xlsx

# Step 3: Generate proposal packages for best opportunities
python agents/proposal_generation_agent.py
# Output: outputs/GMAB_Proposals/[Facility_Name]/
```

### Demo Mode

```bash
# Run all agents with demo/mock data
python agents/run_agents_demo.py
```

---

## 📊 The Three Agents

### 1. Lead Generation Agent (`agents/lead_generation_agent.py`)

**Purpose:** Scan all ~34,000 EEA facilities and identify WtE plants with optimization needs

**Scoring (0-100 points):**
- **Emission Compliance (25 pts)** - Critical violations or approaching limits
- **Low Efficiency (25 pts)** - Thermal efficiency below 30%
- **Waste Heat Recovery Potential (20 pts)** - ORC/recovery opportunity
- **Plant Size (15 pts)** - Larger throughput = larger ROI
- **Urgency (15 pts)** - Boiler replacement, maintenance schedules

**Output:** 6-sheet Excel file with leads segmented by priority
- Priority 1 (Critical): 80-100 pts or emission violations
- Priority 2 (High Value): 65-79 pts
- Priority 3 (High Need): 50-64 pts
- Priority 4 (Good): 35-49 pts
- Priority 5 (Long-term): <35 pts
- ALL LEADS: Complete database

**Specialized Modes:**
```python
asyncio.run(aging_plants_boiler_replacement())    # Urgent replacements
asyncio.run(facility_type_analysis())              # Segment by WtE type
asyncio.run(geographic_wte_market_priority())      # Country-by-country
```

### 2. Lead Evaluation Agent (`agents/lead_evaluation_agent.py`)

**Purpose:** Deep technical and financial analysis of Priority 1-2 leads

**Tools:**
- Technical feasibility assessment
- Detailed ROI calculations (CAPEX, OPEX, payback, NPV, IRR)
- Competitive positioning (GMAB's 50+ WtE installations, ORC tech)
- Sales action plans (contact strategy, objection handling)

**Output:** Multi-sheet Excel with:
- Priority ranking with scores
- Technical feasibility analysis
- Financial models (3-year, 5-year, 10-year projections)
- Competitive positioning
- Recommended sales approach

**Specialized Modes:**
```python
asyncio.run(quick_screening())                     # Filter low-probability leads
asyncio.run(deep_dive_top_10())                    # Ultra-detailed analysis
asyncio.run(market_intelligence_report())          # Strategic insights
```

### 3. Proposal Generation Agent (`agents/proposal_generation_agent.py`)

**Purpose:** Auto-generate complete proposal packages for qualified leads

**Generates:**
- Executive summary proposal (PDF)
- Financial model with sensitivity analysis (Excel)
- Stakeholder presentations (PowerPoint - Energy Manager, CFO, Board)
- Compliance documentation (EU IED, BAT requirements)
- Implementation roadmap
- Risk analysis

**Output:** Organized folder per facility with 6-7 documents, ready for sales team

**Specialized Modes:**
```python
asyncio.run(generate_urgent_only())                # Only emission violation leads
asyncio.run(update_existing_proposals())           # Refresh with new data
```

---

## 📈 Data Sources & Structure

### EEA Database Contents

**Original Data:** `data/raw/1215_Public_Product_Full Access_v8.accdb` (1.2 GB)
- 34,000+ European industrial facilities
- Emissions by pollutant and year (2007-2023)
- Equipment, installation, and permit details
- Best Available Techniques (BAT) compliance status

**Converted Format:** `data/processed/converted_database.db` (771 MB SQLite)

**CSV Tables:** `data/processed/converted_csv/` (30+ files)
- `2_ProductionFacility.csv` - Facility names, locations, sectors
- `2f_PollutantRelease.csv` - Emissions by pollutant/year
- `3_ProductionInstallation.csv` - Equipment and process info
- `3d_BATConclusions.csv` - BAT compliance status
- `2e_ProductionVolume.csv` - Waste input volumes
- And 25+ more detailed tables

### Market Data

**Global WtE Market (2024-2033):**
- `data/market/Active Plants Global WtE market 2024-2033.csv`
- `data/market/Projects Global WtE market 2024-2033.csv`
- `data/market/Market outlook Global WtE market 2024-2033.csv`

**Analysis Documents:**
- `data/market/Waste to Energy 2024-2025.pdf` - Market study
- `data/market/WTE_Market_Analysis_2024-2025.pptx` - Presentation materials

---

## 🔧 Customization & Advanced Usage

### Switch from Mock Data to Real EEA Data

All agents currently use mock data for demonstration. To use real data:

1. Ensure CSVs are in `data/processed/converted_csv/`
2. In each agent file, find `query_eea_database()` function
3. Replace mock data with actual CSV queries:

```python
import pandas as pd

# Replace this:
mock_facilities = [{"facility": "Plant", "efficiency": 22}]

# With this:
facilities_df = pd.read_csv('data/processed/converted_csv/2_ProductionFacility.csv')
emissions_df = pd.read_csv('data/processed/converted_csv/2f_PollutantRelease.csv')
# Then filter and score...
```

### Target Only Specific Countries

Edit agent `COUNTRY_FILTER` variable:
```python
COUNTRY_FILTER = ['DE', 'FR', 'NL']  # Germany, France, Netherlands
```

### Adjust Scoring Thresholds

Modify Priority thresholds in lead_generation_agent.py:
```python
PRIORITY_1_THRESHOLD = 80       # Change from 80 to lower value for more leads
PRIORITY_2_THRESHOLD = 65
PRIORITY_3_THRESHOLD = 50
```

### Custom Analysis Scripts

See `scripts/` for utility examples:
- `eea_emissions_analyzer.py` - General purpose analysis
- `waste_to_energy_lead_finder.py` - WtE-specific filtering
- `emission_compliance_checker.py` - Regulatory compliance checks

---

## 📖 Documentation Map

**Getting Started:**
- Start here: `docs/guides/README.md` (this file)
- Overview: `docs/guides/QUICK_SUMMARY.md`
- Deep guidance: `docs/guides/CLAUDE.md`

**How to Use:**
- Agent workflow: `docs/agents/AGENT_WORKFLOW_GUIDE.md`
- Customize agents: `docs/agents/lead_prompting_guide.md`

**Understanding the Data:**
- EEA database guide: `docs/data_structure/Industrial_Emissions_Data_Guide.md`
- Data insights: `docs/data_structure/DATA_INSIGHTS_ANALYSIS.md`

**Market Intelligence:**
- Current analysis: `docs/market_analysis/WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md`
- 2024-2025 trends: `docs/market_analysis/WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md`

**Technical Reference:**
- Dioxin & APCD: `docs/technical_reference/DIOXIN_APCD_REFERENCE_GUIDE.md`
- Regulatory changes: `docs/technical_reference/DIOXIN_CHANGES_SUMMARY.md`

---

## ⚠️ Important Notes

### Data Limitations
- Only includes facilities above reporting thresholds
- Some countries may have delayed submissions
- Historical data may be revised
- Check metadata for known quality issues

### Current Status (November 2025)
✅ Three-agent system fully implemented
✅ EEA database converted and indexed
✅ 2024-2025 market analysis integrated
✅ Regulatory compliance documentation included
✅ **⚠️ Currently using mock data for demonstration**

### Data Usage
- EEA data is open-access (free to use with attribution)
- See `docs/restrictions.md` for licensing details
- Cite as: "European Environment Agency (2025), Industrial Reporting v14.0"

---

## 🐛 Troubleshooting

### "No leads found" error
- Check CSV files exist in `data/processed/converted_csv/`
- Verify you're using real data (not mock)
- Lower scoring thresholds if needed

### File path errors
- Ensure working directory is: `C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data`
- All paths use directory structure: `data/`, `agents/`, `docs/`
- Use forward slashes in Python paths on Windows

### Agent hangs or times out
- Increase `max_turns` in agent options
- Use specialized functions (e.g., `quick_screening()`) for faster results
- Process in smaller batches

### Excel encoding issues
- Files are UTF-8 encoded
- Check system locale if special characters display incorrectly

---

## 🔗 External Resources

### EEA & Regulatory
- **EEA Data Hub:** https://www.eea.europa.eu/datahub/
- **E-PRTR Regulation:** EU Regulation 166/2006
- **Industrial Emissions Directive:** 2010/75/EU
- **BAT Reference Documents:** https://eippcb.jrc.ec.europa.eu/

### Industry Databases
- **EU ETS:** Emissions Trading System data
- **National Inventories:** Country-level aggregated emissions
- **UNFCCC:** UN Climate Change reporting

### Help
- **EEA Industry Helpdesk:** industry.helpdesk@eea.europa.eu
- **Documentation:** See `docs/` folder

---

## 📞 Questions or Issues?

1. Check the comprehensive guide: `docs/guides/CLAUDE.md`
2. Review relevant documentation in `docs/` folder
3. Check troubleshooting above
4. Contact EEA for data questions: industry.helpdesk@eea.europa.eu

---

**Project:** GMAB Waste-to-Energy Lead Generation System  
**Data Version:** EEA 14.0 (2007-2023)  
**Documentation Updated:** November 19, 2025  
**Status:** Production Ready (Mock Data Mode)