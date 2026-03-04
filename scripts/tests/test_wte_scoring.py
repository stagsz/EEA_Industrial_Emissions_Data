"""
Test cases for enhanced WtE lead scoring with age and regulatory factors
Tests the 5 implementation tasks
"""
import asyncio
import json
from datetime import datetime

# Mock the lead_generation_agent functions for testing
def get_plant_age(start_year_or_date):
    """Calculate plant age from start year or date"""
    try:
        current_year = datetime.now().year

        if isinstance(start_year_or_date, int):
            return current_year - start_year_or_date
        elif isinstance(start_year_or_date, str):
            year_str = str(start_year_or_date).split('-')[0] if '-' in str(start_year_or_date) else str(start_year_or_date)
            try:
                start_year = int(year_str)
                return current_year - start_year
            except:
                return None
        return None
    except:
        return None


country_to_region = {
    # EU Countries
    "Germany": "EU", "France": "EU", "Italy": "EU", "Spain": "EU", "Poland": "EU",
    "Netherlands": "EU", "Belgium": "EU", "Austria": "EU", "Czech Republic": "EU",
    "Denmark": "EU", "Sweden": "EU", "Finland": "EU", "Greece": "EU", "Portugal": "EU",
    "Hungary": "EU", "Romania": "EU", "Slovakia": "EU", "Slovenia": "EU", "Bulgaria": "EU",
    "Croatia": "EU", "Estonia": "EU", "Latvia": "EU", "Lithuania": "EU",
    "United Kingdom": "EU", "Norway": "EU", "Switzerland": "EU",
    # North America
    "USA": "N.America", "Canada": "N.America", "Mexico": "N.America",
    # Developed Asia
    "Japan": "Developed_Asia", "South Korea": "Developed_Asia", "Singapore": "Developed_Asia",
    # Emerging Asia
    "China": "Emerging_Asia", "India": "Emerging_Asia", "Vietnam": "Emerging_Asia",
    "Thailand": "Emerging_Asia", "Indonesia": "Emerging_Asia", "Malaysia": "Emerging_Asia",
}

regulatory_weights = {
    "EU": 25,
    "N.America": 15,
    "Developed_Asia": 20,
    "Emerging_Asia": 10,
    "Other": 5
}


def get_regulatory_weight(country):
    """Get regulatory weight factor for a country"""
    region = country_to_region.get(country, "Other")
    return regulatory_weights.get(region, regulatory_weights["Other"])


def should_filter_lead(lead, min_age=15, regulatory_regions=None):
    """Filter leads based on age and regulatory criteria"""
    if regulatory_regions is None:
        regulatory_regions = ["EU", "Developed_Asia", "Emerging_Asia"]

    plant_age = get_plant_age(lead.get('plant_start_year') or lead.get('start_year') or lead.get('Start'))
    if plant_age and plant_age < min_age:
        return False, f"Plant age {plant_age} < minimum {min_age} years"

    country = lead.get('country', '')
    region = country_to_region.get(country, "Other")
    if region not in regulatory_regions:
        return False, f"Region {region} not in priority list"

    if plant_age and plant_age > 20:
        return True, f"Aged plant ({plant_age} years) + {region} regulation = HIGH priority"

    if plant_age and plant_age > 15 and region in ["EU", "Developed_Asia"]:
        return True, f"Plant age {plant_age} years + {region} strict regulation"

    return True, "Meets age and regulatory criteria"


