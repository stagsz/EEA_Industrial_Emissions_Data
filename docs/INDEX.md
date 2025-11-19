# Documentation Index

Master index for all project documentation. Last updated: November 19, 2025

---

## 🚀 START HERE

**New to this project?** Follow this path:

1. **README.md** (`docs/guides/README.md`) - Project overview, quick start, and directory structure
2. **QUICK_SUMMARY.md** (`docs/guides/QUICK_SUMMARY.md`) - EEA database capabilities and features
3. **CLAUDE.md** (`docs/guides/CLAUDE.md`) - Detailed project guidance (for development)

Then proceed based on your role:

- **Want to run the agents?** → `docs/agents/AGENT_WORKFLOW_GUIDE.md`
- **Want to understand the data?** → `docs/data_structure/Industrial_Emissions_Data_Guide.md`
- **Want to customize agents?** → `docs/agents/lead_prompting_guide.md`
- **Want market insights?** → `docs/market_analysis/`

---

## 📚 Documentation by Category

### 🎯 Getting Started (5-10 minutes)

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **README.md** | Project overview, quick start guide | 5 min |
| **QUICK_SUMMARY.md** | EEA database overview and capabilities | 3 min |

**Location:** `docs/guides/`

### 📖 Guides (10-30 minutes each)

| Document | Purpose | Audience | Read Time |
|----------|---------|----------|-----------|
| **CLAUDE.md** | Project guidance for developers | Developers | 20 min |
| **AGENT_WORKFLOW_GUIDE.md** | Step-by-step execution of all three agents | All | 15 min |
| **lead_prompting_guide.md** | Templates for customizing agent prompts | Developers | 10 min |

**Locations:** `docs/guides/` and `docs/agents/`

### 🗄️ Data Documentation (20-40 minutes)

| Document | Purpose | Use Case | Read Time |
|----------|---------|----------|-----------|
| **Industrial_Emissions_Data_Guide.md** | Deep dive into EEA database structure | Understanding data | 30 min |
| **DATA_INSIGHTS_ANALYSIS.md** | Analysis patterns and insights from EEA data | Data analysis | 25 min |

**Location:** `docs/data_structure/`

### 📈 Market Intelligence (10-20 minutes each)

| Document | Purpose | Last Updated | Read Time |
|----------|---------|--------------|-----------|
| **WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md** | Current 2024-2025 market analysis | Nov 19, 2025 | 15 min |
| **WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md** | Comprehensive market trends and forecast | Nov 19, 2025 | 20 min |

**Location:** `docs/market_analysis/`

### 🔬 Technical Reference (30-60 minutes)

| Document | Purpose | Topic | Read Time |
|----------|---------|-------|-----------|
| **DIOXIN_APCD_REFERENCE_GUIDE.md** | Regulatory reference for dioxin and APCD analysis | Emissions compliance | 45 min |
| **DIOXIN_CHANGES_SUMMARY.md** | Recent regulatory changes affecting WtE plants | Compliance updates | 15 min |
| **EXTERNAL_DATA_CORRELATION_STRATEGY.md** | Strategy for correlating external data sources | Data enrichment | 30 min |

**Location:** `docs/technical_reference/`

### ⚙️ Operational Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **GIT_WORKTREES_GUIDE.md** | Git workflow and worktree setup | 15 min |
| **restrictions.md** | Data usage restrictions and licensing | 5 min |
| **TASK_COMPLETION_SUMMARY.md** | Summary of completed implementation tasks | 10 min |
| **IMPLEMENTATION_COMPLETE.md** | Implementation status report | 15 min |

**Location:** `docs/`

---

## 📁 File Organization

### By Role

**Sales/Business:**
- Start: `docs/guides/README.md`
- Then: `docs/market_analysis/WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md`
- Run agents: `docs/agents/AGENT_WORKFLOW_GUIDE.md`

