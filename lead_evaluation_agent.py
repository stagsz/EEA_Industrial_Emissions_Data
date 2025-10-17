"""
GMAB Lead Evaluation Agent
Evaluates and prioritizes leads found by the Lead Generation Agent

Takes leads from lead generation and performs:
- Technical feasibility assessment
- Detailed ROI calculation
- Implementation complexity analysis
- Solution sizing and design
- Business case development
- Sales priority ranking
"""
import asyncio
import json
from claude_agent_sdk import query, tool, create_sdk_mcp_server


# Define evaluation tools
@tool(
    name="technical_feasibility_analysis",
    description="Analyze technical feasibility of waste heat recovery installation",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Lead information to analyze"
        }
    }
)
async def technical_feasibility_analysis(args, extra):
    """
    Evaluate technical feasibility of GMAB waste heat recovery system

    Considers:
    - Process temperature and flow rates
    - Space availability for equipment
    - Existing infrastructure compatibility
    - Regulatory/permit requirements
    - Integration complexity
    """
    lead = args.get('lead_data', {})

    # Mock technical analysis - Replace with actual engineering calculations
    analysis = {
        "facility": lead.get('facility'),
        "technical_feasibility_score": 85,  # 0-100
        "feasibility_rating": "HIGH",
        "key_factors": [
            "High process temperatures (>400°C) - excellent for heat recovery",
            "Continuous operation (24/7) - maximizes ROI",
            "Existing steam infrastructure - easy integration",
            "No space constraints identified"
        ],
        "challenges": [
            "Requires shutdown window for installation (2-3 weeks)",
            "Flue gas cleaning needed before heat exchanger",
            "Corrosion protection required due to sulfur content"
        ],
        "recommended_solution": "GMAB High-Temperature Heat Recovery Unit + ORC System",
        "system_sizing": {
            "thermal_capacity_MW": 45,
            "electricity_generation_MW": 6.5,
            "steam_generation_tonnes_hour": 38
        },
        "installation_timeline": "12-18 months (engineering + construction)",
        "implementation_complexity": "MEDIUM - Standard GMAB installation"
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(analysis, indent=2)
            }
        ]
    }


@tool(
    name="detailed_roi_calculation",
    description="Calculate detailed ROI and financial metrics for the project",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Lead information for ROI calculation"
        },
        "system_design": {
            "type": "object",
            "description": "Technical system design parameters"
        }
    }
)
async def detailed_roi_calculation(args, extra):
    """
    Detailed financial analysis for waste heat recovery project

    Calculates:
    - Capital expenditure (CAPEX)
    - Annual savings (energy cost reduction)
    - Operating costs (OPEX)
    - Payback period
    - NPV and IRR
    - Carbon credits value
    """
    lead = args.get('lead_data', {})

    # Mock financial analysis - Replace with actual financial models
    roi_analysis = {
        "facility": lead.get('facility'),
        "project_economics": {
            "total_capex_million_euro": 28.5,
            "breakdown_capex": {
                "equipment": 18.2,
                "installation": 6.3,
                "engineering": 2.8,
                "contingency": 1.2
            },
            "annual_savings_million_euro": 12.4,
            "breakdown_savings": {
                "energy_cost_reduction": 9.8,
                "carbon_credits_eu_ets": 1.9,
                "increased_efficiency_bonus": 0.7
            },
            "annual_opex_million_euro": 1.2,
            "net_annual_benefit_million_euro": 11.2
        },
        "financial_metrics": {
            "simple_payback_years": 2.5,
            "npv_million_euro_10y": 62.3,
            "irr_percent": 38.5,
            "roi_percent_10y": 218
        },
        "sensitivity_analysis": {
            "best_case_payback_years": 2.1,
            "worst_case_payback_years": 3.4,
            "key_risk": "Natural gas price volatility"
        },
        "financing_options": [
            "EU Innovation Fund (up to 60% grant)",
            "EIB Green Loan (2.5% interest)",
            "National energy efficiency subsidy (€5M available)"
        ],
        "carbon_impact": {
            "co2_reduction_tonnes_year": 28500,
            "eu_ets_value_million_euro_year": 1.9,
            "contribution_to_corporate_targets": "12% of facility carbon reduction goal"
        }
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(roi_analysis, indent=2)
            }
        ]
    }


