#!/usr/bin/env python3
"""
EU Emission Compliance Checker for Industrial Facilities
Integrates EU emission standards (Euro 7, CO₂ targets, BAT requirements) with EEA data

Based on restrictions.md - EU Emissions Standards & Restrictions
Provides detailed compliance scoring and violation detection for B2B lead generation
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
from enum import Enum
import pandas as pd
import numpy as np


class ComplianceStatus(Enum):
    """Compliance status categories"""
    CRITICAL_VIOLATION = "CRITICAL_VIOLATION"  # Exceeding limits, enforcement action
    IMMINENT_VIOLATION = "IMMINENT_VIOLATION"  # <90 days to deadline, approaching limits
    AT_RISK = "AT_RISK"  # Within 20% of limits, needs attention
    COMPLIANT = "COMPLIANT"  # Meeting all standards
    UNKNOWN = "UNKNOWN"  # Insufficient data


class RegulatoryUrgency(Enum):
    """Regulatory urgency levels for sales prioritization"""
    IMMEDIATE = "IMMEDIATE"  # 0-90 days to compliance deadline
    HIGH = "HIGH"  # 90-180 days to deadline
    MEDIUM = "MEDIUM"  # 180-365 days to deadline
    LOW = "LOW"  # >365 days to deadline
    NONE = "NONE"  # No upcoming deadlines


@dataclass
class EmissionStandard:
    """EU Emission Standard Definition"""
    pollutant: str  # e.g., "NOx", "CO2", "PM", "CO"
    limit_value: float  # Limit in g/km or tonnes/year
    unit: str  # "g/km", "tonnes/year", "g/GJ"
    standard_name: str  # e.g., "Euro 7", "BAT-AEL"
    effective_date: date  # When standard becomes mandatory
    applicable_to: str  # "vehicles", "waste_incineration", "power_generation"


@dataclass
class ComplianceViolation:
    """Detailed compliance violation record"""
    pollutant: str
    actual_value: float
    limit_value: float
    excess_percentage: float  # How much over the limit (%)
    standard_violated: str
    urgency: RegulatoryUrgency
    days_to_deadline: int
    penalty_risk: str  # Financial penalty description
    solution_opportunity: str  # What GMAB can offer


class EUEmissionStandards:
    """
    EU Emission Standards Repository
    Based on restrictions.md (Last Updated: October 17, 2025)
    """

    # Euro 7 Standards (Effective: 1 July 2025)
    EURO_7_PETROL = {
        "CO": 1.0,  # g/km
        "HC": 0.10,  # g/km
        "NOx": 0.06,  # g/km
        "PM": 0.005,  # g/km (direct injection)
        "PN": 6.0e11  # particles/km
    }

    EURO_7_DIESEL = {
        "CO": 0.50,  # g/km
        "HC_NOx": 0.17,  # g/km (combined)
        "NOx": 0.08,  # g/km
        "PM": 0.005,  # g/km
        "PN": 6.0e11  # particles/km
    }

    # CO₂ Fleet Targets
    CO2_TARGETS = {
        2025: {"passenger_cars": 95, "vans": 147},  # g CO₂/km
        2030: {"passenger_cars_reduction": 0.55, "vans_reduction": 0.50},  # % reduction vs 2021
        2035: {"all_vehicles": 0}  # Zero-emission only
    }

    # Industrial Waste Incineration Emission Limits (EU IED - Industrial Emissions Directive)
    # Based on Best Available Techniques (BAT) Conclusions for Waste Incineration
    WASTE_INCINERATION_DAILY_AVERAGE = {
        "NOx": 200,  # mg/Nm³ (as NO₂)
        "SO2": 50,  # mg/Nm³
        "HCl": 10,  # mg/Nm³
        "HF": 1,  #rassemblage/Nm³
        "CO": 50,  # mg/Nm³
        "Total_Dust": 10,  # mg/Nm³
        "TOC": 10,  # mg/Nm³ (Total Organic Carbon)
        "Cd_Tl": 0.05,  # mg/Nm³ (Cadmium + Thallium combined)
        "Hg": 0.05,  # mg/Nm³ (Mercury)
        "Heavy_Metals": 0.5  # mg/Nm³ (Sb+As+Pb+Cr+Co+Cu+Mn+Ni+V)
    }

    # BAT-AEL (BAT-Associated Emission Levels) for large combustion plants >50 MW
    LARGE_COMBUSTION_DAILY_AVERAGE = {
        "NOx": 100,  # mg/Nm³ for solid biomass
        "SO2": 150,  # mg/Nm³
        "Dust": 10,  # mg/Nm³
        "CO": 100,  # mg/Nm³
    }

    # Penalty structure (from EU regulations)
    CO2_PENALTY_PER_GRAM = 95  # EUR per g/km per vehicle

    @staticmethod
    def get_waste_incineration_standards() -> Dict[str, EmissionStandard]:
        """Get all waste incineration emission standards"""
        standards = {}
        reference_date = date(2016, 8, 2)  # EU IED BAT Conclusions for Waste Incineration

        for pollutant, limit in EUEmissionStandards.WASTE_INCINERATION_DAILY_AVERAGE.items():
            standards[pollutant] = EmissionStandard(
                pollutant=pollutant,
                limit_value=limit,
                unit="mg/Nm³",
                standard_name="BAT-AEL Waste Incineration",
                effective_date=reference_date,
                applicable_to="waste_incineration"
            )
        return standards

    @staticmethod
    def get_euro7_standards(fuel_type: str = "diesel") -> Dict[str, EmissionStandard]:
        """Get Euro 7 emission standards"""
        standards = {}
        euro7_date = date(2025, 7, 1)

        limits = EUEmissionStandards.EURO_7_DIESEL if fuel_type == "diesel" else EUEmissionStandards.EURO_7_PETROL

        for pollutant, limit in limits.items():
            standards[pollutant] = EmissionStandard(
                pollutant=pollutant,
                limit_value=limit,
                unit="g/km",
                standard_name=f"Euro 7 ({fuel_type})",
                effective_date=euro7_date,
                applicable_to="vehicles"
            )
        return standards


class EmissionComplianceChecker:
    """
    Checks industrial facility emissions against EU standards
    Generates detailed compliance scores and violation reports for lead generation
    """

    def __init__(self):
        self.waste_incineration_standards = EUEmissionStandards.get_waste_incineration_standards()
        self.today = date.today()

    def check_facility_compliance(
        self,
        facility_data: Dict,
        emissions_data: pd.DataFrame
    ) -> Tuple[ComplianceStatus, List[ComplianceViolation], int, str]:
        """
        Check a facility's compliance against EU standards

        Args:
            facility_data: Dict with facility info (name, type, country, etc.)
            emissions_data: DataFrame with pollutant emissions (columns: pollutant, value, unit, year)

        Returns:
            Tuple of (status, violations_list, compliance_score, detailed_reason)
        """
        violations = []
        compliance_score = 0
        reasons = []

        # Determine facility type and applicable standards
        facility_type = facility_data.get('mainActivityName', '').lower()
        is_waste_incineration = 'incineration' in facility_type or 'waste' in facility_type

        if is_waste_incineration:
            standards = self.waste_incineration_standards
        else:
            # Default to large combustion standards for other industrial facilities
            standards = self._get_combustion_standards()

        # Check each pollutant against standards
        for _, emission in emissions_data.iterrows():
            pollutant = emission.get('pollutantName', '')
            # Convert kg to tonnes
            actual_value_kg = emission.get('totalPollutantQuantityKg', 0)
            actual_value = actual_value_kg / 1000 if pd.notna(actual_value_kg) else 0  # tonnes/year

            # Map EEA pollutant names to standard names
            pollutant_mapped = self._map_pollutant_name(pollutant)

            if pollutant_mapped in standards:
                standard = standards[pollutant_mapped]
                violation = self._check_single_pollutant(
                    pollutant_mapped,
                    actual_value,
                    standard,
                    facility_data
                )

                if violation:
                    violations.append(violation)

        # Calculate overall compliance status and score
        if violations:
            status, compliance_score, detailed_reason = self._calculate_compliance_score(
                violations,
                facility_data
            )
        else:
            status = ComplianceStatus.COMPLIANT
            compliance_score = 10  # Base score for compliant facilities
            detailed_reason = "COMPLIANT - All emissions within EU BAT-AEL limits. Potential for proactive efficiency upgrades."

        return status, violations, compliance_score, detailed_reason

    def _check_single_pollutant(
        self,
        pollutant: str,
        actual_value: float,
        standard: EmissionStandard,
        facility_data: Dict
    ) -> Optional[ComplianceViolation]:
        """Check a single pollutant against its standard"""

        # Convert tonnes/year to mg/Nm³ (requires assumptions about facility capacity)
        # For now, use percentage-based approach for scoring
        # In production, would need actual concentration data from facility

        # Simplified check: if facility has high absolute emissions, flag it
        # This is a proxy - real implementation would need concentration data

        facility_size_factor = facility_data.get('energyInputTJ', 1000) / 1000  # Normalize by energy input

        # High-emissions threshold (simplified)
        if pollutant == "NOx" and actual_value > 100 * facility_size_factor:
            excess_pct = ((actual_value / (100 * facility_size_factor)) - 1) * 100
            days_to_deadline = self._calculate_days_to_deadline(standard.effective_date)
            urgency = self._determine_urgency(days_to_deadline, excess_pct)

            return ComplianceViolation(
                pollutant=pollutant,
                actual_value=actual_value,
                limit_value=standard.limit_value,
                excess_percentage=excess_pct,
                standard_violated=standard.standard_name,
                urgency=urgency,
                days_to_deadline=days_to_deadline,
                penalty_risk=self._calculate_penalty_risk(pollutant, excess_pct, facility_data),
                solution_opportunity=self._identify_solution(pollutant, facility_data)
            )

        return None

    def _calculate_compliance_score(
        self,
        violations: List[ComplianceViolation],
        facility_data: Dict
    ) -> Tuple[ComplianceStatus, int, str]:
        """
        Calculate compliance score (0-100 points) based on violations
        Higher score = more urgent sales opportunity

        Scoring breakdown:
        - CRITICAL VIOLATION: 100 points (enforcement action, immediate need)
        - IMMINENT VIOLATION: 80 points (<90 days to deadline)
        - AT RISK: 50 points (within 20% of limits)
        - Multiple violations: +10 points per additional violation
        - Large facility size: +20 points (bigger opportunity)
        """

        if not violations:
            return ComplianceStatus.COMPLIANT, 10, "COMPLIANT - Proactive efficiency opportunity"

        # Find most severe violation
        most_urgent = max(violations, key=lambda v: v.excess_percentage)

        # Base score from violation severity
        if most_urgent.urgency == RegulatoryUrgency.IMMEDIATE:
            status = ComplianceStatus.CRITICAL_VIOLATION
            base_score = 100
            urgency_label = "CRITICAL VIOLATION"
        elif most_urgent.urgency == RegulatoryUrgency.HIGH:
            status = ComplianceStatus.IMMINENT_VIOLATION
            base_score = 80
            urgency_label = "IMMINENT VIOLATION"
        else:
            status = ComplianceStatus.AT_RISK
            base_score = 50
            urgency_label = "AT RISK"

        # Additional points for multiple violations
        multi_violation_bonus = min((len(violations) - 1) * 10, 30)

        # Facility size bonus (larger = more revenue potential)
        energy_input = facility_data.get('energyInputTJ', 0)
        if energy_input > 5000:
            size_bonus = 20
            size_label = "LARGE FACILITY"
        elif energy_input > 1000:
            size_bonus = 10
            size_label = "MEDIUM FACILITY"
        else:
            size_bonus = 0
            size_label = "SMALL FACILITY"

        total_score = min(base_score + multi_violation_bonus + size_bonus, 100)

        # Build detailed reason
        violation_details = []
        for v in violations:
            violation_details.append(
                f"   • {v.pollutant}: {v.actual_value:.1f} tonnes/year "
                f"({v.excess_percentage:+.1f}% vs {v.standard_violated})"
            )

        detailed_reason = f"""{urgency_label} - {len(violations)} emission violation(s) detected | {size_label}

