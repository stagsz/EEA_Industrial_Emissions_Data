#!/usr/bin/env python3
"""
Spanish Facilities Research Sheet Generator
==========================================

This script generates comprehensive research sheets for each Spanish facility
in the ES_leads.csv file, providing detailed compliance analysis and business
intelligence for emission control service opportunities.
"""

import pandas as pd
import json
import os
from datetime import datetime
import re

def load_spanish_facilities():
    """Load and parse Spanish facilities data"""
    
    # Read the CSV file with proper delimiter
    df = pd.read_csv('outputs/ES_leads.csv', delimiter=';', encoding='utf-8-sig')
    
    # Clean and convert numeric columns
    df['Total Emissions (tonnes/yr)'] = df['Total Emissions (tonnes/yr)'].astype(str).str.replace(',', '.').astype(float)
    df['Lead Score'] = pd.to_numeric(df['Lead Score'], errors='coerce')
    df['Energy Input (TJ/yr)'] = pd.to_numeric(df['Energy Input (TJ/yr)'], errors='coerce')
    df['Number of Pollutants'] = pd.to_numeric(df['Number of Pollutants'], errors='coerce')
    
    print(f"Loaded {len(df)} Spanish facilities from ES_leads.csv")
    print("\nFacilities Overview:")
    for i, row in df.iterrows():
        print(f"{i+1:2d}. {row['Parent Company']} - {row['City']} (Score: {row['Lead Score']})")
    
    return df

def analyze_facility_type(parent_company, activity, city, emissions_data):
    """Determine facility type and industry based on available data"""
    
    company_lower = parent_company.lower()
    
    # Waste management indicators
    if any(keyword in company_lower for keyword in ['sogama', 'tractament', 'residus', 'urbaser', 'tirme', 'incineració', 'consorci', 'tircantabria']):
        return {
            'type': 'Waste-to-Energy/Waste Management',
            'industry': 'Waste Management',
            'primary_activity': 'Municipal solid waste incineration with energy recovery',
            'regulatory_focus': 'IED Annex I (5.2) - Disposal/recovery of municipal waste >3 tonnes/hour'
        }
    
    # Chemical/industrial indicators
    elif any(keyword in company_lower for keyword in ['celulosa', 'showa denko', 'carbon', 'hexcel', 'graftech']):
        return {
            'type': 'Chemical/Industrial Manufacturing',
            'industry': 'Chemical/Materials',
            'primary_activity': 'Chemical manufacturing and processing',
            'regulatory_focus': 'IED Annex I - Chemical industry activities'
        }
    
    else:
        return {
            'type': 'Industrial Facility',
            'industry': 'Manufacturing',
            'primary_activity': 'Industrial manufacturing',
            'regulatory_focus': 'IED compliance required'
        }

