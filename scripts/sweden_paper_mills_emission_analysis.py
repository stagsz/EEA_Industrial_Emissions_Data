"""
Sweden Paper & Pulp Mills - Emission Problem Analysis
======================================================
Identifies mills with growing emissions, high absolute loads,
and compliance risk signals. Uses EEA data 2007-2021.

Output: outputs/Sweden_Paper_Mills_Emission_Report.xlsx
"""

import pandas as pd
import numpy as np

BASE = "C:/Users/staff/anthropicFun/EEA_Industrial_Emissions_Data"

print("Loading EEA data...")
fac = pd.read_csv(f"{BASE}/data/processed/converted_csv/2_ProductionFacility.csv", low_memory=False)
se_paper = fac[
    (fac['countryCode'] == 'SE') &
    fac['mainActivityName'].str.contains('paper|pulp|board', case=False, na=False)
].copy()
facility_ids = se_paper['Facility_INSPIRE_ID'].dropna().unique()

pr = pd.read_csv(f"{BASE}/data/processed/converted_csv/2f_PollutantRelease.csv", low_memory=False)
pr_paper = pr[pr['Facility_INSPIRE_ID'].isin(facility_ids)].copy()
pr_paper['totalPollutantQuantityKg'] = pd.to_numeric(pr_paper['totalPollutantQuantityKg'], errors='coerce')
pr_paper = pr_paper.merge(
    se_paper[['Facility_INSPIRE_ID', 'nameOfFeature', 'city', 'parentCompanyName',
              'streetName', 'postalCode', 'pointGeometryLat', 'pointGeometryLon']],
    on='Facility_INSPIRE_ID', how='left'
)

# ── Key pollutants ──────────────────────────────────────────
AIR_POLL = [
    'Nitrogen oxides',
    'Sulphur oxides',
    'Particulate matter',
    'Carbon dioxide excluding biomass',
    'Carbon monoxide',
    'Halogenated organic compounds (as AOX)',
    'PCDD + PCDF (dioxins + furans) (as Teq)',
    'Mercury and compounds (as Hg)',
    'Chlorine and inorganic compounds (as HCl)',
]
WATER_POLL = [
    'Halogenated organic compounds (as AOX)',
    'Total nitrogen',
    'Total phosphorus',
    'Total organic carbon(as total C or COD/3)',
    'Zinc and compounds (as Zn)',
    'Mercury and compounds (as Hg)',
]

# ── EU IED BAT-AEL reference limits for pulp/paper (indicative) ──────────
# Source: BAT Conclusions for Pulp, Paper and Board Manufacturing (2014/687/EU)
# Values are approximate upper-range BAT-AELs
BAT_AEL_AIR_KG_PER_TONNE = {
    'Nitrogen oxides': 0.7,        # kg NOx per tonne product
    'Sulphur oxides': 0.3,         # kg SOx per tonne product
    'Particulate matter': 0.15,    # kg dust per tonne product
    'Total organic carbon(as total C or COD/3)': 0.05,
}

# ── Absolute emissions 2021 ──────────────────────────────────
print("Calculating absolute emissions (2021)...")
abs2021 = (
    pr_paper[pr_paper['reportingYear'] == 2021]
    .groupby(['nameOfFeature', 'city', 'parentCompanyName', 'medium', 'pollutantName'])
    ['totalPollutantQuantityKg'].sum()
    .reset_index()
)

# Pivot for easy reading
air_2021 = abs2021[abs2021['medium'] == 'AIR'][abs2021['pollutantName'].isin(AIR_POLL)]
air_pivot = air_2021.pivot_table(
    index=['nameOfFeature', 'city', 'parentCompanyName'],
    columns='pollutantName',
    values='totalPollutantQuantityKg',
    aggfunc='sum',
    fill_value=0
).reset_index()
air_pivot.columns.name = None
air_pivot.rename(columns={'nameOfFeature': 'Facility', 'city': 'City', 'parentCompanyName': 'Parent_Company'}, inplace=True)

