"""
AtmoGraph API: Simulation & Mitigation Routes
Runs What-If scenarios and evaluates resilience improvements (buffer increases, alternate routes).
"""

from typing import List, Dict, Any
from .dependencies import get_gnn_model, get_graph_engine

def handle_simulate_what_if(disrupted_node_id: str,
                            disruption_duration_days: int = 21,
                            mitigation_strategy: str = "none",
                            buffer_increase_days: int = 10):
    engine = get_graph_engine()
    gnn = get_gnn_model()

    nodes_copy = [dict(n) for n in engine.nodes]
    edges_copy = [dict(e) for e in engine.edges]

    # Baseline simulation
    baseline_result = gnn.predict_ripple(
        nodes=nodes_copy,
        edges=edges_copy,
        disrupted_node_ids=[disrupted_node_id],
        disruption_severity=0.88,
        estimated_initial_delay=disruption_duration_days
    )

    # Mitigation adjustments
    if mitigation_strategy == "increase_buffer":
        for n in nodes_copy:
            n["inventory_buffer_days"] = n.get("inventory_buffer_days", 7) + buffer_increase_days
    elif mitigation_strategy == "reroute_air":
        for e in edges_copy:
            if e["source"] == disrupted_node_id or e["target"] == disrupted_node_id:
                e["dependency_weight"] = max(0.2, e.get("dependency_weight", 0.75) * 0.45)
                e["transit_time_days"] = max(2, int(e.get("transit_time_days", 14) * 0.3))

    mitigated_result = gnn.predict_ripple(
        nodes=nodes_copy,
        edges=edges_copy,
        disrupted_node_ids=[disrupted_node_id],
        disruption_severity=0.88,
        estimated_initial_delay=disruption_duration_days
    )

    baseline_delay = baseline_result["summary"]["average_downstream_delay_days"]
    mitigated_delay = mitigated_result["summary"]["average_downstream_delay_days"]
    delay_saved = max(0.0, round(baseline_delay - mitigated_delay, 1))

    return {
        "scenario": {
            "disrupted_node": disrupted_node_id,
            "duration_days": disruption_duration_days,
            "mitigation_strategy": mitigation_strategy,
            "buffer_increase_days": buffer_increase_days if mitigation_strategy == "increase_buffer" else 0
        },
        "baseline_summary": baseline_result["summary"],
        "mitigated_summary": mitigated_result["summary"],
        "impact_reduction": {
            "days_saved": delay_saved,
            "high_risk_reduction": baseline_result["summary"]["high_risk_count"] - mitigated_result["summary"]["high_risk_count"]
        },
        "baseline_predictions": baseline_result["predictions"][:8],
        "mitigated_predictions": mitigated_result["predictions"][:8]
    }
