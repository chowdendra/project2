"""
AtmoGraph Graph Engine
Provides high-performance graph operations:
- Node and edge retrieval with filtering
- Downstream reachability search (BFS/DFS)
- Shortest supply route pathfinding
- Bottleneck node centrality analysis
- Disruption cascade simulation
"""

import json
import os
from collections import deque
from typing import Dict, List, Any, Optional, Set


class SupplyChainGraphEngine:
    def __init__(self, data_path: Optional[str] = None):
        if not data_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "supply_chain_dataset.json")
        self.data_path = data_path
        self.nodes = []
        self.edges = []
        self.node_map = {}
        self.adj_out = {}
        self.adj_in = {}
        self.load_graph()

    def load_graph(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Supply chain dataset not found at {self.data_path}")

        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.nodes = data.get("nodes", [])
            self.edges = data.get("edges", [])

        self.node_map = {n["id"]: n for n in self.nodes}
        self.adj_out = {n["id"]: [] for n in self.nodes}
        self.adj_in = {n["id"]: [] for n in self.nodes}

        for e in self.edges:
            src = e["source"]
            tgt = e["target"]
            if src in self.adj_out and tgt in self.node_map:
                self.adj_out[src].append(e)
            if tgt in self.adj_in and src in self.node_map:
                self.adj_in[tgt].append(e)

    def get_full_graph(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "nodes": self.nodes,
            "edges": self.edges
        }

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self.node_map.get(node_id)

    def get_downstream_subgraph(self, origin_ids: List[str], max_depth: int = 4) -> Dict[str, Any]:
        """
        Finds all nodes and edges affected downstream from a set of starting nodes.
        """
        visited_nodes: Set[str] = set(origin_ids)
        visited_edges: List[Dict[str, Any]] = []
        queue = deque([(nid, 0) for nid in origin_ids if nid in self.node_map])

        while queue:
            curr_id, depth = queue.popleft()
            if depth >= max_depth:
                continue

            for edge in self.adj_out.get(curr_id, []):
                tgt = edge["target"]
                visited_edges.append(edge)
                if tgt not in visited_nodes:
                    visited_nodes.add(tgt)
                    queue.append((tgt, depth + 1))

        sub_nodes = [self.node_map[nid] for nid in visited_nodes if nid in self.node_map]

        return {
            "origin_nodes": origin_ids,
            "subgraph_nodes_count": len(sub_nodes),
            "subgraph_edges_count": len(visited_edges),
            "nodes": sub_nodes,
            "edges": visited_edges
        }

    def find_shortest_supply_path(self, start_id: str, end_id: str) -> Optional[Dict[str, Any]]:
        """
        Computes the shortest supply chain path using BFS weighted by transit time.
        """
        if start_id not in self.node_map or end_id not in self.node_map:
            return None

        # Queue storing: (current_node, path_nodes, path_edges, cumulative_transit_days)
        queue = deque([(start_id, [start_id], [], 0)])
        visited = {start_id: 0}

        shortest_res = None

        while queue:
            curr, path, edges, trans = queue.popleft()
            if curr == end_id:
                if shortest_res is None or trans < shortest_res["total_transit_days"]:
                    shortest_res = {
                        "path": path,
                        "path_edges": edges,
                        "total_transit_days": trans,
                        "hops": len(edges)
                    }
                continue

            for edge in self.adj_out.get(curr, []):
                tgt = edge["target"]
                new_trans = trans + edge.get("transit_time_days", 1)
                if tgt not in visited or new_trans < visited[tgt]:
                    visited[tgt] = new_trans
                    queue.append((tgt, path + [tgt], edges + [edge], new_trans))

        return shortest_res

    def get_bottleneck_centrality(self) -> List[Dict[str, Any]]:
        """
        Calculates centrality: in-degree, out-degree, and dependency leverage.
        Identifies critical chokepoints in the supply network.
        """
        rankings = []
        for n in self.nodes:
            nid = n["id"]
            in_deg = len(self.adj_in.get(nid, []))
            out_deg = len(self.adj_out.get(nid, []))
            crit = float(n.get("criticality_score", 0.5))
            
            # Bottleneck index = Out-Degree * In-Degree * Criticality
            chokepoint_score = round(((out_deg + 1) * (in_deg + 1) * crit), 2)
            
            rankings.append({
                "id": nid,
                "name": n["name"],
                "type": n["type"],
                "country": n.get("country", ""),
                "in_degree": in_deg,
                "out_degree": out_deg,
                "criticality_score": crit,
                "chokepoint_index": chokepoint_score
            })

        rankings.sort(key=lambda x: x["chokepoint_index"], reverse=True)
        return rankings