water_2021 = abs2021[(abs2021['medium'] == 'WATER') & abs2021['pollutantName'].isin(WATER_POLL)]
water_pivot = water_2021.pivot_table(
    index=['nameOfFeature', 'city'],
    columns='pollutantName',
    values='totalPollutantQuantityKg',
    aggfunc='sum',
    fill_value=0
).reset_index()
water_pivot.columns.name = None
water_pivot.rename(columns={'nameOfFeature': 'Facility', 'city': 'City'}, inplace=True)

# ── Trend analysis: increasing emissions 2019→2021 ──────────
print("Calculating emission trends 2019-2021...")
trend_data = pr_paper[
    pr_paper['reportingYear'].isin([2017, 2019, 2021]) &
    (pr_paper['medium'].isin(['AIR', 'WATER'])) &
    pr_paper['pollutantName'].isin(AIR_POLL + WATER_POLL)
].copy()

trend = (
    trend_data
    .groupby(['nameOfFeature', 'city', 'medium', 'pollutantName', 'reportingYear'])
    ['totalPollutantQuantityKg'].sum()
    .unstack('reportingYear')
    .fillna(0)
    .reset_index()
)
trend.columns.name = None
years_present = [c for c in [2017, 2019, 2021] if c in trend.columns]

if 2019 in trend.columns and 2021 in trend.columns:
    trend['pct_change_19_21'] = (
        (trend[2021] - trend[2019]) /
        trend[2019].replace(0, np.nan)
    ) * 100

if 2017 in trend.columns and 2021 in trend.columns:
    trend['pct_change_17_21'] = (
        (trend[2021] - trend[2017]) /
        trend[2017].replace(0, np.nan)
    ) * 100

# Flag significant rising trends
rising = trend[
    (trend.get('pct_change_19_21', 0) > 20) &
    (trend[2021] > 5000)  # >5 tonnes/year threshold
].copy().sort_values('pct_change_19_21', ascending=False)

# ── Lead score: emission problem signal ─────────────────────
print("Scoring facilities by emission problem risk...")

def score_facility(name, city):
    score = 0
    flags = []

    # Check rising trends
    f_trend = rising[(rising['nameOfFeature'] == name) & (rising['city'] == city)]
    if len(f_trend) > 0:
        n_rising = len(f_trend)
        max_rise = f_trend['pct_change_19_21'].max()
        score += min(n_rising * 10, 30)
        flags.append(f"{n_rising} pollutant(s) increasing (max +{max_rise:.0f}% vs 2019)")

    # Check absolute NOx level (IED Annex V limit ~400 mg/Nm3 ~ 0.7 kg/tonne)
    f_air = air_pivot[(air_pivot['Facility'] == name) & (air_pivot['City'] == city)]
    if len(f_air) > 0:
        row = f_air.iloc[0]
        nox = row.get('Nitrogen oxides', 0)
        sox = row.get('Sulphur oxides', 0)
        pm  = row.get('Particulate matter', 0)
        co  = row.get('Carbon monoxide', 0)
        hg  = row.get('Mercury and compounds (as Hg)', 0)

        if nox > 500000:   # >500 t NOx/yr
            score += 25; flags.append(f"HIGH NOx: {nox/1000:.0f} t/yr")
        elif nox > 200000:
            score += 15; flags.append(f"ELEVATED NOx: {nox/1000:.0f} t/yr")
        if sox > 200000:
            score += 20; flags.append(f"HIGH SOx: {sox/1000:.0f} t/yr")
        if pm > 100000:    # >100 t particulates/yr
            score += 20; flags.append(f"HIGH Particulate matter: {pm/1000:.0f} t/yr")
        if co > 1000000:   # >1,000 t CO/yr - recovery boiler indicator
            score += 15; flags.append(f"HIGH CO (recovery boiler): {co/1000:.0f} t/yr")
        if hg > 0:
            score += 20; flags.append(f"Mercury reported: {hg:.1f} kg/yr")

    # Check water - AOX is signature pulp mill pollutant under scrutiny
    f_water = water_pivot[(water_pivot['Facility'] == name) & (water_pivot['City'] == city)]
    if len(f_water) > 0:
        row = f_water.iloc[0]
        aox   = row.get('Halogenated organic compounds (as AOX)', 0)
        tn    = row.get('Total nitrogen', 0)
        tp    = row.get('Total phosphorus', 0)
        toc   = row.get('Total organic carbon(as total C or COD/3)', 0)

        if aox > 5000:     # >5 t AOX/yr - significant
            score += 25; flags.append(f"AOX water discharge: {aox/1000:.1f} t/yr")
        elif aox > 1000:
            score += 10; flags.append(f"AOX water discharge: {aox/1000:.1f} t/yr")
        if tn > 100000:    # >100 t Total N/yr
            score += 15; flags.append(f"Total Nitrogen (water): {tn/1000:.0f} t/yr")
        if tp > 10000:
            score += 15; flags.append(f"Total Phosphorus (water): {tp/1000:.0f} t/yr")
        if toc > 500000:
            score += 10; flags.append(f"High TOC (water): {toc/1000:.0f} t/yr")

    return min(score, 100), '; '.join(flags) if flags else 'No major flags'

