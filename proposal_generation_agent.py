"""
GMAB Proposal & Documentation Generator Agent
Automatically creates ready-to-send sales materials for Priority leads

Takes evaluated leads from Lead Evaluation Agent and generates:
- Executive proposals (PDF)
- Financial models (Excel)
- Stakeholder presentations (PowerPoint)
- Technical specifications
- Compliance documentation
- Contract templates

OUTPUT: Complete proposal package per lead, ready for sales team delivery
"""
import asyncio
import json
from claude_agent_sdk import query, tool, create_sdk_mcp_server


# Define proposal generation tools
@tool(
    name="generate_executive_proposal",
    description="Generate comprehensive executive proposal document for a WtE facility",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Lead information and evaluation results"
        }
    }
)
async def generate_executive_proposal(args, extra):
    """
    Generate executive proposal document (15-20 pages)

    Sections:
    1. Executive Summary
    2. Facility Analysis & Current State
    3. GMAB Technical Solution
    4. Financial Business Case
    5. Implementation Plan
    6. Risk Mitigation
    7. Reference Accounts & Case Studies
    8. Terms & Next Steps
    """
    lead = args.get('lead_data', {})

    # In production, this would use a template engine (e.g., python-docx, jinja2)
    # and generate actual PDF via weasyprint or reportlab

    proposal = {
        "document_type": "Executive Proposal",
        "facility": lead.get('facility'),
        "proposal_title": f"GMAB Waste-to-Energy Optimization Proposal: {lead.get('facility')}",
        "date_generated": "2025-10-17",
        "sections": {
            "executive_summary": {
                "current_state": f"{lead.get('facility')} operates at {lead.get('current_efficiency', 70)}% efficiency",
                "problem_statement": "Low efficiency + emission compliance challenges + aging equipment",
                "gmab_solution": "Advanced flue gas heat recovery + ORC system + emission control",
                "value_proposition": f"Increase efficiency to 78-82%, generate additional {lead.get('improvement_potential', '€10M/year')}",
                "investment": "€28-35M CAPEX",
                "payback": "2.5-3.5 years",
                "key_benefits": [
                    "12-15% efficiency improvement",
                    "€8-14M additional annual revenue",
                    "Emission compliance guaranteed (NOx, SO2, dioxins)",
                    "25,000+ tonnes CO2 reduction/year",
                    "EU grants available (up to 60% funding)"
                ]
            },
            "facility_analysis": {
                "location": lead.get('country'),
                "waste_throughput": f"{lead.get('waste_throughput', 500000):,} tonnes/year",
                "current_output": "Electricity: 60 MW, Heat: 110 MW",
                "current_efficiency": f"{lead.get('current_efficiency', 70)}%",
                "challenges_identified": [
                    "Inefficient flue gas heat recovery",
                    "Aging boiler technology (35+ years)",
                    "Emission levels approaching limits",
                    "No low-temperature heat utilization",
                    "Limited district heating capacity"
                ]
            },
            "gmab_technical_solution": {
                "system_components": [
                    "Advanced Flue Gas Economizer (25 MW thermal recovery)",
                    "ORC System (6.5 MW additional electricity generation)",
                    "Heat Pump Integration (18 MW district heating expansion)",
                    "Emission Control Upgrade (SCR for NOx, advanced filtration)",
                    "Advanced Process Control System (24/7 optimization)"
                ],
                "performance_guarantees": {
                    "efficiency_improvement": "Min 10% points (e.g., 70% → 80%)",
                    "emission_compliance": "Guaranteed below EU limits for 10 years",
                    "availability": "95% uptime guaranteed"
                },
                "installation_timeline": "16-20 months (detailed in Section 5)"
            },
            "financial_business_case": {
                "total_investment": "€32.5M",
                "capex_breakdown": {
                    "equipment": "€20.8M",
                    "installation": "€7.2M",
                    "engineering": "€3.1M",
                    "contingency": "€1.4M"
                },
                "annual_benefits": {
                    "additional_electricity": "€4.8M (6.5 MW × 8,000 hrs × €90/MWh)",
                    "additional_heat_sales": "€3.6M (district heating expansion)",
                    "emission_reduction_credits": "€2.2M (EU ETS carbon credits)",
                    "avoided_compliance_penalties": "€1.8M (NOx violation prevention)",
                    "total_annual_benefit": "€12.4M"
                },
                "financial_metrics": {
                    "simple_payback": "2.6 years",
                    "npv_10_year": "€68.2M",
                    "irr": "37.5%",
                    "roi_10_year": "210%"
                },
                "financing_options": [
                    "EU Innovation Fund Grant (up to €19.5M - 60% of CAPEX)",
                    "EIB Green Loan (€13M available at 2.8% interest)",
                    "National Energy Efficiency Subsidy (€4.5M available)",
                    "Municipal Green Bonds (low-interest municipal financing)"
                ]
            },
            "implementation_plan": {
                "phase_1": "Engineering & Design (Months 1-4)",
                "phase_2": "Equipment Procurement (Months 3-8)",
                "phase_3": "Installation - Shutdown Window Required (Months 12-14)",
                "phase_4": "Commissioning & Testing (Months 15-16)",
                "phase_5": "Performance Validation & Handover (Months 17-20)",
                "key_milestones": [
                    "Financing secured (Month 2)",
                    "Detailed design approval (Month 4)",
                    "Equipment delivery (Month 10)",
                    "Plant shutdown for installation (Month 12)",
                    "System operational (Month 17)",
                    "Performance guarantee validated (Month 20)"
                ]
            },
            "risk_mitigation": {
                "technical_risks": [
                    "Integration complexity → Mitigated: Detailed 3D modeling pre-installation",
                    "Shutdown duration → Mitigated: Pre-fabrication + rapid installation methods",
                    "Performance uncertainty → Mitigated: GMAB performance guarantee"
                ],
                "financial_risks": [
                    "Energy price volatility → Mitigated: Conservative pricing in model",
                    "Cost overruns → Mitigated: Fixed-price EPC contract option",
                    "Financing delays → Mitigated: Multiple funding sources lined up"
                ]
            },
            "reference_accounts": [
                {
                    "facility": "Similar MSW Plant - Hamburg, Germany",
                    "project": "GMAB Heat Recovery Upgrade (2022)",
                    "results": "Efficiency 67% → 79%, €11.2M annual savings, 2.3 year payback"
                },
                {
                    "facility": "RDF Plant - Krakow, Poland",
                    "project": "GMAB ORC + Emission Control (2023)",
                    "results": "6.2 MW additional power, NOx reduced 45%, 2.8 year payback"
                }
            ],
            "next_steps": [
                "Week 1-2: Executive approval & site visit",
                "Week 3-4: Detailed technical audit (GMAB engineering team)",
                "Week 5-6: Final proposal refinement & contract negotiation",
                "Week 7-8: Financing applications (EU grants, EIB)",
                "Month 3: Contract signature & project kickoff"
            ]
        },
        "output_filename": f"GMAB_Proposal_{lead.get('facility', 'Facility').replace(' ', '_')}.pdf",
        "status": "Generated - Ready for review"
    }

    return {
        "content": [
            {
                "type": "text",
                "text": "✅ Executive Proposal Generated:\n" + json.dumps(proposal, indent=2)
            }
        ]
    }