# Test facilities (known WtE plants)
TEST_FACILITIES = [
    {
        "name": "Berlin-Ruhleben (Germany) - AGED EU PLANT",
        "facility": "Berlin-Ruhleben Waste Incineration",
        "country": "Germany",
        "Start": 2003,  # 22 years old (2025 - 2003)
        "waste_throughput_tonnes_year": 520000,
        "emission_levels": "compliant",
        "compliance_status": "compliant"
    },
    {
        "name": "Amsterdam AEB (Netherlands) - MODERATE AGE",
        "facility": "Amsterdam AEB",
        "country": "Netherlands",
        "Start": 2008,  # 17 years old
        "waste_throughput_tonnes_year": 550000,
        "emission_levels": "compliant",
        "compliance_status": "compliant"
    },
    {
        "name": "Tokyo Incinerator (Japan) - AGED DEVELOPED ASIA",
        "facility": "Tokyo WtE Plant",
        "country": "Japan",
        "Start": 1998,  # 27 years old
        "waste_throughput_tonnes_year": 350000,
        "emission_levels": "compliant",
        "compliance_status": "compliant"
    },
    {
        "name": "Shanghai Plant (China) - MODERATE AGE EMERGING",
        "facility": "Shanghai WtE",
        "country": "China",
        "Start": 2010,  # 15 years old
        "waste_throughput_tonnes_year": 600000,
        "emission_levels": "compliant",
        "compliance_status": "compliant"
    },
    {
        "name": "SYSAV Sweden (EU) - YOUNGER EU PLANT",
        "facility": "SYSAV Malmö",
        "country": "Sweden",
        "Start": 2015,  # 10 years old
        "waste_throughput_tonnes_year": 650000,
        "emission_levels": "compliant",
        "compliance_status": "compliant"
    },
    {
        "name": "Toronto Plant (Canada) - N.AMERICA AGED",
        "facility": "Toronto WtE",
        "country": "Canada",
        "Start": 1995,  # 30 years old
        "waste_throughput_tonnes_year": 420000,
        "emission_levels": "compliant",
        "compliance_status": "compliant"
    },
    {
        "name": "Brescia Italy (EU) - AGED + DIOXIN RISK",
        "facility": "Brescia Waste Incinerator",
        "country": "Italy",
        "Start": 2000,  # 25 years old
        "waste_throughput_tonnes_year": 750000,
        "emission_levels": "APPROACHING EU limits, warning issued",
        "compliance_status": "At risk - NOx approaching 200 mg/Nm³ limit"
    },
    {
        "name": "Singapore Plant (Developed Asia) - MODERN",
        "facility": "Singapore WtE",
        "country": "Singapore",
        "Start": 2018,  # 7 years old
        "waste_throughput_tonnes_year": 400000,
        "emission_levels": "compliant",
        "compliance_status": "compliant"
    },
]


def test_plant_age_scoring():
    """Test Task 2: Plant age scoring"""
    print("\n" + "="*70)
    print("TEST 1: PLANT AGE CALCULATION & SCORING")
    print("="*70)

    for facility in TEST_FACILITIES:
        age = get_plant_age(facility.get('Start'))
        age_score = 0
        age_desc = "N/A"

        if age:
            if age > 20:
                age_score = 20
                age_desc = "CRITICAL (>20 yrs)"
            elif age > 15:
                age_score = 15
                age_desc = "HIGH (15-20 yrs)"
            elif age > 10:
                age_score = 10
                age_desc = "MEDIUM (10-15 yrs)"
            else:
                age_score = 0
                age_desc = "LOW (<10 yrs)"

        print(f"\n{facility['name']}")
        print(f"  Age: {age} years | Score: {age_score} points ({age_desc})")


def test_regulatory_weight_factors():
    """Test Task 3: Regulatory weight factors"""
    print("\n" + "="*70)
    print("TEST 2: REGULATORY WEIGHT FACTORS BY COUNTRY")
    print("="*70)

    for facility in TEST_FACILITIES:
        country = facility.get('country')
        region = country_to_region.get(country, "Other")
        weight = get_regulatory_weight(country)

        print(f"\n{facility['name']}")
        print(f"  Country: {country} | Region: {region} | Weight: {weight} points")