**Developers:**
- Start: `docs/guides/CLAUDE.md`
- Data: `docs/data_structure/Industrial_Emissions_Data_Guide.md`
- Customize: `docs/agents/lead_prompting_guide.md`
- Reference: `docs/technical_reference/`

**Data Analysts:**
- Start: `docs/guides/QUICK_SUMMARY.md`
- Data: `docs/data_structure/Industrial_Emissions_Data_Guide.md`
- Analysis: `docs/data_structure/DATA_INSIGHTS_ANALYSIS.md`
- Scripts: `scripts/` directory

**Compliance/Regulatory:**
- Reference: `docs/technical_reference/DIOXIN_APCD_REFERENCE_GUIDE.md`
- Updates: `docs/technical_reference/DIOXIN_CHANGES_SUMMARY.md`
- Restrictions: `docs/restrictions.md`

### By Topic

**Project Overview:**
- `docs/guides/README.md` - Full project overview
- `docs/guides/QUICK_SUMMARY.md` - Database overview
- `docs/guides/CLAUDE.md` - Development guidance

**Running the System:**
- `docs/agents/AGENT_WORKFLOW_GUIDE.md` - How to execute agents
- `docs/agents/lead_prompting_guide.md` - Agent customization

**Understanding Data:**
- `docs/data_structure/Industrial_Emissions_Data_Guide.md` - EEA structure
- `docs/data_structure/DATA_INSIGHTS_ANALYSIS.md` - Data patterns

**Market & Competition:**
- `docs/market_analysis/WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md` - Current market
- `docs/market_analysis/WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md` - Market trends

**Technical Deep Dives:**
- `docs/technical_reference/DIOXIN_APCD_REFERENCE_GUIDE.md` - Emissions specs
- `docs/technical_reference/DIOXIN_CHANGES_SUMMARY.md` - Regulatory changes
- `docs/technical_reference/EXTERNAL_DATA_CORRELATION_STRATEGY.md` - Data fusion

**Operations & Maintenance:**
- `docs/GIT_WORKTREES_GUIDE.md` - Version control
- `docs/restrictions.md` - Licensing
- `docs/TASK_COMPLETION_SUMMARY.md` - Work completed
- `docs/IMPLEMENTATION_COMPLETE.md` - Status

---

## 🏗️ Project Structure

```
docs/
├── INDEX.md (this file)
├── guides/
│   ├── README.md                    # START HERE
│   ├── QUICK_SUMMARY.md
│   └── CLAUDE.md
├── agents/
│   ├── AGENT_WORKFLOW_GUIDE.md
│   └── lead_prompting_guide.md
├── data_structure/
│   ├── Industrial_Emissions_Data_Guide.md
│   └── DATA_INSIGHTS_ANALYSIS.md
├── market_analysis/
│   ├── WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md
│   └── WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md
├── technical_reference/
│   ├── DIOXIN_APCD_REFERENCE_GUIDE.md
│   ├── DIOXIN_CHANGES_SUMMARY.md
│   └── EXTERNAL_DATA_CORRELATION_STRATEGY.md
├── GIT_WORKTREES_GUIDE.md
├── restrictions.md
├── TASK_COMPLETION_SUMMARY.md
└── IMPLEMENTATION_COMPLETE.md

agents/
├── lead_generation_agent.py
├── lead_evaluation_agent.py
├── proposal_generation_agent.py
└── run_agents_demo.py

scripts/
├── analyze_data_structure.py
├── eea_emissions_analyzer.py
├── waste_to_energy_lead_finder.py
├── emission_compliance_checker.py
└── ... (utility scripts)

data/
├── raw/
│   ├── 1215_Public_Product_Full Access_v8.accdb
│   └── downloaded_data/
├── processed/
│   ├── converted_database.db
│   └── converted_csv/ (30+ CSV files)
└── market/
    ├── Active Plants Global WtE market 2024-2033.csv
    ├── Projects Global WtE market 2024-2033.csv
    └── ... (market data & PDFs)

outputs/
├── GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx
├── GMAB_Evaluated_Leads_YYYYMMDD.xlsx
└── GMAB_Proposals/
```

