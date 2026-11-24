"""
AtmoGraph Cypher Seed Generator
Exports supply chain nodes and relationships into runnable Cypher (.cql) queries
for direct execution in Neo4j Browser, Neo4j Bloom, or AuraDB cloud instances.
"""

import json
import os
from typing import List, Dict, Any


def generate_cypher_script(dataset_path: str, output_path: str):
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    cypher_lines = [
        "// ========================================================",
        "// AtmoGraph - Supply Chain Knowledge Graph Cypher Schema",
        "// Run in Neo4j Browser / Neo4j Desktop / Neo4j Aura",
        "// ========================================================\n",
        "// 1. Clear existing supply chain graph elements",
        "MATCH (n:SupplyChainEntity) DETACH DELETE n;\n",
        "// 2. Create Unique Constraints",
        "CREATE CONSTRAINT entity_id_unique IF NOT EXISTS FOR (e:SupplyChainEntity) REQUIRE e.id IS UNIQUE;\n",
        "// 3. Create Supply Chain Nodes"
    ]

    for n in nodes:
        nid = n["id"]
        name = n["name"].replace("'", "\\'")
        ntype = n.get("type", "Entity")
        tier = n.get("tier", "N/A")
        industry = n.get("industry", "General")
        country = n.get("country", "")
        lead_time = n.get("lead_time_days", 14)
        buffer_days = n.get("inventory_buffer_days", 7)
        criticality = n.get("criticality_score", 0.7)
        volume = n.get("financial_volume_mil", 1000.0)
        desc = n.get("description", "").replace("'", "\\'")

        label = ntype.replace(" ", "")

        cypher = (
            f"CREATE (:{label}:SupplyChainEntity {{"
            f"id: '{nid}', name: '{name}', type: '{ntype}', tier: '{tier}', "
            f"industry: '{industry}', country: '{country}', lead_time_days: {lead_time}, "
            f"inventory_buffer_days: {buffer_days}, criticality_score: {criticality}, "
            f"financial_volume_mil: {volume}, description: '{desc}', current_status: 'Normal'"
            f"}});"
        )
        cypher_lines.append(cypher)

    cypher_lines.append("\n// 4. Create Supply Chain Directed Relationships")

    for e in edges:
        src = e["source"]
        tgt = e["target"]
        rel = e.get("relationship", "CONNECTED_TO")
        prod = e.get("product", "Goods").replace("'", "\\'")
        transit = e.get("transit_time_days", 3)
        mode = e.get("shipping_mode", "Maritime")
        dep = e.get("dependency_weight", 0.75)

        cypher = (
            f"MATCH (s:SupplyChainEntity {{id: '{src}'}}), (t:SupplyChainEntity {{id: '{tgt}'}}) "
            f"CREATE (s)-[:{rel} {{"
            f"product: '{prod}', transit_time_days: {transit}, shipping_mode: '{mode}', "
            f"dependency_weight: {dep}"
            f"}}]->(t);"
        )
        cypher_lines.append(cypher)

    cypher_lines.append("\n// 5. Verification Query: Return all nodes and edges")
    cypher_lines.append("MATCH (n:SupplyChainEntity)-[r]->(m:SupplyChainEntity) RETURN n, r, m LIMIT 100;\n")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cypher_lines))

    print(f"Generated Cypher script at: {output_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "data", "supply_chain_dataset.json")
    out_file = os.path.join(base_dir, "database", "seed_graph.cql")
    generate_cypher_script(data_file, out_file)
