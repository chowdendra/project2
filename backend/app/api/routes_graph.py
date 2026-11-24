"""
AtmoGraph API: Graph Routes
Endpoints for querying nodes, edges, subgraphs, shortest paths, and bottlenecks.
"""

from typing import Optional, List
from .dependencies import get_graph_engine, get_neo4j_client

# Define lightweight route handlers that work with FastAPI or standalone
def handle_get_graph():
    engine = get_graph_engine()
    return engine.get_full_graph()

def handle_get_node(node_id: str):
    engine = get_graph_engine()
    node = engine.get_node(node_id)
    if not node:
        return {"error": f"Node with ID '{node_id}' not found"}
    
    # Direct upstream suppliers
    suppliers = engine.adj_in.get(node_id, [])
    # Direct downstream customers
    customers = engine.adj_out.get(node_id, [])

    return {
        "node": node,
        "direct_suppliers": suppliers,
        "direct_customers": customers
    }

def handle_get_downstream(node_ids: List[str], max_depth: int = 4):
    engine = get_graph_engine()
    return engine.get_downstream_subgraph(node_ids, max_depth)

def handle_get_bottlenecks():
    engine = get_graph_engine()
    return {"bottlenecks": engine.get_bottleneck_centrality()}

def handle_get_shortest_path(start_id: str, end_id: str):
    engine = get_graph_engine()
    res = engine.find_shortest_supply_path(start_id, end_id)
    if not res:
        return {"error": f"No connected path found between {start_id} and {end_id}"}
    return res

def handle_get_neo4j_status():
    neo4j = get_neo4j_client()
    return neo4j.get_status()
