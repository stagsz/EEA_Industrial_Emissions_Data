# European Industrial Emissions Data - Complete Guide

## Overview
The European Environment Agency (EEA) maintains comprehensive databases of industrial emissions across Europe through the **European Pollutant Release and Transfer Register (E-PRTR)** and **Industrial Emissions Directive (IED)** reporting systems.

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

**Document Created**: October 16, 2025
**Data Version**: 14.0 (March 2025)
**Temporal Coverage**: 2007-2023
**Last Updated**: October 16, 2025