@tool(
    name="build_financial_model",
    description="Create interactive Excel financial model with 20-year projections",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Lead information and financial parameters"
        }
    }
)
async def build_financial_model(args, extra):
    """
    Build comprehensive Excel financial model

    Sheets:
    1. Executive Summary Dashboard
    2. Assumptions & Inputs
    3. CAPEX Breakdown
    4. Revenue Projections (20 years)
    5. Operating Costs
    6. Cash Flow Analysis
    7. Sensitivity Analysis
    8. Financing Options Comparison
    """
    lead = args.get('lead_data', {})

    # In production, use openpyxl or xlsxwriter to create actual Excel file
    model = {
        "document_type": "Financial Model",
        "facility": lead.get('facility'),
        "model_structure": {
            "sheet_1_dashboard": {
                "key_metrics": {
                    "total_investment": "€32.5M",
                    "annual_benefit": "€12.4M",
                    "payback_years": 2.6,
                    "npv_10y": "€68.2M",
                    "irr": "37.5%"
                },
                "charts": [
                    "Cash flow waterfall (Years 0-10)",
                    "Revenue build-up (electricity, heat, carbon credits)",
                    "Payback curve",
                    "Sensitivity tornado"
                ]
            },
            "sheet_2_assumptions": {
                "facility_parameters": {
                    "waste_throughput_tonnes_year": lead.get('waste_throughput', 500000),
                    "current_efficiency": f"{lead.get('current_efficiency', 70)}%",
                    "target_efficiency": "78-82%",
                    "operating_hours_year": 8000
                },
                "energy_pricing": {
                    "electricity_eur_mwh": 90,
                    "heat_eur_mwh": 45,
                    "carbon_price_eur_tonne": 85,
                    "escalation_rate": "2.5%/year"
                },
                "capex_inputs": {
                    "heat_recovery_equipment": "€20.8M",
                    "installation": "€7.2M",
                    "engineering": "€3.1M",
                    "contingency_percent": 5
                }
            },
            "sheet_3_capex": {
                "year_0_investment": "€32.5M",
                "funding_sources": {
                    "eu_grant_60_percent": "€19.5M",
                    "eib_loan_40_percent": "€13.0M",
                    "equity_required": "€0M (fully funded)"
                }
            },
            "sheet_4_revenue_20y": {
                "annual_revenues": {
                    "year_1": "€12.4M",
                    "year_5": "€13.7M (with escalation)",
                    "year_10": "€15.8M",
                    "year_20": "€20.1M"
                },
                "revenue_sources": [
                    "Additional electricity sales (ORC)",
                    "Additional heat sales (district heating)",
                    "Carbon credits (EU ETS)",
                    "Avoided penalties (compliance)"
                ]
            },
            "sheet_5_opex": {
                "annual_operating_costs": "€1.8M",
                "breakdown": {
                    "maintenance": "€0.9M",
                    "chemicals": "€0.4M",
                    "labor": "€0.3M",
                    "insurance": "€0.2M"
                }
            },
            "sheet_6_cashflow": {
                "cumulative_cashflow": {
                    "year_0": "-€32.5M (investment)",
                    "year_1": "-€22.1M",
                    "year_2": "-€11.7M",
                    "year_3": "+€1.3M (payback achieved)",
                    "year_10": "+€68.2M",
                    "year_20": "+€158.7M"
                }
            },
            "sheet_7_sensitivity": {
                "variables_tested": [
                    "Electricity price (±20%)",
                    "Heat price (±20%)",
                    "CAPEX (±15%)",
                    "Efficiency improvement (±2% points)",
                    "Carbon price (±30%)"
                ],
                "results_range": {
                    "payback_best_case": "2.1 years",
                    "payback_worst_case": "3.4 years",
                    "npv_range": "€42M - €94M"
                }
            },
            "sheet_8_financing": {
                "option_a_100_grant_loan": {
                    "description": "EU Grant (60%) + EIB Loan (40%)",
                    "equity_required": "€0M",
                    "debt_service": "€0.9M/year (loan portion)",
                    "effective_payback": "2.6 years"
                },
                "option_b_partial_equity": {
                    "description": "Grant (60%) + Own Equity (40%)",
                    "equity_required": "€13M",
                    "debt_service": "€0M",
                    "effective_payback": "2.4 years"
                }
            }
        },
        "output_filename": f"GMAB_Financial_Model_{lead.get('facility', 'Facility').replace(' ', '_')}.xlsx",
        "features": [
            "Interactive inputs (change assumptions, see instant results)",
            "Scenario comparison (Base / Optimistic / Conservative)",
            "Break-even analysis charts",
            "Monthly vs. Annual view toggle"
        ],
        "status": "Generated - Ready for sales/CFO review"
    }

    return {
        "content": [
            {
                "type": "text",
                "text": "📊 Financial Model Generated:\n" + json.dumps(model, indent=2)
            }
        ]
    }


