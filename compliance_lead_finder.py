#!/usr/bin/env python3
"""
GMAB Compliance-Based Lead Finder
Simple script that uses EU emission compliance checking for lead generation
No SDK dependency - direct analysis with compliance integration
"""

import pandas as pd
import numpy as np
from datetime import datetime
from emission_compliance_checker import EmissionComplianceChecker, ComplianceStatus

print("=" * 80)
print("   GMAB COMPLIANCE-BASED LEAD FINDER")
print("   EU Emission Standards Integration (restrictions.md)")
print("   'TOGETHER WE SUCCEED, TOGETHER WE GO GREEN'")
print("=" * 80)

# Initialize compliance checker
print("\nInitializing EU Emission Compliance Checker...")
compliance_checker = EmissionComplianceChecker()
print("Compliance checker ready - checking against Euro 7, BAT-AEL, and IED standards")

# Load data
print("\nLoading EEA Industrial Emissions Data...")
try:
    facilities = pd.read_csv('converted_csv/2_ProductionFacility.csv', low_memory=False)
    energy = pd.read_csv('converted_csv/4d_EnergyInput.csv', low_memory=False)
    pollutant_releases = pd.read_csv('converted_csv/2f_PollutantRelease.csv', low_memory=False)
    installations = pd.read_csv('converted_csv/3_ProductionInstallation.csv', low_memory=False)

    print(f"Loaded {len(facilities):,} facilities")
    print(f"Loaded {len(energy):,} energy records")
    print(f"Loaded {len(pollutant_releases):,} pollutant release records")
except FileNotFoundError as e:
    print(f"ERROR: Could not find data files. Make sure converted_csv/ directory exists.")
    print(f"Details: {e}")
    exit(1)

# Filter for waste incineration facilities
print("\nIdentifying waste-to-energy facilities...")
wte_facilities = facilities[
    facilities['mainActivityName'].str.contains('incineration', case=False, na=False)
]

print(f"Found {len(wte_facilities)} waste incineration facilities")
print(f"\nCountries with WtE facilities:")
print(wte_facilities['countryCode'].value_counts().head(10))

# Get latest year data
latest_year = energy['reportingYear'].max()
print(f"\nLatest reporting year: {latest_year}")

# Merge data
print("\nMerging facility, energy, and pollutant data...")
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

print(f"Merged dataset: {len(merged)} records")

# Limit to first 100 facilities for reasonable processing time
merged = merged.head(100)
print(f"\nProcessing first {len(merged)} facilities with EU compliance checking...")

# Score each facility with compliance checking
scored_leads = []

for idx, row in merged.iterrows():
    facility_id = row.get('Facility_INSPIRE_ID')
    facility_name = row.get('nameOfFeature', 'Unknown')

    if pd.isna(facility_id):
        continue

    # Get pollutant data for this facility
    facility_pollutants = pollutant_releases[
        pollutant_releases['Facility_INSPIRE_ID'] == facility_id
    ]

    # Skip if no pollutant data
    if facility_pollutants.empty:
        continue

    # Prepare facility data
    facility_data = {
        'nameOfFeature': facility_name,
        'countryCode': row.get('countryCode', 'EU'),
        'mainActivityName': row.get('mainActivityName', ''),
        'energyInputTJ': row.get('energyInputTJ', 0)
    }

    # Check EU compliance
    try:
        status, violations, compliance_score, detailed_reason = compliance_checker.check_facility_compliance(
            facility_data,
            facility_pollutants
        )

        # Build lead record
        lead = {
            'Facility Name': facility_name,
            'Country': row.get('countryCode', 'Unknown'),
            'City': row.get('city', 'Unknown'),
            'Parent Company': row.get('parentCompanyName', 'Unknown'),
            'Activity Type': row.get('mainActivityName', 'Unknown'),
            'Energy Input (TJ/year)': row.get('energyInputTJ', 0),
            'Compliance Status': status.value,
            'Lead Score': compliance_score,
            'Number of Violations': len(violations),
            'Compliance Detail': detailed_reason,
            'Street': row.get('streetName', 'Unknown'),
            'Postal Code': row.get('postalCode', 'Unknown')
        }

        scored_leads.append(lead)

        if (idx + 1) % 10 == 0:
            print(f"   Processed {idx + 1} facilities... ({len(scored_leads)} with pollutant data)")

    except Exception as e:
        # Skip facilities that cause errors
        continue

print(f"\nCompliance checking complete! Found {len(scored_leads)} facilities with emission data")

# Convert to DataFrame
if len(scored_leads) == 0:
    print("\nERROR: No leads found with compliance data.")
    print("This may be because:")
    print("  1. No facilities have pollutant release data in 2f_PollutantRelease.csv")
    print("  2. Facility IDs don't match between tables")
    print("  3. Data needs to be re-converted from Access database")
    exit(1)

leads_df = pd.DataFrame(scored_leads)

# Sort by lead score (highest first)
leads_df = leads_df.sort_values('Lead Score', ascending=False)

# Filter qualified leads (score >= 30)
qualified_leads = leads_df[leads_df['Lead Score'] >= 30].copy()

print(f"\nQualified leads (score >= 30): {len(qualified_leads)}")

