"""
GMAB Waste-to-Energy Lead Finder
Direct data analysis without SDK dependency
NOW WITH EU EMISSION COMPLIANCE CHECKING (based on restrictions.md)
"""
import pandas as pd
import numpy as np
from datetime import datetime
from emission_compliance_checker import EmissionComplianceChecker, ComplianceStatus

print("=" * 80)
print("   GMAB Waste-to-Energy Plant Optimization Lead Finder")
print("   'TOGETHER WE SUCCEED, TOGETHER WE GO GREEN'")
print("=" * 80)

# Load data
print("\nLoading data files...")
facilities = pd.read_csv('converted_csv/2_ProductionFacility.csv', low_memory=False)
energy = pd.read_csv('converted_csv/4d_EnergyInput.csv', low_memory=False)
emissions = pd.read_csv('converted_csv/4e_EmissionsToAir.csv', low_memory=False)
pollutant_releases = pd.read_csv('converted_csv/2f_PollutantRelease.csv', low_memory=False)
installations = pd.read_csv('converted_csv/3_ProductionInstallation.csv', low_memory=False)
install_parts = pd.read_csv('converted_csv/4_ProductionInstallationPart.csv', low_memory=False)

print(f"Loaded {len(facilities):,} facilities")
print(f"Loaded {len(energy):,} energy records")
print(f"Loaded {len(emissions):,} emission records")
print(f"Loaded {len(pollutant_releases):,} pollutant release records")

# Initialize EU Compliance Checker
print("\nInitializing EU Emission Compliance Checker (based on restrictions.md)...")
compliance_checker = EmissionComplianceChecker()
print("Compliance checker ready - checking against Euro 7, BAT-AEL, and IED standards")

# Filter for waste incineration facilities
print("\n Identifying waste-to-energy facilities...")
waste_activities = [
    'Installations for the incineration of non-hazardous waste',
    'Installations for the disposal of non-hazardous waste',
    'Installations for the recovery or disposal of hazardous waste'
]

wte_facilities = facilities[
    facilities['mainActivityName'].str.contains('incineration', case=False, na=False)
]

print(f" Found {len(wte_facilities)} waste incineration facilities")
print(f"\nCountries with WtE facilities:")
print(wte_facilities['countryCode'].value_counts().head(10))

# Get latest year data
latest_year = energy['reportingYear'].max()
print(f"\n Latest reporting year: {latest_year}")

# Merge data
print("\n Merging facility, energy, and emissions data...")
# Match facilities to installations
merged = wte_facilities.merge(
    installations,
    left_on='Facility_INSPIRE_ID',
    right_on='Parent_Facility_INSPIRE_ID',
    how='left'
)

# Add energy data
merged = merged.merge(
    energy[energy['reportingYear'] == latest_year],
    left_on='Installation_INSPIRE_ID',
    right_on='Installation_Part_INSPIRE_ID',
    how='left'
)

# Add emissions data
merged = merged.merge(
    emissions[emissions['reportingYear'] == latest_year].groupby('Installation_Part_INSPIRE_ID').agg({
        'totalPollutantQuantityTNE': 'sum'
    }).reset_index(),
    on='Installation_Part_INSPIRE_ID',
    how='left'
)

print(f" Merged dataset: {len(merged)} records")

# Calculate lead scores with EU COMPLIANCE CHECKING
print("\n Calculating lead scores with EU emission compliance analysis...")

