# CLAUDE.md - EEA Industrial Emissions Data Project

## Project Identity

B2B sales intelligence system for GMAB/WET (www.SPIG-GMAB.com). Analyzes European Environment Agency industrial emissions data (~34,000 facilities) to generate leads for waste-to-energy and industrial emissions control equipment sales. Nordic market focus (SE, DK, FI, NO).

Read identity and voice context from: `C:/Users/staff/ObsidianVaults/WET knowledgebase/claude-context/`

## File Manifest

### Tier 1 - Read on every session (loaded automatically or critical reference)

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file. Project rules, manifest, safety boundaries |
| `data/processed/converted_database.db` | Main SQLite DB, 2007-2024 (v16). 771MB. DO NOT read directly - query with SQL |
| `docs/INDEX.md` | Documentation map with all doc paths and purposes |

### Tier 2 - Read when relevant to the task

| File/Dir | Purpose | When to read |
|----------|---------|--------------|
| `agents/lead_generation_agent.py` | Lead gen agent (scoring logic, WtE detection) | Modifying lead gen or scoring |
| `agents/lead_evaluation_agent.py` | Lead eval agent (ROI, competitive analysis) | Modifying evaluation logic |
| `agents/proposal_generation_agent.py` | Proposal generation agent | Modifying proposal output |
| `scripts/download/import_v16.py` | v16 data import (handles pollutant code mapping) | Data updates or import issues |
| `scripts/analysis/eea_emissions_analyzer.py` | Emissions analysis utilities | Querying emissions data |
| `docs/guides/CLAUDE.md` | Extended project guide (344 lines, agent architecture, scoring, troubleshooting) | Deep development context |
| `docs/data_structure/Industrial_Emissions_Data_Guide.md` | EEA database schema deep dive | Understanding table relationships |
| `docs/technical_reference/DIOXIN_APCD_REFERENCE_GUIDE.md` | Dioxin/APCD regulatory reference | Compliance analysis |
| `docs/market_analysis/WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md` | 2024-2025 WtE market analysis | Market context for leads |

### Tier 3 - Reference only

| File/Dir | Purpose |
|----------|---------|
| `docs/agents/AGENT_WORKFLOW_GUIDE.md` | Step-by-step agent execution |
| `docs/agents/lead_prompting_guide.md` | Agent prompt customization templates |
| `docs/data_structure/DATA_INSIGHTS_ANALYSIS.md` | Data patterns and analysis insights |
| `docs/market_analysis/WTE_2024_2025_MARKET_ANALYSIS_SUMMARY.md` | Comprehensive market trends |
| `docs/technical_reference/DIOXIN_CHANGES_SUMMARY.md` | Recent regulatory changes |
| `docs/technical_reference/EXTERNAL_DATA_CORRELATION_STRATEGY.md` | External data enrichment strategy |
| `scripts/reports/generate_nordic_leads_pdf.py` | PDF report generation for Nordic leads |
| `data/market/EU_ETS_Data/` | EU ETS allowance data 2005-2024 |
| `docs/archive/` | Archived docs (restrictions, implementation status, git worktrees) |
| `archive/` | Archived root artifacts (completion summaries, old presentations) |

## Directory Structure

```
EEA_Industrial_Emissions_Data/
  CLAUDE.md                    # Project manifest (this file)
  .env                         # Environment variables
  agents/                      # Three-agent AI system
    lead_generation_agent.py
    lead_evaluation_agent.py
    proposal_generation_agent.py
    run_agents_demo.py
  scripts/
    download/                  # Data download and import scripts
    analysis/                  # Emissions analysis and lead finding
    reports/                   # PDF/Excel/presentation generators
    tests/                     # Test scripts
  data/
    raw/                       # Original EEA Access database
    processed/                 # SQLite DB + CSV exports
    market/                    # Market data, EU ETS, PDFs
  docs/
    INDEX.md                   # Documentation map
    guides/                    # Getting started, project guide
    agents/                    # Agent workflow and prompting docs
    data_structure/            # EEA database schema docs
    market_analysis/           # WtE market intelligence
    technical_reference/       # Dioxin, APCD, regulatory docs
    archive/                   # Stale/historical docs
  outputs/                     # Generated reports, leads, proposals
  archive/                     # Historical project artifacts
```