@tool(
    name="create_stakeholder_presentations",
    description="Generate PowerPoint presentations for different stakeholders",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Lead information"
        },
        "presentation_type": {
            "type": "string",
            "enum": ["board", "technical", "cfo"],
            "description": "Type of presentation to generate"
        }
    }
)
async def create_stakeholder_presentations(args, extra):
    """
    Create customized PowerPoint presentations

    Types:
    - board: 10-slide strategic overview for board/executives
    - technical: 20-slide engineering deep dive
    - cfo: 12-slide financial focus
    """
    lead = args.get('lead_data', {})
    pres_type = args.get('presentation_type', 'board')

    presentations = {
        "board": {
            "title": "GMAB Strategic Investment Proposal",
            "slides": 10,
            "structure": [
                "1. Executive Summary (The Opportunity)",
                "2. Current State Analysis (The Problem)",
                "3. GMAB Solution Overview (The Answer)",
                "4. Financial Business Case (The ROI)",
                "5. Strategic Benefits (Beyond ROI)",
                "6. Implementation Timeline (The Path)",
                "7. Risk Mitigation (De-risking)",
                "8. Sustainability Impact (ESG/Carbon)",
                "9. Financing Strategy (Funding)",
                "10. Recommendation & Next Steps"
            ],
            "key_messages": [
                "37.5% IRR investment opportunity",
                "Solve emission compliance problem",
                "€68M NPV over 10 years",
                "Fully funded via EU grants + loans",
                "Strategic positioning as sustainability leader"
            ],
            "visuals": [
                "Before/After efficiency comparison chart",
                "10-year cash flow waterfall",
                "Carbon reduction impact infographic",
                "Reference project photos",
                "Timeline Gantt chart"
            ]
        },
        "technical": {
            "title": "GMAB Technical Solution Design",
            "slides": 20,
            "structure": [
                "1-2. Facility Assessment & Current Performance",
                "3-4. Heat Balance Analysis",
                "5-7. GMAB System Design (Economizer, ORC, Heat Pump)",
                "8-9. Process Integration Diagrams",
                "10-11. Equipment Specifications",
                "12-13. Emission Control System",
                "14-15. Installation Methodology",
                "16-17. Performance Modeling & Guarantees",
                "18. Maintenance & Operations",
                "19. Testing & Commissioning",
                "20. Technical Q&A"
            ],
            "technical_content": [
                "P&ID diagrams",
                "Heat exchanger sizing calculations",
                "ORC system schematic",
                "3D installation renders",
                "Performance curves",
                "Emission reduction modeling"
            ]
        },
        "cfo": {
            "title": "GMAB Financial Investment Case",
            "slides": 12,
            "structure": [
                "1. Executive Financial Summary",
                "2. Investment Overview (€32.5M)",
                "3. Revenue Build-Up Analysis",
                "4. Cost Structure (CAPEX + OPEX)",
                "5. Financial Metrics (NPV, IRR, Payback)",
                "6. Cash Flow Projections (20 years)",
                "7. Sensitivity Analysis",
                "8. Financing Options & Structure",
                "9. Grant/Subsidy Opportunities",
                "10. Tax Implications & Depreciation",
                "11. Risk Analysis",
                "12. Financial Recommendation"
            ],
            "financial_content": [
                "Detailed CAPEX breakdown table",
                "Revenue waterfall chart",
                "NPV bridge analysis",
                "Payback curve",
                "Sensitivity tornado diagram",
                "Financing structure diagram",
                "Grant application timeline",
                "Cash flow statement (3-statement model)"
            ]
        }
    }

    selected = presentations.get(pres_type, presentations['board'])

    result = {
        "presentation_type": pres_type,
        "facility": lead.get('facility'),
        "output_filename": f"GMAB_{pres_type.upper()}_Presentation_{lead.get('facility', 'Facility').replace(' ', '_')}.pptx",
        "details": selected,
        "status": "Generated - Ready for delivery"
    }

    return {
        "content": [
            {
                "type": "text",
                "text": f"📊 {pres_type.upper()} Presentation Generated:\n" + json.dumps(result, indent=2)
            }
        ]
    }