@tool(
    name="competitive_analysis",
    description="Analyze competitive landscape and GMAB positioning",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Lead information"
        }
    }
)
async def competitive_analysis(args, extra):
    """
    Competitive intelligence and positioning analysis

    Evaluates:
    - Existing suppliers/relationships
    - Competitive threats
    - GMAB differentiators
    - Win probability
    - Pricing strategy
    """
    lead = args.get('lead_data', {})

    competitive_intel = {
        "facility": lead.get('facility'),
        "competitive_landscape": {
            "existing_supplier": "Generic Industrial Boilers GmbH",
            "current_solution": "Basic economizer (limited recovery)",
            "satisfaction_level": "MEDIUM - seeking upgrade",
            "contract_status": "No exclusive agreement"
        },
        "competitors": [
            {
                "name": "Competitor A (Heat Recovery Systems)",
                "strength": "Lower price point",
                "weakness": "Lower efficiency, no ORC capability",
                "threat_level": "MEDIUM"
            },
            {
                "name": "Competitor B (EnergySolutions Int'l)",
                "strength": "Established relationship in region",
                "weakness": "Generic solutions, not specialized in this industry",
                "threat_level": "LOW"
            }
        ],
        "gmab_advantages": [
            "Specialized steel industry experience - 50+ installations",
            "Advanced ORC technology - 15% higher efficiency",
            "Full turnkey solution including integration",
            "24/7 remote monitoring and optimization",
            "Local service center (250km away)",
            "Proven ROI - average 2.3 year payback in similar projects"
        ],
        "win_probability": "75%",
        "key_decision_factors": [
            "Proven technology and references",
            "Total cost of ownership (not just CAPEX)",
            "Speed of implementation",
            "Post-installation support"
        ],
        "pricing_strategy": "Value-based - emphasize superior ROI vs. competitors",
        "reference_accounts": [
            "Similar steel plant in Germany (2022) - €54M savings achieved",
            "Cement plant Poland (2021) - 2.1 year actual payback"
        ]
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(competitive_intel, indent=2)
            }
        ]
    }


@tool(
    name="sales_action_plan",
    description="Create detailed sales action plan and next steps",
    inputSchema={
        "lead_data": {
            "type": "object",
            "description": "Lead information"
        },
        "evaluation_results": {
            "type": "object",
            "description": "Technical and financial evaluation results"
        }
    }
)
async def sales_action_plan(args, extra):
    """
    Generate actionable sales strategy and engagement plan
    """
    lead = args.get('lead_data', {})

    action_plan = {
        "facility": lead.get('facility'),
        "priority_level": "🔥 PRIORITY 1 - IMMEDIATE ACTION",
        "target_contacts": [
            {
                "role": "Energy Manager",
                "approach": "Lead with ROI case study + carbon reduction",
                "talking_points": ["2.5 year payback", "€11M annual savings", "28,500 tonnes CO2/year"]
            },
            {
                "role": "Plant Director",
                "approach": "Strategic - operational efficiency + sustainability goals",
                "talking_points": ["Competitive advantage", "Future-proof operations", "EU compliance"]
            },
            {
                "role": "CFO",
                "approach": "Financial metrics + financing options",
                "talking_points": ["38% IRR", "€62M NPV", "EU grants available"]
            }
        ],
        "engagement_sequence": [
            {
                "step": 1,
                "action": "Initial email - share similar customer success story",
                "timeline": "Week 1",
                "owner": "Sales Rep - DACH Region"
            },
            {
                "step": 2,
                "action": "Discovery call - understand pain points and priorities",
                "timeline": "Week 2",
                "owner": "Sales Rep + Technical Pre-Sales"
            },
            {
                "step": 3,
                "action": "Site visit - energy audit and data collection",
                "timeline": "Week 3-4",
                "owner": "Applications Engineer"
            },
            {
                "step": 4,
                "action": "Proposal presentation - detailed ROI and technical design",
                "timeline": "Week 6",
                "owner": "Account Manager + Engineering Lead"
            },
            {
                "step": 5,
                "action": "Executive briefing - C-suite presentation on strategic value",
                "timeline": "Week 8",
                "owner": "Regional VP + Sustainability Expert"
            }
        ],
        "value_proposition": "Turn waste heat into €11M annual profit while cutting CO2 emissions by 28,500 tonnes",
        "objection_handling": {
            "capex_concern": "Financing available - EU grants + EIB loans reduce upfront investment by 60%",
            "technical_risk": "50+ proven installations in steel industry, guaranteed performance",
            "implementation_disruption": "Modular installation during planned maintenance window"
        },
        "success_metrics": {
            "target_close_date": "Q2 2026",
            "deal_size_million_euro": 28.5,
            "probability_weighted_value": 21.4
        }
    }

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(action_plan, indent=2)
            }
        ]
    }


