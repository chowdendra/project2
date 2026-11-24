"""
AtmoGraph Neo4j Database Client
Manages connection to Neo4j graph database instance, executes Cypher queries,
and provides seamless fallback to in-memory graph engine when Neo4j server is offline.
"""

import os
from typing import Dict, List, Any, Optional

NEO4J_AVAILABLE = False
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False


class Neo4jClient:
    def __init__(self,
                 uri: Optional[str] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password123")
        self.driver = None
        self.is_connected = False
        self._init_connection()

    def _init_connection(self):
        if not NEO4J_AVAILABLE:
            self.is_connected = False
            return

        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                record = result.single()
                if record and record["test"] == 1:
                    self.is_connected = True
        except Exception:
            self.is_connected = False
            self.driver = None

    def get_status(self) -> Dict[str, Any]:
        return {
            "driver_installed": NEO4J_AVAILABLE,
            "connected": self.is_connected,
            "uri": self.uri,
            "user": self.user,
            "status_message": "Neo4j Active & Connected" if self.is_connected else "Neo4j Offline (Using In-Memory Graph Engine Fallback)"
        }

    def execute_cypher(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Executes a raw Cypher query if connected to Neo4j.
        """
        if not self.is_connected or not self.driver:
            return []

        parameters = parameters or {}
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            print(f"[Neo4j] Error executing Cypher: {e}")
            return []

    def close(self):
        if self.driver:
            self.driver.close()
