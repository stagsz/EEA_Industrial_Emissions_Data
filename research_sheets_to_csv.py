#!/usr/bin/env python3
"""
Spanish Facilities Research Sheets to CSV Converter
==================================================

This script converts all the JSON research sheets into a comprehensive CSV file
for easy analysis, filtering, and business development planning.
"""

import pandas as pd
import json
import os
from datetime import datetime

def load_all_research_sheets():
    """Load all individual research sheet JSON files"""
    
    sheets_dir = "outputs/facility_research_sheets"
    all_facilities = []
    
    # Get all JSON files except the master file
    json_files = [f for f in os.listdir(sheets_dir) if f.endswith('.json') and not f.startswith('ALL_')]
    
    print(f"Loading {len(json_files)} facility research sheets...")
    
    for filename in json_files:
        filepath = os.path.join(sheets_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                facility_data = json.load(f)
                
            # Extract key information into flat structure
            facility_record = extract_facility_data(facility_data, filename)
            all_facilities.append(facility_record)
            
            print(f"[LOADED] {facility_record['Company_Name']} - {facility_record['City']}")
            
        except Exception as e:
            print(f"[ERROR] Error loading {filename}: {e}")
    
    return all_facilities

def extract_facility_data(data, filename):
    """Extract and flatten facility data into CSV-friendly format"""
    
    # Basic facility information
    overview = data.get('facility_overview', {})
    emissions = data.get('emissions_profile', {})
    compliance = data.get('compliance_analysis', {})
    business = data.get('business_opportunity', {})
    contact = data.get('contact_strategy', {})
    competitive = data.get('competitive_analysis', {})
    
    # Extract compliance risks
    risks = compliance.get('compliance_risks', [])
    immediate_concerns = compliance.get('immediate_concerns', [])
    
    # NOx specific data
    nox_risk = next((r for r in risks if r.get('pollutant') == 'NOx'), {})
    co2_risk = next((r for r in risks if r.get('pollutant') == 'CO2'), {})
    so2_risk = next((r for r in risks if r.get('pollutant') == 'SO2'), {})
    
    # Parse address
    full_address = overview.get('full_address', '')
    address_parts = full_address.split(', ')
    street = address_parts[0] if address_parts else ''
    postal_code = ''
    city = overview.get('facility_location', '').replace(', Spain', '')
    
    # Extract postal code from address if present
    for part in address_parts:
        if part.strip().isdigit() and len(part.strip()) == 5:
            postal_code = part.strip()
            break
    
    # Create flattened record
    record = {
        # Basic Information
        'Company_Name': overview.get('company_name', ''),
        'City': city,
        'Street_Address': street,
        'Postal_Code': postal_code,
        'Full_Address': full_address,
        'Country': 'Spain',
        
        # Facility Classification
        'Facility_Type': overview.get('facility_type', ''),
        'Industry_Sector': overview.get('industry_sector', ''),
        'Primary_Activity': overview.get('primary_activity', ''),
        'Lead_Score': overview.get('lead_score', '').replace('/100', ''),
        'Priority_Level': overview.get('priority_level', ''),
        
        # Emissions Data
        'Total_Annual_Emissions_Tonnes': emissions.get('total_annual_emissions_tonnes', 0),
        'Number_of_Pollutants': emissions.get('number_of_pollutants', 0),
        'Energy_Input_TJ_per_Year': emissions.get('energy_input_tj_yr', 0),
        'Has_NOx': 'YES' if emissions.get('has_nox', False) else 'NO',
        'Has_CO2': 'YES' if emissions.get('has_co2', False) else 'NO',
        'Has_SO2': 'YES' if emissions.get('has_so2', False) else 'NO',
        
        # NOx Analysis
        'NOx_Risk_Level': nox_risk.get('type', ''),
        'NOx_Emissions_Level': nox_risk.get('level', ''),
        'NOx_Concern': nox_risk.get('concern', ''),
        'NOx_Recommended_Action': nox_risk.get('action', ''),
        
        # CO2 Analysis
        'CO2_Risk_Level': co2_risk.get('type', ''),
        'CO2_Emissions_Level': co2_risk.get('level', ''),
        'CO2_Concern': co2_risk.get('concern', ''),
        'CO2_Recommended_Action': co2_risk.get('action', ''),
        
        # SO2 Analysis
        'SO2_Risk_Level': so2_risk.get('type', ''),
        'SO2_Emissions_Level': so2_risk.get('level', ''),
        'SO2_Concern': so2_risk.get('concern', ''),
        'SO2_Recommended_Action': so2_risk.get('action', ''),
        
        # Compliance Information
        'Regulatory_Framework': compliance.get('regulatory_framework', ''),
        'BAT_Requirements': compliance.get('bat_requirements', ''),
        'Monitoring_Requirements': compliance.get('monitoring_requirements', ''),
        'Total_Risk_Count': len(risks),
        'Critical_Risk_Count': len([r for r in risks if r.get('type') == 'CRITICAL']),
        'High_Risk_Count': len([r for r in risks if r.get('type') == 'HIGH']),
        
        # Business Opportunity
        'Estimated_Contract_Value': business.get('estimated_contract_value', ''),
        'Decision_Timeline': business.get('decision_timeline', ''),
        'Immediate_Services_1': ', '.join(business.get('immediate_services', [])[:3]),
        'Immediate_Services_2': ', '.join(business.get('immediate_services', [])[3:6]),
        'All_Immediate_Services': '; '.join(business.get('immediate_services', [])),
        
        # Contact Strategy
        'Primary_Target': contact.get('primary_target', ''),
        'Company_Type': contact.get('company_type', ''),
        'Decision_Process': contact.get('decision_process', ''),
        'Approach_Method': contact.get('approach_method', ''),
        'Key_Contacts': '; '.join(contact.get('key_contacts', [])),
        'Headquarters_Location': contact.get('headquarters', ''),
        
        # Competitive Analysis
        'Market_Position': competitive.get('market_position', ''),
        'Regulatory_Pressure': competitive.get('regulatory_pressure', ''),
        'Funding_Availability': competitive.get('funding_availability', ''),
        
        # Additional Analysis
        'EU_ETS_Subject': 'YES' if 'EU ETS' in co2_risk.get('concern', '') else 'NO',
        'Waste_to_Energy_Facility': 'YES' if 'waste' in overview.get('facility_type', '').lower() else 'NO',
        'Public_Company': 'YES' if 'public' in contact.get('company_type', '').lower() else 'NO',
        'Urgent_Compliance_Required': 'YES' if any(r.get('type') == 'CRITICAL' for r in risks) else 'NO',
        
        # Scoring and Prioritization
        'Emissions_Score': calculate_emissions_score(emissions.get('total_annual_emissions_tonnes', 0)),
        'NOx_Score': calculate_nox_score(nox_risk.get('level', '')),
        'Business_Potential_Score': calculate_business_score(business.get('estimated_contract_value', '')),
        
        # Regional Information
        'Region': determine_region(city),
        'Province': determine_province(city, postal_code),
        
        # Technical Requirements
        'Requires_SCR_SNCR': 'YES' if 'SCR' in nox_risk.get('action', '') or 'SNCR' in nox_risk.get('action', '') else 'NO',
        'Requires_Monitoring_Upgrade': 'YES' if 'monitoring' in '; '.join(business.get('immediate_services', [])).lower() else 'NO',
        'Requires_BAT_Assessment': 'YES' if 'BAT' in '; '.join(business.get('immediate_services', [])) else 'NO',
        
        # Source File
        'Source_Filename': filename,
        'Analysis_Date': datetime.now().strftime('%Y-%m-%d')
    }
    
    return record

def calculate_emissions_score(total_emissions):
    """Calculate emissions score based on total annual emissions"""
    if total_emissions > 1000000:  # > 1M tonnes
        return 10
    elif total_emissions > 500000:  # > 500K tonnes
        return 9
    elif total_emissions > 100000:  # > 100K tonnes
        return 8
    elif total_emissions > 50000:   # > 50K tonnes
        return 7
    elif total_emissions > 10000:   # > 10K tonnes
        return 6
    elif total_emissions > 5000:    # > 5K tonnes
        return 5
    elif total_emissions > 1000:    # > 1K tonnes
        return 4
    elif total_emissions > 500:     # > 500 tonnes
        return 3
    elif total_emissions > 100:     # > 100 tonnes
        return 2
    else:
        return 1

def calculate_nox_score(nox_level):
    """Calculate NOx score based on emission level"""
    if not nox_level:
        return 0
    
    # Extract numeric value from string like "5,314 tonnes/year"
    import re
    match = re.search(r'([\d,]+)', nox_level.replace(',', ''))
    if match:
        nox_tonnes = int(match.group(1).replace(',', ''))
        if nox_tonnes > 5000:
            return 10
        elif nox_tonnes > 3000:
            return 9
        elif nox_tonnes > 2000:
            return 8
        elif nox_tonnes > 1000:
            return 7
        elif nox_tonnes > 500:
            return 6
        elif nox_tonnes > 200:
            return 5
        elif nox_tonnes > 100:
            return 4
        elif nox_tonnes > 50:
            return 3
        else:
            return 2
    return 0

def calculate_business_score(contract_value):
    """Calculate business potential score based on estimated contract value"""
    if '€5-15M' in contract_value:
        return 10
    elif '€2-8M' in contract_value:
        return 7
    elif '€0.5-3M' in contract_value:
        return 4
    else:
        return 1

def determine_region(city):
    """Determine Spanish region based on city"""
    region_mapping = {
        'ENCROBAS': 'Galicia',
        'Sant Adrià de Besòs': 'Catalonia',
        'BURGO DE EBRO (EL)': 'Aragon', 
        'MADRID': 'Madrid',
        'GRELA (LA)': 'Galicia',
        'PALMA': 'Balearic Islands',
        'Tarragona': 'Catalonia',
        'ILLESCAS': 'Castile-La Mancha',
        'SAN BARTOLOME DE MERUELO': 'Cantabria',
        'Mataró': 'Catalonia',
        'ORORBIA': 'Navarre'
    }
    return region_mapping.get(city, 'Unknown')

def determine_province(city, postal_code):
    """Determine Spanish province based on city and postal code"""
    province_mapping = {
        'ENCROBAS': 'A Coruña',
        'Sant Adrià de Besòs': 'Barcelona',
        'BURGO DE EBRO (EL)': 'Zaragoza',
        'MADRID': 'Madrid',
        'GRELA (LA)': 'A Coruña',
        'PALMA': 'Balearic Islands',
        'Tarragona': 'Tarragona',
        'ILLESCAS': 'Toledo',
        'SAN BARTOLOME DE MERUELO': 'Cantabria',
        'Mataró': 'Barcelona',
        'ORORBIA': 'Navarre'
    }
    return province_mapping.get(city, 'Unknown')

def create_summary_statistics(df):
    """Create summary statistics for the CSV"""
    
    summary = {
        'Total_Facilities': len(df),
        'Critical_Priority_Count': len(df[df['Priority_Level'] == 'CRITICAL']),
        'High_Priority_Count': len(df[df['Priority_Level'] == 'HIGH']),
        'Medium_Priority_Count': len(df[df['Priority_Level'] == 'MEDIUM']),
        'Waste_to_Energy_Count': len(df[df['Waste_to_Energy_Facility'] == 'YES']),
        'Public_Company_Count': len(df[df['Public_Company'] == 'YES']),
        'EU_ETS_Subject_Count': len(df[df['EU_ETS_Subject'] == 'YES']),
        'Urgent_Compliance_Count': len(df[df['Urgent_Compliance_Required'] == 'YES']),
        'Total_Annual_Emissions': df['Total_Annual_Emissions_Tonnes'].sum(),
        'Average_Lead_Score': df['Lead_Score'].astype(float).mean(),
        'Max_Contract_Value_Facilities': len(df[df['Estimated_Contract_Value'].str.contains('€5-15M', na=False)]),
        'Analysis_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return summary

def save_csv_with_summary(facilities_data):
    """Save CSV file with summary sheet"""
    
    # Create main dataframe
    df = pd.DataFrame(facilities_data)
    
    # Sort by Lead Score (descending) and Total Emissions (descending)
    df['Lead_Score_Numeric'] = df['Lead_Score'].astype(float)
    df = df.sort_values(['Lead_Score_Numeric', 'Total_Annual_Emissions_Tonnes'], ascending=[False, False])
    df = df.drop('Lead_Score_Numeric', axis=1)
    
    # Create summary statistics
    summary_stats = create_summary_statistics(df)
    
    # Save main CSV
    main_csv_path = "outputs/Spanish_Facilities_Complete_Research_Data.csv"
    df.to_csv(main_csv_path, index=False, encoding='utf-8-sig')
    
    # Create summary DataFrame
    summary_df = pd.DataFrame([summary_stats])
    summary_csv_path = "outputs/Spanish_Facilities_Summary_Statistics.csv"
    summary_df.to_csv(summary_csv_path, index=False, encoding='utf-8-sig')
    
    return main_csv_path, summary_csv_path, len(df)

def generate_priority_contact_list(df):
    """Generate priority contact list CSV"""
    
    # Select key contact fields for priority facilities
    contact_fields = [
        'Company_Name', 'City', 'Priority_Level', 'Lead_Score',
        'Full_Address', 'Primary_Target', 'Company_Type',
        'Estimated_Contract_Value', 'Decision_Timeline',
        'Key_Contacts', 'Approach_Method', 'NOx_Risk_Level',
        'Urgent_Compliance_Required', 'Region'
    ]
    
    # Filter for high priority facilities
    priority_df = df[df['Priority_Level'].isin(['CRITICAL', 'HIGH'])][contact_fields]
    
    # Save priority contact list
    contact_csv_path = "outputs/Spanish_Facilities_Priority_Contact_List.csv"
    priority_df.to_csv(contact_csv_path, index=False, encoding='utf-8-sig')
    
    return contact_csv_path, len(priority_df)

if __name__ == "__main__":
    print("Spanish Facilities Research Sheets to CSV Converter")
    print("=" * 60)
    
    try:
        # Load all research sheets
        facilities_data = load_all_research_sheets()
        
        if not facilities_data:
            print("No facility data found!")
            exit(1)
        
        # Save comprehensive CSV
        main_csv, summary_csv, total_facilities = save_csv_with_summary(facilities_data)
        
        # Create priority contact list
        df = pd.DataFrame(facilities_data)
        contact_csv, priority_count = generate_priority_contact_list(df)
        
        print(f"\n" + "=" * 60)
        print(f"CSV GENERATION COMPLETE")
        print("=" * 60)
        print(f"Main Data File: {main_csv}")
        print(f"Summary Statistics: {summary_csv}")
        print(f"Priority Contacts: {contact_csv}")
        print(f"\nFacilities Processed: {total_facilities}")
        print(f"Priority Facilities: {priority_count}")
        print(f"Total Columns: {len(df.columns) if not df.empty else 0}")
        
        # Display first few records for verification
        if not df.empty:
            print(f"\nTop 3 Priority Facilities:")
            for i, row in df.head(3).iterrows():
                print(f"{i+1}. {row['Company_Name']} ({row['City']}) - Score: {row['Lead_Score']} - {row['Estimated_Contract_Value']}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()