def score_facility_with_compliance(row):
    """
    Score a facility based on GMAB criteria + EU COMPLIANCE VIOLATIONS
    Integrates restrictions.md emission standards for regulatory-driven sales
    """
    base_score = 0
    reasons = []

    # Prepare facility data for compliance check
    facility_data = {
        'nameOfFeature': row.get('nameOfFeature', 'Unknown'),
        'countryCode': row.get('countryCode', 'EU'),
        'mainActivityName': row.get('mainActivityName', ''),
        'energyInputTJ': row.get('energyInputTJ', 0)
    }

    # Get emissions data for this facility
    facility_id = row.get('Facility_INSPIRE_ID')
    if pd.notna(facility_id):
        facility_emissions = pollutant_releases[
            pollutant_releases['Facility_INSPIRE_ID'] == facility_id
        ]
    else:
        facility_emissions = pd.DataFrame()

    # CHECK EU COMPLIANCE (highest priority scoring factor)
    compliance_score = 0
    compliance_reason = ""

    if not facility_emissions.empty and len(facility_emissions) > 0:
        try:
            status, violations, compliance_score, detailed_reason = compliance_checker.check_facility_compliance(
                facility_data,
                facility_emissions
            )
            compliance_reason = detailed_reason

            # Compliance violations are the PRIMARY scoring factor
            if compliance_score > 0:
                reasons.append(f" EU COMPLIANCE: {compliance_score} points")
        except Exception as e:
            # If compliance check fails, continue with basic scoring
            compliance_score = 0
            compliance_reason = f"Compliance check unavailable: {str(e)}"

    # SECONDARY SCORING FACTORS (only if no major compliance issues)

    # Energy consumption (higher = larger plant = better opportunity)
    energy_tj = row.get('energyInputTJ', 0)
    if pd.notna(energy_tj) and energy_tj > 1000:
        base_score += 20
        reasons.append(f"Large facility: {energy_tj:,.0f} TJ/year energy input")
    elif pd.notna(energy_tj) and energy_tj > 500:
        base_score += 15
        reasons.append(f"Medium facility: {energy_tj:,.0f} TJ/year energy input")

    # Total emissions (indicates facility size/waste throughput)
    emissions_tne = row.get('totalPollutantQuantityTNE', 0)
    if pd.notna(emissions_tne) and emissions_tne > 1000:
        base_score += 15
        reasons.append(f"High waste throughput: {emissions_tne:,.0f} tonnes emissions/year")
    elif pd.notna(emissions_tne) and emissions_tne > 100:
        base_score += 10
        reasons.append(f"Medium waste throughput: {emissions_tne:,.0f} tonnes emissions/year")

    # Country priority (GMAB market focus)
    priority_countries = ['DE', 'NL', 'IT', 'SE', 'PL', 'FR', 'ES', 'DK']
    if row.get('countryCode') in priority_countries:
        base_score += 10
        reasons.append(f"Priority market: {row.get('countryCode')}")

    # Facility type confirmation
    if 'incineration' in str(row.get('mainActivityName', '')).lower():
        base_score += 5
        reasons.append("Waste-to-energy facility (WtE)")

    # FINAL SCORE: Compliance score takes precedence
    # If there's a compliance violation, it dominates the score
    # Otherwise use base score
    if compliance_score >= 50:
        # Major compliance issue - this becomes the lead score
        final_score = min(compliance_score, 100)
        final_reason = compliance_reason
    else:
        # No major compliance issues - combine scores
        final_score = min(base_score + compliance_score, 100)
        if compliance_reason:
            final_reason = f"{compliance_reason}\n\nADDITIONAL FACTORS:\n" + '\n'.join(f"    {r}" for r in reasons)
        else:
            final_reason = "OPPORTUNITY FACTORS:\n" + '\n'.join(f"    {r}" for r in reasons)

    return final_score, final_reason

# Apply scoring
print("   Analyzing facilities against EU emission standards...")
print("   This may take a moment...")
merged[['lead_score', 'score_reasons']] = merged.apply(
    lambda row: pd.Series(score_facility_with_compliance(row)), axis=1
)

# Filter qualified leads (score > 30)
qualified_leads = merged[merged['lead_score'] > 30].copy()
qualified_leads = qualified_leads.sort_values('lead_score', ascending=False)

print(f" Found {len(qualified_leads)} qualified leads (score > 30)")

# Create output
print("\n Preparing export...")
output_columns = [
    'nameOfFeature', 'countryCode', 'city', 'mainActivityName',
    'energyInputTJ', 'totalPollutantQuantityTNE', 'lead_score', 'score_reasons',
    'parentCompanyName', 'streetName', 'postalCode'
]

# Filter for columns that actually exist
existing_cols = [col for col in output_columns if col in qualified_leads.columns]
export_df = qualified_leads[existing_cols].copy()

