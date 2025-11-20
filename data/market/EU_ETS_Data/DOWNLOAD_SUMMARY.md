# EU ETS Data Download Summary

**Date Downloaded:** November 19, 2025  
**Source:** European Environment Agency (EEA) Union Registry Data  
**Data Version:** v2.0 (September 2025)  
**Temporal Coverage:** 2005-2024

## Downloaded Files

### Main Data Files (Extracted from ZIP)
Location: `eea_t_eu-emission-trading-scheme_p_2005-2024_v02_r00/`

1. **ETS_cube_final_version78_2025-09-16.xlsx**
   - Main EU ETS data cube with verified emissions, allowances, and compliance data
   - Format: Excel spreadsheet
   - Coverage: 2005-2024

2. **ETS_DataViewer_20250916.xlsx**
   - EU ETS data viewer dataset
   - Format: Excel spreadsheet
   - Aggregated data by country, sector, and year

3. **EU ETS table definition.xlsx**
   - Data dictionary and table definitions
   - Explains column meanings and data structure

### Documentation Files

4. **ETC-CM EU-ETS data quality July2025.pdf**
   - Data quality assessment report
   - Latest quality validation

5. **ETC-CM_EEA EU ETS data viewer background note_July2025.pdf**
   - Background documentation on ETS data
   - Methodology and data sources

6. **ETS.png**
   - Visual diagram of EU ETS structure

7. **README.md**
   - Additional documentation and instructions

8. **XML Metadata File**
   - Complete metadata in XML format

## Data Contents

The EU ETS data includes:
- **Verified Emissions**: Annual CO2-equivalent emissions from covered sectors
- **Allowances**: Free allocation and auctioned allowances
- **Compliance Data**: Surrender of allowances and compliance status
- **Operator Information**: Details on participating installations
- **Transactions**: Historical transaction data (where applicable)

## Coverage by Country
All EU member states and participating EEA countries:
Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Latvia, Liechtenstein, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden, Switzerland, Turkey, and others.

## Next Steps

### For Analysis
1. Open `ETS_cube_final_version78_2025-09-16.xlsx` for main data
2. Use `ETS_DataViewer_20250916.xlsx` for pre-aggregated views
3. Refer to `EU ETS table definition.xlsx` for column definitions

### For Programming Integration
The data can be imported into Python (pandas), R, or other data analysis tools:
- Excel files can be read with standard libraries
- Consider converting to CSV for easier processing
- See `README.md` for additional guidance

### Data Quality
- Check `ETC-CM EU-ETS data quality*.pdf` for known issues
- Data is verified by European Commission
- 2024 data may be preliminary (submitted by March 31, 2025)

## Files Location
`C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\data\market\EU_ETS_Data\`

## Additional Resources
- **EEA Datahub:** https://www.eea.europa.eu/en/datahub/
- **Union Registry:** https://union-registry-data.ec.europa.eu/
- **EU ETS Data Viewer:** https://www.eea.europa.eu/data-and-maps/dashboards/emissions-trading-viewer-1

---
Downloaded via EEA Direct Download Link