---

## 🔄 Common Tasks

### I want to...

**Run the lead generation system**
1. Read: `docs/guides/README.md` (Quick Start)
2. Execute: `docs/agents/AGENT_WORKFLOW_GUIDE.md` (Step-by-step)
3. Reference: `docs/guides/CLAUDE.md` (Troubleshooting)

**Understand how the data works**
1. Start: `docs/guides/QUICK_SUMMARY.md`
2. Deep dive: `docs/data_structure/Industrial_Emissions_Data_Guide.md`
3. Analyze: `docs/data_structure/DATA_INSIGHTS_ANALYSIS.md`

**Modify an agent**
1. Understand: `docs/guides/CLAUDE.md` (Architecture)
2. Customize: `docs/agents/lead_prompting_guide.md` (Templates)
3. Reference: `docs/agents/AGENT_WORKFLOW_GUIDE.md` (How it runs)

**Add market/competitive analysis**
1. Review: `docs/market_analysis/WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md`
2. Reference: `docs/market_analysis/WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md`
3. Integrate: `docs/agents/lead_prompting_guide.md` (Agent modifications)

**Check regulatory compliance**
1. Reference: `docs/technical_reference/DIOXIN_APCD_REFERENCE_GUIDE.md`
2. Updates: `docs/technical_reference/DIOXIN_CHANGES_SUMMARY.md`
3. Implement: Modify agent scoring in `agents/lead_generation_agent.py`

**Contribute code**
1. Understand: `docs/guides/CLAUDE.md`
2. Workflow: `docs/GIT_WORKTREES_GUIDE.md`
3. Implementation: Follow code patterns in `agents/`

---

## 📊 Documentation Status

**Last Updated:** November 19, 2025

### Fresh (Today - Nov 19)
✅ CLAUDE.md - Updated with new directory structure
✅ README.md - Updated with project overview
✅ INDEX.md - Created new

### Updated (Nov 19, Earlier)
✅ WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md
✅ WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md
✅ GIT_WORKTREES_GUIDE.md
✅ DIOXIN_APCD_REFERENCE_GUIDE.md
✅ DIOXIN_CHANGES_SUMMARY.md

### Older (Oct 17-21)
⚠️ AGENT_WORKFLOW_GUIDE.md (33 days old)
⚠️ lead_prompting_guide.md
⚠️ QUICK_SUMMARY.md
⚠️ Industrial_Emissions_Data_Guide.md
⚠️ DATA_INSIGHTS_ANALYSIS.md
⚠️ EXTERNAL_DATA_CORRELATION_STRATEGY.md
⚠️ restrictions.md
⚠️ TASK_COMPLETION_SUMMARY.md
⚠️ IMPLEMENTATION_COMPLETE.md

---

## 🔗 Quick Links

| Task | Document |
|------|----------|
| Quick start | `docs/guides/README.md` |
| How to run agents | `docs/agents/AGENT_WORKFLOW_GUIDE.md` |
| Understanding data | `docs/data_structure/Industrial_Emissions_Data_Guide.md` |
| Market insights | `docs/market_analysis/WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md` |
| Regulatory reference | `docs/technical_reference/DIOXIN_APCD_REFERENCE_GUIDE.md` |
| Development guide | `docs/guides/CLAUDE.md` |
| Git workflow | `docs/GIT_WORKTREES_GUIDE.md` |
| Customization | `docs/agents/lead_prompting_guide.md` |

---

## 📞 Navigation

- **You are here:** `docs/INDEX.md` (Documentation Map)
- **Quick Start:** `docs/guides/README.md`
- **Full Guide:** `docs/guides/CLAUDE.md`
- **Run Agents:** `docs/agents/AGENT_WORKFLOW_GUIDE.md`