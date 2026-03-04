#!/usr/bin/env python3
"""
EEA Data Update Script
======================
Step 1 of 2: Download latest EEA CSV files
Step 2 of 2: Import them into the SQLite database

HOW TO GET A FRESH SHARE KEY
------------------------------
1. Open this page in a browser:
   https://industry.eea.europa.eu/download
2. Choose "Download as CSV (all files)" for the latest version
3. You will be redirected to a Nextcloud URL like:
   https://sdi.eea.europa.eu/datashare/s/XXXXXXXXXX/download?path=...
4. Copy the part between /s/ and /download  (that is your SHARE_KEY)
5. Paste it into SHARE_KEY below and run this script

Current DB covers: 2007-2021 (v8)
Latest available : ~2007-2023 (v13) or 2007-2024 (v14)

After this script completes, re-run search_app.py — the new years
will appear automatically in the Year slider.
"""

import sqlite3
import csv
import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURATION  ← only thing you need to change
# ─────────────────────────────────────────────
SHARE_KEY = "PASTE_NEW_SHARE_KEY_HERE"

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "processed" / "converted_database.db"
DOWNLOAD_DIR = ROOT / "data" / "raw" / "v_latest_downloaded"

BASE_URL = f"https://sdi.eea.europa.eu/datashare/s/{SHARE_KEY}/download?path=%2FCSV&files="

# Files to download (same names across all versions)
DOWNLOAD_FILES = [
    "F6_1_Total Information on Installations.csv",
    "F1_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Air.csv",
    "F2_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Water.csv",
    "F7_1_Detailed information on WI and co-WI.csv",
    "F3_2_Detailed pollutant transfer at facility level with E-PRTR Sector and Annex I Activity.csv",
    "F4_2_Detailed waste transfer at facility level with E-PRTR Sector and Annex I Activity.csv",
    "F5_2_Detailed emissions and energy input from LCP.csv",
    "F1_1_Total Releases at National Level into Air.csv",
    "F2_1_Total Releases at National Level into Water.csv",
]

# ─────────────────────────────────────────────
# STEP 1 – DOWNLOAD
# ─────────────────────────────────────────────

def check_key():
    if SHARE_KEY == "PASTE_NEW_SHARE_KEY_HERE":
        print("=" * 65)
        print("  ERROR: Share key not set!")
        print("=" * 65)
        print()
        print("  1. Visit: https://industry.eea.europa.eu/download")
        print("  2. Click the latest CSV download button")
        print("  3. Copy the share key from the redirect URL")
        print("     URL format: https://sdi.eea.europa.eu/datashare/s/[KEY]/...")
        print("  4. Set SHARE_KEY at the top of this script")
        print()
        sys.exit(1)


def download_file(filename, idx, total):
    encoded = urllib.parse.quote(filename)
    url = BASE_URL + encoded
    out = DOWNLOAD_DIR / filename

    if out.exists() and out.stat().st_size > 1_000:
        print(f"  [{idx}/{total}] SKIP (exists): {filename}")
        return True

    print(f"\n  [{idx}/{total}] Downloading: {filename}")
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=600) as resp:
            total_bytes = int(resp.headers.get("Content-Length", 0))
            done = 0
            with open(out, "wb") as f:
                while chunk := resp.read(1024 * 1024):
                    f.write(chunk)
                    done += len(chunk)
                    if total_bytes:
                        pct = done / total_bytes * 100
                        print(f"\r    {pct:.1f}% ({done / 1e6:.0f}/{total_bytes / 1e6:.0f} MB)", end="")
        print(f"\r    Done: {out.stat().st_size / 1e6:.1f} MB")
        return True
    except Exception as e:
        print(f"\r    ERROR: {e}")
        if out.exists():
            out.unlink()
        return False


def run_downloads():
    check_key()
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nDownloading {len(DOWNLOAD_FILES)} files to {DOWNLOAD_DIR}\n")

    ok, fail = 0, []
    for i, f in enumerate(DOWNLOAD_FILES, 1):
        if download_file(f, i, len(DOWNLOAD_FILES)):
            ok += 1
        else:
            fail.append(f)
        time.sleep(0.3)

    print(f"\nDownloaded {ok}/{len(DOWNLOAD_FILES)} files.")
    if fail:
        print("Failed:", fail)
    return len(fail) == 0


# ─────────────────────────────────────────────
# STEP 2 – IMPORT INTO SQLITE
# Column mappings: F-file column → SQLite column
# ─────────────────────────────────────────────

# F6_1 → used to update 2_ProductionFacility (facility registry)
F6_FACILITY_MAP = {
    "InstallationInspireID":  None,   # links to Installation, not Facility
    "installationName":       "nameOfFeature",
    "CityofFacility":         "city",
    "Latitude":               "pointGeometryLat",
    "Longitude":              "pointGeometryLon",
    "IEDActivityCode":        "mainActivityCode",
    "IEDActivityName":        "mainActivityName",
    "countryName":            "_countryName",   # need to map to countryCode
    "reportingYear":          "_reportingYear",
}

COUNTRY_CODE_MAP = {
    "Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Switzerland": "CH",
    "Cyprus": "CY", "Czech Republic": "CZ", "Germany": "DE", "Denmark": "DK",
    "Estonia": "EE", "Spain": "ES", "Finland": "FI", "France": "FR",
    "United Kingdom": "GB", "Greece": "GR", "Croatia": "HR", "Hungary": "HU",
    "Ireland": "IE", "Iceland": "IS", "Italy": "IT", "Liechtenstein": "LI",
    "Lithuania": "LT", "Luxembourg": "LU", "Latvia": "LV", "Malta": "MT",
    "Netherlands": "NL", "Norway": "NO", "Poland": "PL", "Portugal": "PT",
    "Romania": "RO", "Serbia": "RS", "Sweden": "SE", "Slovenia": "SI",
    "Slovakia": "SK",
}

