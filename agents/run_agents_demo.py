"""
GMAB Agents Demonstration Script
Simulates what the three-agent system would find using mock data
"""
import json
from datetime import datetime
import pandas as pd

def simulate_lead_generation():
    """Simulate Agent 1: Lead Generation"""
    print("="*80)
    print("AGENT 1: LEAD GENERATION - Finding Waste-to-Energy Plants")
    print("="*80)
    print()

    # Mock WtE facilities (same as in the agents)
    facilities = [
        {
            "facility": "Amsterdam Waste Energy Center (AEB)",
            "facility_type": "Municipal Solid Waste Incinerator",
            "country": "Netherlands",
            "waste_throughput_tonnes_year": 550000,
            "current_efficiency_percent": 68,
            "flue_gas_temp_post_boiler": "185°C",
            "waste_heat_potential": "VERY HIGH - 25 MW thermal",
            "emission_levels": "NOx: 85 mg/Nm³, compliant",
            "compliance_status": "Compliant but optimizable",
            "urgency": "HIGH - Plant upgrade planned 2025-2026",
            "improvement_potential_million_euro": "8-12"
        },
        {
            "facility": "SYSAV Waste-to-Energy Plant",
            "facility_type": "MSW + RDF Incineration",
            "country": "Sweden (Malmö)",
            "waste_throughput_tonnes_year": 650000,
            "current_efficiency_percent": 72,
            "flue_gas_temp_post_boiler": "140°C",
            "waste_heat_potential": "HIGH - 18 MW thermal",
            "emission_levels": "Best-in-class, carbon neutral",
            "compliance_status": "Compliant",
            "urgency": "MEDIUM - Seeking optimization",
            "improvement_potential_million_euro": "5-7"
        },
        {
            "facility": "Brescia Waste Incinerator",
            "facility_type": "Municipal Waste-to-Energy",
            "country": "Italy",
            "waste_throughput_tonnes_year": 750000,
            "current_efficiency_percent": 65,
            "flue_gas_temp_post_boiler": "220°C",
            "waste_heat_potential": "VERY HIGH - 35 MW thermal",
            "emission_levels": "APPROACHING EU limits - NOx warning",
            "compliance_status": "At risk - <90 days to improve",
            "urgency": "CRITICAL - Boiler replacement 2025",
            "improvement_potential_million_euro": "12-18"
        },
        {
            "facility": "Berlin-Ruhleben Waste Incineration",
            "facility_type": "MSW Thermal Treatment",
            "country": "Germany",
            "waste_throughput_tonnes_year": 520000,
            "current_efficiency_percent": 70,
            "flue_gas_temp_post_boiler": "165°C",
            "waste_heat_potential": "HIGH - 22 MW thermal",
            "emission_levels": "Compliant",
            "compliance_status": "Compliant",
            "urgency": "HIGH - Energy prices driving efficiency",
            "improvement_potential_million_euro": "7-10"
        },
        {
            "facility": "Warsaw-Targówek Waste Treatment",
            "facility_type": "MSW + Biomass",
            "country": "Poland",
            "waste_throughput_tonnes_year": 480000,
            "current_efficiency_percent": 66,
            "flue_gas_temp_post_boiler": "195°C",
            "waste_heat_potential": "VERY HIGH - 28 MW thermal",
            "emission_levels": "Recent violation (dioxin) - corrected",
            "compliance_status": "History of issues",
            "urgency": "HIGH - Expansion project 2026",
            "improvement_potential_million_euro": "9-14"
        }
    ]

    # Score each facility
    scored_leads = []
    for facility in facilities:
        score = 0
        reasons = []

        # 1. Emission compliance (25 pts)
        if "APPROACHING" in facility["emission_levels"] or "warning" in facility["emission_levels"]:
            score += 20
            reasons.append("Emission compliance deadline imminent")
        elif "Recent violation" in facility["emission_levels"]:
            score += 15
            reasons.append("Recent emissions violations")

        # 2. Low efficiency (25 pts)
        eff = facility["current_efficiency_percent"]
        if eff < 67:
            score += 25
            reasons.append(f"Very low efficiency ({eff}%)")
        elif eff < 70:
            score += 20
            reasons.append(f"Low efficiency ({eff}%)")
        elif eff < 73:
            score += 15
            reasons.append(f"Moderate efficiency ({eff}%)")

        # 3. Waste heat potential (20 pts)
        if "VERY HIGH" in facility["waste_heat_potential"]:
            score += 20
            reasons.append("Very high waste heat recovery potential")
        elif "HIGH" in facility["waste_heat_potential"]:
            score += 15
            reasons.append("High waste heat recovery potential")

        # 4. Plant size (15 pts)
        throughput = facility["waste_throughput_tonnes_year"]
        if throughput > 600000:
            score += 15
            reasons.append(f"Large facility ({throughput:,} tonnes/year)")
        elif throughput > 500000:
            score += 12
            reasons.append(f"Medium-large facility ({throughput:,} tonnes/year)")

        # 5. Urgency (15 pts)
        if "CRITICAL" in facility["urgency"]:
            score += 15
            reasons.append("Critical timing - major upgrade planned")
        elif "HIGH" in facility["urgency"]:
            score += 10
            reasons.append("High urgency - upgrade planned")

        # Determine priority
        if score >= 80 or "APPROACHING" in facility["emission_levels"]:
            priority = 1
            priority_label = "CRITICAL & URGENT"
        elif score >= 70:
            priority = 2
            priority_label = "HIGH VALUE"
        elif score >= 60:
            priority = 3
            priority_label = "HIGH NEED"
        elif score >= 50:
            priority = 4
            priority_label = "GOOD OPPORTUNITY"
        else:
            priority = 5
            priority_label = "LONG TERM"

        scored_leads.append({
            **facility,
            "score": score,
            "priority": priority,
            "priority_label": priority_label,
            "reasons": reasons
        })

    # Sort by priority and score
    scored_leads.sort(key=lambda x: (x["priority"], -x["score"]))

    # Display results
    print(f"Found {len(scored_leads)} Waste-to-Energy plants with improvement opportunities\n")

    for i, lead in enumerate(scored_leads, 1):
        print(f"{i}. {lead['facility']}")
        print(f"   Country: {lead['country']}")
        print(f"   Priority: {lead['priority']} - {lead['priority_label']}")
        print(f"   Score: {lead['score']}/100")
        print(f"   Efficiency: {lead['current_efficiency_percent']}% (Improvement potential: €{lead['improvement_potential_million_euro']}M/year)")
        print(f"   Status: {lead['compliance_status']}")
        print(f"   Key factors: {', '.join(lead['reasons'][:2])}")
        print()

    # Save to Excel simulation
    df = pd.DataFrame(scored_leads)
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"GMAB_WasteToEnergy_Leads_Demo_{timestamp}.xlsx"

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df[df['priority'] == 1].to_excel(writer, sheet_name='PRIORITY 1 - CRITICAL', index=False)
        df[df['priority'] == 2].to_excel(writer, sheet_name='PRIORITY 2 - HIGH VALUE', index=False)
        df[df['priority'] == 3].to_excel(writer, sheet_name='PRIORITY 3 - HIGH NEED', index=False)
        df[df['priority'] == 4].to_excel(writer, sheet_name='PRIORITY 4 - GOOD', index=False)
        df[df['priority'] == 5].to_excel(writer, sheet_name='PRIORITY 5 - LONG TERM', index=False)
        df.to_excel(writer, sheet_name='ALL LEADS', index=False)

    print(f"[SAVED] Results exported to: {filename}")
    print()

    return scored_leads

