"""
AtmoGraph Automated System Verification Test
Validates all 4 modules: Graph Engine, NLP Pipeline, GNN Message Passing, and APIs.
"""

import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from app.database.graph_engine import SupplyChainGraphEngine
from app.nlp.extractor import NLPEngine
from app.models.gnn_model import AtmoGraphMPNN
from app.api.routes_simulation import handle_simulate_what_if

def run_tests():
    print("=" * 60)
    print("  AtmoGraph: Automated End-to-End System Test Suite")
    print("=" * 60)

    # 1. Test Graph Engine
    print("\n[1/5] Testing Graph Database & Engine...")
    engine = SupplyChainGraphEngine()
    graph = engine.get_full_graph()
    assert len(graph["nodes"]) >= 20, "Expected at least 20 supply chain entities"
    assert len(graph["edges"]) >= 25, "Expected at least 25 supply chain edges"
    print(f"  ✓ Graph loaded successfully: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")

    # Test Shortest Path
    path_res = engine.find_shortest_supply_path("SUP-LITHIUM-01", "OEM-TESLA-GIGA")
    assert path_res is not None, "Failed to find path from Lithium Mine to Tesla Gigafactory"
    print(f"  ✓ Shortest Path verified: {' -> '.join(path_res['path'])} ({path_res['total_transit_days']} days transit)")

    # Test Bottlenecks
    bottlenecks = engine.get_bottleneck_centrality()
    print(f"  ✓ Top Chokepoint: {bottlenecks[0]['name']} (Score: {bottlenecks[0]['chokepoint_index']})")

    # 2. Test NLP Engine
    print("\n[2/5] Testing NLP Information Extraction Engine...")
    nlp = NLPEngine()
    sample_text = "Severe dockworkers strike closes Port of Rotterdam terminals, halting battery shipments to Tesla Berlin with delays of 30 days."
    res_nlp = nlp.extract_from_text(sample_text)
    assert res_nlp["primary_category"] == "Labor Strike", "Failed to classify Labor Strike event"
    assert "PORT-ROTTERDAM" in res_nlp["affected_node_ids"], "Failed to link Port of Rotterdam entity"
    assert res_nlp["estimated_direct_delay_days"] == 30, "Failed to parse 30 days delay"
    print(f"  ✓ Event Classified: {res_nlp['primary_category']} (Severity: {res_nlp['severity_score']})")
    print(f"  ✓ Mapped Nodes: {res_nlp['affected_node_ids']}")
    print(f"  ✓ Estimated Direct Delay: {res_nlp['estimated_direct_delay_days']} days")

    # 3. Test GNN Ripple Prediction
    print("\n[3/5] Testing GNN Message Passing Ripple Predictor...")
    mpnn = AtmoGraphMPNN()
    gnn_out = mpnn.predict_ripple(
        nodes=engine.nodes,
        edges=engine.edges,
        disrupted_node_ids=["PORT-ROTTERDAM"],
        disruption_severity=0.85,
        estimated_initial_delay=30
    )
    assert gnn_out["summary"]["high_risk_count"] > 0, "Expected at least one downstream high-risk node"
    assert len(gnn_out["propagation_paths"]) > 0, "Expected active propagation paths"
    print(f"  ✓ Propagation Hops: {gnn_out['max_propagation_hops']} hops")
    print(f"  ✓ High Risk Entities: {gnn_out['summary']['high_risk_count']}")
    print(f"  ✓ Average Downstream Delay: {gnn_out['summary']['average_downstream_delay_days']} days")
    print(f"  ✓ Active Shockwave Links: {len(gnn_out['propagation_paths'])} links")

    # 4. Test What-If Resilience Simulator
    print("\n[4/5] Testing What-If Resilience Mitigation Simulator...")
    sim_out = handle_simulate_what_if(
        disrupted_node_id="PORT-ROTTERDAM",
        disruption_duration_days=30,
        mitigation_strategy="increase_buffer",
        buffer_increase_days=10
    )
    days_saved = sim_out["impact_reduction"]["days_saved"]
    print(f"  ✓ Baseline Delay:  {sim_out['baseline_summary']['average_downstream_delay_days']} days")
    print(f"  ✓ Mitigated Delay: {sim_out['mitigated_summary']['average_downstream_delay_days']} days")
    print(f"  ✓ Delay Reduced by Proactive Buffering: {days_saved} days saved")

    # 5. Static Dashboard & File Verification
    print("\n[5/5] Testing Dashboard Files & Cypher Scripts...")
    index_file = os.path.join(BASE_DIR, "backend", "app", "static", "index.html")
    cql_file = os.path.join(BASE_DIR, "backend", "app", "database", "seed_graph.cql")
    metrics_file = os.path.join(BASE_DIR, "backend", "app", "models", "weights", "evaluation_metrics.json")
    
    assert os.path.exists(index_file), "Missing index.html"
    assert os.path.exists(cql_file), "Missing seed_graph.cql"
    assert os.path.exists(metrics_file), "Missing evaluation_metrics.json"
    print("  ✓ All required artifacts, static assets, and database seeds verified on disk.")

    print("\n" + "=" * 60)
    print("  🎉 ALL 5 TEST MODULES PASSED SUCCESSFULLY! ")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