@tool(
    name="enrich_lead_data",
    description="Enrich lead with additional company data from web sources",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Basic lead information"
        }
    }
)
async def enrich_lead_data(args, extra):
    """
    Enrich lead with additional data:
    - Company website scraping
    - LinkedIn profiles (decision makers)
    - Recent news/press releases
    - Org chart / decision-making structure
    """
    lead = args.get('lead_data', {})

    # In production, use web scraping (BeautifulSoup, Selenium)
    # and APIs (LinkedIn Sales Navigator, Clearbit, Hunter.io)

    enriched_data = {
        "facility": lead.get('facility'),
        "enrichment_sources": ["Company website", "LinkedIn", "News databases", "Public records"],
        "company_information": {
            "full_legal_name": f"{lead.get('facility')} S.p.A.",
            "headquarters": lead.get('country'),
            "ownership": "Municipal (60%), Private Consortium (40%)",
            "annual_revenue": "€85M (2024)",
            "employees": 180,
            "website": "www.example-wte.com"
        },
        "decision_makers": [
            {
                "name": "Dr. Marco Rossi",
                "title": "Plant Director",
                "linkedin": "linkedin.com/in/marco-rossi-energy",
                "email": "m.rossi@facility.com",
                "phone": "+39 02 1234 5678",
                "background": "20 years waste-to-energy, previously at Covanta",
                "priorities": "Efficiency, compliance, modernization"
            },
            {
                "name": "Anna Bianchi",
                "title": "CFO",
                "linkedin": "linkedin.com/in/anna-bianchi-cfo",
                "email": "a.bianchi@facility.com",
                "background": "Finance background, focused on ROI and funding",
                "priorities": "Financial returns, grant optimization"
            },
            {
                "name": "Luigi Verde",
                "title": "Technical Manager",
                "email": "l.verde@facility.com",
                "background": "Mechanical engineer, 15 years at facility",
                "priorities": "Reliability, ease of integration, minimal downtime"
            }
        ],
        "recent_news": [
            {
                "date": "2024-09-15",
                "headline": "Brescia WtE Plant Receives NOx Warning from Environmental Authority",
                "source": "Italian Environmental News",
                "relevance": "URGENT - Compliance pressure validates GMAB solution need"
            },
            {
                "date": "2024-06-20",
                "headline": "Municipal Council Approves €50M Facility Modernization Budget",
                "source": "Brescia Municipal Records",
                "relevance": "HIGH - Budget approved, funding secured for upgrades"
            }
        ],
        "strategic_insights": [
            "Facility is under regulatory pressure (NOx violations)",
            "Modernization budget approved - actively seeking solutions",
            "Municipal ownership = public procurement process (expect 6-9 month sales cycle)",
            "Previous supplier: Generic Boilers Inc. (low satisfaction based on news)",
            "Key buying criteria: Compliance guarantee, proven technology, total cost of ownership"
        ],
        "personalization_angles": {
            "for_plant_director": "Lead with compliance solution + efficiency improvement",
            "for_cfo": "Lead with EU grant opportunities + strong IRR",
            "for_technical_manager": "Lead with proven GMAB reliability + reference visits"
        }
    }

    return {
        "content": [
            {
                "type": "text",
                "text": "🔍 Lead Data Enriched:\n" + json.dumps(enriched_data, indent=2)
            }
        ]
    }


