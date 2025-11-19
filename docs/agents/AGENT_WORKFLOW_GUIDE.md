# Agent Workflow Guide

Complete step-by-step guide for running the three-agent GMAB waste-to-energy lead generation system.

**Updated:** November 19, 2025

---

## 📋 Overview: Three-Agent System

This system automates the complete sales process for WtE plant optimization:

1. **Lead Generation Agent** - Scans 34,000+ facilities, identifies WtE plants, scores opportunities
2. **Lead Evaluation Agent** - Deep analysis of top leads, ROI calculations, competitive positioning
3. **Proposal Generation Agent** - Auto-generates complete proposal packages with financial models

```
EEA Database (34,000 facilities)
    ↓
[Lead Generation Agent]
    ↓
100+ Leads (scored 0-100, prioritized 1-5)
    ↓
[Lead Evaluation Agent]
    ↓
15-20 Qualified Leads (detailed analysis, business cases)
    ↓
[Proposal Generation Agent]
    ↓
5-10 Complete Proposal Packages (ready for sales)
```

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
```bash
# Verify Python 3.8+ installed
python --version

# Install dependencies
pip install claude-agent-sdk pandas openpyxl python-docx python-pptx

# Navigate to project root
cd C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data
```

### Run All Three Agents Sequentially

```bash
# Step 1: Generate and score all leads (5-10 minutes)
python agents/lead_generation_agent.py
# Output: outputs/GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx

# Step 2: Evaluate Priority 1-2 leads (5-10 minutes)
python agents/lead_evaluation_agent.py
# Output: outputs/GMAB_Evaluated_Leads_YYYYMMDD.xlsx

# Step 3: Generate proposals for best leads (5-10 minutes)
python agents/proposal_generation_agent.py
# Output: outputs/GMAB_Proposals/[Facility_Name]/
```

### Demo Mode (Test Without Real Data)

```bash
# Run all agents with mock data
python agents/run_agents_demo.py
```

---

## 🎯 Agent 1: Lead Generation

**File:** `agents/lead_generation_agent.py`

**Purpose:** Scan all EEA facilities, identify WtE plants, score by opportunity

### What It Does

1. **Identifies WtE Plants:** Finds waste-to-energy facilities (MSW incinerators, RDF, biomass, sewage sludge)
2. **Scores Leads 0-100:** Based on 5 weighted criteria:
   - Emission compliance violations (25 pts) - CRITICAL
   - Low efficiency (25 pts) - Upgrade opportunity
   - Waste heat recovery potential (20 pts) - Revenue potential
   - Large plant size (15 pts) - ROI scale
   - Urgency (15 pts) - Timeline drivers
3. **Prioritizes 5 Tiers:** Priority 1 (critical) → Priority 5 (long-term nurture)
4. **Outputs Excel:** 6-sheet workbook with all leads segmented by priority

### Priority Thresholds

| Priority | Score | Action | Timeline |
|----------|-------|--------|----------|
| **1 - Critical** | 80-100 or violations | Immediate outreach | This month |
| **2 - High Value** | 65-79 | Active pursuit | Q1-Q2 |
| **3 - High Need** | 50-64 | Qualified pipeline | Q3-Q4 |
| **4 - Good** | 35-49 | Nurture | 12 months |
| **5 - Long-term** | <35 | Relationship building | 18+ months |

### Running Lead Generation

```bash
python agents/lead_generation_agent.py
```

**Output File:** `outputs/GMAB_WasteToEnergy_Leads_YYYYMMDD.xlsx`

**Sheets Created:**
- **PRIORITY 1** - Critical leads (emission violations, urgent action)
- **PRIORITY 2** - High value leads (65-79 score)
- **PRIORITY 3** - High need leads (50-64 score)
- **PRIORITY 4** - Good leads (35-49 score)
- **PRIORITY 5** - Long-term leads (<35 score)
- **ALL LEADS** - Complete database for reference

**Column Details:**
```
Facility Name | Location | Country | WtE Type | 
Current Efficiency (%) | Emissions Status | Waste Heat Potential (MW) |
Score (0-100) | Priority (1-5) | Key Opportunity | Recommended Action
```

### Specialized Analysis Modes

