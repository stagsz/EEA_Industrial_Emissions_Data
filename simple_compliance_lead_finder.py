#!/usr/bin/env python3
"""
GMAB Simple Compliance-Based Lead Finder
Shows all waste-to-energy facilities with pollutant data
Assigns scores based on pollution levels and facility size
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("   GMAB WASTE-TO-ENERGY LEAD FINDER")
print("   With Pollutant Emission Analysis")
print("=" * 80)

# Load data
print("\nLoading EEA data...")
facilities = pd.read_csv('converted_csv/2_ProductionFacility.csv', low_memory=False)
energy = pd.read_csv('converted_csv/4d_EnergyInput.csv', low_memory=False)
pollutant_releases = pd.read_csv('converted_csv/2f_PollutantRelease.csv', low_memory=False)
installations = pd.read_csv('converted_csv/3_ProductionInstallation.csv', low_memory=False)

print(f"Loaded {len(facilities):,} facilities")
print(f"Loaded {len(pollutant_releases):,} pollutant records")

# Filter for waste incineration
print("\nFiltering waste-to-energy facilities...")
wte = facilities[facilities['mainActivityName'].str.contains('incineration', case=False, na=False)]
print(f"Found {len(wte)} WtE facilities")

# Get latest year
latest_year = energy['reportingYear'].max()

# Merge
print(f"\nMerging data (year {latest_year})...")
merged = wte.merge(
    installations,
    left_on='Facility_INSPIRE_ID',
    right_on='Parent_Facility_INSPIRE_ID',
    how='left'
)

merged = merged.merge(
    energy[energy['reportingYear'] == latest_year],
    left_on='Installation_INSPIRE_ID',
    right_on='Installation_Part_INSPIRE_ID',
    how='left'
)

# Process ALL facilities (not just first 200)
print(f"Processing ALL {len(merged)} facilities across Europe...")
print("This may take a few minutes...")

leads = []
facilities_processed = 0
facilities_with_data = 0

for idx, row in merged.iterrows():
    facilities_processed += 1

    # Progress indicator every 50 facilities
    if facilities_processed % 50 == 0:
        print(f"  Processed {facilities_processed}/{len(merged)} facilities... ({facilities_with_data} with emissions data)")

    fac_id = row.get('Facility_INSPIRE_ID')
    if pd.isna(fac_id):
        continue

    # Get pollutants
    pollutants = pollutant_releases[pollutant_releases['Facility_INSPIRE_ID'] == fac_id]

    if pollutants.empty:
        continue

    facilities_with_data += 1

    # Calculate total emissions (all pollutants)
    total_emissions_kg = pollutants['totalPollutantQuantityKg'].sum()
    total_emissions_tonnes = total_emissions_kg / 1000

    # Count pollutant types
    num_pollutants = len(pollutants['pollutantName'].unique())

    # Get specific pollutants of interest
    nox_data = pollutants[pollutants['pollutantName'].str.contains('NOx|Nitrogen oxides', case=False, na=False)]
    co2_data = pollutants[pollutants['pollutantName'].str.contains('CO2|Carbon dioxide', case=False, na=False)]
    so2_data = pollutants[pollutants['pollutantName'].str.contains('SO2|Sulphur', case=False, na=False)]

    # SCORING LOGIC
    score = 0
    reasons = []

    # 1. Total emissions level (0-30 points)
    if total_emissions_tonnes > 1000:
        score += 30
        reasons.append(f"Very high total emissions: {total_emissions_tonnes:.1f} tonnes/year")
    elif total_emissions_tonnes > 500:
        score += 25
        reasons.append(f"High total emissions: {total_emissions_tonnes:.1f} tonnes/year")
    elif total_emissions_tonnes > 100:
        score += 20
        reasons.append(f"Moderate total emissions: {total_emissions_tonnes:.1f} tonnes/year")
    elif total_emissions_tonnes > 10:
        score += 10
        reasons.append(f"Low emissions: {total_emissions_tonnes:.1f} tonnes/year")

    # 2. Number of pollutant types (0-20 points)
    if num_pollutants >= 10:
        score += 20
        reasons.append(f"Multiple pollutant types: {num_pollutants} different pollutants")
    elif num_pollutants >= 5:
        score += 15
        reasons.append(f"Several pollutant types: {num_pollutants} pollutants")
    elif num_pollutants >= 3:
        score += 10
        reasons.append(f"Few pollutant types: {num_pollutants} pollutants")

    # 3. Key pollutants present (0-20 points each)
    if not nox_data.empty:
        nox_kg = nox_data['totalPollutantQuantityKg'].sum()
        score += 20
        reasons.append(f"NOx emissions: {nox_kg:.1f} kg/year (regulatory concern)")

    if not co2_data.empty:
        co2_kg = co2_data['totalPollutantQuantityKg'].sum()
        score += 15
        reasons.append(f"CO2 emissions: {co2_kg:.1f} kg/year")

    if not so2_data.empty:
        so2_kg = so2_data['totalPollutantQuantityKg'].sum()
        score += 15
        reasons.append(f"SO2 emissions: {so2_kg:.1f} kg/year (requires scrubbing)")

    # 4. Facility size (0-15 points)
    energy_input = row.get('energyInputTJ', 0)
    if pd.notna(energy_input) and energy_input > 1000:
        score += 15
        reasons.append(f"Large facility: {energy_input:.0f} TJ/year energy input")
    elif pd.notna(energy_input) and energy_input > 500:
        score += 10
        reasons.append(f"Medium facility: {energy_input:.0f} TJ/year energy input")

    # 5. Priority country (0-10 points)
    country = row.get('countryCode', 'Unknown')
    priority_countries = ['DE', 'NL', 'IT', 'SE', 'PL', 'FR', 'ES', 'DK', 'GB']
    if country in priority_countries:
        score += 10
        reasons.append(f"Priority market: {country}")

    # Build lead record
    lead = {
        'Facility Name': row.get('nameOfFeature', 'Unknown'),
        'Country': country,
        'City': row.get('city', 'Unknown'),
        'Parent Company': row.get('parentCompanyName', 'Unknown'),
        'Activity': row.get('mainActivityName', 'Unknown'),
        'Energy Input (TJ/yr)': energy_input if pd.notna(energy_input) else 0,
        'Total Emissions (tonnes/yr)': total_emissions_tonnes,
        'Number of Pollutants': num_pollutants,
        'Has NOx': 'YES' if not nox_data.empty else 'NO',
        'Has CO2': 'YES' if not co2_data.empty else 'NO',
        'Has SO2': 'YES' if not so2_data.empty else 'NO',
        'Lead Score': score,
        'Scoring Reasons': '; '.join(reasons),
        'Street': row.get('streetName', ''),
        'Postal Code': row.get('postalCode', '')
    }

    leads.append(lead)

print(f"\nProcessing complete!")
print(f"  Total facilities processed: {facilities_processed}")
print(f"  Facilities with emission data: {facilities_with_data}")
print(f"  Leads generated: {len(leads)}")

# Convert to DataFrame
df = pd.DataFrame(leads)
df = df.sort_values('Lead Score', ascending=False)

# Show all countries found
print(f"\nCountries with waste-to-energy facilities:")
country_counts = df['Country'].value_counts()
for country, count in country_counts.items():
    print(f"  {country}: {count} facilities")

# Export
output_file = f'GMAB_WtE_Leads_ALL_Europe_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Priority sheets
    p1 = df[df['Lead Score'] >= 80]
    p2 = df[(df['Lead Score'] >= 60) & (df['Lead Score'] < 80)]
    p3 = df[(df['Lead Score'] >= 40) & (df['Lead Score'] < 60)]
    p4 = df[(df['Lead Score'] >= 30) & (df['Lead Score'] < 40)]

    if len(p1) > 0:
        p1.to_excel(writer, sheet_name='Priority 1 (80+)', index=False)
    if len(p2) > 0:
        p2.to_excel(writer, sheet_name='Priority 2 (60-79)', index=False)
    if len(p3) > 0:
        p3.to_excel(writer, sheet_name='Priority 3 (40-59)', index=False)
    if len(p4) > 0:
        p4.to_excel(writer, sheet_name='Priority 4 (30-39)', index=False)

    df.to_excel(writer, sheet_name='ALL LEADS', index=False)

    # By country - ALL countries (not just top 5)
    print(f"\nCreating country sheets...")
    for country in df['Country'].value_counts().index:
        country_df = df[df['Country'] == country]
        sheet_name = f'{country} ({len(country_df)})'[:31]
        country_df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"  {sheet_name}")

print(f"\nExported to: {output_file}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nTotal leads: {len(df)}")
print(f"  Priority 1 (80+): {len(df[df['Lead Score'] >= 80])}")
print(f"  Priority 2 (60-79): {len(df[(df['Lead Score'] >= 60) & (df['Lead Score'] < 80)])}")
print(f"  Priority 3 (40-59): {len(df[(df['Lead Score'] >= 40) & (df['Lead Score'] < 60)])}")
print(f"  Priority 4 (30-39): {len(df[(df['Lead Score'] >= 30) & (df['Lead Score'] < 40)])}")

print(f"\nCountries: {df['Country'].nunique()}")
print(f"Top 3: {', '.join(df['Country'].value_counts().head(3).index.tolist())}")

print(f"\nFacilities with key pollutants:")
print(f"  NOx: {len(df[df['Has NOx'] == 'YES'])}")
print(f"  CO2: {len(df[df['Has CO2'] == 'YES'])}")
print(f"  SO2: {len(df[df['Has SO2'] == 'YES'])}")

print("\n" + "=" * 80)
print("TOP 15 LEADS")
print("=" * 80)
print(df[['Facility Name', 'Country', 'Lead Score', 'Total Emissions (tonnes/yr)', 'Has NOx']].head(15).to_string(index=False))

print("\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
