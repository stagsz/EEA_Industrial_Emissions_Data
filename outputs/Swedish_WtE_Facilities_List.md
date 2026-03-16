# Swedish Waste-to-Energy Facilities

**Generated**: 2026-03-16
**Source**: EEA Industrial Emissions Portal, Avfall Sverige, Nordic Council, Harvard GSD WtE Catalogue, public sources
**Note**: The EEA database (`converted_database.db`) was not available for this query. This list is compiled from public web sources. For a definitive facility-level list with INSPIRE IDs and emission data, rebuild the database using `scripts/download/update_eea_data.py`.

## Overview

Sweden operates **34-38 waste-to-energy plants** (count varies by source and year), supplying ~1.45 million households with heat and ~780,000 with electricity. Total installed incineration capacity is approximately **7.1 Mtonnes/year** (2021). WtE supplies ~25% of all Swedish district heating and ~1.8% of electricity.

## Identified Facilities

| # | Facility Name | City | Operator / Owner | Capacity (tonnes/yr) | Notes |
|---|---------------|------|------------------|---------------------|-------|
| 1 | Hogdalenverket | Stockholm | Stockholm Exergi (Fortum + City of Stockholm) | 700,000 | One of Europe's largest WtE plants. CHP. |
| 2 | Bristaverket | Sigtuna (Stockholm area) | Stockholm Exergi | -- | Second WtE plant of Stockholm Exergi |
| 3 | Hogbytorp WtE | Upplands-Bro (Stockholm area) | Soderenergi / E.ON | ~25 MW | Biopower/waste CHP |
| 4 | Savenasverket | Gothenburg | Renova AB (municipally owned) | ~550,000 | 4 furnace lines. 30% of Gothenburg's district heating, 5% of electricity |
| 5 | SYSAV WtE Plant | Malmo | SYSAV (14 Skane municipalities) | 650,000 | Most energy-efficient WtE plant in Sweden. Carbon neutral certified. |
| 6 | Lejonpannan / TVL | Linkoping | Tekniska verken i Linkoping (municipal) | Large | One of Sweden's 3 largest WtE plants. State-of-the-art CHP. "Linkoping model" |
| 7 | Filborna WtE | Helsingborg | Oresundskraft | 160,000 (permitted) | ~50 trucks/day. 18 MW electricity. ~40% of city heating. |
| 8 | Korstaverket | Sundsvall | Sundsvall Energi | -- | CHP plant for waste fuel, operational since 2006 |
| 9 | Dava CHP Plant | Umea | Umea Energi | -- | Nearly 100% waste-fueled. Sorted waste + forest residues. |
| 10 | Malarenergi CHP | Vasteras | Malarenergi (municipal) | -- | WtE + biomass CHP. Building 300,000 m3 underground hot water storage. |
| 11 | Vattenfall WtE | Uppsala | Vattenfall / Uppsala municipality | -- | District heating from waste incineration |
| 12 | E.ON Norrkoping | Norrkoping | E.ON | -- | WtE district heating |
| 13 | Boras Energi | Boras | Boras Energi och Miljo (municipal) | -- | Municipal WtE plant |
| 14 | Jonkoping WtE | Jonkoping | Jonkoping Energi (municipal) | -- | Municipal WtE/CHP |
| 15 | Halmstad WtE | Halmstad | Halmstad Energi och Miljo | -- | Municipal WtE plant |
| 16 | Karlstad WtE | Karlstad | Karlstad Energi (municipal) | -- | Municipal WtE/CHP |
| 17 | Gavle WtE | Gavle | Gavle Energi (municipal) | -- | Municipal WtE plant |
| 18 | Nassjo Affarsverk | Nassjo | Nassjo Affarsverk AB (municipal) | -- | Smaller municipal WtE. See: outputs/Nassjo_Affarsverk_Deep_Dive.pdf |
| 19 | Kristianstad WtE | Kristianstad | C4 Energi (municipal) | -- | Municipal WtE/CHP |
| 20 | Borlange WtE | Borlange | Borlange Energi (municipal) | -- | Municipal WtE plant |
| 21 | Kumla WtE | Kumla | Kumla Energi (municipal) | -- | Smaller municipal WtE |
| 22 | Eksjo WtE | Eksjo | Eksjo Energi (municipal) | -- | Smaller municipal WtE |
| 23 | Kiruna WtE | Kiruna | Kiruna municipality / Tekniska Verken Kiruna | -- | Northernmost WtE in Sweden |

**Additional plants exist** but could not be confirmed from available public sources. The total count of 34-38 suggests 11-15 additional facilities not individually identified here.

## EEA Activity Codes for WtE in Sweden

| Code | Description | Usage |
|------|-------------|-------|
| 5(b) | Installations for the incineration of non-hazardous waste (IED scope, capacity >= 3 tonnes/hour) | Main code for Swedish WtE |
| 5(c) | Installations for the disposal of non-hazardous waste (capacity > 50 tonnes/day) | Some waste disposal facilities |

## How to Get the Complete, Authoritative List

### Option 1: Rebuild the EEA Database (Recommended)
```bash
cd /home/user/EEA_Industrial_Emissions_Data

# 1. Get share key from https://industry.eea.europa.eu/download
# 2. Update SHARE_KEY in scripts/download/update_eea_data.py
# 3. Run:
python scripts/download/update_eea_data.py

# 4. Then query:
# SELECT DISTINCT f.facilityName, f.city, f.Facility_INSPIRE_ID, i.mainActivityCode
# FROM "2_ProductionFacility" f
# JOIN "3_ProductionInstallation" i ON f.Facility_INSPIRE_ID = i.Facility_INSPIRE_ID
# WHERE f.countryCode = 'SE'
#   AND (i.mainActivityCode LIKE '5(b)%' OR i.mainActivityCode LIKE '5(c)%')
# ORDER BY f.facilityName;
```

### Option 2: Swedish EPA PRTR
1. Go to https://utslappisiffror.naturvardsverket.se/en/Search/
2. Select Sector: "5. Waste and waste water management" -> "5(b)"
3. Search for all Swedish facilities

### Option 3: CEWEP Interactive Map
- Visit https://www.cewep.eu/interactive-map-of-waste-to-energy-plants/
- Click on Sweden to see individual plants

### Option 4: Avfall Sverige Reports
- https://www.avfallsverige.se/in-english/
- Annual "Kapacitetsutredning" (capacity survey) contains complete plant-by-plant data

## Key Operators in Sweden

| Operator | Plants | Type |
|----------|--------|------|
| Stockholm Exergi | 2+ | Municipal (Stockholm) |
| Renova AB | 1+ | Municipal (Gothenburg region) |
| SYSAV | 1 | Municipal consortium (Skane, 14 municipalities) |
| Tekniska verken i Linkoping | 1+ | Municipal |
| E.ON | 1+ | Private |
| Vattenfall | 1+ | State-owned |
| Various municipal energy companies | ~25 | Municipal |

## GMAB Sales Relevance

Per market analysis (docs/market_analysis/WTE_ANALYSIS_SUMMARY_FOR_AGENTS.md):
- Sweden: **36 plants** (Priority 3 market per ecoprog data)
- EU BAT compliance mandatory (0.05 ng I-TEQ/Nm3 target)
- Average fleet age 15-25 years - entering replacement/upgrade cycle
- Nordic market is core GMAB territory (SE, DK, FI, NO)
- SYSAV already identified as mock lead in agents/lead_generation_agent.py
- Nassjo Affarsverk has existing deep-dive analysis (outputs/)