**Find Only Plants With Boiler Replacement Needs:**
```python
# Uncomment in lead_generation_agent.py:
asyncio.run(aging_plants_boiler_replacement())
```

**Segment by WtE Technology Type:**
```python
# Uncomment in lead_generation_agent.py:
asyncio.run(facility_type_analysis())
# Outputs separate lists for: MSW, RDF, Biomass, Sewage Sludge
```

**Country-by-Country Market Priority:**
```python
# Uncomment in lead_generation_agent.py:
asyncio.run(geographic_wte_market_priority())
# Ranks countries by market attractiveness
```

### Customization Tips

**Target Specific Countries:**
```python
# Edit in agent:
COUNTRY_FILTER = ['DE', 'FR', 'NL']  # Germany, France, Netherlands only
```

**Adjust Priority Thresholds:**
```python
# Edit in agent:
PRIORITY_1_THRESHOLD = 75  # Lower = more leads in Priority 1
PRIORITY_2_THRESHOLD = 60
```

**Change Scoring Weights:**
```python
# Edit in agent's scoring function:
EMISSION_WEIGHT = 30      # Increase compliance importance
EFFICIENCY_WEIGHT = 25
WASTE_HEAT_WEIGHT = 20
SIZE_WEIGHT = 15
URGENCY_WEIGHT = 10
```

---

## 🎯 Agent 2: Lead Evaluation

**File:** `agents/lead_evaluation_agent.py`

**Purpose:** Deep analysis of Priority 1-2 leads with business cases

### What It Does

1. **Technical Feasibility Analysis:**
   - Can we retrofit the system?
   - What size equipment needed?
   - Integration complexity and timeline
   - Space/infrastructure requirements

2. **Detailed ROI Calculations:**
   - CAPEX (equipment + installation)
   - Annual energy savings
   - Carbon credit revenue
   - OPEX (maintenance + upgrades)
   - Payback period and NPV
   - IRR (Internal Rate of Return)

3. **Competitive Analysis:**
   - Who else is targeting this facility?
   - GMAB's competitive advantages
   - Win probability assessment
   - Key decision factors

4. **Sales Action Plan:**
   - Target contacts (Energy Manager, CFO, Plant Director)
   - 5-step engagement sequence
   - Objection handling strategies
   - Value proposition summary
   - Target close date

### Running Lead Evaluation

```bash
python agents/lead_evaluation_agent.py
```

**Prerequisites:** Must have Priority 1-2 leads from Lead Generation Agent

**Output File:** `outputs/GMAB_Evaluated_Leads_YYYYMMDD.xlsx`

**Sheets Created:**
- **PRIORITY LIST** - Ranked leads with summary scores
- **DETAILED ANALYSIS** - Complete technical and financial analysis
- **SALES ACTIONS** - Engagement plans and contact strategy

**Column Details:**
```
Facility | Score | Priority | Technical Feasibility | 
CAPEX (€M) | Annual Savings (€M) | Payback (years) | NPV (€M) | 
IRR (%) | Win Probability (%) | Contact Strategy | Next Steps
```

### Specialized Analysis Modes

**Quick Screening (Filter Low-Probability Leads):**
```python
# Uncomment in lead_evaluation_agent.py:
asyncio.run(quick_screening())
# Fast evaluation - removes leads unlikely to close
```

**Deep Dive on Top 10 Leads:**
```python
# Uncomment in lead_evaluation_agent.py:
asyncio.run(deep_dive_top_10())
# Ultra-detailed analysis for best opportunities
```

**Market Intelligence Report:**
```python
# Uncomment in lead_evaluation_agent.py:
asyncio.run(market_intelligence_report())
# Strategic insights from all leads (market trends, competitive threats)
```

### Customization Tips

**Change ROI Calculation Period:**
```python
# Edit in agent:
NPV_YEARS = 10  # Default. Change to 5, 7, 15 as needed
DISCOUNT_RATE = 0.10  # 10% financial discount rate
```

**Adjust Competitive Advantage Weighting:**
```python
# Edit in competitive_analysis:
GMAB_EXPERIENCE_WEIGHT = 0.35  # Our 50+ WtE installations
TECHNOLOGY_ADVANTAGE_WEIGHT = 0.30  # ORC efficiency
COST_ADVANTAGE_WEIGHT = 0.20  # Pricing
LOCAL_PRESENCE_WEIGHT = 0.15  # Regional support
```