# F1_4 columns → 2f_PollutantRelease columns
F1_RELEASE_COLS = {
    "facilityInspireID":          "Facility_INSPIRE_ID",
    "reportingYear":              "reportingYear",
    "EPRTRAnnexIPollutantCode":   "pollutantCode",
    "pollutantName":              "pollutantName",
    "Medium":                     "medium",
    "totalPollutantQuantityKg":   "totalPollutantQuantityKg",
    "AccidentalPollutantQuantityKg": "accidentalPollutantQuantityKG",
    "MethodUsed":                 "methodCode",
    "MethodName":                 "methodName",
}


def get_existing_years(conn, table):
    try:
        df_years = conn.execute(f'SELECT DISTINCT reportingYear FROM "{table}"').fetchall()
        return {r[0] for r in df_years}
    except Exception:
        return set()


def import_releases(conn, csv_path, medium_filter=None):
    """Import new-year records from F1_4 or F2_4 into 2f_PollutantRelease."""
    table = "2f_PollutantRelease"
    existing_years = get_existing_years(conn, table)
    print(f"  Existing years in DB: {sorted(existing_years)}")

    inserted = 0
    skipped = 0

    with open(csv_path, encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        print(f"  CSV columns: {headers[:10]} ...")

        batch = []
        for row in reader:
            year_str = (
                row.get("reportingYear") or row.get("ReportingYear") or ""
            )
            try:
                year = int(year_str)
            except ValueError:
                continue

            if year in existing_years:
                skipped += 1
                continue

            medium = row.get("Medium") or row.get("medium") or ""
            if medium_filter and medium.upper() not in medium_filter:
                continue

            rec = (
                None,                                                      # fileId_EPRTR_LCP
                None,                                                      # PollutantReleaseId
                row.get("facilityInspireID") or row.get("FacilityInspireID", ""),
                year,
                row.get("EPRTRAnnexIPollutantCode") or row.get("pollutantCode", ""),
                row.get("pollutantName", ""),
                medium.upper(),
                _safe_float(row.get("totalPollutantQuantityKg", "")),
                _safe_float(row.get("AccidentalPollutantQuantityKg", "0")),
                row.get("MethodUsed") or row.get("methodCode", ""),
                row.get("MethodName") or row.get("methodName", ""),
                None, None, None,
            )
            batch.append(rec)

            if len(batch) >= 10_000:
                conn.executemany(
                    f'INSERT INTO "{table}" VALUES ({",".join(["?"]*14)})',
                    batch,
                )
                inserted += len(batch)
                batch = []
                print(f"\r  Inserted {inserted:,} new records...", end="")

        if batch:
            conn.executemany(
                f'INSERT INTO "{table}" VALUES ({",".join(["?"]*14)})',
                batch,
            )
            inserted += len(batch)

    conn.commit()
    print(f"\r  Done: {inserted:,} new records inserted, {skipped:,} existing-year rows skipped.")
    return inserted


def _safe_float(val):
    try:
        return float(str(val).replace(",", "").strip()) if val else None
    except ValueError:
        return None


def import_facilities(conn, csv_path):
    """Add any new facilities from F6_1 that don't exist in 2_ProductionFacility."""
    table = "2_ProductionFacility"
    existing_ids = {
        r[0] for r in conn.execute(f'SELECT Facility_INSPIRE_ID FROM "{table}"').fetchall()
    }
    print(f"  Existing facilities in DB: {len(existing_ids):,}")

    inserted = 0
    with open(csv_path, encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            # F6 is installation-level (not facility-level), skip facility insert
            # Just report years available
            pass

    years = set()
    with open(csv_path, encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            years.add(row.get("reportingYear", ""))

    print(f"  New data years in F6: {sorted(years)}")
    return 0


def run_import():
    print(f"\nOpening database: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))

    csv_air = DOWNLOAD_DIR / "F1_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Air.csv"
    csv_water = DOWNLOAD_DIR / "F2_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Water.csv"
    csv_f6 = DOWNLOAD_DIR / "F6_1_Total Information on Installations.csv"

    total = 0
    if csv_air.exists():
        print(f"\nImporting AIR releases from {csv_air.name} ...")
        total += import_releases(conn, csv_air, medium_filter={"AIR"})
    else:
        print(f"  SKIP (not found): {csv_air.name}")

    if csv_water.exists():
        print(f"\nImporting WATER releases from {csv_water.name} ...")
        total += import_releases(conn, csv_water, medium_filter={"WATER"})
    else:
        print(f"  SKIP (not found): {csv_water.name}")

    if csv_f6.exists():
        print(f"\nChecking facility registry from {csv_f6.name} ...")
        import_facilities(conn, csv_f6)

    conn.close()
    print(f"\nImport complete. {total:,} new emission records added to DB.")
    print("Restart search_app.py to see the new years in the Year slider.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Update EEA database with latest data")
    parser.add_argument("--download-only", action="store_true",
                        help="Only download files, skip DB import")
    parser.add_argument("--import-only", action="store_true",
                        help="Skip download, only import already-downloaded files")
    args = parser.parse_args()

    print("=" * 65)
    print("  EEA Industrial Emissions Data Updater")
    print("=" * 65)

    if not args.import_only:
        ok = run_downloads()
        if not ok and not args.download_only:
            print("\nSome downloads failed. Attempting import with partial data.")

    if not args.download_only:
        run_import()
