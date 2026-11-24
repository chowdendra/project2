"""
AtmoGraph API: NLP Routes
Endpoints for analyzing news articles and extracting supply chain disruptions.
"""

import json
import os
from .dependencies import get_nlp_engine
from ..config import NEWS_SAMPLES_PATH

def handle_analyze_news(text: str):
    if not text or not text.strip():
        return {"error": "News text cannot be empty"}
    nlp = get_nlp_engine()
    return nlp.extract_from_text(text)

def handle_get_news_samples():
    if os.path.exists(NEWS_SAMPLES_PATH):
        with open(NEWS_SAMPLES_PATH, "r", encoding="utf-8") as f:
            return {"samples": json.load(f)}
    return {"samples": []}
