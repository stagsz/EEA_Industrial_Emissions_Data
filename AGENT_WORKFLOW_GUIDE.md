# GMAB Lead Generation & Evaluation Workflow

## Two-Agent System for Waste Energy Recovery Lead Management

This system uses **two specialized AI agents** to find and qualify waste energy recovery opportunities:

1. **Lead Generation Agent** - Finds potential leads from EEA database
2. **Lead Evaluation Agent** - Deeply evaluates and prioritizes those leads

---

## 🎯 Complete Workflow

### STAGE 1: Lead Generation
**Agent**: `lead_generation_agent.py`

**Purpose**: Scan EEA Industrial Emissions Database to find facilities with high waste energy recovery potential

**What it does**:
- Queries 34,000+ industrial facilities across EU
- Identifies high energy consumers (>15,000 TJ/year)
- Finds high-temperature processes (>300°C)
- Detects facilities with NO current heat recovery
- Scores leads based on waste heat potential

**Output**: `GMAB_waste_energy_recovery_leads.csv`
- Top 30-50 leads
- Basic scoring (70+ = HOT, 50-69 = WARM)
- Energy consumption, temperatures, industry sector

**Run it**:
```bash
python lead_generation_agent.py
```

---

### STAGE 2: Lead Evaluation
**Agent**: `lead_evaluation_agent.py`

**Purpose**: Deep analysis and qualification of leads from Stage 1

**What it does**:
- **Technical Feasibility**: Can we install our system? What size? Timeline?
- **Financial Analysis**: Detailed ROI, payback, NPV, IRR calculations
- **Competitive Intelligence**: Who are we competing against? Win probability?
- **Sales Strategy**: Contact plan, value proposition, objection handling

**Output**: `GMAB_evaluated_leads_PRIORITY_LIST.csv`
- Top 10-15 fully qualified leads
- Complete business cases
- Sales action plans
- Priority ranking

**Run it**:
```bash
python lead_evaluation_agent.py
```

---

## 📊 What Each Agent Finds

### Lead Generation Agent Scores On:
| Criteria | Points | What It Means |
|----------|--------|---------------|
| **Waste Heat Potential** | 40 | VERY HIGH (>15,000 TJ/year) = best |
| **Current Recovery** | 30 | NONE = greenfield opportunity |
| **Process Temperature** | 20 | >400°C = premium heat quality |
| **ROI Potential** | 10 | >€50M/year savings |

**Example Output**:
```
Facility: ArcelorMittal Steel Plant
Score: 90/100 (🔥 HOT)
Energy Input: 45,000 TJ/year
Temperature: 800-1200°C
Waste Heat: 15,000+ TJ/year recoverable
Savings: €50-70M/year
```

### Lead Evaluation Agent Analyzes:

#### 1. Technical Feasibility (0-100 score)
- Process compatibility
- Integration complexity
- Equipment sizing (MW capacity)
- Installation timeline
- Space/infrastructure requirements

#### 2. Financial Metrics
- **CAPEX**: Total investment (€M)
- **Annual Savings**: Energy cost reduction + carbon credits
- **Payback Period**: Years to break even
- **NPV**: 10-year net present value
- **IRR**: Internal rate of return
- **Financing**: Available grants and loans

#### 3. Competitive Analysis
- Existing suppliers
- Competitor threats
- GMAB advantages
- Win probability (%)
- Key decision factors

#### 4. Sales Action Plan
- Target contacts (Energy Manager, CFO, Plant Director)
- Engagement sequence (5-step plan)
- Objection handling
- Value proposition
- Target close date

---

## 🚀 Quick Start: Run Both Agents

### Option 1: Sequential Execution
```bash
# Step 1: Generate leads
python lead_generation_agent.py

# Step 2: Evaluate leads (automatically reads output from step 1)
python lead_evaluation_agent.py
```

### Option 2: Specialized Analysis

**Find Ultra-High ROI targets only**:
```python
# Edit lead_generation_agent.py, uncomment:
asyncio.run(ultra_high_roi_targets())
```

**Deep dive on top 10 leads**:
```python
# Edit lead_evaluation_agent.py, uncomment:
asyncio.run(deep_dive_top_10())
```

**Market intelligence report**:
```python
# Edit lead_evaluation_agent.py, uncomment:
asyncio.run(market_intelligence_report())
```

---

## 📁 Output Files

| File | Source | Content |
|------|--------|---------|
| `GMAB_waste_energy_recovery_leads.csv` | Lead Gen Agent | 30-50 raw leads with basic scoring |
| `GMAB_evaluated_leads_PRIORITY_LIST.csv` | Evaluation Agent | 10-15 fully qualified leads with complete analysis |
| `ULTRA_HIGH_ROI_WASTE_ENERGY.csv` | Lead Gen (specialized) | Only mega-projects (>€40M savings) |
| `GMAB_qualified_leads_after_screening.csv` | Evaluation (quick screen) | Filtered leads (removed low probability) |

---

## 💡 Usage Examples

### Example 1: Find Best Leads for Q1 Sales Campaign

**Goal**: Find 10 high-probability deals for immediate outreach

```bash
# 1. Run lead generation
python lead_generation_agent.py

# 2. Evaluate all leads
python lead_evaluation_agent.py

# 3. Review output
# File: GMAB_evaluated_leads_PRIORITY_LIST.csv
# Sort by: Win_Probability DESC, ROI DESC
# Take top 10
```

**Result**: 10 leads with:
- Technical feasibility confirmed
- ROI >30% IRR
- Win probability >60%
- Complete sales action plans

---

### Example 2: Target Specific Industry (Steel)

**Goal**: Find all steel plants with waste heat opportunities