# Apply to active mills
active = pd.read_csv(f"{BASE}/outputs/Sweden_Paper_Mills_VERIFIED_2025.csv")
active = active[active['Current Status'] != 'CLOSED'].copy()

scores = []
for _, row in active.iterrows():
    s, flags = score_facility(row['Facility'], row['City'])
    scores.append({'Facility': row['Facility'], 'City': row['City'],
                   'Emission_Risk_Score': s, 'Risk_Flags': flags,
                   'Parent_Company': row.get('Parent Company', ''),
                   'Category': row['Category'],
                   'Current_Status': row['Current Status']})

score_df = pd.DataFrame(scores).sort_values('Emission_Risk_Score', ascending=False)

# Merge air/water data for export
full = score_df.merge(air_pivot.drop(columns=['Parent_Company'], errors='ignore'), on=['Facility', 'City'], how='left')
full = full.merge(water_pivot, on=['Facility', 'City'], how='left', suffixes=('_air', '_water'))

# Rename for clarity
col_map = {
    'Nitrogen oxides': 'NOx_kg_yr',
    'Sulphur oxides': 'SOx_kg_yr',
    'Particulate matter': 'PM_kg_yr',
    'Carbon dioxide excluding biomass': 'CO2_fossil_kg_yr',
    'Carbon monoxide': 'CO_kg_yr',
    'Mercury and compounds (as Hg)': 'Mercury_kg_yr',
    'Halogenated organic compounds (as AOX)': 'AOX_water_kg_yr',
    'Total nitrogen': 'Total_N_water_kg_yr',
    'Total phosphorus': 'Total_P_water_kg_yr',
}
full.rename(columns=col_map, inplace=True)

# Print summary
print()
print("=" * 75)
print("  SWEDISH PAPER & PULP MILLS - EMISSION RISK RANKING")
print("  Based on EEA 2021 data | Score = compliance/sales urgency")
print("=" * 75)
print()
cols_display = ['Facility', 'City', 'Category', 'Emission_Risk_Score', 'Risk_Flags']
print(full[cols_display].to_string(index=False))

print()
print("=" * 75)
print("  TOP 5 PRIORITY LEADS (highest emission risk)")
print("=" * 75)
for _, r in full.head(5).iterrows():
    print(f"\n  [{r['Emission_Risk_Score']}/100] {r['Facility']} ({r['City']})")
    print(f"    Owner: {r['Parent_Company']}")
    print(f"    Status: {r['Current_Status']}")
    print(f"    Issues: {r['Risk_Flags']}")

# Export
out_path = f"{BASE}/outputs/Sweden_Paper_Mills_Emission_Report.xlsx"
with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
    # Sheet 1: Ranked by risk score
    full.to_excel(writer, sheet_name='Emission Risk Ranking', index=False)

    # Sheet 2: Rising trends detail
    if len(rising) > 0:
        rising.to_excel(writer, sheet_name='Rising Emission Trends', index=False)

    # Sheet 3: Air emissions pivot
    air_pivot.to_excel(writer, sheet_name='Air Emissions 2021', index=False)

    # Sheet 4: Water emissions pivot
    water_pivot.to_excel(writer, sheet_name='Water Emissions 2021', index=False)

print()
print(f"\nSaved full report to: {out_path}")
print("Sheets: Emission Risk Ranking | Rising Emission Trends | Air 2021 | Water 2021")
