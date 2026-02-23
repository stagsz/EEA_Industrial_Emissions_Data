#!/usr/bin/env python3
"""
Download EEA Industrial Reporting Database - Latest Version
=============================================================
Downloads the newest available EEA CSV data files from the
European Industrial Emissions Portal.

HOW TO GET THE SHARE KEY:
1. Go to: https://industry.eea.europa.eu/download
2. Click the CSV download link for the latest version (v13 or newer)
3. You will be redirected to a URL like:
   https://sdi.eea.europa.eu/datashare/s/XXXXXXXXXX/download?path=...
4. Copy the share key (XXXXXXXXXX) and paste it into SHARE_KEY below.
   The v8 key (our current data) was: 6wrowetdF5ByE8X

CURRENT DATA:  v8  (2007-2021) - already downloaded
TARGET DATA:   v13 (2007-2023) or v14/v15 (2007-2024)

Alternative direct page:
https://www.eea.europa.eu/data-and-maps/data/industrial-reporting-under-the-industrial-7/eu-registry-e-prtr-lcp
"""

import urllib.request
import urllib.parse
import os
import time
import sys

# ============================================================
# CONFIGURATION - UPDATE SHARE_KEY AFTER VISITING DOWNLOAD PAGE
# ============================================================
SHARE_KEY = "PASTE_NEW_SHARE_KEY_HERE"   # <-- update this

# Output directory for new data
OUTPUT_DIR = r"C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\data\raw\v13_downloaded"

# Base URL pattern (same structure as v8)
BASE_URL = f"https://sdi.eea.europa.eu/datashare/s/{SHARE_KEY}/download?path=%2FCSV&files="

# ============================================================
# FILES TO DOWNLOAD
# These are the same file names across all versions
# ============================================================
FILES = [
    # E-PRTR Air releases (key for emissions analysis)
    "F1_1_Total Releases at National Level into Air.csv",
    "F1_2_Total Release at E-PRTR Sector Level into Air.csv",
    "F1_3_Total Release at E-PRTR Annex I Activity into Air.csv",
    "F1_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Air.csv",
    # Water releases (AOX, nitrogen, phosphorus for pulp mills)
    "F2_1_Total Releases at National Level into Water.csv",
    "F2_2_Total Release at E-PRTR Sector Level into Water.csv",
    "F2_3_Total Release at E-PRTR Annex I Activity into Water.csv",
    "F2_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Water.csv",
    # Pollutant and waste transfers
    "F3_1_Total pollutant transfer.csv",
    "F3_2_Detailed pollutant transfer at facility level with E-PRTR Sector and Annex I Activity.csv",
    "F4_1_Total waste transfer.csv",
    "F4_2_Detailed waste transfer at facility level with E-PRTR Sector and Annex I Activity.csv",
    # Large Combustion Plants (energy + emissions for pulp/paper boilers)
    "F5_1_Total emissions and energy input from LCP at national level.csv",
    "F5_2_Detailed emissions and energy input from LCP.csv",
    # Facility registry (installations, permits, inspections)
    "F6_1_Total Information on Installations.csv",
    # Waste Incineration (WtE focus)
    "F7_1_Detailed information on WI and co-WI.csv",
]

# Priority subset - download these first if bandwidth is limited
PRIORITY_FILES = [
    "F1_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Air.csv",
    "F2_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Water.csv",
    "F6_1_Total Information on Installations.csv",
    "F7_1_Detailed information on WI and co-WI.csv",
]


def check_share_key():
    """Validate that the share key has been configured."""
    if SHARE_KEY == "PASTE_NEW_SHARE_KEY_HERE":
        print("=" * 70)
        print("  SHARE KEY NOT SET")
        print("=" * 70)
        print()
        print("  To get the new share key:")
        print("  1. Open in browser: https://industry.eea.europa.eu/download")
        print("  2. Click the CSV download button for the latest version")
        print("  3. Copy the share key from the redirect URL:")
        print("     https://sdi.eea.europa.eu/datashare/s/[KEY]/download?...")
        print("  4. Edit this script and set SHARE_KEY = 'your_key_here'")
        print()
        print("  Alternative access point:")
        print("  https://www.eea.europa.eu/data-and-maps/data/")
        print("  industrial-reporting-under-the-industrial-7/eu-registry-e-prtr-lcp")
        print()
        print("  Current data (v8, 2007-2021): already in data/raw/downloaded_data/")
        print("  Target data (v13+, 2007-2023): will go to data/raw/v13_downloaded/")
        sys.exit(1)


def test_connection():
    """Test that the share key works by hitting the first file."""
    test_file = FILES[0]
    encoded = urllib.parse.quote(test_file)
    url = BASE_URL + encoded
    print(f"Testing connection with share key '{SHARE_KEY}'...")
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('Accept', '*/*')
        # Just get headers
        with urllib.request.urlopen(req, timeout=15) as resp:
            size = resp.headers.get('Content-Length', 'unknown')
            print(f"  Connection OK. First file size: {int(size)/(1024*1024):.1f} MB" if size != 'unknown' else "  Connection OK.")
            return True
    except Exception as e:
        print(f"  Connection FAILED: {e}")
        print("  Check that the share key is correct and not expired.")
        return False


def download_file(filename, output_dir, idx, total):
    """Download a single file with progress reporting."""
    encoded = urllib.parse.quote(filename)
    url = BASE_URL + encoded
    output_path = os.path.join(output_dir, filename)

    # Skip if already downloaded
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  [{idx}/{total}] SKIP (exists, {size_mb:.1f} MB): {filename}")
        return True

    print(f"\n  [{idx}/{total}] Downloading: {filename}")

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('Accept', '*/*')

        with urllib.request.urlopen(req, timeout=300) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            chunk_size = 1024 * 1024  # 1 MB chunks

            with open(output_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        pct = (downloaded / total_size) * 100
                        print(f"\r    Progress: {pct:.1f}% ({downloaded/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB)", end='')

        final_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\r    Done: {final_size:.1f} MB saved")
        return True

    except Exception as e:
        print(f"\r    ERROR: {e}")
        # Remove partial file
        if os.path.exists(output_path):
            os.remove(output_path)
        return False


def main():
    print("=" * 70)
    print("  EEA Industrial Reporting Database - Download Script")
    print("  Target: Latest version (v13/v14, covering 2007-2023/2024)")
    print("=" * 70)
    print()

    check_share_key()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Test connection
    if not test_connection():
        sys.exit(1)
    print()

    # Choose download set
    download_set = FILES
    print(f"Files to download: {len(download_set)}")
    print("(Run with --priority flag to download key files only)")
    print()

    success = 0
    failed = []

    for idx, filename in enumerate(download_set, 1):
        ok = download_file(filename, OUTPUT_DIR, idx, len(download_set))
        if ok:
            success += 1
        else:
            failed.append(filename)
        time.sleep(0.5)  # polite delay between requests

    print()
    print("=" * 70)
    print(f"  COMPLETE: {success}/{len(download_set)} files downloaded")
    if failed:
        print(f"  FAILED ({len(failed)} files):")
        for f in failed:
            print(f"    - {f}")
    print(f"  Location: {OUTPUT_DIR}")
    print()
    print("  NEXT STEP: Run scripts/convert_v13_to_sqlite.py")
    print("  to convert these CSV files into a queryable SQLite database.")
    print("=" * 70)


if __name__ == "__main__":
    # Support --priority flag for fast partial download
    if '--priority' in sys.argv:
        FILES.clear()
        FILES.extend(PRIORITY_FILES)
    main()
