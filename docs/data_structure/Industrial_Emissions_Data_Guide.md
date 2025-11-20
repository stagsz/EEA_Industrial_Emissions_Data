# European Industrial Emissions Data - Complete Guide

## Overview
The European Environment Agency (EEA) maintains comprehensive databases of industrial emissions across Europe through the **European Pollutant Release and Transfer Register (E-PRTR)** and **Industrial Emissions Directive (IED)** reporting systems.

### Data Integration Status
** Updated: November 19, 2025**
- E-PRTR Industrial Emissions: Fully operational
- **EU ETS Data: NOW AVAILABLE** - See EU Emissions Trading System section below

## Key Database: Industrial Reporting Database

### Coverage
- **Geographic Coverage**: EU-27 Member States, plus Iceland, Liechtenstein, Norway, Serbia, Switzerland, and the United Kingdom
- **Time Period**: 2007-2023 (latest version published March 2025)
- **Facilities**: Approximately 34,000 industrial facilities across 65 economic activities

### What Data is Available

The database includes:
1. **Location and Administrative Data** for the largest industrial complexes
2. **Pollutant Releases**:
   - Air emissions
   - Water releases
   - Land releases
   - 91 different pollutants tracked
3. **Waste Transfers**: Both hazardous and non-hazardous waste
4. **Large Combustion Plants (LCP) Data**: Detailed energy input and emissions data (2016-2023)

### Industries Covered
The E-PRTR covers 65 economic activities including:
- Energy production (combustion plants, refineries)
- Metal production and processing
- Chemical industry
- Waste and wastewater management
- Paper and pulp industry
- Mining operations
- Food and beverage production
- Intensive agriculture

## Main Data Access Points

### 1. European Industrial Emissions Portal
**URL**: https://industry.eea.europa.eu/

Features:
- Interactive web interface
- Search by facility, country, pollutant, or industry sector
- Map-based visualization
- Downloadable datasets

### 2. Latest Dataset (Version 14.0, March 2025)
**Direct Link**: https://www.eea.europa.eu/en/datahub/datahubitem-view/9405f714-8015-4b5b-a63c-280b82861b3d

**Available Formats**:
- Microsoft Excel (.xlsx)
- CSV files (.csv)
- Microsoft Access database (.accdb)
- SQL format
- Spatial data (GeoPackage, Geodatabase, REST services, WMS)

**Temporal Coverage**: 2007-2023

### 3. Download Page
**URL**: https://industry.eea.europa.eu/download

Direct access to:
- Industrial reporting datasets
- Guidance documents (in 20+ languages)
- Diffuse emissions studies
- Historical versions

## Finding Plants with Emission Problems

### Approach 1: Use the Interactive Portal
1. Visit https://industry.eea.europa.eu/
2. Use the search/filter functions to:
   - Select specific pollutants (e.g., CO2, NOx, SO2, particulate matter)
   - Filter by country or region
   - Filter by industry sector
   - Set emission thresholds

### Approach 2: Download and Analyze the Data

The database contains multiple tables:

#### Key Tables for Identifying Problem Facilities:

1. **PUBLISH_POLLUTANTRELEASE**
   - Contains all reported pollutant releases
   - Fields include:
     - FacilityReportID
     - PollutantCode
     - ReleaseQuantity
     - MediumCode (Air/Water/Land)
     - ReportingYear

2. **PUBLISH_FACILITY**
   - Facility location and details
   - Fields include:
     - FacilityReportID
     - FacilityName
     - CountryCode
     - City
     - Coordinates (Lat/Long)
     - MainIAActivity (Industrial activity type)

3. **PUBLISH_POLLUTANTTRANSFER**
   - Off-site waste transfers
   - Pollutants in wastewater

4. **LCP_* Tables** (Large Combustion Plants)
   - Detailed emissions data for power plants
   - Fuel consumption
   - Operating hours
   - Specific emission values

### Approach 3: Key Indicators for "Problem Plants"

Plants with emission concerns typically show:

