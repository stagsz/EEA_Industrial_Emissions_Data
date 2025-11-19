#!/usr/bin/env python3
"""
Download EEA Industrial Emissions Data Files
Downloads all 16 CSV files from the EEA data repository
"""

import urllib.request
import urllib.parse
import os
import time

# Base URL for downloading files
base_url = "https://sdi.eea.europa.eu/datashare/s/6wrowetdF5ByE8X/download?path=%2FCSV&files="

# Output directory
output_dir = r"C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\downloaded_data"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# List of all CSV files to download
files = [
    "F1_1_Total Releases at National Level into Air.csv",
    "F1_2_Total Release at E-PRTR Sector Level into Air.csv",
    "F1_3_Total Release at E-PRTR Annex I Activity into Air.csv",
    "F1_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Air.csv",
    "F2_1_Total Releases at National Level into Water.csv",
    "F2_2_Total Release at E-PRTR Sector Level into Water.csv",
    "F2_3_Total Release at E-PRTR Annex I Activity into Water.csv",
    "F2_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Water.csv",
    "F3_1_Total pollutant transfer.csv",
    "F3_2_Detailed pollutant transfer at facility level with E-PRTR Sector and Annex I Activity.csv",
    "F4_1_Total waste transfer.csv",
    "F4_2_Detailed waste transfer at facility level with E-PRTR Sector and Annex I Activity.csv",
    "F5_1_Total emissions and energy input from LCP at national level.csv",
    "F5_2_Detailed emissions and energy input from LCP.csv",
    "F6_1_Total Information on Installations.csv",
    "F7_1_Detailed information on WI and co-WI.csv"
]

print(f"Starting download of {len(files)} CSV files...")
print(f"Output directory: {output_dir}")
print("-" * 80)

success_count = 0
fail_count = 0

for idx, filename in enumerate(files, 1):
    try:
        # URL encode the filename
        encoded_filename = urllib.parse.quote(filename)
        download_url = base_url + encoded_filename
        output_path = os.path.join(output_dir, filename)
        
        print(f"\n[{idx}/{len(files)}] Downloading: {filename}")
        
        # Add headers to mimic browser request
        req = urllib.request.Request(download_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        # Download the file
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.read())
        
        # Get file size
        file_size = os.path.getsize(output_path)
        size_mb = file_size / (1024 * 1024)
        print(f"    ✓ Downloaded successfully ({size_mb:.2f} MB)")
        success_count += 1
        
        # Small delay between downloads
        time.sleep(0.5)
        
    except Exception as e:
        print(f"    ✗ Error downloading {filename}: {str(e)}")
        fail_count += 1

print("\n" + "=" * 80)
print("Download Complete!")
print(f"  Successful: {success_count} files")
print(f"  Failed: {fail_count} files")
print(f"\nFiles saved to: {output_dir}")

# List all downloaded files with their sizes
print("\nDownloaded files:")
if os.path.exists(output_dir):
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith('.csv'):
            filepath = os.path.join(output_dir, filename)
            size = os.path.getsize(filepath)
            size_mb = size / (1024 * 1024)
            print(f"  - {filename} ({size_mb:.2f} MB)")
