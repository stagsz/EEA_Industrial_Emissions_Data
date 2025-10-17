"""
GMAB Waste-to-Energy Lead Finder
Direct data analysis without SDK dependency
"""
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("   GMAB Waste-to-Energy Plant Optimization Lead Finder")
print("   'TOGETHER WE SUCCEED, TOGETHER WE GO GREEN'")
print("=" * 80)

# Load data
print("\n📂 Loading data files...")
facilities = pd.read_csv('converted_csv/2_ProductionFacility.csv', low_memory=False)
energy = pd.read_csv('converted_csv/4d_EnergyInput.csv', low_memory=False)
emissions = pd.read_csv('converted_csv/4e_EmissionsToAir.csv', low_memory=False)
installations = pd.read_csv('converted_csv/3_ProductionInstallation.csv', low_memory=False)
install_parts = pd.read_csv('converted_csv/4_ProductionInstallationPart.csv', low_memory=False)

print(f"✅ Loaded {len(facilities):,} facilities")
print(f"✅ Loaded {len(energy):,} energy records")
print(f"✅ Loaded {len(emissions):,} emission records")

# Filter for waste incineration facilities
print("\n🔍 Identifying waste-to-energy facilities...")
waste_activities = [
    'Installations for the incineration of non-hazardous waste',
    'Installations for the disposal of non-hazardous waste',
    'Installations for the recovery or disposal of hazardous waste'
]

wte_facilities = facilities[
    facilities['mainActivityName'].str.contains('incineration', case=False, na=False)
]

print(f"✅ Found {len(wte_facilities)} waste incineration facilities")
print(f"\nCountries with WtE facilities:")
print(wte_facilities['countryCode'].value_counts().head(10))

# Get latest year data
latest_year = energy['reportingYear'].max()
print(f"\n📅 Latest reporting year: {latest_year}")

# Merge data
print("\n🔗 Merging facility, energy, and emissions data...")
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

print(f"✅ Merged dataset: {len(merged)} records")

# Calculate lead scores
print("\n⚡ Calculating lead scores...")

def score_facility(row):
    """Score a facility based on GMAB criteria"""
    score = 0
    reasons = []
    
    # Energy consumption (higher = larger plant = better)
    energy_tj = row.get('energyInputTJ', 0)
    if pd.notna(energy_tj) and energy_tj > 1000:
        score += 20
        reasons.append(f"Large energy input: {energy_tj:,.0f} TJ/year")
    elif pd.notna(energy_tj) and energy_tj > 500:
        score += 15
        reasons.append(f"Medium energy input: {energy_tj:,.0f} TJ/year")
    
    # Emissions (higher = more waste processed = larger opportunity)
    emissions_tne = row.get('totalPollutantQuantityTNE', 0)
    if pd.notna(emissions_tne) and emissions_tne > 1000:
        score += 20
        reasons.append(f"High emissions: {emissions_tne:,.0f} tonnes/year")
    elif pd.notna(emissions_tne) and emissions_tne > 100:
        score += 15
        reasons.append(f"Medium emissions: {emissions_tne:,.0f} tonnes/year")
    
    # Country priority (focus countries)
    priority_countries = ['DE', 'NL', 'IT', 'SE', 'PL', 'FR', 'ES', 'DK']
    if row.get('countryCode') in priority_countries:
        score += 10
        reasons.append(f"Priority country: {row.get('countryCode')}")
    
    # Facility type
    if 'incineration' in str(row.get('mainActivityName', '')).lower():
        score += 15
        reasons.append("Waste incineration facility")
    
    # Has data (indicates active reporting)
    if pd.notna(energy_tj) and pd.notna(emissions_tne):
        score += 10
        reasons.append("Complete data available")
    
    return score, '; '.join(reasons)

# Apply scoring
print("   Scoring facilities...")
merged[['lead_score', 'score_reasons']] = merged.apply(
    lambda row: pd.Series(score_facility(row)), axis=1
)

# Filter qualified leads (score > 30)
qualified_leads = merged[merged['lead_score'] > 30].copy()
qualified_leads = qualified_leads.sort_values('lead_score', ascending=False)

print(f"✅ Found {len(qualified_leads)} qualified leads (score > 30)")

# Create output
print("\n📊 Preparing export...")
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

# Export to Excel
output_file = f'GMAB_WasteToEnergy_Leads_{datetime.now().strftime("%Y%m%d")}.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # All qualified leads
    export_df.to_excel(writer, sheet_name='All Qualified Leads', index=False)
    
    # Hot leads (score >= 60)
    hot_leads = export_df[export_df['Lead Score'] >= 60]
    hot_leads.to_excel(writer, sheet_name='HOT LEADS (60+)', index=False)
    
    # By country
    for country in export_df['Country'].value_counts().head(5).index:
        country_leads = export_df[export_df['Country'] == country]
        sheet_name = f'{country} ({len(country_leads)} leads)'[:31]  # Excel limit
        country_leads.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\n✅ Exported to: {output_file}")
print(f"\n📈 Summary:")
print(f"   Total qualified leads: {len(export_df)}")
if 'Lead Score' in export_df.columns:
    print(f"   HOT leads (60+): {len(export_df[export_df['Lead Score'] >= 60])}")
    print(f"   WARM leads (40-59): {len(export_df[(export_df['Lead Score'] >= 40) & (export_df['Lead Score'] < 60)])}")
if 'Country' in export_df.columns:
    print(f"   Countries covered: {export_df['Country'].nunique()}")
print(f"\n🎯 Top 10 leads:")
# Print available columns
display_cols = [col for col in ['Facility Name', 'Country', 'City', 'Lead Score'] if col in export_df.columns]
if display_cols:
    print(export_df[display_cols].head(10).to_string(index=False))
else:
    print(export_df.head(10).to_string(index=False))

print("\n" + "=" * 80)
print("✅ Lead generation complete!")
print("=" * 80)