1. **High Absolute Emissions**
   - Among top emitters in their sector
   - Exceeding sector averages by significant margins

2. **Multiple Pollutant Releases**
   - Releasing several regulated pollutants simultaneously
   - High ecotoxicity potential

3. **Increasing Trends**
   - Year-over-year increases in emissions
   - Failure to implement BAT (Best Available Techniques)

4. **Regulatory Non-Compliance**
   - Facilities that don't meet emission limits
   - Those under enforcement actions

## Pollutants to Focus On

### Air Pollutants:
- **Greenhouse Gases**: CO2, CH4, N2O
- **Acidification**: SO2 (Sulfur dioxide), NOx (Nitrogen oxides)
- **Health Hazards**: PM10, PM2.5 (Particulate matter)
- **Toxic**: Heavy metals (Lead, Mercury, Cadmium), Benzene, Dioxins

### Water Pollutants:
- Heavy metals (Mercury, Cadmium, Lead, Nickel)
- Nitrogen and Phosphorus (eutrophication)
- Organic pollutants
- Chlorides

### Priority Sectors for Emission Problems:

Based on EEA analysis:
1. **Energy Production** - Largest contributor to air emissions
2. **Metal Manufacturing** - Heavy metals and toxic releases
3. **Chemical Industry** - Diverse pollutant portfolio
4. **Cement and Lime Production** - High CO2 emissions
5. **Pulp and Paper** - Water pollution concerns

## Data Download Instructions

### For CSV/Excel Analysis:

1. Go to: https://www.eea.europa.eu/en/datahub/datahubitem-view/9405f714-8015-4b5b-a63c-280b82861b3d
2. Look for "Industrial Reporting... ver. 14.0 Mar. 2025 (Tabular data)"
3. Download preferred format:
   - Excel for quick analysis
   - CSV for programming/scripting
   - Access database for relational queries

### File Structure:
The download typically includes:
- Multiple CSV/Excel files (one per table)
- Metadata file (data dictionary)
- Guidance document
- Data quality notes

## Example Analysis Queries

### SQL Query Example (if using Access or importing to database):
```sql
SELECT
    f.FacilityName,
    f.CountryCode,
    f.City,
    f.MainIAActivity,
    pr.PollutantName,
    pr.MediumCode,
    SUM(pr.TotalQuantity) as Total_Emissions,
    pr.ReportingYear
FROM PUBLISH_FACILITY f
JOIN PUBLISH_POLLUTANTRELEASE pr ON f.FacilityReportID = pr.FacilityReportID
WHERE pr.PollutantCode IN ('CO2', 'NOX', 'SO2', 'PM10')
  AND pr.ReportingYear >= 2020
GROUP BY f.FacilityName, f.CountryCode, pr.PollutantName, pr.ReportingYear
HAVING SUM(pr.TotalQuantity) > 1000000  -- Facilities emitting over 1M kg
ORDER BY Total_Emissions DESC;
```

### Excel/Python Analysis Approach:
1. Load PUBLISH_FACILITY table
2. Load PUBLISH_POLLUTANTRELEASE table
3. Join on FacilityReportID
4. Filter by:
   - Specific pollutants
   - Emission thresholds
   - Geographic area
   - Industry sector
5. Calculate percentiles or rank facilities
6. Identify outliers and trends

## Important Notes

### Data Quality:
- Countries perform quality checks before submission
- EEA performs additional validation
- Some countries may have delayed or incomplete reporting
- Historical data for some countries mapped from older systems

### Reporting Thresholds:
- Not all emissions are reported
- Only facilities exceeding specific thresholds must report
- Small facilities may not be included
- Different thresholds for different pollutants

### Data Updates:
- Annual updates typically in December
- Quality-checked data released in March/April
- Historical data may be revised

## Additional Resources

### Related Databases:
1. **EU Emissions Trading System (ETS)**
   - Greenhouse gas emissions from large installations
   - Carbon trading data
   - URL: Available through EEA website