def determine_compliance_risks(row):
    """Analyze compliance risks based on emissions data"""
    
    risks = []
    
    # NOx analysis
    if row['Has NOx'] == 'YES':
        nox_match = re.search(r'NOx emissions: ([\d.]+) kg/year', row['Scoring Reasons'])
        if nox_match:
            nox_kg = float(nox_match.group(1))
            nox_tonnes = nox_kg / 1000
            
            if nox_tonnes > 5000:
                risks.append({
                    'type': 'CRITICAL',
                    'pollutant': 'NOx',
                    'level': f'{nox_tonnes:,.0f} tonnes/year',
                    'concern': 'Extremely high NOx emissions likely exceed all BAT-AEL standards',
                    'action': 'Immediate SCR/SNCR implementation required'
                })
            elif nox_tonnes > 1000:
                risks.append({
                    'type': 'HIGH',
                    'pollutant': 'NOx',
                    'level': f'{nox_tonnes:,.0f} tonnes/year',
                    'concern': 'High NOx emissions likely exceed BAT-AEL standards',
                    'action': 'Advanced NOx reduction technology needed'
                })
            else:
                risks.append({
                    'type': 'MEDIUM',
                    'pollutant': 'NOx',
                    'level': f'{nox_tonnes:,.0f} tonnes/year',
                    'concern': 'NOx emissions may exceed future stricter standards',
                    'action': 'Optimization and monitoring improvements'
                })
    
    # CO2 analysis
    if row['Has CO2'] == 'YES':
        co2_match = re.search(r'CO2 emissions: ([\d.]+) kg/year', row['Scoring Reasons'])
        if co2_match:
            co2_kg = float(co2_match.group(1))
            co2_tonnes = co2_kg / 1000
            
            if co2_tonnes > 25000:  # EU ETS threshold
                risks.append({
                    'type': 'HIGH',
                    'pollutant': 'CO2',
                    'level': f'{co2_tonnes:,.0f} tonnes/year',
                    'concern': 'Subject to EU ETS - carbon trading obligations',
                    'action': 'EU ETS compliance and carbon reduction strategies'
                })
    
    # SO2 analysis
    if row['Has SO2'] == 'YES':
        so2_match = re.search(r'SO2 emissions: ([\d.]+) kg/year', row['Scoring Reasons'])
        if so2_match:
            so2_kg = float(so2_match.group(1))
            so2_tonnes = so2_kg / 1000
            
            risks.append({
                'type': 'MEDIUM',
                'pollutant': 'SO2',
                'level': f'{so2_tonnes:,.0f} tonnes/year',
                'concern': 'SO2 emissions require acid gas treatment',
                'action': 'Wet/dry scrubbing technology implementation'
            })
    
    return risks

def generate_contact_strategy(parent_company, city, postal_code, street):
    """Generate contact strategy for each facility"""
    
    # Clean up company name for search
    company_clean = parent_company.replace(',', '').replace('.', '').strip()
    
    strategy = {
        'primary_target': company_clean,
        'location': f"{city}, Spain",
        'address': f"{street}, {postal_code} {city}",
        'approach_method': 'Direct corporate contact',
        'key_contacts': [
            'Environmental Manager',
            'Plant Manager',
            'Technical Director',
            'Compliance Officer',
            'Procurement Manager'
        ]
    }
    
    # Special handling for specific company types
    if 'sogama' in company_clean.lower():
        strategy.update({
            'company_type': 'Public company (Galician Government)',
            'decision_process': 'Public procurement procedures',
            'headquarters': 'Santiago de Compostela, Galicia',
            'approach_method': 'Government relations approach'
        })
    
    elif any(term in company_clean.lower() for term in ['consorci', 'mancomunats']):
        strategy.update({
            'company_type': 'Municipal consortium',
            'decision_process': 'Multi-municipal decision making',
            'approach_method': 'Municipal government relations'
        })
    
    elif 'sa' in company_clean.lower() or 'sl' in company_clean.lower():
        strategy.update({
            'company_type': 'Private corporation',
            'decision_process': 'Corporate procurement',
            'approach_method': 'B2B corporate sales'
        })
    
    return strategy

