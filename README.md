# EEA Industrial Emissions Data Analysis

Quick start guide for analyzing European industrial emissions data to identify plants with emission problems.

## 📁 Contents

1. **Industrial_Emissions_Data_Guide.md** - Comprehensive guide to EEA data sources and analysis methods
2. **eea_emissions_analyzer.py** - Python script for automated data analysis
3. **downloaded_data/** - Directory for downloaded EEA datasets (you need to populate this)

## 🚀 Quick Start

### Step 1: Download the Data

1. Visit the **EEA Data Hub**:
   - https://www.eea.europa.eu/en/datahub/datahubitem-view/9405f714-8015-4b5b-a63c-280b82861b3d

2. Look for **"Industrial Reporting... ver. 14.0 Mar. 2025 (Tabular data)"**

3. Download **CSV format** (recommended)

4. Extract all files to the `downloaded_data` directory

5. Key files needed:
   - `PUBLISH_FACILITY.csv` - Facility information
   - `PUBLISH_POLLUTANTRELEASE.csv` - Emissions data
   - `PUBLISH_POLLUTANTTRANSFER.csv` - Waste transfer data (optional)

### Step 2: Install Requirements

```bash
pip install pandas requests openpyxl
```

Optional (for visualizations):
```bash
pip install matplotlib seaborn
```

### Step 3: Run the Analysis

```bash
python eea_emissions_analyzer.py
```

The script will:
- Automatically detect and load your downloaded data files
- Identify top 50 problem plants
- Analyze emissions by sector and country
- Find pollutant hotspots (CO2, NOx, SO2, etc.)
- Generate a comprehensive summary report
- Export all results to CSV files

### Step 4: Review Results

Results are saved in `downloaded_data/analysis_results/`:
- `top_50_problem_plants_2023.csv` - Facilities with highest emissions
- `sector_analysis_2023.csv` - Emissions by industrial sector
- `country_analysis_2023.csv` - Emissions by country
- `co2_hotspots_2023.csv` - Highest CO2 emitters
- `emission_summary_report.txt` - Overall summary

## 📊 Key Pollutants to Track

### Greenhouse Gases:
- **CO2** - Carbon dioxide (climate change)
- **CH4** - Methane (climate change)
- **N2O** - Nitrous oxide (climate change)

### Air Quality:
- **NOX** - Nitrogen oxides (smog, acid rain)
- **SO2** - Sulfur dioxide (acid rain)
- **PM10** - Particulate matter (health)
- **PM2.5** - Fine particulate matter (health)

### Heavy Metals:
- **Hg** - Mercury (toxic)
- **Cd** - Cadmium (toxic)
- **Pb** - Lead (toxic)

### Organic Compounds:
- **NMVOC** - Non-methane volatile organic compounds
- **Benzene** - Known carcinogen

## 🔍 Finding Problem Plants

### Criteria for "Problem Plants":

1. **High Absolute Emissions**
   - Top 10% in their sector
   - Above regulatory thresholds

2. **Multiple Pollutants**
   - Releasing several regulated substances
   - High cumulative environmental impact

3. **Negative Trends**
   - Year-over-year emission increases
   - Failure to implement Best Available Techniques (BAT)

4. **Location-Specific Issues**
   - Facilities near sensitive areas
   - In regions with existing air/water quality problems

## 💡 Custom Analysis Examples

### Example 1: Find all facilities in Germany with CO2 > 1 million tonnes

```python
from eea_emissions_analyzer import EEAEmissionsAnalyzer

analyzer = EEAEmissionsAnalyzer()
analyzer.load_data()

# Filter releases for Germany and CO2
german_co2 = analyzer.releases_df[
    (analyzer.releases_df['ReportingYear'] == 2023) &
    (analyzer.releases_df['PollutantCode'] == 'CO2') &
    (analyzer.releases_df['TotalQuantity'] > 1_000_000_000)  # kg
]

# Merge with facility data
result = german_co2.merge(
    analyzer.facilities_df[analyzer.facilities_df['CountryCode'] == 'DE'],
    on='FacilityReportID'
)

print(result[['FacilityName', 'City', 'TotalQuantity']])
```

### Example 2: Track emission trends for a specific facility

```python
# Find facility ID first
facility = analyzer.facilities_df[
    analyzer.facilities_df['FacilityName'].str.contains('Plant Name')
].iloc[0]

# Track trends
trends = analyzer.track_trends(
    facility_id=facility['FacilityReportID'],
    start_year=2018,
    end_year=2023
)
```

### Example 3: Find facilities exceeding sector average by 200%

```python
import pandas as pd

# Calculate sector averages
sector_avg = analyzer.releases_df.groupby('MainIAActivity')['TotalQuantity'].mean()

# Find outliers
for facility in analyzer.facilities_df['FacilityReportID'].unique():
    facility_data = analyzer.releases_df[
        analyzer.releases_df['FacilityReportID'] == facility
    ]
    sector = facility_data['MainIAActivity'].iloc[0]
    total_emissions = facility_data['TotalQuantity'].sum()
    
    if total_emissions > sector_avg[sector] * 2:
        print(f"Outlier: {facility} - {total_emissions:,.0f} kg")
```

## 🌍 Alternative: Use the Web Interface

If you prefer not to code, use the **European Industrial Emissions Portal**:
- https://industry.eea.europa.eu/

Features:
- Interactive map
- Filter by country, pollutant, sector
- Export facility lists
- View individual facility profiles

## 📖 Additional Resources

### Official Documentation:
- **E-PRTR Regulation**: EU Regulation 166/2006
- **IED**: Industrial Emissions Directive 2010/75/EU
- **BAT Reference Documents**: https://eippcb.jrc.ec.europa.eu/

### Related Databases:
- **EU ETS**: Emissions Trading System data
- **National Inventories**: Country-level aggregated emissions
- **UNFCCC**: UN Climate Change reporting

### Contact:
- **EEA Industry Helpdesk**: industry.helpdesk@eea.europa.eu

## ⚠️ Important Notes

### Data Limitations:
- Only includes facilities above reporting thresholds
- Small operations may not be covered
- Some countries may have delayed submissions
- Historical data may be revised

### Reporting Thresholds:
Different pollutants have different reporting thresholds:
- CO2: 100,000 tonnes/year
- NOx: 100 tonnes/year
- Heavy metals: Often 1-20 kg/year
- See E-PRTR Regulation Annex II for full list

### Data Quality:
- Countries perform initial QA/QC
- EEA performs additional validation
- Some facilities may have estimated data
- Check metadata for known issues

## 📝 License & Citation

### Data License:
EEA standard re-use policy - free to use with attribution

### Citation:
```
European Environment Agency (EEA), Industrial Reporting under the 
Industrial Emissions Directive 2010/75/EU and European Pollutant Release 
and Transfer Register Regulation (EC) No 166/2006, Version 14.0, 
March 2025.
```

## 🔧 Troubleshooting

### "No data files found"
- Ensure you've downloaded the EEA data
- Extract files to the `downloaded_data` directory
- Check file names contain "FACILITY" or "POLLUTANTRELEASE"

### "Columns not found" errors
- EEA may update column names between versions
- Check the actual column names in your CSV files
- Update script variable names accordingly

### Memory issues with large datasets
- Use `chunksize` parameter in pandas
- Filter data by year early in the process
- Process countries individually

### Missing pollutant codes
- Some pollutants may not be reported in certain years
- Check available pollutant codes: `analyzer.releases_df['PollutantCode'].unique()`
- Refer to E-PRTR pollutant list

## 💬 Questions or Issues?

1. Check the comprehensive guide: `Industrial_Emissions_Data_Guide.md`
2. Review EEA documentation: https://industry.eea.europa.eu/about
3. Contact EEA helpdesk: industry.helpdesk@eea.europa.eu

---

**Created**: October 16, 2025  
**Data Version**: 14.0 (covering 2007-2023)  
**Last Updated**: October 16, 2025