def test_age_and_regulation_filtering():
    """Test Task 4: Filtering by age AND regulation"""
    print("\n" + "="*70)
    print("TEST 3: LEAD FILTERING (Age >15 yrs AND EU/Developed/Emerging Asia)")
    print("="*70)

    passes = []
    fails = []

    for facility in TEST_FACILITIES:
        passes_filter, reason = should_filter_lead(facility, min_age=15)

        if passes_filter:
            passes.append((facility['name'], reason))
        else:
            fails.append((facility['name'], reason))

    print(f"\nPASSES FILTER ({len(passes)}):")
    for name, reason in passes:
        print(f"  [PASS] {name}")
        print(f"    | {reason}")

    print(f"\nFAILS FILTER ({len(fails)}):")
    for name, reason in fails:
        print(f"  [FAIL] {name}")
        print(f"    | {reason}")

    print(f"\nFILTER PASS RATE: {len(passes)}/{len(TEST_FACILITIES)} ({len(passes)/len(TEST_FACILITIES)*100:.1f}%)")


def test_combined_scoring():
    """Test Task 5: Combined scoring (age + regulatory + facility factors)"""
    print("\n" + "="*70)
    print("TEST 4: COMBINED SCORING (Age + Regulatory + Facility Factors)")
    print("="*70)

    for facility in TEST_FACILITIES:
        # Age scoring
        age = get_plant_age(facility.get('Start'))
        age_score = 0
        if age and age > 20:
            age_score = 20
        elif age and age > 15:
            age_score = 15
        elif age and age > 10:
            age_score = 10

        # Regulatory scoring
        reg_score = get_regulatory_weight(facility.get('country'))

        # Compliance scoring
        comp_score = 0
        if 'approaching' in facility.get('emission_levels', '').lower() or \
           'warning' in facility.get('compliance_status', '').lower():
            comp_score = 20

        # Total score
        total = age_score + reg_score + comp_score

        # Priority
        if total >= 50:
            priority = "[PRIORITY 1] HOT LEAD"
        elif total >= 35:
            priority = "[PRIORITY 2] WARM LEAD"
        elif total >= 25:
            priority = "[PRIORITY 3] GOOD LEAD"
        else:
            priority = "[PRIORITY 4] LONG-TERM"

        print(f"\n{facility['name']}")
        print(f"  Age: {age_score} | Regulation: {reg_score} | Compliance: {comp_score} | TOTAL: {total}")
        print(f"  {priority}")


def test_csv_data_loading():
    """Test Task 1: CSV data loading"""
    print("\n" + "="*70)
    print("TEST 5: CSV DATA LOADING CAPABILITY")
    print("="*70)

    import os

    csv_files = {
        "active_plants": "Active Plants Global WtE market 2024-2033.csv",
        "market_outlook": "Market outlook Global WtE market 2024-2033.csv",
        "projects": "Projects Global WtE market 2024-2033.csv"
    }

    print("\nChecking CSV files:")
    for key, filename in csv_files.items():
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"  [OK] {filename} ({file_size:,} bytes) - READY TO LOAD")
        else:
            print(f"  [NO] {filename} - NOT FOUND")

    try:
        import pandas as pd
        print(f"\n[OK] pandas library available - CSV loading ENABLED")

        # Try loading one file as example
        try:
            df = pd.read_csv("Active Plants Global WtE market 2024-2033.csv", encoding='utf-8-sig')
            print(f"  Sample data: {len(df)} rows, columns: {list(df.columns)[:5]}")
        except Exception as e:
            print(f"  Error loading sample: {e}")

    except ImportError:
        print(f"\n[WARN] pandas not available - CSV loading will use mock data")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("WTE LEAD GENERATION AGENT - SCORING TESTS")
    print("Tests for 5 Implementation Tasks")
    print("="*70)

    # Run all tests
    test_csv_data_loading()
    test_plant_age_scoring()
    test_regulatory_weight_factors()
    test_age_and_regulation_filtering()
    test_combined_scoring()

    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70)
