"""
Simple Lead Finder - Direct CSV Analysis
No SDK needed, works with local data files
"""
import pandas as pd
import glob

# Check what CSV files you have
csv_files = glob.glob('converted_csv/*.csv')
print("Available data files:")
for f in csv_files:
    print(f"  - {f}")

# Load key files
print("\nLoading facility data...")
facilities = pd.read_csv('converted_csv/2_ProductionFacility.csv')
print(f"Columns: {facilities.columns.tolist()}")
print(f"\nSample data:")
print(facilities.head())