def simulate_lead_evaluation(leads):
    """Simulate Agent 2: Lead Evaluation"""
    print("="*80)
    print("AGENT 2: LEAD EVALUATION - Deep Analysis of Priority 1-2 Leads")
    print("="*80)
    print()

    # Filter Priority 1-2 leads
    priority_leads = [l for l in leads if l['priority'] <= 2]

    print(f"Evaluating {len(priority_leads)} high-priority leads\n")

    evaluated_leads = []

    for lead in priority_leads:
        print(f"Evaluating: {lead['facility']}")
        print("-" * 60)

        # Technical Feasibility
        tech_feasibility = {
            "score": 85,
            "rating": "HIGH",
            "system_sizing_MW": 45,
            "installation_timeline": "12-18 months",
            "complexity": "MEDIUM"
        }
        print(f"  Technical Feasibility: {tech_feasibility['rating']} ({tech_feasibility['score']}/100)")
        print(f"  Recommended System: {tech_feasibility['system_sizing_MW']} MW thermal capacity")

        # Financial Analysis
        roi_analysis = {
            "capex_million_euro": 28.5,
            "annual_savings_million_euro": 12.4,
            "payback_years": 2.5,
            "npv_10y_million_euro": 62.3,
            "irr_percent": 38.5
        }
        print(f"  CAPEX: €{roi_analysis['capex_million_euro']}M")
        print(f"  Annual Savings: €{roi_analysis['annual_savings_million_euro']}M/year")
        print(f"  Payback: {roi_analysis['payback_years']} years")
        print(f"  IRR: {roi_analysis['irr_percent']}%")

        # Competitive Analysis
        competitive = {
            "win_probability": "75%",
            "gmab_advantages": [
                "Specialized WtE experience (50+ installations)",
                "Advanced ORC technology (15% higher efficiency)",
                "Local service center"
            ]
        }
        print(f"  Win Probability: {competitive['win_probability']}")
        print(f"  Key Advantage: {competitive['gmab_advantages'][0]}")

        # Sales Action Plan
        action_plan = {
            "priority_level": "PRIORITY 1 - IMMEDIATE ACTION" if lead['priority'] == 1 else "PRIORITY 2 - ACTIVE PURSUIT",
            "target_close": "Q2 2026",
            "next_steps": [
                "Initial email with similar customer success story",
                "Discovery call with Energy Manager",
                "Site visit and energy audit",
                "Proposal presentation",
                "Executive briefing"
            ]
        }
        print(f"  Action Priority: {action_plan['priority_level']}")
        print(f"  Target Close: {action_plan['target_close']}")
        print(f"  Next Step: {action_plan['next_steps'][0]}")
        print()

        evaluated_leads.append({
            **lead,
            **tech_feasibility,
            **roi_analysis,
            **competitive,
            **action_plan
        })

    # Save evaluation results
    df = pd.DataFrame(evaluated_leads)
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"GMAB_Evaluated_Leads_Demo_{timestamp}.xlsx"

    df.to_excel(filename, sheet_name='PRIORITY LIST', index=False)
    print(f"[SAVED] Evaluation results exported to: {filename}")
    print()

    return evaluated_leads

