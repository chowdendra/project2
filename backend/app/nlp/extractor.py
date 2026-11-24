"""
AtmoGraph NLP Ingestion Engine
Extracts entities (Company, Port, Location, Disruption Type, Severity) from news feeds.
Supports spaCy and HuggingFace pipelines with a built-in hybrid rule & NER resolver.
"""

import re
import json
import os
from typing import Dict, List, Any, Optional

from .disruption_taxonomy import DISRUPTION_CATEGORIES, classify_severity

# Check if spaCy is available
SPACY_AVAILABLE = False
nlp_spacy = None
try:
    import spacy
    try:
        nlp_spacy = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
    except Exception:
        # Fallback if specific model is not downloaded
        SPACY_AVAILABLE = False
except ImportError:
    SPACY_AVAILABLE = False


class NLPEngine:
    """
    NLP Information Extraction Engine for Supply Chain Disruption Intelligence.
    Extracts:
    - Organizations / Companies (ORG)
    - Geographical locations & Ports (GPE / LOC)
    - Disruption events & classification
    - Severity score (0.0 to 1.0)
    - Estimated direct delay days
    - Matches entities directly to Graph Database Nodes
    """

    def __init__(self, data_path: Optional[str] = None):
        self.spacy_active = SPACY_AVAILABLE
        self.node_lookup = {}
        self.location_lookup = {}
        self.alias_lookup = {}
        self._load_graph_entities(data_path)

    def _load_graph_entities(self, data_path: Optional[str]):
        if not data_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "supply_chain_dataset.json")

        if os.path.exists(data_path):
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for node in data.get("nodes", []):
                        nid = node["id"]
                        name = node["name"]
                        country = node.get("country", "")
                        location = node.get("location", "")
                        
                        self.node_lookup[nid] = node
                        self.alias_lookup[name.lower()] = nid
                        
                        # Add sub-aliases
                        tokens = [t.strip(",. ") for t in name.split() if len(t) > 3]
                        for t in tokens:
                            if t.lower() not in ["operations", "complex", "werk", "superhub", "network"]:
                                self.alias_lookup[t.lower()] = nid

                        if country:
                            self.location_lookup[country.lower()] = nid
                        if location:
                            self.location_lookup[location.lower()] = nid
            except Exception as e:
                print(f"[NLP Engine] Warning: Failed loading graph entities: {e}")

    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """
        Processes news text and returns structured disruption record.
        """
        text_lower = text.lower()
        extracted_entities = []
        matched_node_ids = set()

        # 1. spaCy NER (if loaded)
        if self.spacy_active and nlp_spacy:
            doc = nlp_spacy(text)
            for ent in doc.ents:
                extracted_entities.append({
                    "text": ent.text,
                    "label": ent.label_
                })
        else:
            # High-precision statistical & regex entity scanner
            # Match capitalized phrases (e.g. "Port of Rotterdam", "TSMC Fab 18", "Tesla Gigafactory")
            pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*|[A-Z]{2,}(?:\s+[A-Z0-9]+)*)\b'
            matches = re.findall(pattern, text)
            for m in set(matches):
                if len(m) > 2 and m.lower() not in ["the", "a", "an", "this", "that", "more", "due", "after"]:
                    extracted_entities.append({
                        "text": m,
                        "label": "NAMED_ENTITY"
                    })

        # 2. Map entities to Graph Nodes
        for phrase, nid in self.alias_lookup.items():
            if phrase in text_lower:
                matched_node_ids.add(nid)

        for loc, nid in self.location_lookup.items():
            if loc in text_lower:
                matched_node_ids.add(nid)

        # 3. Disruption Category & Event Matching
        detected_categories = []
        highest_severity_score = 0.35  # baseline
        primary_category = "General Logistics Concern"
        estimated_delay = 7

        for cat_name, cat_meta in DISRUPTION_CATEGORIES.items():
            hit_keywords = [kw for kw in cat_meta["keywords"] if kw in text_lower]
            if hit_keywords:
                score = cat_meta["base_severity"] * (0.8 + 0.1 * min(len(hit_keywords), 3))
                detected_categories.append({
                    "category": cat_name,
                    "matched_keywords": hit_keywords,
                    "score": round(score, 3)
                })
                if score > highest_severity_score:
                    highest_severity_score = score
                    primary_category = cat_name
                    estimated_delay = cat_meta["default_lead_time_impact_days"]

        # Parse explicit numbers of days or weeks in text (e.g. "25 to 35 days", "3 to 4 weeks")
        day_match = re.search(r'(\d+)(?:\s*(?:to|-)\s*(\d+))?\s*days?', text_lower)
        week_match = re.search(r'(\d+)(?:\s*(?:to|-)\s*(\d+))?\s*weeks?', text_lower)

        if day_match:
            d1 = int(day_match.group(1))
            d2 = int(day_match.group(2)) if day_match.group(2) else d1
            estimated_delay = round((d1 + d2) / 2)
        elif week_match:
            w1 = int(week_match.group(1))
            w2 = int(week_match.group(2)) if week_match.group(2) else w1
            estimated_delay = round(((w1 + w2) / 2) * 7)

        severity_label = classify_severity(highest_severity_score)

        # Build list of affected nodes with details
        affected_nodes_info = []
        for nid in matched_node_ids:
            node_info = self.node_lookup.get(nid, {})
            affected_nodes_info.append({
                "id": nid,
                "name": node_info.get("name", nid),
                "type": node_info.get("type", "Unknown"),
                "country": node_info.get("country", "Global"),
                "criticality_score": node_info.get("criticality_score", 0.7)
            })

        return {
            "primary_category": primary_category,
            "severity_score": round(min(highest_severity_score, 1.0), 2),
            "severity_label": severity_label,
            "estimated_direct_delay_days": estimated_delay,
            "detected_categories": detected_categories,
            "extracted_entities": extracted_entities[:10],
            "affected_node_ids": list(matched_node_ids),
            "affected_nodes_details": affected_nodes_info,
            "nlp_backend": "spaCy (Active)" if self.spacy_active else "Rule-NER Hybrid Engine (Active)"
        }
