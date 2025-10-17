"""
Simple Lead Evaluator for GMAB Waste-to-Energy Projects
Takes leads from waste_to_energy_lead_finder.py and adds detailed evaluation
No SDK required - pure pandas/Excel analysis
"""
import pandas as pd
import numpy as np
from datetime import datetime
import glob

print("=" * 80)
print("   GMAB Lead Evaluator - Detailed Analysis")
print("   'TOGETHER WE SUCCEED, TOGETHER WE GO GREEN'")
print("=" * 80)

# Find the latest leads file
print("\n📂 Looking for leads file...")
leads_files = glob.glob('GMAB_WasteToEnergy_Leads_*.xlsx')
if not leads_files:
    print("❌ No leads file found! Run waste_to_energy_lead_finder.py first.")
    exit(1)

latest_file = max(leads_files)
print(f"✅ Found: {latest_file}")

# Load leads
print("\n📊 Loading leads...")
leads_df = pd.read_excel(latest_file, sheet_name='All Qualified Leads')
print(f"✅ Loaded {len(leads_df)} leads")

# Add evaluation metrics
print("\n⚡ Adding evaluation metrics...")

def evaluate_technical_feasibility(row):
    """Score technical feasibility (0-100)"""
    score = 50  # Base score
    reasons = []
    
    # Energy input indicates plant size
    energy = row.get('Energy Input (TJ/year)', 0)
    if pd.notna(energy):
        if energy > 2000:
            score += 25
            reasons.append("Very large plant - excellent economies of scale")
        elif energy > 1000:
            score += 20
            reasons.append("Large plant - good project size")
        elif energy > 500:
            score += 10
            reasons.append("Medium plant - viable project")
    
    # Emissions indicate active combustion process
    emissions = row.get('Emissions (tonnes/year)', 0)
    if pd.notna(emissions) and emissions > 0:
        score += 15
        reasons.append("Active waste incineration confirmed")
    
    # Activity type
    activity = str(row.get('Activity Type', ''))
    if 'incineration' in activity.lower():
        score += 10
        reasons.append("Waste incineration facility - ideal for GMAB")
    
    return min(score, 100), '; '.join(reasons) if reasons else 'Standard evaluation'

def calculate_estimated_capex(row):
    """Estimate capital expenditure based on plant size"""
    energy = row.get('Energy Input (TJ/year)', 1000)
    if pd.isna(energy) or energy == 0:
        energy = 1000
    
    # Rule of thumb: €1-2M per MW thermal capacity
    # 1 TJ = 0.278 MW continuous
    mw_thermal = energy * 0.278
    capex_low = mw_thermal * 0.8  # Million EUR
    capex_high = mw_thermal * 1.5  # Million EUR
    
    return capex_low, capex_high, mw_thermal

def estimate_annual_savings(row):
    """Estimate annual energy cost savings"""
    energy = row.get('Energy Input (TJ/year)', 1000)
    if pd.isna(energy) or energy == 0:
        energy = 1000
    
    # Assume 15-25% waste heat recovery potential
    # Energy price: €150/MWh average
    mwh_year = energy * 277.8  # Convert TJ to MWh
    recoverable_mwh = mwh_year * 0.20  # 20% recovery rate
    savings_million = (recoverable_mwh * 150) / 1_000_000
    
    return savings_million

def calculate_roi_metrics(capex_avg, annual_savings):
    """Calculate ROI metrics"""
    if annual_savings <= 0 or capex_avg <= 0:
        return None, None, None
    
    payback_years = capex_avg / annual_savings
    roi_10y = ((annual_savings * 10 - capex_avg) / capex_avg) * 100
    irr_approx = (annual_savings / capex_avg) * 100  # Simplified IRR
    
    return payback_years, roi_10y, irr_approx