async def evaluate_leads():
    """
    Main evaluation function - analyzes leads from lead generation agent
    """

    # Create MCP server with evaluation tools
    mcp_server = create_sdk_mcp_server(
        name="evaluation-tools",
        version="1.0.0",
        tools=[
            technical_feasibility_analysis,
            detailed_roi_calculation,
            competitive_analysis,
            sales_action_plan
        ]
    )

    # EVALUATION PROMPT
    prompt = """
    You are evaluating waste energy recovery leads for GMAB.

    INPUT: Leads from lead generation agent (file: GMAB_waste_energy_recovery_leads.csv)

    For each HIGH-PRIORITY lead (score 70+), perform comprehensive evaluation:

    1. TECHNICAL FEASIBILITY ANALYSIS
       - Process compatibility with GMAB systems
       - Temperature/flow rate suitability
       - Integration complexity
       - Space and infrastructure requirements
       - Regulatory considerations
       - Recommended GMAB solution (heat exchanger, ORC, steam generation)
       - System sizing (MW thermal capacity)
       - Installation timeline

    2. DETAILED ROI CALCULATION
       - Capital expenditure (CAPEX) estimate
       - Annual energy savings calculation
       - Operating costs (OPEX)
       - Carbon credits value (EU ETS)
       - Financial metrics: Payback, NPV, IRR, ROI
       - Sensitivity analysis (best/worst case)
       - Available financing options (EU grants, loans)
       - Carbon impact (tonnes CO2 reduced)

    3. COMPETITIVE ANALYSIS
       - Existing suppliers and solutions
       - Competitive threats assessment
       - GMAB competitive advantages
       - Win probability estimation
       - Key decision factors for this customer
       - Pricing strategy recommendation
       - Relevant reference accounts

    4. SALES ACTION PLAN
       - Priority ranking (1-5)
       - Target contacts (roles + approach)
       - Engagement sequence (steps + timeline)
       - Value proposition (customized for this facility)
       - Objection handling strategies
       - Success metrics and target close date

    PRIORITIZATION CRITERIA:
    - Highest ROI opportunities first
    - Technical feasibility (avoid high-risk projects)
    - Win probability (consider competitive landscape)
    - Strategic value (reference account potential, market entry)

    OUTPUT:
    - Create detailed evaluation report for each lead
    - Rank leads by overall opportunity score
    - Generate executive summary with top 10 targets
    - Export to 'GMAB_evaluated_leads_PRIORITY_LIST.csv'
    - Create individual business case PDFs for top 5 leads

    Focus on creating ACTIONABLE intelligence for the sales team.
    """

    print("📊 GMAB Lead Evaluation Agent")
    print("   Analyzing leads from lead generation...\n")

    async for message in query(
        prompt=prompt,
        options={
            "cwd": "C:\\Users\\staff\\anthropicFun\\EEA_Industrial_Emissions_Data",
            "maxTurns": 40,
            "model": "sonnet",
            "mcpServers": {
                "evaluation": mcp_server
            }
        }
    ):
        if message.type == "assistant":
            for content in message.message.content:
                if hasattr(content, 'text') and content.text:
                    print(f"\n{content.text}")
                elif hasattr(content, 'name'):
                    print(f"\n🔧 Evaluating: {content.name}")

        elif message.type == "result":
            print(f"\n\n✅ Evaluation Complete!")
            print(f"   Duration: {message.duration_ms/1000:.2f} seconds")
            print(f"   Cost: ${message.total_cost_usd:.4f}")
            print(f"   Turns: {message.num_turns}")


# Specialized evaluation modes
async def quick_screening():
    """Quick screening to filter out low-probability leads"""
    prompt = """
    Quickly screen all leads to filter out:
    - Low technical feasibility (<60% score)
    - Poor ROI (>5 year payback)
    - High competitive risk (incumbent with exclusive contract)
    - Geographic challenges (no GMAB service coverage)

    Focus sales resources on QUALIFIED opportunities only.
    Export: 'GMAB_qualified_leads_after_screening.csv'
    """


async def deep_dive_top_10():
    """Ultra-detailed analysis of top 10 leads"""
    prompt = """
    Perform DEEP DIVE analysis on top 10 leads:

    For each lead:
    1. Full energy audit simulation
    2. 3D equipment layout design
    3. Detailed 20-year financial model
    4. Complete competitive intelligence dossier
    5. Customized executive presentation deck
    6. Risk mitigation strategy
    7. Contract negotiation playbook

    Create complete sales package for immediate customer engagement.
    """


async def market_intelligence_report():
    """Generate market intelligence from evaluated leads"""
    prompt = """
    Analyze all evaluated leads to generate market intelligence:

    Market Insights:
    - Total addressable market size (€M)
    - Market segmentation (by industry, country, size)
    - Average deal size and sales cycle
    - Common objections and buying criteria
    - Competitive landscape mapping
    - Pricing benchmarks
    - Technology trends

    Strategic Recommendations:
    - Which sectors to prioritize (highest win rate + deal size)
    - Geographic expansion priorities
    - Product development opportunities
    - Partnership/acquisition targets
    - Sales team sizing and territories

    Export comprehensive market report for executive leadership.
    """


if __name__ == "__main__":
    print("=" * 75)
    print("   GMAB Lead Evaluation Agent")
    print("   Comprehensive Analysis of Waste Energy Recovery Opportunities")
    print("=" * 75)
    print()
    print("   Input: GMAB_waste_energy_recovery_leads.csv")
    print("   Output: GMAB_evaluated_leads_PRIORITY_LIST.csv")
    print()
    print("=" * 75)

    # Run evaluation
    asyncio.run(evaluate_leads())

    # Or run specialized evaluations:
    # asyncio.run(quick_screening())              # Fast filter of unqualified leads
    # asyncio.run(deep_dive_top_10())             # Detailed analysis of best leads
    # asyncio.run(market_intelligence_report())   # Strategic market insights
