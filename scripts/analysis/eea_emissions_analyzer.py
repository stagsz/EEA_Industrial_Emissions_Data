"""
EEA Industrial Emissions Data Downloader and Analyzer
======================================================

This script helps download and analyze industrial emissions data from the 
European Environment Agency (EEA) to identify plants with emission problems.

Requirements:
- pandas
- requests
- matplotlib (optional, for visualizations)
- seaborn (optional, for visualizations)

Usage:
    python eea_emissions_analyzer.py

Author: Generated for EEA Data Analysis
Date: October 16, 2025
"""

import pandas as pd
import requests
import os
from datetime import datetime
from pathlib import Path

# Configuration
DATA_DIR = Path("downloaded_data")
DATA_DIR.mkdir(exist_ok=True)

# EEA Data URLs (These are examples - actual URLs from the EEA portal)
BASE_URL = "https://industry.eea.europa.eu"
DATA_PORTAL = "https://www.eea.europa.eu/en/datahub/datahubitem-view/9405f714-8015-4b5b-a63c-280b82861b3d"

class EEAEmissionsAnalyzer:
    """
    A class to download, process, and analyze EEA industrial emissions data.
    """
    
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = Path(data_dir)
        self.facilities_df = None
        self.releases_df = None
        self.transfers_df = None
        
    def download_instructions(self):
        """
        Print instructions for downloading data manually from EEA portal.
        """
        print("=" * 80)
        print("EEA INDUSTRIAL EMISSIONS DATA DOWNLOAD INSTRUCTIONS")
        print("=" * 80)
        print()
        print("Since the EEA data requires interactive download, please follow these steps:")
        print()
        print("1. Visit the EEA Data Hub:")
        print(f"   {DATA_PORTAL}")
        print()
        print("2. Look for 'Industrial Reporting... ver. 14.0 Mar. 2025 (Tabular data)'")
        print()
        print("3. Download one of these formats:")
        print("   - CSV files (recommended for this script)")
        print("   - Excel files (.xlsx)")
        print("   - Microsoft Access (.accdb)")
        print()
        print("4. Extract the files to this directory:")
        print(f"   {self.data_dir.absolute()}")
        print()
        print("5. The main files you need are:")
        print("   - PUBLISH_FACILITY.csv (or .xlsx)")
        print("   - PUBLISH_POLLUTANTRELEASE.csv (or .xlsx)")
        print("   - PUBLISH_POLLUTANTTRANSFER.csv (optional)")
        print()
        print("=" * 80)
        
    def load_data(self, facilities_file=None, releases_file=None, transfers_file=None):
        """
        Load the downloaded EEA data files.
        
        Parameters:
        -----------
        facilities_file : str or Path
            Path to the facilities data file (CSV or Excel)
        releases_file : str or Path
            Path to the pollutant releases data file
        transfers_file : str or Path (optional)
            Path to the pollutant transfers data file
        """
        print("Loading data files...")
        
        # Auto-detect files if not specified
        if facilities_file is None:
            facilities_file = self._find_file("FACILITY")
        if releases_file is None:
            releases_file = self._find_file("POLLUTANTRELEASE")
        if transfers_file is None:
            transfers_file = self._find_file("POLLUTANTTRANSFER")
            
        # Load facilities
        if facilities_file:
            print(f"Loading facilities from: {facilities_file}")
            self.facilities_df = self._load_file(facilities_file)
            print(f"  Loaded {len(self.facilities_df)} facilities")
        else:
            print("  Warning: Facilities file not found")
            
        # Load releases
        if releases_file:
            print(f"Loading pollutant releases from: {releases_file}")
            self.releases_df = self._load_file(releases_file)
            print(f"  Loaded {len(self.releases_df)} release records")
        else:
            print("  Warning: Releases file not found")
            
        # Load transfers (optional)
        if transfers_file:
            print(f"Loading pollutant transfers from: {transfers_file}")
            self.transfers_df = self._load_file(transfers_file)
            print(f"  Loaded {len(self.transfers_df)} transfer records")
            
        print("Data loading complete!")
        
    def _find_file(self, keyword):
        """Find a file in data directory containing keyword."""
        for ext in ['.csv', '.xlsx', '.xls']:
            files = list(self.data_dir.glob(f"*{keyword}*{ext}"))
            if files:
                return files[0]
        return None
        
    def _load_file(self, filepath):
        """Load CSV or Excel file."""
        filepath = Path(filepath)
        if filepath.suffix.lower() == '.csv':
            return pd.read_csv(filepath, low_memory=False)
        elif filepath.suffix.lower() in ['.xlsx', '.xls']:
            return pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
    
    def find_problem_plants(self, pollutant_codes=None, year=2023, 
                           top_n=50, threshold=None):
        """
        Identify plants with emission problems.
        
        Parameters:
        -----------
        pollutant_codes : list of str
            List of pollutant codes to analyze (e.g., ['CO2', 'NOX', 'SO2'])
            If None, analyzes all pollutants
        year : int
            Reporting year to analyze
        top_n : int
            Number of top emitters to return
        threshold : float
            Minimum emission quantity (in kg) to consider
            
        Returns:
        --------
        pd.DataFrame : Problem plants with their emission details
        """
        if self.releases_df is None or self.facilities_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        print(f"\nAnalyzing emissions for year {year}...")
        
        # Filter by year
        releases = self.releases_df[self.releases_df['ReportingYear'] == year].copy()
        
        # Filter by pollutants if specified
        if pollutant_codes:
            releases = releases[releases['PollutantCode'].isin(pollutant_codes)]
            print(f"  Filtering for pollutants: {', '.join(pollutant_codes)}")
        
        # Filter by threshold if specified
        if threshold:
            releases = releases[releases['TotalQuantity'] >= threshold]
            print(f"  Applying threshold: >= {threshold:,.0f} kg")
        
        # Aggregate emissions by facility
        facility_emissions = releases.groupby('FacilityReportID').agg({
            'TotalQuantity': 'sum',
            'PollutantCode': 'count'  # Number of different pollutants
        }).reset_index()
        
        facility_emissions.columns = ['FacilityReportID', 'Total_Emissions_kg', 'Pollutant_Count']
        
        # Merge with facility information
        result = facility_emissions.merge(
            self.facilities_df[['FacilityReportID', 'FacilityName', 'CountryCode', 
                               'City', 'Lat', 'Long', 'MainIAActivity']],
            on='FacilityReportID',
            how='left'
        )
        
        # Sort by total emissions
        result = result.sort_values('Total_Emissions_kg', ascending=False)
        
        # Get top N
        top_emitters = result.head(top_n)
        
        print(f"\nFound {len(result)} facilities with emissions")
        print(f"Returning top {top_n} emitters")
        print(f"Total emissions from top {top_n}: {top_emitters['Total_Emissions_kg'].sum():,.0f} kg")
        
        return top_emitters
    
    def analyze_by_sector(self, year=2023, top_sectors=10):
        """
        Analyze emissions by industrial sector.
        
        Parameters:
        -----------
        year : int
            Reporting year to analyze
        top_sectors : int
            Number of top emitting sectors to return
            
        Returns:
        --------
        pd.DataFrame : Sector analysis with total emissions
        """
        if self.releases_df is None or self.facilities_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        print(f"\nAnalyzing emissions by sector for year {year}...")
        
        # Filter by year
        releases = self.releases_df[self.releases_df['ReportingYear'] == year].copy()
        
        # Merge with facility information to get sectors
        data = releases.merge(
            self.facilities_df[['FacilityReportID', 'MainIAActivity']],
            on='FacilityReportID',
            how='left'
        )
        
        # Aggregate by sector
        sector_emissions = data.groupby('MainIAActivity').agg({
            'TotalQuantity': 'sum',
            'FacilityReportID': 'nunique'
        }).reset_index()
        
        sector_emissions.columns = ['Sector', 'Total_Emissions_kg', 'Facility_Count']
        
        # Calculate average per facility
        sector_emissions['Avg_Emissions_per_Facility'] = (
            sector_emissions['Total_Emissions_kg'] / sector_emissions['Facility_Count']
        )
        
        # Sort by total emissions
        sector_emissions = sector_emissions.sort_values('Total_Emissions_kg', ascending=False)
        
        print(f"\nTop {top_sectors} emitting sectors:")
        print(sector_emissions.head(top_sectors).to_string(index=False))
        
        return sector_emissions.head(top_sectors)
    
    def analyze_by_country(self, year=2023):
        """
        Analyze emissions by country.
        
        Parameters:
        -----------
        year : int
            Reporting year to analyze
            
        Returns:
        --------
        pd.DataFrame : Country analysis with total emissions
        """
        if self.releases_df is None or self.facilities_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        print(f"\nAnalyzing emissions by country for year {year}...")
        
        # Filter by year
        releases = self.releases_df[self.releases_df['ReportingYear'] == year].copy()
        
        # Merge with facility information
        data = releases.merge(
            self.facilities_df[['FacilityReportID', 'CountryCode']],
            on='FacilityReportID',
            how='left'
        )
        
        # Aggregate by country
        country_emissions = data.groupby('CountryCode').agg({
            'TotalQuantity': 'sum',
            'FacilityReportID': 'nunique'
        }).reset_index()
        
        country_emissions.columns = ['Country', 'Total_Emissions_kg', 'Facility_Count']
        
        # Sort by total emissions
        country_emissions = country_emissions.sort_values('Total_Emissions_kg', ascending=False)
        
        print("\nCountry emissions summary:")
        print(country_emissions.to_string(index=False))
        
        return country_emissions
    
    def find_pollutant_hotspots(self, pollutant_code, year=2023, top_n=20):
        """
        Find facilities with highest emissions of a specific pollutant.
        
        Parameters:
        -----------
        pollutant_code : str
            Pollutant code (e.g., 'CO2', 'NOX', 'SO2', 'PM10')
        year : int
            Reporting year to analyze
        top_n : int
            Number of top emitters to return
            
        Returns:
        --------
        pd.DataFrame : Top emitters of specified pollutant
        """
        if self.releases_df is None or self.facilities_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        print(f"\nFinding hotspots for {pollutant_code} in year {year}...")
        
        # Filter by year and pollutant
        releases = self.releases_df[
            (self.releases_df['ReportingYear'] == year) &
            (self.releases_df['PollutantCode'] == pollutant_code)
        ].copy()
        
        if len(releases) == 0:
            print(f"No data found for pollutant {pollutant_code} in year {year}")
            return pd.DataFrame()
        
        # Merge with facility information
        hotspots = releases.merge(
            self.facilities_df[['FacilityReportID', 'FacilityName', 'CountryCode', 
                               'City', 'Lat', 'Long', 'MainIAActivity']],
            on='FacilityReportID',
            how='left'
        )
        
        # Sort by emissions
        hotspots = hotspots.sort_values('TotalQuantity', ascending=False).head(top_n)
        
        print(f"\nTop {top_n} emitters of {pollutant_code}:")
        print(f"Total {pollutant_code} emissions: {hotspots['TotalQuantity'].sum():,.0f} kg")
        
        return hotspots[['FacilityName', 'CountryCode', 'City', 'MainIAActivity', 
                        'TotalQuantity', 'MediumCode', 'Lat', 'Long']]
    
    def track_trends(self, facility_id, start_year=2018, end_year=2023):
        """
        Track emission trends for a specific facility over time.
        
        Parameters:
        -----------
        facility_id : str or int
            Facility Report ID
        start_year : int
            Start year for trend analysis
        end_year : int
            End year for trend analysis
            
        Returns:
        --------
        pd.DataFrame : Yearly emissions for the facility
        """
        if self.releases_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        # Filter for the specific facility and year range
        facility_data = self.releases_df[
            (self.releases_df['FacilityReportID'] == facility_id) &
            (self.releases_df['ReportingYear'] >= start_year) &
            (self.releases_df['ReportingYear'] <= end_year)
        ].copy()
        
        if len(facility_data) == 0:
            print(f"No data found for facility {facility_id}")
            return pd.DataFrame()
        
        # Aggregate by year and pollutant
        trends = facility_data.groupby(['ReportingYear', 'PollutantCode']).agg({
            'TotalQuantity': 'sum'
        }).reset_index()
        
        # Pivot to have years as rows and pollutants as columns
        trends_pivot = trends.pivot(index='ReportingYear', 
                                    columns='PollutantCode', 
                                    values='TotalQuantity')
        
        print(f"\nEmission trends for facility {facility_id}:")
        print(trends_pivot.to_string())
        
        return trends_pivot
    
    def export_results(self, dataframe, filename, format='csv'):
        """
        Export analysis results to file.
        
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Data to export
        filename : str
            Output filename (without extension)
        format : str
            Output format: 'csv' or 'excel'
        """
        output_dir = self.data_dir / "analysis_results"
        output_dir.mkdir(exist_ok=True)
        
        if format == 'csv':
            filepath = output_dir / f"{filename}.csv"
            dataframe.to_csv(filepath, index=False)
        elif format == 'excel':
            filepath = output_dir / f"{filename}.xlsx"
            dataframe.to_excel(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"\nResults exported to: {filepath}")
        return filepath
    
    def generate_summary_report(self, year=2023, output_file="emission_summary_report.txt"):
        """
        Generate a comprehensive summary report of emissions.
        
        Parameters:
        -----------
        year : int
            Reporting year to analyze
        output_file : str
            Output filename for the report
        """
        output_path = self.data_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"EEA INDUSTRIAL EMISSIONS SUMMARY REPORT - Year {year}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall statistics
            releases = self.releases_df[self.releases_df['ReportingYear'] == year]
            f.write("OVERALL STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total emission records: {len(releases):,}\n")
            f.write(f"Total emissions (all pollutants): {releases['TotalQuantity'].sum():,.0f} kg\n")
            f.write(f"Number of facilities reporting: {releases['FacilityReportID'].nunique():,}\n")
            f.write(f"Number of pollutants tracked: {releases['PollutantCode'].nunique()}\n\n")
            
            # Top pollutants
            f.write("TOP 10 POLLUTANTS BY TOTAL QUANTITY\n")
            f.write("-" * 80 + "\n")
            top_pollutants = releases.groupby('PollutantCode')['TotalQuantity'].sum().sort_values(ascending=False).head(10)
            for pollutant, quantity in top_pollutants.items():
                f.write(f"{pollutant:15s}: {quantity:>20,.0f} kg\n")
            f.write("\n")
            
            # Country summary
            f.write("EMISSIONS BY COUNTRY\n")
            f.write("-" * 80 + "\n")
            country_data = releases.merge(
                self.facilities_df[['FacilityReportID', 'CountryCode']],
                on='FacilityReportID',
                how='left'
            )
            country_summary = country_data.groupby('CountryCode')['TotalQuantity'].sum().sort_values(ascending=False)
            for country, quantity in country_summary.items():
                f.write(f"{country:5s}: {quantity:>25,.0f} kg\n")
            f.write("\n")
            
            # Sector summary
            f.write("TOP 10 SECTORS BY EMISSIONS\n")
            f.write("-" * 80 + "\n")
            sector_data = releases.merge(
                self.facilities_df[['FacilityReportID', 'MainIAActivity']],
                on='FacilityReportID',
                how='left'
            )
            sector_summary = sector_data.groupby('MainIAActivity')['TotalQuantity'].sum().sort_values(ascending=False).head(10)
            for sector, quantity in sector_summary.items():
                f.write(f"{sector[:60]:60s}: {quantity:>20,.0f} kg\n")
            f.write("\n")
            
            f.write("=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        print(f"\nSummary report generated: {output_path}")
        return output_path


def main():
    """
    Main function demonstrating usage of the EEAEmissionsAnalyzer class.
    """
    print("\n" + "=" * 80)
    print("EEA INDUSTRIAL EMISSIONS ANALYZER")
    print("=" * 80 + "\n")
    
    # Initialize analyzer
    analyzer = EEAEmissionsAnalyzer()
    
    # Show download instructions
    analyzer.download_instructions()
    
    # Check if data files exist
    data_files = list(DATA_DIR.glob("*.csv")) + list(DATA_DIR.glob("*.xlsx"))
    
    if not data_files:
        print("\n⚠️  No data files found. Please download the data first using the instructions above.")
        return
    
    print(f"\n✓ Found {len(data_files)} data files in {DATA_DIR}")
    
    # Try to load data
    try:
        analyzer.load_data()
    except Exception as e:
        print(f"\n❌ Error loading data: {e}")
        print("Please ensure you have downloaded and extracted the EEA data files.")
        return
    
    if analyzer.releases_df is None or analyzer.facilities_df is None:
        print("\n❌ Required data files not loaded. Cannot proceed with analysis.")
        return
    
    # Run example analyses
    print("\n" + "=" * 80)
    print("RUNNING EXAMPLE ANALYSES")
    print("=" * 80)
    
    # 1. Find top 50 problem plants for 2023
    print("\n1. FINDING TOP 50 PROBLEM PLANTS (2023)")
    print("-" * 80)
    problem_plants = analyzer.find_problem_plants(
        pollutant_codes=['CO2', 'NOX', 'SO2', 'PM10', 'PM2.5'],
        year=2023,
        top_n=50
    )
    analyzer.export_results(problem_plants, "top_50_problem_plants_2023")
    
    # 2. Analyze by sector
    print("\n2. ANALYZING EMISSIONS BY INDUSTRIAL SECTOR")
    print("-" * 80)
    sector_analysis = analyzer.analyze_by_sector(year=2023, top_sectors=10)
    analyzer.export_results(sector_analysis, "sector_analysis_2023")
    
    # 3. Analyze by country
    print("\n3. ANALYZING EMISSIONS BY COUNTRY")
    print("-" * 80)
    country_analysis = analyzer.analyze_by_country(year=2023)
    analyzer.export_results(country_analysis, "country_analysis_2023")
    
    # 4. Find CO2 hotspots
    print("\n4. FINDING CO2 EMISSION HOTSPOTS")
    print("-" * 80)
    co2_hotspots = analyzer.find_pollutant_hotspots('CO2', year=2023, top_n=30)
    if not co2_hotspots.empty:
        analyzer.export_results(co2_hotspots, "co2_hotspots_2023")
    
    # 5. Generate summary report
    print("\n5. GENERATING SUMMARY REPORT")
    print("-" * 80)
    analyzer.generate_summary_report(year=2023)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nResults have been saved to: {DATA_DIR / 'analysis_results'}")
    print("\nNext steps:")
    print("- Review the exported CSV files for detailed results")
    print("- Use the analyzer methods for custom queries")
    print("- Combine with other datasets for deeper insights")
    print()


if __name__ == "__main__":
    main()