def create_facility_research_sheet(facility_data, facility_info, compliance_risks, contact_strategy):
    """Create comprehensive research sheet for a facility"""
    
    sheet = {
        'facility_overview': {
            'company_name': facility_data['Parent Company'],
            'facility_location': f"{facility_data['City']}, Spain",
            'full_address': f"{facility_data['Street']}, {facility_data['Postal Code']} {facility_data['City']}",
            'facility_type': facility_info['type'],
            'industry_sector': facility_info['industry'],
            'primary_activity': facility_info['primary_activity'],
            'lead_score': f"{facility_data['Lead Score']}/100",
            'priority_level': 'CRITICAL' if facility_data['Lead Score'] >= 90 else 'HIGH' if facility_data['Lead Score'] >= 70 else 'MEDIUM'
        },
        
        'emissions_profile': {
            'total_annual_emissions_tonnes': facility_data['Total Emissions (tonnes/yr)'],
            'number_of_pollutants': facility_data['Number of Pollutants'],
            'has_nox': facility_data['Has NOx'] == 'YES',
            'has_co2': facility_data['Has CO2'] == 'YES',
            'has_so2': facility_data['Has SO2'] == 'YES',
            'energy_input_tj_yr': facility_data['Energy Input (TJ/yr)'],
            'scoring_details': facility_data['Scoring Reasons']
        },
        
        'compliance_analysis': {
            'regulatory_framework': facility_info['regulatory_focus'],
            'compliance_risks': compliance_risks,
            'immediate_concerns': [risk for risk in compliance_risks if risk['type'] in ['CRITICAL', 'HIGH']],
            'bat_requirements': 'Subject to Best Available Techniques (BAT) conclusions',
            'monitoring_requirements': 'Continuous emission monitoring for key pollutants'
        },
        
        'business_opportunity': {
            'immediate_services': [],
            'medium_term_opportunities': [],
            'estimated_contract_value': '',
            'decision_timeline': ''
        },
        
        'contact_strategy': contact_strategy,
        
        'competitive_analysis': {
            'market_position': facility_info['industry'],
            'regulatory_pressure': 'HIGH' if compliance_risks else 'MEDIUM',
            'funding_availability': 'PUBLIC' if 'public' in contact_strategy.get('company_type', '').lower() else 'PRIVATE'
        }
    }
    
    # Determine business opportunities based on emissions and risks
    if any(risk['type'] == 'CRITICAL' for risk in compliance_risks):
        sheet['business_opportunity'].update({
            'immediate_services': [
                'Emergency compliance assessment',
                'Advanced emission control technology',
                'Regulatory compliance consulting',
                'Continuous monitoring systems'
            ],
            'estimated_contract_value': '€5-15 million',
            'decision_timeline': '3-6 months (urgent compliance)'
        })
    elif any(risk['type'] == 'HIGH' for risk in compliance_risks):
        sheet['business_opportunity'].update({
            'immediate_services': [
                'Emission control system audit',
                'BAT compliance assessment',
                'Technology upgrade planning',
                'Monitoring system enhancement'
            ],
            'estimated_contract_value': '€2-8 million',
            'decision_timeline': '6-12 months'
        })
    else:
        sheet['business_opportunity'].update({
            'immediate_services': [
                'Emission optimization',
                'Preventive compliance planning',
                'Monitoring system modernization'
            ],
            'estimated_contract_value': '€500K-3 million',
            'decision_timeline': '12-18 months'
        })
    
    return sheet

def save_facility_sheets(facilities_df):
    """Generate and save research sheets for all facilities"""
    
    # Create output directory
    output_dir = "outputs/facility_research_sheets"
    os.makedirs(output_dir, exist_ok=True)
    
    all_sheets = {}
    
    for index, row in facilities_df.iterrows():
        print(f"\nGenerating research sheet for: {row['Parent Company']} - {row['City']}")
        
        # Analyze facility
        facility_info = analyze_facility_type(
            row['Parent Company'], 
            row['Activity'], 
            row['City'],
            row['Scoring Reasons']
        )
        
        # Determine compliance risks
        compliance_risks = determine_compliance_risks(row)
        
        # Generate contact strategy
        contact_strategy = generate_contact_strategy(
            row['Parent Company'],
            row['City'],
            row['Postal Code'],
            row['Street']
        )
        
        # Create comprehensive research sheet
        research_sheet = create_facility_research_sheet(
            row, facility_info, compliance_risks, contact_strategy
        )
        
        # Save individual sheet
        facility_filename = f"{row['Parent Company'].replace(',', '').replace('.', '').replace(' ', '_')}_{row['City'].replace(' ', '_')}.json"
        facility_filepath = os.path.join(output_dir, facility_filename)
        
        with open(facility_filepath, 'w', encoding='utf-8') as f:
            json.dump(research_sheet, f, indent=2, ensure_ascii=False)
        
        # Add to master collection
        sheet_key = f"{row['Parent Company']} - {row['City']}"
        all_sheets[sheet_key] = research_sheet
        
        print(f"[SAVED] Research sheet saved: {facility_filename}")
    
    # Save master compilation
    master_file = os.path.join(output_dir, "ALL_Spanish_Facilities_Research_Master.json")
    master_summary = {
        'generation_date': datetime.now().isoformat(),
        'total_facilities': len(facilities_df),
        'facilities': all_sheets,
        'summary_statistics': {
            'critical_facilities': len([f for f in all_sheets.values() if f['facility_overview']['priority_level'] == 'CRITICAL']),
            'high_priority_facilities': len([f for f in all_sheets.values() if f['facility_overview']['priority_level'] == 'HIGH']),
            'total_estimated_value': 'See individual facility estimates',
            'primary_compliance_concerns': ['NOx emissions', 'CO2 reporting', 'BAT compliance']
        }
    }
    
    with open(master_file, 'w', encoding='utf-8') as f:
        json.dump(master_summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SAVED] Master research compilation saved: {master_file}")
    return output_dir, len(all_sheets)