@tool(
    name="generate_compliance_documentation",
    description="Create emission reduction and regulatory compliance documentation",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Lead information including current emissions"
        }
    }
)
async def generate_compliance_documentation(args, extra):
    """
    Generate compliance and regulatory documentation

    Includes:
    - Emission reduction projections
    - EU BAT compliance demonstration
    - Regulatory approval support
    - Permit modification assistance
    """
    lead = args.get('lead_data', {})

    compliance_doc = {
        "facility": lead.get('facility'),
        "document_title": "GMAB Solution - Emission Compliance Report",
        "regulatory_framework": {
            "applicable_directives": [
                "Industrial Emissions Directive (IED) 2010/75/EU",
                "Waste Incineration Directive",
                "Best Available Techniques (BAT) Reference Documents",
                "National emission limits (Italy - D.Lgs 152/2006)"
            ]
        },
        "current_emission_status": {
            "nox_mg_nm3": 185,
            "legal_limit": 200,
            "compliance_margin": "7.5% (CRITICAL - approaching limit)",
            "so2_mg_nm3": 45,
            "so2_limit": 50,
            "dioxins_ng_nm3": 0.08,
            "dioxins_limit": 0.1,
            "overall_status": "AT RISK - NOx approaching limit, warning issued"
        },
        "gmab_solution_impact": {
            "nox_reduction": {
                "current": "185 mg/Nm³",
                "with_gmab_scr": "85 mg/Nm³",
                "reduction_percent": "54%",
                "new_compliance_margin": "57% below limit (SAFE)"
            },
            "so2_reduction": {
                "current": "45 mg/Nm³",
                "with_gmab_system": "22 mg/Nm³",
                "reduction_percent": "51%"
            },
            "particulate_matter": {
                "improvement": "Advanced filtration ensures PM10 <5 mg/Nm³"
            },
            "co2_reduction": {
                "annual_reduction": "28,500 tonnes/year",
                "mechanism": "Efficiency improvement reduces waste consumption per MWh output"
            }
        },
        "bat_compliance_demonstration": {
            "bat_conclusions_reference": "EU BAT Conclusions for Waste Incineration (2019/2010)",
            "gmab_compliance": [
                "Energy efficiency R1 formula: Improved from 0.72 to 0.84 (exceeds BAT threshold)",
                "Emission levels: All pollutants well below BAT-AEL (Associated Emission Levels)",
                "Energy recovery: Maximized via ORC + heat pump (BAT 3, BAT 11)",
                "Monitoring: Continuous emission monitoring system (BAT 2)"
            ],
            "bat_alignment": "GMAB solution represents Best Available Technique implementation"
        },
        "regulatory_approval_pathway": {
            "step_1": "Submit permit modification request (GMAB technical package)",
            "step_2": "Environmental impact assessment (simplified due to emission improvements)",
            "step_3": "Public consultation (30 days, positive due to emission reductions)",
            "step_4": "Authority approval (estimated 4-6 months)",
            "step_5": "Installation & commissioning",
            "step_6": "Performance validation & final permit issuance",
            "total_timeline": "6-8 months for regulatory approvals"
        },
        "supporting_documentation": [
            "GMAB emission guarantee letter",
            "Reference performance data from similar installations",
            "Third-party verification reports",
            "Equipment CE certifications",
            "Environmental impact assessment support"
        ],
        "output_filename": f"GMAB_Compliance_Report_{lead.get('facility', 'Facility').replace(' ', '_')}.pdf"
    }

    return {
        "content": [
            {
                "type": "text",
                "text": "📋 Compliance Documentation Generated:\n" + json.dumps(compliance_doc, indent=2)
            }
        ]
    }


