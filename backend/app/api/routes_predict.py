"""
AtmoGraph API: Prediction Routes
Endpoints for executing GNN Message Passing ripple effect predictions and viewing evaluation metrics.
"""

import json
import os
from typing import List, Dict, Any
from .dependencies import get_gnn_model, get_graph_engine
from ..config import METRICS_PATH

def handle_predict_ripple(disrupted_nodes: List[str],
                          severity: float = 0.85,
                          initial_delay: int = 21,
                          damping_factor: float = 0.82):
    if not disrupted_nodes:
        return {"error": "At least one disrupted node ID must be provided"}
    
    engine = get_graph_engine()
    gnn = get_gnn_model()

    return gnn.predict_ripple(
        nodes=engine.nodes,
        edges=engine.edges,
        disrupted_node_ids=disrupted_nodes,
        disruption_severity=severity,
        estimated_initial_delay=initial_delay,
        damping_factor=damping_factor
    )

def handle_get_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"status": "Metrics not yet generated. Run python scripts/train_gnn.py to evaluate."}