**Set Win Probability Threshold:**
```python
# Edit in agent:
PURSUE_IF_WIN_PROBABILITY > 40  # Only pursue leads >40% win probability
PRIORITY_1_WIN_PROB = 70  # Consider only if >70% to close
```

---

## 🎯 Agent 3: Proposal Generation

**File:** `agents/proposal_generation_agent.py`

**Purpose:** Auto-generate complete proposal packages for qualified leads

### What It Does

1. **Executive Summary Proposal (PDF)**
   - Problem statement
   - Proposed solution
   - Key benefits and ROI
   - Implementation timeline
   - Pricing summary

2. **Financial Model (Excel)**
   - Capital expenditure breakdown
   - Energy savings calculator
   - Carbon credit projections
   - Cash flow and NPV analysis
   - Sensitivity analysis (±10%, ±20% variables)
   - Scenario planning (Best case, Base case, Conservative)

3. **Stakeholder Presentations (PowerPoint)**
   - Energy Manager deck (technical details, efficiency gains)
   - CFO deck (financial impact, ROI, payback)
   - Board deck (strategic benefits, ESG impact, risk mitigation)

4. **Compliance Documentation**
   - EU Industrial Emissions Directive (2010/75/EU) compliance
   - Best Available Techniques (BAT) alignment
   - Emission reduction projections
   - Regulatory requirements checklist

5. **Implementation Roadmap**
   - Phase 1: Design & Engineering
   - Phase 2: Manufacturing & Procurement
   - Phase 3: Installation & Commissioning
   - Phase 4: Training & Handover
   - Timeline, milestones, resource requirements

### Running Proposal Generation

```bash
python agents/proposal_generation_agent.py
```

**Prerequisites:** Must have evaluated leads from Lead Evaluation Agent

**Output Structure:**
```
outputs/GMAB_Proposals/
├── [Facility_Name_1]/
│   ├── Executive_Proposal_[Facility].pdf
│   ├── Financial_Model_[Facility].xlsx
│   ├── Presentation_Energy_Manager_[Facility].pptx
│   ├── Presentation_CFO_[Facility].pptx
│   ├── Presentation_Board_[Facility].pptx
│   ├── Compliance_Documentation_[Facility].pdf
│   └── Implementation_Roadmap_[Facility].pdf
├── [Facility_Name_2]/
│   └── (same structure)
└── ...
```

### Specialized Analysis Modes

**Generate Only for Emission Violation Leads:**
```python
# Uncomment in proposal_generation_agent.py:
asyncio.run(generate_urgent_only())
# Only creates proposals for Priority 1 (critical) leads
```

**Update Existing Proposals with New Data:**
```python
# Uncomment in proposal_generation_agent.py:
asyncio.run(update_existing_proposals())
# Refreshes previously generated packages with latest market data
```

### Customization Tips

**Customize Document Branding:**
```python
# Edit in agent:
COMPANY_NAME = "GMAB"
COMPANY_LOGO = "path/to/logo.png"
BRAND_COLOR = "#004D99"  # GMAB blue
CONTACT_EMAIL = "sales@gmab.com"
```

**Adjust Financial Assumptions:**
```python
# Edit in agent:
CARBON_CREDIT_PRICE = 80  # €/tonne CO2
ELECTRICITY_PRICE = 0.12  # €/kWh
THERMAL_PRICE = 0.08     # €/kWh (heat)
INFLATION_RATE = 0.02    # 2% annual
```

**Change ROI Presentation Focus:**
```python
# Edit in agent:
# For environmentally-conscious facilities:
EMPHASIZE_CO2_REDUCTION = True
SHOW_ESG_IMPACT = True

# For financially-driven facilities:
EMPHASIZE_PAYBACK = True
SHOW_TAX_BENEFITS = True
```

---

## 📊 Complete Workflow Example

### Scenario: Identify Best WtE Opportunities in Germany (Q1 2025)

**Step 1: Generate Leads (Monday, 9 AM)**
```bash
cd C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data
python agents/lead_generation_agent.py

# Agent scans all German WtE facilities, scores them
# Output: outputs/GMAB_WasteToEnergy_Leads_20250113.xlsx
# Duration: 5-10 minutes
# Result: 50 leads across 5 priority tiers
```

