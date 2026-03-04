#!/usr/bin/env python3
"""
Industrial Emissions Lead Finder
Transforms EEA Industrial Emissions Data into Qualified B2B Leads

Features:
- Analyzes 98,000+ European industrial facilities
- Filters by country, industry, and company criteria
- AI-powered lead scoring (5-factor model)
- Enrichment with web search for contacts
- Professional Excel export with analytics
- Geographic mapping capabilities
"""

import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import PieChart, BarChart, Reference
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import json

@dataclass
class IndustrialLead:
    """Lead data structure for industrial facilities"""
    id: int
    company_name: str
    parent_company: Optional[str]
    facility_name: str
    industry: str
    activity_code: str
    activity_description: str
    
    # Address
    street: str
    building: str
    city: str
    postal_code: str
    country: str
    
    # Geographic
    latitude: float
    longitude: float
    
    # Scoring
    score: int = 0
    tier: int = 0
    tier_label: str = ""
    
    # Qualification factors
    facility_type: str = ""
    estimated_size: str = ""
    emissions_category: str = ""
    
    # Contact (to be enriched)
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    contact_email: Optional[str] = None
