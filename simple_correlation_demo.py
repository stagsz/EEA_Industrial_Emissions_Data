"""
Simple External Database Correlation Demonstration
Shows how to enhance EEA data with external intelligence
"""

import pandas as pd
import numpy as np
from datetime import datetime

class SimpleCorrelationDemo:
    def __init__(self):
        print("Database Correlation Toolkit Initialized")
        print("Ready to enhance EEA data with external intelligence\n")
    
    def load_and_analyze(self):
        """Load EEA data and demonstrate correlation potential"""
        
        print("=== LOADING EEA DATA ===")
        facilities = pd.read_csv('converted_csv/2_ProductionFacility.csv', low_memory=False)
        energy_data = pd.read_csv('converted_csv/4d_EnergyInput.csv', low_memory=False)
        pollutants = pd.read_csv('converted_csv/2f_PollutantRelease.csv', low_memory=False)
        
        print(f"Loaded {len(facilities):,} facilities")
        print(f"Loaded {len(energy_data):,} energy records")
        print(f"Loaded {len(pollutants):,} pollutant records")
        
        # Get latest year data
        latest_year = energy_data['reportingYear'].max()
        energy_latest = energy_data[energy_data['reportingYear'] == latest_year]
        
        # Create analysis dataset
        analysis_data = facilities.merge(
            energy_latest.groupby('Installation_Part_INSPIRE_ID').agg({
                'energyInputTJ': 'sum'
            }).reset_index(),
            left_on='Facility_INSPIRE_ID',
            right_on='Installation_Part_INSPIRE_ID',
            how='left'
        )
        
        print(f"Analysis dataset created: {len(analysis_data):,} records")
        
        return analysis_data, facilities, energy_latest, pollutants
    
    def demonstrate_eu_ets_correlation(self, facilities_data):
        """Demonstrate EU ETS Registry correlation"""
        
        print("\n=== EU ETS REGISTRY CORRELATION DEMO ===")
        
        # Identify large facilities likely in EU ETS
        large_facilities = facilities_data[
            (facilities_data['energyInputTJ'] > 1000) |
            (facilities_data['mainActivityName'].str.contains('power|combustion', case=False, na=False))
        ]
        
        print(f"Large facilities (likely EU ETS): {len(large_facilities):,}")
        
        # Simulate ETS compliance data
        ets_data = []
        for _, facility in large_facilities.head(50).iterrows():
            # Simulate compliance status based on facility characteristics
            if facility.get('energyInputTJ', 0) > 10000:
                compliance_risk = 'HIGH'
                carbon_cost = np.random.randint(500000, 2000000)
            elif facility.get('energyInputTJ', 0) > 5000:
                compliance_risk = 'MEDIUM' 
                carbon_cost = np.random.randint(100000, 500000)
            else:
                compliance_risk = 'LOW'
                carbon_cost = np.random.randint(10000, 100000)
            
            ets_data.append({
                'facility_name': facility['nameOfFeature'],
                'country': facility['countryCode'],
                'compliance_risk': compliance_risk,
                'carbon_cost_eur': carbon_cost,
                'ets_priority': 100 if compliance_risk == 'HIGH' else 50 if compliance_risk == 'MEDIUM' else 25
            })
        
        ets_df = pd.DataFrame(ets_data)
        
        print(f"EU ETS correlation complete:")
        print(f"  HIGH risk facilities: {len(ets_df[ets_df['compliance_risk'] == 'HIGH'])}")
        print(f"  MEDIUM risk facilities: {len(ets_df[ets_df['compliance_risk'] == 'MEDIUM'])}")
        print(f"  Total carbon costs: EUR {ets_df['carbon_cost_eur'].sum():,}")
        
        return ets_df
    
    def demonstrate_financial_correlation(self, facilities_data):
        """Demonstrate financial database correlation"""
        
        print("\n=== FINANCIAL DATABASE CORRELATION DEMO ===")
        
        # Target facilities with significant operations
        target_facilities = facilities_data[
            (facilities_data['energyInputTJ'] > 500) |
            (facilities_data['mainActivityName'].str.contains('waste|power|chemical|metal', case=False, na=False))
        ]
        
        print(f"Target facilities for financial analysis: {len(target_facilities):,}")
        
        # Simulate financial intelligence
        financial_data = []
        for _, facility in target_facilities.head(100).iterrows():
            energy = facility.get('energyInputTJ', 0)
            if pd.isna(energy):
                energy = 0
            
            # Estimate revenue based on facility size and type
            if 'power' in str(facility.get('mainActivityName', '')).lower():
                revenue_multiplier = 100000  # Power plants
            elif 'waste' in str(facility.get('mainActivityName', '')).lower():
                revenue_multiplier = 80000   # Waste facilities
            else:
                revenue_multiplier = 60000   # Other industrial
            
            estimated_revenue = max(energy * revenue_multiplier, 1000000)
            
            financial_data.append({
                'facility_name': facility['nameOfFeature'],
                'country': facility['countryCode'],
                'estimated_revenue_eur': int(estimated_revenue * np.random.uniform(0.7, 1.5)),
                'capex_budget_eur': int(estimated_revenue * np.random.uniform(0.05, 0.12)),
                'credit_rating': np.random.choice(['A', 'BBB', 'BB', 'B'], p=[0.3, 0.4, 0.2, 0.1]),
                'financial_priority': int(estimated_revenue / 1000000)  # Millions as priority score
            })
        
        financial_df = pd.DataFrame(financial_data)
        
        print(f"Financial correlation complete:")
        print(f"  Large enterprises (>EUR 10M): {len(financial_df[financial_df['estimated_revenue_eur'] > 10000000])}")
        print(f"  High CapEx budget (>EUR 1M): {len(financial_df[financial_df['capex_budget_eur'] > 1000000])}")
        print(f"  Total addressable revenue: EUR {financial_df['estimated_revenue_eur'].sum()/1000000:.0f} million")
        
        return financial_df
    
    def create_enhanced_scoring(self, facilities_data, ets_data, financial_data):
        """Create enhanced lead scoring using multiple data sources"""
        
        print("\n=== ENHANCED LEAD SCORING ===")
        
        # Merge all data sources
        enhanced_leads = []
        
        for _, facility in facilities_data.head(200).iterrows():
            facility_name = facility['nameOfFeature']
            
            # Base scoring factors
            base_score = 0
            scoring_factors = []
            
            # Facility size scoring
            energy = facility.get('energyInputTJ', 0)
            if energy > 10000:
                base_score += 30
                scoring_factors.append(f"Large facility: {energy:,.0f} TJ/year")
            elif energy > 1000:
                base_score += 20
                scoring_factors.append(f"Medium facility: {energy:,.0f} TJ/year")
            elif energy > 100:
                base_score += 10
                scoring_factors.append(f"Small facility: {energy:,.0f} TJ/year")
            
            # Industry type scoring
            activity = str(facility.get('mainActivityName', '')).lower()
            if 'waste' in activity or 'incineration' in activity:
                base_score += 25
                scoring_factors.append("Waste sector: High regulatory pressure")
            elif 'power' in activity or 'combustion' in activity:
                base_score += 20
                scoring_factors.append("Power sector: EU ETS compliance")
            
            # Geographic scoring
            country = facility.get('countryCode', '')
            if country in ['DE', 'UK', 'FR', 'IT', 'ES']:
                base_score += 15
                scoring_factors.append(f"Priority market: {country}")
            
            # ETS correlation bonus
            ets_match = ets_data[ets_data['facility_name'] == facility_name]
            if len(ets_match) > 0:
                ets_priority = ets_match.iloc[0]['ets_priority']
                base_score += ets_priority
                risk_level = ets_match.iloc[0]['compliance_risk']
                scoring_factors.append(f"EU ETS {risk_level} risk: +{ets_priority} points")
            
            # Financial correlation bonus
            fin_match = financial_data[financial_data['facility_name'] == facility_name]
            if len(fin_match) > 0:
                fin_priority = min(fin_match.iloc[0]['financial_priority'], 20)
                base_score += fin_priority
                revenue = fin_match.iloc[0]['estimated_revenue_eur']
                scoring_factors.append(f"Revenue: EUR {revenue/1000000:.1f}M")
            
            # Final scoring
            final_score = min(base_score, 100)
            
            if final_score > 40:  # Qualified lead threshold
                enhanced_leads.append({
                    'facility_name': facility_name,
                    'country': facility['countryCode'],
                    'city': facility.get('city', ''),
                    'activity': facility.get('mainActivityName', ''),
                    'energy_tj': energy,
                    'lead_score': final_score,
                    'scoring_reasons': '; '.join(scoring_factors),
                    'parent_company': facility.get('parentCompanyName', ''),
                    'address': facility.get('streetName', '')
                })
        
        enhanced_df = pd.DataFrame(enhanced_leads)
        enhanced_df = enhanced_df.sort_values('lead_score', ascending=False)
        
        print(f"Enhanced scoring complete:")
        print(f"  Total qualified leads: {len(enhanced_df)}")
        
        # Score distribution
        critical = len(enhanced_df[enhanced_df['lead_score'] >= 80])
        high = len(enhanced_df[(enhanced_df['lead_score'] >= 60) & (enhanced_df['lead_score'] < 80)])
        qualified = len(enhanced_df[(enhanced_df['lead_score'] >= 40) & (enhanced_df['lead_score'] < 60)])
        
        print(f"  CRITICAL leads (80-100): {critical}")
        print(f"  HIGH VALUE leads (60-79): {high}")
        print(f"  QUALIFIED leads (40-59): {qualified}")
        
        return enhanced_df
    
    def export_results(self, enhanced_leads, ets_data, financial_data):
        """Export enhanced lead intelligence"""
        
        print("\n=== EXPORTING RESULTS ===")
        
        output_file = f'Enhanced_Leads_Demo_{datetime.now().strftime("%Y%m%d")}.xlsx'
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main leads sheet
            enhanced_leads.to_excel(writer, sheet_name='Enhanced Leads', index=False)
            
            # Priority segments
            critical = enhanced_leads[enhanced_leads['lead_score'] >= 80]
            if len(critical) > 0:
                critical.to_excel(writer, sheet_name='Critical Leads (80-100)', index=False)
            
            high_value = enhanced_leads[(enhanced_leads['lead_score'] >= 60) & 
                                      (enhanced_leads['lead_score'] < 80)]
            if len(high_value) > 0:
                high_value.to_excel(writer, sheet_name='High Value (60-79)', index=False)
            
            # Supporting data
            ets_data.to_excel(writer, sheet_name='EU ETS Intelligence', index=False)
            financial_data.to_excel(writer, sheet_name='Financial Intelligence', index=False)
            
            # Country breakdown
            for country in enhanced_leads['country'].value_counts().head(3).index:
                country_data = enhanced_leads[enhanced_leads['country'] == country]
                country_data.to_excel(writer, sheet_name=f'{country} Leads', index=False)
        
        print(f"Results exported to: {output_file}")
        print(f"Total sheets created: {6 + len(enhanced_leads['country'].value_counts().head(3))}")
        
        # Display top 10 leads
        print("\nTOP 10 ENHANCED LEADS:")
        top_10 = enhanced_leads[['facility_name', 'country', 'city', 'lead_score', 'scoring_reasons']].head(10)
        print(top_10.to_string(index=False, max_colwidth=50))
    
    def run_demonstration(self):
        """Run complete correlation demonstration"""
        
        print("EXTERNAL DATABASE CORRELATION DEMONSTRATION")
        print("=" * 60)
        
        # Load base data
        facilities_data, facilities, energy_latest, pollutants = self.load_and_analyze()
        
        # Demonstrate correlations
        ets_data = self.demonstrate_eu_ets_correlation(facilities_data)
        financial_data = self.demonstrate_financial_correlation(facilities_data)
        
        # Enhanced scoring
        enhanced_leads = self.create_enhanced_scoring(facilities_data, ets_data, financial_data)
        
        # Export results
        self.export_results(enhanced_leads, ets_data, financial_data)
        
        print("\n" + "=" * 60)
        print("CORRELATION DEMONSTRATION COMPLETE!")
        print("Enhanced lead intelligence demonstrates the power of")
        print("multi-database correlation for sales effectiveness.")
        print("=" * 60)

if __name__ == "__main__":
    demo = SimpleCorrelationDemo()
    demo.run_demonstration()