def create_priority_summary():
    """Create executive summary of all facilities by priority"""
    
    facilities_df = load_spanish_facilities()
    
    # Sort by lead score
    facilities_sorted = facilities_df.sort_values('Lead Score', ascending=False)
    
    print("\n" + "="*80)
    print("SPANISH FACILITIES PRIORITY RANKING - EXECUTIVE SUMMARY")
    print("="*80)
    
    total_value_estimate = 0
    
    for i, (index, row) in enumerate(facilities_sorted.iterrows(), 1):
        priority = 'CRITICAL' if row['Lead Score'] >= 90 else 'HIGH' if row['Lead Score'] >= 70 else 'MEDIUM'
        
        # Estimate contract value based on emissions and score
        if row['Lead Score'] >= 90 and row['Total Emissions (tonnes/yr)'] > 100000:
            value_estimate = "€5-15M"
            total_value_estimate += 10  # Average
        elif row['Lead Score'] >= 80:
            value_estimate = "€2-8M"
            total_value_estimate += 5
        else:
            value_estimate = "€0.5-3M"
            total_value_estimate += 1.75
        
        print(f"\n{i:2d}. {priority} PRIORITY - Score: {row['Lead Score']}")
        print(f"    Company: {row['Parent Company']}")
        print(f"    Location: {row['City']}")
        print(f"    Emissions: {row['Total Emissions (tonnes/yr)']:,} tonnes/year")
        print(f"    Est. Value: {value_estimate}")
        
        # Extract key emissions
        nox_match = re.search(r'NOx emissions: ([\d.]+) kg/year', row['Scoring Reasons'])
        if nox_match:
            nox_tonnes = float(nox_match.group(1)) / 1000
            print(f"    NOx: {nox_tonnes:,.0f} tonnes/year")
    
    print(f"\n" + "="*80)
    print(f"TOTAL MARKET OPPORTUNITY: Estimated €{total_value_estimate:.1f}M+ across {len(facilities_df)} facilities")
    print(f"CRITICAL FACILITIES: {len(facilities_sorted[facilities_sorted['Lead Score'] >= 90])}")
    print(f"HIGH PRIORITY FACILITIES: {len(facilities_sorted[facilities_sorted['Lead Score'] >= 70])}")
    print("="*80)

if __name__ == "__main__":
    print("Spanish Facilities Research Sheet Generator")
    print("=" * 50)
    
    try:
        # Load facilities data
        facilities_df = load_spanish_facilities()
        
        # Create priority summary
        create_priority_summary()
        
        # Generate all research sheets
        print(f"\nGenerating detailed research sheets for {len(facilities_df)} facilities...")
        output_dir, sheets_created = save_facility_sheets(facilities_df)
        
        print(f"\n" + "="*50)
        print(f"[COMPLETE] RESEARCH SHEETS GENERATION COMPLETE")
        print(f"Output Directory: {output_dir}")
        print(f"Sheets Created: {sheets_created}")
        print(f"Master File: ALL_Spanish_Facilities_Research_Master.json")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()