def estimate_carbon_reduction(row):
    """Estimate CO2 reduction potential"""
    energy = row.get('Energy Input (TJ/year)', 1000)
    if pd.isna(energy) or energy == 0:
        energy = 1000
    
    # Assume 15% efficiency improvement = 15% fuel reduction
    # Natural gas: 56 kg CO2/GJ
    co2_reduction_tonnes = energy * 1000 * 0.15 * 0.056
    
    # EU ETS carbon price: ~€80/tonne
    carbon_value_million = (co2_reduction_tonnes * 80) / 1_000_000
    
    return co2_reduction_tonnes, carbon_value_million

def assign_priority_level(row):
    """Assign priority 1-5 based on comprehensive factors"""
    score = row.get('Lead Score', 0)
    capex = row.get('CAPEX (Mid, M€)', 999)
    payback = row.get('Payback (years)', 10)
    
    # Priority 1: High score + good payback
    if score >= 60 and payback < 3:
        return 1, "🔥 CRITICAL - High value + Quick payback"
    
    # Priority 2: Good metrics overall
    elif score >= 50 and payback < 4:
        return 2, "⚡ HIGH - Strong business case"
    
    # Priority 3: Acceptable project
    elif score >= 40 and payback < 5:
        return 3, "✓ MEDIUM - Good opportunity"
    
    # Priority 4: Lower priority but viable
    elif score >= 35:
        return 4, "○ LOW - Consider for pipeline"
    
    # Priority 5: Long-term nurture
    else:
        return 5, "− NURTURE - Future potential"

# Apply evaluation functions
print("   Calculating technical feasibility...")
leads_df[['Technical Feasibility Score', 'Feasibility Notes']] = leads_df.apply(
    lambda row: pd.Series(evaluate_technical_feasibility(row)), axis=1
)

print("   Estimating CAPEX...")
leads_df[['CAPEX Low (M€)', 'CAPEX High (M€)', 'Thermal Capacity (MW)']] = leads_df.apply(
    lambda row: pd.Series(calculate_estimated_capex(row)), axis=1
)
leads_df['CAPEX (Mid, M€)'] = (leads_df['CAPEX Low (M€)'] + leads_df['CAPEX High (M€)']) / 2

print("   Estimating annual savings...")
leads_df['Annual Savings (M€)'] = leads_df.apply(estimate_annual_savings, axis=1)

print("   Calculating ROI metrics...")
leads_df[['Payback (years)', 'ROI 10y (%)', 'IRR Approx (%)']] = leads_df.apply(
    lambda row: pd.Series(calculate_roi_metrics(
        row['CAPEX (Mid, M€)'], 
        row['Annual Savings (M€)']
    )), axis=1
)

print("   Estimating carbon impact...")
leads_df[['CO2 Reduction (tonnes/year)', 'Carbon Value (M€/year)']] = leads_df.apply(
    lambda row: pd.Series(estimate_carbon_reduction(row)), axis=1
)

print("   Assigning priority levels...")
leads_df[['Priority Level', 'Priority Description']] = leads_df.apply(
    lambda row: pd.Series(assign_priority_level(row)), axis=1
)

# Calculate competitive win probability
def estimate_win_probability(row):
    """Estimate probability of winning the deal"""
    base_prob = 50
    
    # Strong business case increases win rate
    if row.get('Payback (years)', 10) < 3:
        base_prob += 20
    elif row.get('Payback (years)', 10) < 4:
        base_prob += 10
    
    # High technical feasibility
    if row.get('Technical Feasibility Score', 0) > 80:
        base_prob += 15
    
    # Priority country (established presence)
    if row.get('Country') in ['DE', 'NL', 'IT', 'SE']:
        base_prob += 10
    
    return min(base_prob, 95)

leads_df['Win Probability (%)'] = leads_df.apply(estimate_win_probability, axis=1)
leads_df['Probability Weighted Value (M€)'] = (
    leads_df['CAPEX (Mid, M€)'] * leads_df['Win Probability (%)'] / 100
)

# Sort by priority and opportunity value
leads_df = leads_df.sort_values(['Priority Level', 'Probability Weighted Value (M€)'], 
                                  ascending=[True, False])

