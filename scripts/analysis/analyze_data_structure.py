"""
Check key data files for lead generation
"""
import pandas as pd

print("=" * 80)
print("CHECKING KEY DATA FILES FOR WASTE-TO-ENERGY LEAD GENERATION")
print("=" * 80)

# 1. Check facilities
print("\n1. FACILITIES (2_ProductionFacility.csv)")
facilities = pd.read_csv('converted_csv/2_ProductionFacility.csv', low_memory=False)
print(f"Total facilities: {len(facilities)}")
print(f"Countries: {facilities['countryCode'].unique()}")
print(f"\nActivity types available:")
print(facilities['mainActivityName'].value_counts().head(10))

# 2. Check energy input
print("\n2. ENERGY INPUT (4d_EnergyInput.csv)")
energy = pd.read_csv('converted_csv/4d_EnergyInput.csv', low_memory=False)
print(f"Total energy records: {len(energy)}")
print(f"Columns: {energy.columns.tolist()}")
print(energy.head())

# 3. Check emissions
print("\n3. EMISSIONS TO AIR (4e_EmissionsToAir.csv)")
emissions = pd.read_csv('converted_csv/4e_EmissionsToAir.csv', low_memory=False)
print(f"Total emission records: {len(emissions)}")
print(f"Columns: {emissions.columns.tolist()}")
print(emissions.head())

# 4. Check for waste-related activities
print("\n4. WASTE-TO-ENERGY FACILITIES:")
waste_keywords = ['waste', 'incineration', 'energy recovery', 'municipal', 'msw', 'refuse']
waste_facilities = facilities[
    facilities['mainActivityName'].str.lower().str.contains('|'.join(waste_keywords), na=False)
]
print(f"Found {len(waste_facilities)} potential waste-to-energy facilities")
print("\nActivity types:")
print(waste_facilities['mainActivityName'].value_counts())