**Modify lead_generation_agent.py**:
```python
# In the main prompt, change:
TARGET FACILITIES:
- Industries: Steel Production ONLY (blast furnaces, EAF, rolling mills)
- Energy Input: >30,000 TJ/year
- Process Temp: >800°C (steel-specific)
```

**Run**:
```bash
python lead_generation_agent.py
python lead_evaluation_agent.py
```

---

### Example 3: Geographic Focus (Germany + Poland)

**Goal**: Prioritize two countries with best market conditions

**Modify lead_generation_agent.py**:
```python
# Uncomment:
asyncio.run(geographic_energy_market_priority())
```

This will:
- Rank all EU countries by waste energy opportunity
- Provide top 40 facilities per country
- Include national incentives/subsidies
- Market size estimates

---

## 🎓 Understanding the Scores

### Lead Generation Score (0-100)
- **90-100**: EXCEPTIONAL - No-brainer projects (mega ROI, zero recovery now)
- **70-89**: HOT - Excellent opportunities (immediate outreach)
- **50-69**: WARM - Good opportunities (priority outreach)
- **<50**: COLD - Long-term nurture

### Evaluation Priority Ranking (1-5)
- **Priority 1**: Close in Q1/Q2 - immediate action
- **Priority 2**: Close in Q2/Q3 - active pursuit
- **Priority 3**: Close in H2 - qualified pipeline
- **Priority 4**: Close in next year - nurture
- **Priority 5**: Low probability - revisit later

---

## 🔧 Customization Tips

### Adjust Lead Generation Criteria

**Find smaller projects** (currently targets >15,000 TJ/year):
```python
# In prompt, change:
- Energy Consumption: HIGH (>8,000 TJ/year)  # Lower threshold
```

**Target different industries**:
```python
TARGET FACILITIES:
- Industries: Glass Production, Ceramics, Paper & Pulp
```

**Change geographic focus**:
```python
- Location: Central Europe (Germany, Poland, Czech Republic, Austria)
```

### Adjust Evaluation Criteria

**Prioritize faster payback** (currently accepts up to 5 years):
```python
# In detailed_roi_calculation, filter:
if payback_period < 3.0:  # Only projects with <3 year payback
```

**Focus on strategic accounts** (reference potential):
```python
# In competitive_analysis, add:
- Reference account potential (industry leaders, visibility)
```

---

## 📈 Expected Results

### Typical Lead Funnel (from EEA database of ~34,000 facilities):

```
EEA Database: 34,000 facilities
    ↓ (High energy consumption filter)
Initial Screen: ~2,500 facilities
    ↓ (Waste heat potential scoring)
Lead Generation: 50 leads (HOT + WARM)
    ↓ (Technical + financial evaluation)
Qualified Leads: 15 leads (Priority 1-2)
    ↓ (Sales process)
Expected Wins: 3-5 deals per quarter
```

### Deal Metrics (based on mock data):

- **Average deal size**: €25-30M
- **Average payback**: 2-3 years
- **Average IRR**: 35-40%
- **Average savings**: €15-25M/year
- **Average CO2 reduction**: 20,000-30,000 tonnes/year

---

## 🎯 Best Practices

### 1. Run Lead Generation Monthly
Markets change - new facilities, energy prices, regulations
```bash
# Create monthly job
# Month 1: Run full analysis
# Month 2-3: Run quick update (new facilities only)
```

### 2. Evaluate in Batches
Don't evaluate all 50 leads - focus on HOT leads first
```bash
# Week 1: Evaluate leads with score >80 (Priority 1)
# Week 2: Evaluate leads with score 70-79 (Priority 2)
# Week 3+: Evaluate WARM leads (50-69) if capacity allows
```

### 3. Update Lead Statuses
Track which leads are being pursued by sales
```python
# Add status field:
- CONTACTED
- DISCOVERY
- PROPOSAL
- NEGOTIATION
- WON
- LOST
```

### 4. Feed Back Results
Improve agent accuracy by analyzing wins/losses
```python
# After 6 months, analyze:
- Which scored leads actually closed?
- What did we miss in evaluation?
- Update scoring weights accordingly
```

---

## 🆘 Troubleshooting

### "No leads found"
**Issue**: Lead generation returns zero results

**Solutions**:
1. Check data files exist in `converted_csv/`
2. Lower thresholds (energy consumption, temperature)
3. Expand geographic scope
4. Check mock data is being used (if CSV files missing)

### "All leads score low"
**Issue**: No leads above 70 points

**Solutions**:
1. Adjust scoring weights (reduce threshold to 60)
2. Check if industry filter too narrow
3. Verify energy data is loading correctly
4. Review mock results vs. real data

### "Evaluation agent hangs"
**Issue**: Evaluation takes too long or doesn't complete

**Solutions**:
1. Reduce number of leads to evaluate (top 10 only)
2. Check CSV file format is correct
3. Increase timeout in agent options
4. Run quick_screening() first to filter

---

## 📞 Next Steps

1. **Run Lead Generation**: Get your first list of opportunities
2. **Review Outputs**: Understand what the agents found
3. **Evaluate Top Leads**: Deep analysis on highest potential
4. **Hand to Sales**: Provide qualified leads with business cases
5. **Track Results**: Monitor which leads convert
6. **Refine**: Adjust agent parameters based on real results

---

## 🔗 Related Files

- `lead_generation_agent.py` - Stage 1 agent
- `lead_evaluation_agent.py` - Stage 2 agent
- `lead_prompting_guide.md` - Guide to customizing prompts
- `QUICK_SUMMARY.md` - Overview of EEA database
- `Industrial_Emissions_Data_Guide.md` - Detailed data guide

---

**Questions?** Review the prompt customization in each agent file for advanced configuration options.