# Create rename mapping for existing columns
column_rename = {
    'nameOfFeature': 'Facility Name',
    'countryCode': 'Country',
    'city': 'City',
    'mainActivityName': 'Activity Type',
    'energyInputTJ': 'Energy Input (TJ/year)',
    'totalPollutantQuantityTNE': 'Emissions (tonnes/year)',
    'lead_score': 'Lead Score',
    'score_reasons': 'Scoring Reasons',
    'parentCompanyName': 'Parent Company',
    'streetName': 'Street',
    'postalCode': 'Postal Code'
}

# Rename only columns that exist
export_df.rename(columns={k: v for k, v in column_rename.items() if k in existing_cols}, inplace=True)

# Export to Excel with COMPLIANCE-FOCUSED SHEETS
output_file = f'GMAB_WasteToEnergy_Leads_EU_Compliance_{datetime.now().strftime("%Y%m%d")}.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # PRIORITY 1: CRITICAL COMPLIANCE VIOLATIONS (score >= 80)
    critical_leads = export_df[export_df['Lead Score'] >= 80]
    if len(critical_leads) > 0:
        critical_leads.to_excel(writer, sheet_name=' CRITICAL VIOLATIONS', index=False)

    # PRIORITY 2: HIGH-VALUE OPPORTUNITIES (score 60-79)
    high_value_leads = export_df[(export_df['Lead Score'] >= 60) & (export_df['Lead Score'] < 80)]
    if len(high_value_leads) > 0:
        high_value_leads.to_excel(writer, sheet_name=' HIGH VALUE (60-79)', index=False)

    # PRIORITY 3: QUALIFIED LEADS (score 40-59)
    qualified = export_df[(export_df['Lead Score'] >= 40) & (export_df['Lead Score'] < 60)]
    if len(qualified) > 0:
        qualified.to_excel(writer, sheet_name=' QUALIFIED (40-59)', index=False)

    # All qualified leads
    export_df.to_excel(writer, sheet_name='ALL LEADS', index=False)

    # By country (top 5)
    for country in export_df['Country'].value_counts().head(5).index:
        country_leads = export_df[export_df['Country'] == country]
        sheet_name = f'{country} ({len(country_leads)})'[:31]  # Excel limit
        country_leads.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\n Exported to: {output_file}")
print(f"\n LEAD SUMMARY (EU COMPLIANCE-BASED SCORING):")
print(f"   Total qualified leads: {len(export_df)}")

if 'Lead Score' in export_df.columns:
    critical_count = len(export_df[export_df['Lead Score'] >= 80])
    high_value_count = len(export_df[(export_df['Lead Score'] >= 60) & (export_df['Lead Score'] < 80)])
    qualified_count = len(export_df[(export_df['Lead Score'] >= 40) & (export_df['Lead Score'] < 60)])

    print(f"\n    CRITICAL VIOLATIONS (80-100): {critical_count} facilities")
    print(f"       Immediate enforcement risk, compliance deadlines <90 days")
    print(f"       SALES ACTION: Same-day contact, technical assessment within 48hrs")

    print(f"\n    HIGH VALUE (60-79): {high_value_count} facilities")
    print(f"       Significant compliance risk or large facility opportunity")
    print(f"       SALES ACTION: Contact within 3 days, proposal within 2 weeks")

    print(f"\n    QUALIFIED (40-59): {qualified_count} facilities")
    print(f"       Good opportunity, proactive efficiency improvements")
    print(f"       SALES ACTION: Nurture campaign, contact within 30 days")

if 'Country' in export_df.columns:
    print(f"\n    Geographic Coverage: {export_df['Country'].nunique()} countries")
    print(f"   Top 3 markets: {', '.join(export_df['Country'].value_counts().head(3).index.tolist())}")

print(f"\n TOP 10 LEADS (Compliance-Priority Ranking):")
display_cols = [col for col in ['Facility Name', 'Country', 'City', 'Lead Score'] if col in export_df.columns]
if display_cols:
    top_10 = export_df[display_cols].head(10)
    print(top_10.to_string(index=False))
else:
    print(export_df.head(10).to_string(index=False))

print("\n" + "=" * 80)
print(" EU COMPLIANCE-BASED LEAD GENERATION COMPLETE!")
print(" Based on restrictions.md: Euro 7, BAT-AEL, and IED emission standards")
print(" Leads prioritized by regulatory urgency and financial penalty risk")
print("=" * 80)