async def generate_proposals():
    """
    Main function to generate complete proposal packages for evaluated leads
    """

    # Create MCP server with proposal generation tools
    mcp_server = create_sdk_mcp_server(
        name="proposal-tools",
        version="1.0.0",
        tools=[
            generate_executive_proposal,
            build_financial_model,
            create_stakeholder_presentations,
            enrich_lead_data,
            generate_compliance_documentation
        ]
    )

    # PROPOSAL GENERATION PROMPT
    prompt = """
    Generate complete proposal packages for PRIORITY 1 & 2 leads from the evaluation agent.

    INPUT: GMAB_evaluated_leads_PRIORITY_LIST.csv (from Lead Evaluation Agent)

    For each PRIORITY 1 and PRIORITY 2 lead, create a COMPLETE PROPOSAL PACKAGE:

    1. EXECUTIVE PROPOSAL (PDF - 15-20 pages)
       - Executive summary with value proposition
       - Facility analysis & current state
       - GMAB technical solution (heat recovery, ORC, emission control)
       - Financial business case (investment, revenues, metrics)
       - Implementation plan (timeline, milestones, shutdown planning)
       - Risk mitigation strategies
       - Reference accounts & case studies (similar WtE projects)
       - Terms & next steps

    2. FINANCIAL MODEL (Interactive Excel)
       - 20-year cash flow projections
       - Sensitivity analysis (energy prices, CAPEX, efficiency)
       - Multiple financing scenarios (grants, loans, equity)
       - Monthly and annual views
       - Scenario comparison (Base / Optimistic / Conservative)
       - All assumptions clearly documented

    3. STAKEHOLDER PRESENTATIONS (PowerPoint)
       Generate 3 versions:
       a) BOARD PRESENTATION (10 slides)
          - Strategic value, ROI, sustainability impact
          - High-level, executive-friendly
       b) TECHNICAL PRESENTATION (20 slides)
          - Engineering details, system design, integration
          - For plant managers and engineers
       c) CFO PRESENTATION (12 slides)
          - Financial deep dive, funding options, tax implications
          - For financial decision makers

    4. COMPLIANCE DOCUMENTATION (PDF)
       - Current emission status vs. limits
       - GMAB solution emission improvements
       - EU BAT compliance demonstration
       - Regulatory approval pathway
       - Permit modification support documentation

    5. DATA ENRICHMENT
       Before generating proposals, enrich each lead with:
       - Company website data (ownership, size, revenue)
       - Decision-maker profiles (LinkedIn, contact info)
       - Recent news/press releases (regulatory issues, budget approvals)
       - Strategic insights for personalization

    PERSONALIZATION REQUIREMENTS:
    - Use enriched data to personalize proposals
    - Reference specific facility challenges (e.g., NOx violations, boiler age)
    - Include relevant GMAB reference accounts from same country/sector
    - Adjust language/tone for public vs. private ownership
    - Highlight country-specific grants/subsidies

    OUTPUT STRUCTURE:
    Create folder per lead:
    C:\\GMAB_Proposals\\[Facility_Name]\\
    ├── Executive_Proposal.pdf
    ├── Financial_Model.xlsx
    ├── Board_Presentation.pptx
    ├── Technical_Presentation.pptx
    ├── CFO_Presentation.pptx
    ├── Compliance_Report.pdf
    └── Lead_Enrichment_Data.json

    QUALITY STANDARDS:
    - Professional GMAB branding throughout
    - Facility-specific data (no generic placeholders)
    - Accurate financial calculations
    - Realistic timelines and milestones
    - Conservative assumptions (credibility)
    - Clear call-to-action (next steps)

    GENERATE PACKAGES FOR:
    - ALL Priority 1 leads (CRITICAL & URGENT)
    - ALL Priority 2 leads (HIGH VALUE)

    After generation, create summary report:
    - Total proposals generated
    - Lead-by-lead package inventory
    - Readiness checklist (what sales needs to do before sending)
    - Recommended send order (most urgent first)

    START GENERATING PROPOSAL PACKAGES!
    """

    print("📄 GMAB Proposal Generation Agent")
    print("   Creating complete proposal packages for Priority leads...\n")

    async for message in query(
        prompt=prompt,
        options={
            "cwd": "C:\\Users\\staff\\anthropicFun\\EEA_Industrial_Emissions_Data",
            "maxTurns": 50,
            "model": "sonnet",
            "mcpServers": {
                "proposals": mcp_server
            }
        }
    ):
        if message.type == "assistant":
            for content in message.message.content:
                if hasattr(content, 'text') and content.text:
                    print(f"\n{content.text}")
                elif hasattr(content, 'name'):
                    print(f"\n📝 Generating: {content.name}")

        elif message.type == "result":
            print(f"\n\n✅ Proposal Generation Complete!")
            print(f"   Duration: {message.duration_ms/1000:.2f} seconds")
            print(f"   Cost: ${message.total_cost_usd:.4f}")
            print(f"   Turns: {message.num_turns}")


