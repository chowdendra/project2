"""
AtmoGraph Application Configuration
"""

import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(APP_DIR, "data")
DATASET_PATH = os.path.join(DATA_DIR, "supply_chain_dataset.json")
NEWS_SAMPLES_PATH = os.path.join(DATA_DIR, "news_samples.json")
WEIGHTS_PATH = os.path.join(APP_DIR, "models", "weights", "gnn_calibrated_weights.json")
METRICS_PATH = os.path.join(APP_DIR, "models", "weights", "evaluation_metrics.json")
STATIC_DIR = os.path.join(APP_DIR, "static")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password123")