print(f"✅ Evaluation complete!\n")

# Export enhanced leads file
output_file = f'GMAB_Evaluated_Leads_{datetime.now().strftime("%Y%m%d")}.xlsx'
print(f"📤 Exporting to: {output_file}")

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Priority 1 - Critical
    priority_1 = leads_df[leads_df['Priority Level'] == 1]
    if len(priority_1) > 0:
        priority_1.to_excel(writer, sheet_name='P1 - CRITICAL', index=False)
    
    # Priority 2 - High
    priority_2 = leads_df[leads_df['Priority Level'] == 2]
    if len(priority_2) > 0:
        priority_2.to_excel(writer, sheet_name='P2 - HIGH', index=False)
    
    # Priority 3 - Medium
    priority_3 = leads_df[leads_df['Priority Level'] == 3]
    if len(priority_3) > 0:
        priority_3.to_excel(writer, sheet_name='P3 - MEDIUM', index=False)
    
    # All evaluated leads
    leads_df.to_excel(writer, sheet_name='All Evaluated Leads', index=False)
    
    # Summary statistics
    summary_data = {
        'Metric': [
            'Total Leads',
            'Priority 1 (Critical)',
            'Priority 2 (High)',
            'Priority 3 (Medium)',
            'Total Pipeline Value (M€)',
            'Weighted Pipeline Value (M€)',
            'Average Payback (years)',
            'Total CO2 Reduction Potential (tonnes/year)',
            'Countries Covered'
        ],
        'Value': [
            len(leads_df),
            len(priority_1),
            len(priority_2),
            len(priority_3),
            f"{leads_df['CAPEX (Mid, M€)'].sum():.1f}",
            f"{leads_df['Probability Weighted Value (M€)'].sum():.1f}",
            f"{leads_df['Payback (years)'].mean():.1f}",
            f"{leads_df['CO2 Reduction (tonnes/year)'].sum():.0f}",
            leads_df['Country'].nunique()
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)

print(f"✅ Exported successfully!")

# Print summary
print("\n" + "=" * 80)
print("📊 EVALUATION SUMMARY")
print("=" * 80)
print(f"\n✅ Total Leads Evaluated: {len(leads_df)}")
print(f"\n🔥 Priority Breakdown:")
print(f"   Priority 1 (CRITICAL):  {len(priority_1)} leads")
print(f"   Priority 2 (HIGH):      {len(priority_2)} leads")
print(f"   Priority 3 (MEDIUM):    {len(priority_3)} leads")

print(f"\n💰 Financial Summary:")
print(f"   Total Pipeline Value:    €{leads_df['CAPEX (Mid, M€)'].sum():.1f}M")
print(f"   Weighted Value:          €{leads_df['Probability Weighted Value (M€)'].sum():.1f}M")
print(f"   Avg Annual Savings:      €{leads_df['Annual Savings (M€)'].mean():.1f}M")
print(f"   Avg Payback Period:      {leads_df['Payback (years)'].mean():.1f} years")

print(f"\n🌍 Environmental Impact:")
print(f"   Total CO2 Reduction:     {leads_df['CO2 Reduction (tonnes/year)'].sum():,.0f} tonnes/year")
print(f"   Carbon Credit Value:     €{leads_df['Carbon Value (M€/year)'].sum():.2f}M/year")

print(f"\n🎯 Top 5 Opportunities:")
print("=" * 80)
top_5_cols = ['Facility Name', 'Country', 'Priority Level', 'CAPEX (Mid, M€)', 
              'Payback (years)', 'Win Probability (%)']
available_cols = [col for col in top_5_cols if col in leads_df.columns]
if available_cols:
    print(leads_df[available_cols].head(5).to_string(index=False))

print("\n" + "=" * 80)
print("✅ Lead evaluation complete!")
print(f"📁 Results saved to: {output_file}")
print("=" * 80)