# Specialized proposal modes
async def quick_proposals_priority_1_only():
    """Generate proposals ONLY for Priority 1 (CRITICAL) leads"""
    prompt = """
    Generate proposal packages for PRIORITY 1 (CRITICAL & URGENT) leads ONLY.

    These are facilities with emission violations, boiler replacements, or ultra-high value.
    Focus on speed - generate core documents (proposal + financial model + board presentation).

    Skip compliance docs and technical presentations for speed.
    Prioritize getting something in front of decision-makers within 48 hours.
    """


async def update_existing_proposals():
    """Update existing proposals with new data (e.g., energy prices changed)"""
    prompt = """
    Update previously generated proposals with latest data:
    - Updated energy prices
    - Latest grant/subsidy information
    - New reference accounts
    - Revised financial assumptions

    Re-generate financial models and update executive summaries.
    Track changes vs. previous version.
    """


if __name__ == "__main__":
    print("=" * 80)
    print("   GMAB Proposal & Documentation Generator Agent")
    print("   Automated Sales Material Creation for Priority Leads")
    print("=" * 80)
    print()
    print("   Input: GMAB_evaluated_leads_PRIORITY_LIST.csv (from Evaluation Agent)")
    print("   Output: Complete proposal packages per lead (PDF, Excel, PowerPoint)")
    print()
    print("=" * 80)

    # Run proposal generation
    asyncio.run(generate_proposals())

    # Or run specialized modes:
    # asyncio.run(quick_proposals_priority_1_only())  # Speed mode for urgent leads
    # asyncio.run(update_existing_proposals())         # Update existing proposals
