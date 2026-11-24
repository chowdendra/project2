"""
AtmoGraph API Shared Dependencies
Singletons for graph engine, NLP pipeline, GNN model, and database client.
"""

from ..database.graph_engine import SupplyChainGraphEngine
from ..database.neo4j_client import Neo4jClient
from ..nlp.extractor import NLPEngine
from ..models.gnn_model import AtmoGraphMPNN
from ..config import DATASET_PATH, WEIGHTS_PATH

_graph_engine = None
_nlp_engine = None
_gnn_model = None
_neo4j_client = None

def get_graph_engine() -> SupplyChainGraphEngine:
    global _graph_engine
    if _graph_engine is None:
        _graph_engine = SupplyChainGraphEngine(DATASET_PATH)
    return _graph_engine

def get_nlp_engine() -> NLPEngine:
    global _nlp_engine
    if _nlp_engine is None:
        _nlp_engine = NLPEngine(DATASET_PATH)
    return _nlp_engine

def get_gnn_model() -> AtmoGraphMPNN:
    global _gnn_model
    if _gnn_model is None:
        _gnn_model = AtmoGraphMPNN(WEIGHTS_PATH)
    return _gnn_model

def get_neo4j_client() -> Neo4jClient:
    global _neo4j_client
    if _neo4j_client is None:
        _neo4j_client = Neo4jClient()
    return _neo4j_client
