"""
AtmoGraph NLP Disruption Taxonomy
Standardized categories, keywords, and severity scoring matrices for supply chain events.
"""

from typing import Dict, List, Any

DISRUPTION_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "Labor Strike": {
        "keywords": ["strike", "dockworkers", "walkout", "picket", "union", "labor dispute", "work stoppage", "crane operators"],
        "base_severity": 0.85,
        "category_group": "Transportation & Labor",
        "default_lead_time_impact_days": 21
    },
    "Natural Disaster": {
        "keywords": ["earthquake", "typhoon", "hurricane", "flood", "tsunami", "tornado", "volcanic", "drought", "landslide"],
        "base_severity": 0.90,
        "category_group": "Environmental",
        "default_lead_time_impact_days": 28
    },
    "Geopolitical & Conflict": {
        "keywords": ["sanction", "embargo", "missile", "war", "blockade", "reroute", "detour", "tariffs", "trade ban", "piracy"],
        "base_severity": 0.88,
        "category_group": "Geopolitical",
        "default_lead_time_impact_days": 25
    },
    "Industrial Accident / Fire": {
        "keywords": ["fire", "explosion", "chemical leak", "reactor blast", "factory collapse", "pipeline burst", "structural failure"],
        "base_severity": 0.75,
        "category_group": "Production Halt",
        "default_lead_time_impact_days": 18
    },
    "Cyberattack": {
        "keywords": ["cyberattack", "ransomware", "hack", "data breach", "malware", "system outage", "scada", "telemetry offline"],
        "base_severity": 0.80,
        "category_group": "Cyber & Systems",
        "default_lead_time_impact_days": 14
    },
    "Port & Maritime Congestion": {
        "keywords": ["congestion", "stranded", "vessel stacking", "berth delay", "chokepoint", "container backlog", "anchored"],
        "base_severity": 0.70,
        "category_group": "Logistics & Freight",
        "default_lead_time_impact_days": 12
    },
    "Raw Material Shortage": {
        "keywords": ["shortage", "scarcity", "depletion", "rationing", "yield drop", "export ban", "ore deficit"],
        "base_severity": 0.65,
        "category_group": "Supply Squeeze",
        "default_lead_time_impact_days": 20
    }
}

SEVERITY_LEVELS = [
    {"label": "Critical", "threshold": 0.80, "color": "#ef4444"},
    {"label": "High", "threshold": 0.60, "color": "#f97316"},
    {"label": "Medium", "threshold": 0.40, "color": "#eab308"},
    {"label": "Low", "threshold": 0.0, "color": "#22c55e"}
]

def classify_severity(score: float) -> str:
    for level in SEVERITY_LEVELS:
        if score >= level["threshold"]:
            return level["label"]
    return "Low"