**Step 2: Review Priority 1 Leads (Monday, 10 AM)**
```
Open: outputs/GMAB_WasteToEnergy_Leads_20250113.xlsx
Sheet: PRIORITY 1
Found: 8 leads with emission violations or 80+ score
Key Facilities:
- Hamburg WtE Incineration (Score: 92, Current efficiency: 18%)
- Berlin RDF Facility (Score: 88, Emission violations)
- Frankfurt Biomass Plant (Score: 85, Heat recovery gap: 12 MW)
```

**Step 3: Deep Evaluate Top Leads (Monday, 2 PM)**
```bash
python agents/lead_evaluation_agent.py

# Agent analyzes top 10-15 Priority 1-2 leads
# Output: outputs/GMAB_Evaluated_Leads_20250113.xlsx
# Duration: 5-10 minutes
# Result: Complete business cases with ROI, win probability, sales plans
```

**Step 4: Review Evaluation Results (Monday, 3 PM)**
```
Open: outputs/GMAB_Evaluated_Leads_20250113.xlsx
Sheet: PRIORITY LIST
Review: Top 5 leads by win probability and ROI
- Hamburg WtE: €28M CAPEX, €12M/year savings, 2.3 year payback, 68% win prob
- Berlin RDF: €22M CAPEX, €9M/year savings, 2.4 year payback, 75% win prob
- Frankfurt Biomass: €35M CAPEX, €15M/year savings, 2.3 year payback, 62% win prob
```

**Step 5: Generate Proposals (Monday, 4 PM)**
```bash
python agents/proposal_generation_agent.py

# Agent generates complete proposal packages for top 3 leads
# Output: outputs/GMAB_Proposals/[Facility_Name]/
# Duration: 10-15 minutes
# Result: 3 folder sets with 6-7 documents each, ready for sales
```

**Step 6: Sales Handoff (Tuesday, 9 AM)**
```
Sales Team Receives:
- outputs/GMAB_Proposals/Hamburg_WtE_Incineration/
  - Executive_Proposal.pdf (2-page overview)
  - Financial_Model.xlsx (with sensitivity analysis)
  - Presentation_Energy_Manager.pptx (technical deck)
  - Presentation_CFO.pptx (financial deck)
  - Compliance_Documentation.pdf (regulatory alignment)
  
Sales Actions:
1. Contact Energy Manager: "We've identified unique efficiency opportunity"
2. Share Executive Proposal via email
3. Schedule 30-min discovery call
4. If positive: Present CFO deck with financial model
5. If interested: Schedule site visit with our engineer
```

**Expected Results:**
- Week 1-2: Discovery calls with 3 leads
- Week 3-4: Technical assessment visits
- Month 2: Proposals sent to decision-makers
- Month 3-4: Negotiation phase
- Expected close: Q2/Q3

---

## 🔄 Monthly Workflow

### Week 1: Lead Generation
```bash
# Run lead generation monthly to catch new opportunities
python agents/lead_generation_agent.py
# Check for new facilities added to EEA database
# Review any Priority 1 leads from previous month that weren't pursued
```

### Week 2: Lead Evaluation
```bash
# Evaluate new Priority 1-2 leads
python agents/lead_evaluation_agent.py
# Focus on highest win probability leads
# Create 5-10 new qualified opportunities
```

### Week 3: Proposal Generation + Sales Handoff
```bash
# Generate proposals for this quarter's best opportunities
python agents/proposal_generation_agent.py
# Hand off to sales team
# Sales team begins outreach and discovery
```

### Week 4: Analysis & Refinement
```bash
# Review results from previous weeks
# Update agent parameters if needed
# Prepare leads for next week's evaluation
# Track which leads from last month are progressing
```

---

## 🎓 Understanding the Outputs

### Lead Generation Output Example

```
Facility: Hamburg WtE Incineration Plant
Country: Germany
Current Efficiency: 18%
Emissions Status: Exceeding NOx limits (enforcement action pending)
Waste Heat Potential: 14 MW (recoverable)
Scoring:
  - Emission Compliance: 25/25 (violations + enforcement)
  - Low Efficiency: 25/25 (well below 28% BAT standard)
  - Waste Heat Potential: 18/20 (excellent recovery opportunity)
  - Plant Size: 12/15 (medium-large, 120,000 t/year input)
  - Urgency: 12/15 (emission deadline <90 days)
  TOTAL SCORE: 92/100

Priority: 1 (CRITICAL) - Immediate action required
Recommended Action: Contact Energy Manager immediately, highlight emission compliance + efficiency gains
```