# Export to Excel with compliance-based priority sheets
output_file = f'GMAB_Compliance_Leads_{datetime.now().strftime("%Y%m%d")}.xlsx'
print(f"\nExporting to Excel: {output_file}")

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # PRIORITY 1: CRITICAL COMPLIANCE VIOLATIONS (score >= 80)
    critical = qualified_leads[qualified_leads['Lead Score'] >= 80]
    if len(critical) > 0:
        critical.to_excel(writer, sheet_name='P1 CRITICAL (80-100)', index=False)
        print(f"  Priority 1 (CRITICAL): {len(critical)} facilities")

    # PRIORITY 2: HIGH VALUE (score 60-79)
    high_value = qualified_leads[(qualified_leads['Lead Score'] >= 60) & (qualified_leads['Lead Score'] < 80)]
    if len(high_value) > 0:
        high_value.to_excel(writer, sheet_name='P2 HIGH VALUE (60-79)', index=False)
        print(f"  Priority 2 (HIGH VALUE): {len(high_value)} facilities")

    # PRIORITY 3: QUALIFIED (score 40-59)
    qualified_mid = qualified_leads[(qualified_leads['Lead Score'] >= 40) & (qualified_leads['Lead Score'] < 60)]
    if len(qualified_mid) > 0:
        qualified_mid.to_excel(writer, sheet_name='P3 QUALIFIED (40-59)', index=False)
        print(f"  Priority 3 (QUALIFIED): {len(qualified_mid)} facilities")

    # PRIORITY 4: NURTURE (score 30-39)
    nurture = qualified_leads[(qualified_leads['Lead Score'] >= 30) & (qualified_leads['Lead Score'] < 40)]
    if len(nurture) > 0:
        nurture.to_excel(writer, sheet_name='P4 NURTURE (30-39)', index=False)
        print(f"  Priority 4 (NURTURE): {len(nurture)} facilities")

    # All qualified leads
    qualified_leads.to_excel(writer, sheet_name='ALL QUALIFIED LEADS', index=False)

    # All facilities (including low scores)
    leads_df.to_excel(writer, sheet_name='ALL FACILITIES', index=False)

    # By country (top 5)
    top_countries = qualified_leads['Country'].value_counts().head(5)
    for country in top_countries.index:
        country_leads = qualified_leads[qualified_leads['Country'] == country]
        sheet_name = f'{country} ({len(country_leads)})'[:31]
        country_leads.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\nExported to: {output_file}")

# Display summary
print("\n" + "=" * 80)
print("LEAD SUMMARY (EU COMPLIANCE-BASED SCORING)")
print("=" * 80)

critical_count = len(qualified_leads[qualified_leads['Lead Score'] >= 80])
high_value_count = len(qualified_leads[(qualified_leads['Lead Score'] >= 60) & (qualified_leads['Lead Score'] < 80)])
qualified_count = len(qualified_leads[(qualified_leads['Lead Score'] >= 40) & (qualified_leads['Lead Score'] < 60)])
nurture_count = len(qualified_leads[(qualified_leads['Lead Score'] >= 30) & (qualified_leads['Lead Score'] < 40)])

print(f"\nTotal qualified leads: {len(qualified_leads)}")
print(f"\n  PRIORITY 1 - CRITICAL (80-100): {critical_count} facilities")
print(f"    -> Immediate enforcement risk, compliance deadlines <90 days")
print(f"    -> SALES ACTION: Same-day contact, technical assessment within 48hrs")

print(f"\n  PRIORITY 2 - HIGH VALUE (60-79): {high_value_count} facilities")
print(f"    -> Significant compliance risk or large facility opportunity")
print(f"    -> SALES ACTION: Contact within 3 days, proposal within 2 weeks")

print(f"\n  PRIORITY 3 - QUALIFIED (40-59): {qualified_count} facilities")
print(f"    -> Good opportunity, proactive efficiency improvements")
print(f"    -> SALES ACTION: Nurture campaign, contact within 30 days")

print(f"\n  PRIORITY 4 - NURTURE (30-39): {nurture_count} facilities")
print(f"    -> Long-term opportunity, monitor for regulatory changes")
print(f"    -> SALES ACTION: Quarterly check-in, relationship building")

print(f"\nGeographic Coverage: {qualified_leads['Country'].nunique()} countries")
print(f"Top 3 markets: {', '.join(qualified_leads['Country'].value_counts().head(3).index.tolist())}")

print(f"\n" + "=" * 80)
print("TOP 10 LEADS (Compliance-Priority Ranking)")
print("=" * 80)

top_10 = qualified_leads[['Facility Name', 'Country', 'City', 'Lead Score', 'Compliance Status']].head(10)
print(top_10.to_string(index=False))

print("\n" + "=" * 80)
print("EU COMPLIANCE-BASED LEAD GENERATION COMPLETE!")
print("Based on restrictions.md: Euro 7, BAT-AEL, and IED emission standards")
print("Leads prioritized by regulatory urgency and financial penalty risk")
print("=" * 80)

print(f"\nNext steps:")
print(f"  1. Open {output_file} in Excel")
print(f"  2. Review Priority 1 (CRITICAL) leads for immediate action")
print(f"  3. Read 'Compliance Detail' column for detailed violation analysis")
print(f"  4. Use sales strategy guidance in compliance details")