2. **National Emission Inventories**
   - Country-level aggregated data
   - Includes diffuse sources

3. **Diffuse Emissions Data**
   - Air: Road transport, shipping, agriculture
   - Water: Agricultural runoff, urban wastewater

### Reports and Analysis:
- **Industrial Pollution Country Profiles** (by country)
- **Trends in Industrial Pollution** (periodic assessments)
- **Sectoral Analysis Reports**

### Guidance Documents:
- E-PRTR Reporting Guidelines (20+ languages)
- Best Available Techniques (BAT) Reference Documents
- Data Quality Procedures

## Contact Information

**Industry Helpdesk**: industry.helpdesk@eea.europa.eu

For questions about:
- Data interpretation
- Reporting requirements
- Technical issues
- Data corrections

## Quick Start Recommendations

### For Finding Problem Plants:

**Option 1 - Quick Visual Identification:**
1. Visit https://industry.eea.europa.eu/
2. Use map interface
3. Filter by your target country/region and pollutant
4. Sort facilities by emission quantity
5. Export list of top emitters

**Option 2 - Detailed Analysis:**
1. Download latest CSV/Excel dataset
2. Focus on PUBLISH_POLLUTANTRELEASE and PUBLISH_FACILITY tables
3. Import into Excel, Python, or R
4. Calculate:
   - Total emissions by facility
   - Emissions per production unit (if data available)
   - Year-over-year trends
   - Percentile rankings within sectors
5. Identify facilities in top 10% of emitters
6. Cross-reference with environmental incidents/complaints if available

**Option 3 - Regulatory Compliance Focus:**
- Look for facilities with enforcement actions
- Check against Best Available Techniques (BAT) conclusions
- Identify facilities with outdated technology
- Note facilities with increasing emissions despite BAT requirements

## Data Citation

When using this data, cite as:
European Environment Agency (EEA), Industrial Reporting under the Industrial Emissions Directive 2010/75/EU and European Pollutant Release and Transfer Register Regulation (EC) No 166/2006, Version 14.0, March 2025.
DOI: https://doi.org/10.2909/[specific DOI from dataset]

---

## EU Emissions Trading System (ETS) Data  NEW

### Overview
The EU ETS is the cornerstone of the EU's climate policy and provides complementary data to the E-PRTR industrial emissions reports. While E-PRTR covers all pollutants from large industrial sources, the EU ETS specifically tracks greenhouse gas emissions and carbon allowance trading for large installations.

### Data Available
**Version**: 2.0 (September 2025)
**Temporal Coverage**: 2005-2024
**Geographic Coverage**: All EU member states + EEA countries
**Format**: Excel workbooks + CSV data

### Files Included
1. **ETS_cube_final_version78_2025-09-16.xlsx**
   - Main data cube with detailed installation-level data
   - Verified CO2-equivalent emissions
   - Free allowances and auction allowances
   - Compliance status
   - Installation information

2. **ETS_DataViewer_20250916.xlsx**
   - Pre-aggregated data viewer
   - Aggregated by country, sector, and year
   - Easier for dashboard and reporting
   - Interactive pivot-table ready

3. **EU ETS table definition.xlsx**
   - Data dictionary explaining all fields
   - Field descriptions and formats
   - Validation rules

### Key Data Elements

#### Emissions Data
- **Verified emissions** (tCO2e) by installation and year
- Includes Scopes 1, 2 (for specific sectors), and some Scope 3
- Quality-assured and verified by accredited verifiers
- Annual reporting (submissions by March 31)

#### Allowances
- **Free allocation**: Based on benchmarks and historical data
- **Auctioned allowances**: Available through public auctions
- **Surplus/deficit**: Installations with excess or shortfall
- **Banking/borrowing**: Multi-year flexibility mechanisms

#### Compliance Tracking
- **Surrendered units**: Against verified emissions
- **Penalties**: Non-compliance actions (€100/tCO2e penalty from 2021)
- **Installation status**: Active, closed, or transferred