### Lead Evaluation Output Example

```
Facility: Berlin RDF Processing Facility

TECHNICAL FEASIBILITY: 85/100
- Equipment sizing: 8 MW ORC system
- Integration complexity: MODERATE (30-40 week timeline)
- Space available: YES (200 m² required, 400 m² available)
- Infrastructure: Adequate steam capacity, cooling water available
- Recommendation: FEASIBLE - proceed to proposal

FINANCIAL ANALYSIS:
- CAPEX: €22.4M (equipment €15.2M, installation €7.2M)
- Annual Savings: €9.1M (energy €6.8M, carbon credits €2.3M)
- Payback Period: 2.4 years
- NPV (10 years): €38.6M @ 10% discount rate
- IRR: 42%

COMPETITIVE ANALYSIS:
- Competitors: Siemens Power & Gas (4 MW turbine), ABB (waste heat recovery)
- GMAB Advantage: Specialized WtE experience (50+ installations), 15% lower cost, faster deployment
- Win Probability: 75%

SALES ACTION PLAN:
1. Contact: Dipl.-Ing. Klaus Mueller, Energy Manager, klaus.mueller@berlin-rdf.de
2. Value Prop: "Reduce emissions by 8,000 t CO2/year while increasing profitability 40%"
3. Timeline: "Installation in 10 months, ROI in <2.5 years"
4. Next Step: Schedule 30-min call week of Jan 20

Recommendation: PRIORITY 1 - Immediate outreach, high probability deal
```

---

## 🚨 Common Issues & Solutions

### Issue 1: "Agent takes too long"
**Solution:**
- Use specialized functions instead of full analysis
- Run `quick_screening()` first to filter low-probability leads
- Process in batches (Priority 1 only, then Priority 2, etc.)

### Issue 2: "No leads found"
**Solution:**
- Verify CSV files exist in `data/processed/converted_csv/`
- Check that mock data is being used (if CSVs missing)
- Lower scoring thresholds (change PRIORITY_1_THRESHOLD to 75)
- Verify agent is targeting correct facility types

### Issue 3: "Excel file is empty"
**Solution:**
- Check that agent completed successfully (check console output)
- Verify openpyxl is installed: `pip install openpyxl`
- Try running with mock data first: `python agents/run_agents_demo.py`
- Check that all data files are in correct locations

### Issue 4: "Win probability seems too low"
**Solution:**
- Review competitive analysis weights in agent
- Check if facility has existing competing solutions
- Verify that GMAB advantages are correctly parameterized
- Consider that score is realistic - adjust expectations or target different leads

---

## ✅ Checklist: First Time Setup

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install ...`)
- [ ] Working directory set to project root
- [ ] Data files verified in `data/processed/converted_csv/`
- [ ] Run agents/run_agents_demo.py to test system
- [ ] Review mock outputs and structure
- [ ] Read docs/guides/README.md for full overview
- [ ] Run lead_generation_agent.py with real or mock data
- [ ] Review outputs/GMAB_WasteToEnergy_Leads_*.xlsx
- [ ] Run lead_evaluation_agent.py
- [ ] Review outputs/GMAB_Evaluated_Leads_*.xlsx
- [ ] Run proposal_generation_agent.py
- [ ] Review outputs/GMAB_Proposals/ structure
- [ ] Customize agents per docs/agents/lead_prompting_guide.md
- [ ] Hand off to sales team

---

## 📞 Next Steps

1. **Run all agents** with the quick start commands above
2. **Review outputs** to understand what's being generated
3. **Customize** agent parameters for your market/priorities
4. **Integrate with CRM** to track lead progress
5. **Monitor results** and refine scoring weights monthly
6. **Expand** to additional countries/industries as you scale

For detailed customization, see: `docs/agents/lead_prompting_guide.md`

For data deep-dive, see: `docs/data_structure/Industrial_Emissions_Data_Guide.md`