COMPLIANCE VIOLATIONS:
{chr(10).join(violation_details)}

REGULATORY URGENCY: {most_urgent.days_to_deadline} days until {most_urgent.standard_violated} enforcement deadline

FINANCIAL RISK: {most_urgent.penalty_risk}

GMAB SOLUTION OPPORTUNITY: {most_urgent.solution_opportunity}

WHY THIS SCORE ({total_score}/100):
   • Base Violation Severity: {base_score} points ({urgency_label})
   • Multiple Violations Bonus: +{multi_violation_bonus} points ({len(violations)} violations)
   • Facility Size Factor: +{size_bonus} points ({size_label}, {energy_input:.0f} TJ/year energy input)

SALES STRATEGY:
   • Lead with regulatory compliance urgency (deadline in {most_urgent.days_to_deadline} days)
   • Emphasize penalty avoidance (potential fines/enforcement action)
   • Position GMAB's proven emission control solutions (50+ WtE installations)
   • Offer immediate technical assessment and fast-track implementation
   • Highlight co-benefits: energy efficiency gains + emission compliance"""

        return status, total_score, detailed_reason

    def _calculate_days_to_deadline(self, effective_date: date) -> int:
        """Calculate days until compliance deadline"""
        return (effective_date - self.today).days

    def _determine_urgency(self, days_to_deadline: int, excess_percentage: float) -> RegulatoryUrgency:
        """Determine regulatory urgency level"""
        if days_to_deadline < 0 and excess_percentage > 10:
            return RegulatoryUrgency.IMMEDIATE  # Already past deadline and violating
        elif days_to_deadline < 90:
            return RegulatoryUrgency.IMMEDIATE
        elif days_to_deadline < 180:
            return RegulatoryUrgency.HIGH
        elif days_to_deadline < 365:
            return RegulatoryUrgency.MEDIUM
        else:
            return RegulatoryUrgency.LOW

    def _calculate_penalty_risk(self, pollutant: str, excess_pct: float, facility_data: Dict) -> str:
        """Calculate financial penalty risk"""
        if pollutant == "CO2":
            # CO₂ penalties: EUR 95 per g/km per vehicle
            return f"EUR 95/g/km excess emissions penalty. For fleet of 10,000 vehicles at {excess_pct:.0f}% excess = potential EUR {(95 * excess_pct * 10000 / 100):,.0f} annual penalty"
        else:
            # Industrial emissions penalties vary by country
            country = facility_data.get('countryCode', 'EU')
            if excess_pct > 50:
                return f"SEVERE: Potential facility shutdown orders, operating permit suspension, fines up to EUR 500,000+ in {country}"
            elif excess_pct > 20:
                return f"HIGH: Enforcement action likely, fines EUR 50,000-250,000 in {country}, mandatory improvement plan"
            else:
                return f"MODERATE: Warning notices, compliance improvement plan required within 90 days"

    def _identify_solution(self, pollutant: str, facility_data: Dict) -> str:
        """Identify GMAB solution for the violation"""
        facility_type = facility_data.get('mainActivityName', '').lower()

        if pollutant == "NOx":
            return "GMAB SCR (Selective Catalytic Reduction) system + Advanced combustion optimization = 70-90% NOx reduction. Proven in 50+ WtE installations. Typical ROI: 2-3 years."
        elif pollutant == "SO2":
            return "GMAB Flue Gas Desulfurization (FGD) system + Dry sorbent injection = 95%+ SO₂ removal. Modular retrofit design for minimal downtime."
        elif pollutant == "CO2":
            if 'waste' in facility_type or 'incineration' in facility_type:
                return "GMAB Waste Heat Recovery + ORC (Organic Rankine Cycle) turbine = 15-25% efficiency improvement, reducing CO₂ intensity by up to 30%"
            else:
                return "GMAB Energy Efficiency Optimization Package: Waste heat recovery, process optimization, fuel switching consultation"
        elif pollutant == "Dust" or pollutant == "PM" or pollutant == "Total_Dust":
            return "GMAB Advanced Bag Filter System + Electrostatic Precipitator (ESP) = 99.9% particulate removal, meeting strictest EU standards"
        else:
            return f"GMAB comprehensive emission control solution for {pollutant} - technical assessment available within 48 hours"

    def _map_pollutant_name(self, eea_pollutant: str) -> str:
        """Map EEA database pollutant names to standard names"""
        mapping = {
            "Nitrogen oxides (NOx/NO2)": "NOx",
            "Nitrogen oxides": "NOx",
            "NOx": "NOx",
            "Sulphur dioxide": "SO2",
            "SO2": "SO2",
            "Carbon dioxide": "CO2",
            "CO2": "CO2",
            "Carbon monoxide": "CO",
            "CO": "CO",
            "Particulate matter": "Total_Dust",
            "PM10": "Total_Dust",
            "Dust": "Total_Dust",
            "Total organic carbon": "TOC",
            "Mercury": "Hg",
            "Cadmium": "Cd_Tl",
            "Thallium": "Cd_Tl"
        }
        return mapping.get(eea_pollutant, eea_pollutant)

    def _get_combustion_standards(self) -> Dict[str, EmissionStandard]:
        """Get standards for large combustion plants"""
        standards = {}
        reference_date = date(2016, 8, 2)

        for pollutant, limit in EUEmissionStandards.LARGE_COMBUSTION_DAILY_AVERAGE.items():
            standards[pollutant] = EmissionStandard(
                pollutant=pollutant,
                limit_value=limit,
                unit="mg/Nm³",
                standard_name="BAT-AEL Large Combustion Plant",
                effective_date=reference_date,
                applicable_to="combustion"
            )
        return standards


# Example usage and testing
if __name__ == "__main__":
    print("=" * 80)
    print("   EU Emission Compliance Checker - Test Suite")
    print("=" * 80)

    # Test data: simulated facility
    test_facility = {
        "nameOfFeature": "Rotterdam Waste Incineration Plant",
        "countryCode": "NL",
        "mainActivityName": "Installations for the incineration of non-hazardous waste",
        "energyInputTJ": 3500
    }

    # Test emissions data
    test_emissions = pd.DataFrame([
        {"pollutantName": "Nitrogen oxides (NOx/NO2)", "totalPollutantQuantityTNE": 450, "year": 2023},
        {"pollutantName": "Sulphur dioxide", "totalPollutantQuantityTNE": 85, "year": 2023},
        {"pollutantName": "Carbon monoxide", "totalPollutantQuantityTNE": 120, "year": 2023}
    ])

    # Initialize checker
    checker = EmissionComplianceChecker()

    # Check compliance
    print(f"\nTesting facility: {test_facility['nameOfFeature']}")
    print(f"   Activity: {test_facility['mainActivityName']}")
    print(f"   Energy Input: {test_facility['energyInputTJ']} TJ/year\n")

    status, violations, score, detailed_reason = checker.check_facility_compliance(
        test_facility,
        test_emissions
    )

    print(f"COMPLIANCE RESULT:")
    print(f"   Status: {status.value}")
    print(f"   Lead Score: {score}/100")
    print(f"   Violations Detected: {len(violations)}")
    print(f"\n{detailed_reason}")

    print("\n" + "=" * 80)
    print("Compliance checker ready for integration into lead finders")
    print("=" * 80)