#### Installation Information
- **Operator details**: Company name, contact, permit number
- **Facility location**: Coordinates, city, address
- **Main activity**: NACE code, sector classification
- **Capacity data**: Production capacity, fuel input where available

### Integration with E-PRTR Data

**Complementary Perspective:**
- **E-PRTR**: All pollutants (CO2, NOx, SO2, heavy metals, etc.)
- **EU ETS**: Focused on greenhouse gases (CO2, N2O, PFCs for certain sectors)

**Facility Matching:**
- Most large industrial facilities appear in both databases
- Use facility names, locations, and NAC codes for correlation
- ETS installations cover ~11,000 major emitters
- E-PRTR covers ~34,000 facilities (includes smaller ones)

**Combined Analysis Value:**
1. **Carbon costs**: ETS allowance prices vs. emissions
2. **Environmental burden**: E-PRTR pollutants + ETS carbon impact
3. **Compliance pressure**: Both systems' requirements
4. **Urgency scoring**: Facilities with both high emissions and carbon cost exposure

### Data Access

**Location**: `data/market/EU_ETS_Data/`

**Download Source**: European Environment Agency Datahub
URL: https://www.eea.europa.eu/en/datahub/datahubitem-view/98f04097-26de-4fca-86c4-63834818c0c0

**Quality Assurance**:
- ETC-CM EU-ETS data quality reports (quarterly)
- Latest: September 2025
- Background notes available for methodology

### Suggested Analysis Approaches

#### Approach 1: Identify Carbon Cost Exposure
```
SELECT installations WHERE:
  - Verified emissions > 50,000 tCO2e/year
  - AND compliance deficit in recent years
  - AND free allocation declining
  - RANK by emission trend (increasing = urgent need)
```

#### Approach 2: Compliance Risk Assessment
```
SELECT installations WHERE:
  - Emissions growing vs. 2005 baseline (should decline)
  - Shortfall in allowances (need to buy/reduce)
  - Allocation mechanism changes approaching
  - Result: Sales opportunity for emission reduction solutions
```

#### Approach 3: Technology Investment Indicators
```
SELECT installations WHERE:
  - High emissions but low emissions intensity
  - Growing production + growing emissions
  - Still using BAT from 2000s (dated benchmarks)
  - Result: Candidates for technology upgrade investments
```

### Key Metrics for Lead Scoring

1. **Absolute Emission Level**: tCO2e/year
2. **Compliance Status**: Surplus/deficit in allowances
3. **Emission Trend**: % change year-over-year
4. **Carbon Cost Exposure**: Allowance deficit × carbon price
5. **Sector**: Energy-intensive vs. less intensive
6. **Installation Status**: Active, expanding, or closing

### Regulatory Context

**EU ETS Phases:**
- **Phase 1 (2005-2007)**: Pilot phase, free allocation 100%
- **Phase 2 (2008-2012)**: First real compliance period, 90% free
- **Phase 3 (2013-2020)**: Increasing auctioning, transition to 100%
- **Phase 4 (2021-2030)**: Market-based allocation, strengthened targets

**2024-2025 Relevance:**
- Phase 4 in progress: Tighter emission caps
- EU ETS Directive amendment passed (2023)
- Carbon Boarder Adjustment Mechanism (CBAM) starting
- Free allocation declining towards zero for some sectors

### Contact & Resources

**Data Provider**: European Environment Agency
**Technical Support**: https://www.eea.europa.eu/about-us/contact

**Latest Reports**:
- EU ETS data viewer: https://www.eea.europa.eu/en/analysis/maps-and-charts/emissions-trading-viewer-1-dashboards
- Background documentation: Included in download package

---

**EU ETS Data Added**: November 19, 2025
**Document Created**: October 16, 2025
**E-PRTR Data Version**: 14.0 (March 2025)
**EU ETS Data Version**: 2.0 (September 2025)
**Temporal Coverage**: 2007-2023 (E-PRTR), 2005-2024 (EU ETS)
**Last Updated**: November 19, 2025