def simulate_proposal_generation(evaluated_leads):
    """Simulate Agent 3: Proposal Generation"""
    print("="*80)
    print("AGENT 3: PROPOSAL GENERATION - Creating Complete Packages")
    print("="*80)
    print()

    # Generate proposals for top 3 leads
    top_leads = evaluated_leads[:3]

    print(f"Generating proposal packages for top {len(top_leads)} leads\n")

    for i, lead in enumerate(top_leads, 1):
        print(f"{i}. {lead['facility']}")
        print("-" * 60)
        print(f"   Creating proposal package...")

        documents = [
            "Executive Proposal (15 pages PDF)",
            "Financial Model (Interactive Excel with 20-year projections)",
            "Board Presentation (10 slides - Strategic value)",
            "Technical Presentation (20 slides - Engineering details)",
            "CFO Presentation (12 slides - Financial metrics)",
            "Compliance Report (EU IED compliance pathway)",
            "Lead Enrichment Data (Company research, decision-makers)"
        ]

        for doc in documents:
            print(f"   [OK] Generated: {doc}")

        folder = f"C:\\GMAB_Proposals\\{lead['facility'].replace(' ', '_')}\\"
        print(f"   [SAVED] Package location: {folder}")
        print()

    print("[DONE] All proposal packages generated!")
    print()

def main():
    """Run the complete three-agent demonstration"""
    print()
    print("="*80)
    print(" "*25 + "GMAB AI AGENT SYSTEM")
    print(" "*10 + "Waste-to-Energy Plant Optimization Lead Pipeline")
    print("="*80)
    print()
    print("Company: SPIG-GMAB (www.SPIG-GMAB.com)")
    print("Mission: 'TOGETHER WE SUCCEED, TOGETHER WE GO GREEN'")
    print()
    print("This demonstration shows what the three-agent system would find")
    print("from the EEA Industrial Emissions Database (34,000+ facilities)")
    print()
    input("Press Enter to start Agent 1: Lead Generation...")
    print()

    # Run Agent 1
    leads = simulate_lead_generation()

    input("Press Enter to start Agent 2: Lead Evaluation...")
    print()

    # Run Agent 2
    evaluated = simulate_lead_evaluation(leads)

    input("Press Enter to start Agent 3: Proposal Generation...")
    print()

    # Run Agent 3
    simulate_proposal_generation(evaluated)

    # Final summary
    print("="*80)
    print("PIPELINE SUMMARY")
    print("="*80)
    print()
    print(f"Total WtE Plants Found: {len(leads)}")
    print(f"Priority 1 (Critical): {len([l for l in leads if l['priority'] == 1])}")
    print(f"Priority 2 (High Value): {len([l for l in leads if l['priority'] == 2])}")
    print(f"Leads Evaluated: {len(evaluated)}")
    print(f"Proposal Packages Generated: 3")
    print()
    print(f"Total Pipeline Value: €{sum([float(l['improvement_potential_million_euro'].split('-')[0]) for l in leads[:3]])}-{sum([float(l['improvement_potential_million_euro'].split('-')[1]) for l in leads[:3]])}M/year")
    print()
    print("[SUCCESS] GMAB Three-Agent System demonstration complete!")
    print()

if __name__ == "__main__":
    main()