## Database Rules

- **SQLite path**: `data/processed/converted_database.db`
- **Table names have numeric prefixes** - always quote them: `"2_ProductionFacility"`, `"2f_PollutantRelease"`
- **Join path**: `"3_ProductionInstallation"` joins to `"2_ProductionFacility"` via `Facility_INSPIRE_ID` (NOT to `"1_ProductionSite"` directly)
- **Country filtering**: Use `"2_ProductionFacility".countryCode`
- **WtE activity codes**: `5(b)` = incineration, `5(c)` = waste disposal. Danish codes: `5.2(a)` non-hazardous, `5.2(b)` hazardous
- **v16 pollutant code change (2022-2024)**: New codes like "as Hg" (was HGANDCOMPOUNDS), "as Teq" (was PCDD+PCDF(DIOXINS+FURANS)). `import_v16.py` maps these back. NOX/SOX/CO2/NH3 unchanged.

## Output Rules

1. **Always offer to save analysis results to Obsidian** vault at `C:/Users/staff/ObsidianVaults/WET knowledgebase/6-Projects/`
2. Write directly to the vault path (Obsidian MCP does NOT work - use file writes)
3. Use timestamped outputs for Excel/data files: `outputs/GMAB_*_YYYYMMDD.xlsx`
4. Facility analysis notes go to `6-Projects/` in the Obsidian vault
5. No emojis in any output unless explicitly requested

## Prompting Rules

### End-State Definitions
When asked to "analyze a facility" or "find leads", always clarify the desired output:
- Obsidian note? Excel file? Terminal summary? PDF report?
- Which country/region? Which pollutants? What time range?
- If ambiguous, ask before proceeding. Do not guess scope.

### Uncertainty Handling
- If a query could match multiple facilities, list the candidates and ask which one
- If data is missing or looks anomalous, flag it explicitly ("No NOx data reported for 2023 - this may indicate a reporting gap, not zero emissions")
- Never fabricate emission values. If data doesn't exist, say so
- When comparing to regulatory limits, cite which limit (BAT-AEL, national permit, IED Annex VI)

### Batch Operations
For multi-facility or multi-country analyses:
- Process in logical batches (by country, by pollutant type, by priority tier)
- Show progress after each batch
- Save intermediate results to avoid losing work on large queries

## Sub-Agent Guidance

Use sub-agents (Agent tool) for:
- **Explore agent**: Finding specific facilities, tables, or scripts in the codebase
- **General-purpose agent**: Running multi-step SQL analyses across multiple tables
- **Plan agent**: Designing new analysis workflows or agent modifications

Do NOT use sub-agents for:
- Simple single-table SQL queries (just run them directly)
- Reading a known file path (use Read tool)
- Writing to Obsidian (just use Write tool)

## Safety Rules

### No-Delete Policy
- NEVER delete data files under `data/`
- NEVER drop tables or modify schema of `converted_database.db`
- NEVER overwrite existing Obsidian notes without confirming first
- NEVER delete agent files. Create new versions instead if needed.

### Scope Boundaries
- This project targets WtE plants and industrial emissions facilities
- Do NOT modify files outside the project directory or Obsidian vault without asking
- Do NOT push to remote repositories without explicit permission
- Do NOT expose facility contact information or commercial pricing in outputs

### Sensitive Data
- The EEA database is public data, but GMAB commercial information (pricing, margins, client lists) is confidential
- Never include GMAB pricing or proprietary technology details in Obsidian notes or git-tracked files
- Facility INSPIRE IDs and emission data are public and can be shared freely
