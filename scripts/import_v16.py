#!/usr/bin/env python3
"""
Import v16 (2022-2024) emission data from the downloaded CSV zip into the DB.
Handles the new column names and pollutant code format introduced in v16.
"""

import sqlite3
import csv
import io
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "processed" / "converted_database.db"
ZIP_PATH = ROOT / "data" / "raw" / "v_latest_downloaded" / "v16_csv_files.zip"

# Map v16 parsed codes back to v8 codes for consistency
CODE_MAP = {
    "as Hg":  "HGANDCOMPOUNDS",
    "as Ni":  "NIANDCOMPOUNDS",
    "as Pb":  "PBANDCOMPOUNDS",
    "as Zn":  "ZNANDCOMPOUNDS",
    "as Cd":  "CDANDCOMPOUNDS",
    "as As":  "ASANDCOMPOUNDS",
    "as Cr":  "CRANDCOMPOUNDS",
    "as Cu":  "CUANDCOMPOUNDS",
    "as Teq": "PCDD+PCDF(DIOXINS+FURANS)",
    "as total Cl": "CLANDCOMPOUNDS",
    "as HCl": "HCL",
    "as HF":  "HF",
    "as total F": "FLUORIDES",
    "CO2) excluding biomass": "CO2EXCLBIOMASS",
}


def parse_pollutant(raw):
    """Extract (code, name) from v16 'Name (CODE)' format."""
    idx = raw.rfind(" (")
    if idx >= 0:
        name = raw[:idx].strip()
        code = raw[idx + 2:].rstrip(")").strip()
    else:
        name = raw.strip()
        code = raw.strip()
    code = CODE_MAP.get(code, code)
    return code, name


def _safe_float(val):
    try:
        return float(str(val).replace(",", "").strip()) if val else None
    except ValueError:
        return None


def import_releases(conn, zf, csv_name, medium_filter):
    table = "2f_PollutantRelease"
    # Check existing years per medium so air and water are tracked separately
    med_clause = f"AND medium = '{list(medium_filter)[0]}'" if medium_filter else ""
    existing = {r[0] for r in conn.execute(f'SELECT DISTINCT reportingYear FROM "{table}" WHERE 1=1 {med_clause}').fetchall()}
    print(f"  Existing years in DB for {medium_filter}: {sorted(existing)}")

    inserted = skipped = 0
    with zf.open(csv_name) as raw:
        reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace"))
        batch = []
        for row in reader:
            try:
                year = int(row.get("reportingYear", ""))
            except ValueError:
                continue

            if year in existing:
                skipped += 1
                continue

            medium = (row.get("TargetRelease") or "").upper()
            if medium_filter and medium not in medium_filter:
                continue

            pollutant_raw = row.get("Pollutant", "")
            code, name = parse_pollutant(pollutant_raw)

            rec = (
                None,                                           # fileId_EPRTR_LCP
                None,                                           # PollutantReleaseId
                row.get("FacilityInspireId", ""),               # Facility_INSPIRE_ID
                year,
                code,                                           # pollutantCode
                name,                                           # pollutantName
                medium,                                         # medium
                _safe_float(row.get("Releases", "")),           # totalPollutantQuantityKg
                None,                                           # accidentalPollutantQuantityKG
                None,                                           # methodCode
                None,                                           # methodName
                None, None, None,
            )
            batch.append(rec)

            if len(batch) >= 10_000:
                conn.executemany(f'INSERT INTO "{table}" VALUES ({",".join(["?"]*14)})', batch)
                inserted += len(batch)
                batch.clear()
                print(f"\r  {inserted:,} records inserted...", end="", flush=True)

        if batch:
            conn.executemany(f'INSERT INTO "{table}" VALUES ({",".join(["?"]*14)})', batch)
            inserted += len(batch)

    conn.commit()
    print(f"\r  Done: {inserted:,} new records, {skipped:,} existing-year rows skipped.")
    return inserted


def main():
    print(f"\nDB:  {DB_PATH}")
    print(f"ZIP: {ZIP_PATH}\n")

    if not ZIP_PATH.exists():
        print("ERROR: zip not found. Run the download step first.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    zf = zipfile.ZipFile(str(ZIP_PATH))

    total = 0

    print("Importing AIR releases from F1_4_Air_Releases_Facilities.csv ...")
    total += import_releases(conn, zf, "F1_4_Air_Releases_Facilities.csv", {"AIR"})

    print("\nImporting WATER releases from F2_4_Water_Releases_Facilities.csv ...")
    total += import_releases(conn, zf, "F2_4_Water_Releases_Facilities.csv", {"WATER"})

    zf.close()
    conn.close()

    print(f"\nImport complete. {total:,} new records added.")

    # Verify
    conn = sqlite3.connect(str(DB_PATH))
    years = [r[0] for r in conn.execute('SELECT DISTINCT reportingYear FROM "2f_PollutantRelease" ORDER BY reportingYear').fetchall()]
    print(f"DB now covers years: {years}")
    conn.close()


if __name__ == "__main__":
    main()
