"""
AtmoGraph FastAPI Application
Connects Graph Database, NLP Engine, and GNN Message Passing to REST Endpoints & UI Dashboard.
"""

import os
from typing import List, Optional
from pydantic import BaseModel

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, JSONResponse
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

from .config import STATIC_DIR
from .api.routes_graph import (
    handle_get_graph, handle_get_node, handle_get_downstream,
    handle_get_bottlenecks, handle_get_shortest_path, handle_get_neo4j_status
)
from .api.routes_nlp import handle_analyze_news, handle_get_news_samples
from .api.routes_predict import handle_predict_ripple, handle_get_metrics
from .api.routes_simulation import handle_simulate_what_if


if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="AtmoGraph API",
        description="Supply Chain Ripple Effect Predictor: GNN, NLP, and Graph Database Services",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request schemas
    class NewsAnalysisRequest(BaseModel):
        text: str

    class RipplePredictionRequest(BaseModel):
        disrupted_nodes: List[str]
        severity: Optional[float] = 0.85
        initial_delay: Optional[int] = 21
        damping_factor: Optional[float] = 0.82

    class WhatIfRequest(BaseModel):
        disrupted_node_id: str
        disruption_duration_days: Optional[int] = 21
        mitigation_strategy: Optional[str] = "none"
        buffer_increase_days: Optional[int] = 10

    # API Endpoints
    @app.get("/api/graph")
    def get_graph():
        return handle_get_graph()

    @app.get("/api/graph/node/{node_id}")
    def get_node(node_id: str):
        res = handle_get_node(node_id)
        if "error" in res:
            raise HTTPException(status_code=404, detail=res["error"])
        return res

    @app.get("/api/graph/downstream")
    def get_downstream(node_ids: str = Query(..., description="Comma-separated node IDs")):
        ids = [nid.strip() for nid in node_ids.split(",") if nid.strip()]
        return handle_get_downstream(ids)

    @app.get("/api/graph/bottlenecks")
    def get_bottlenecks():
        return handle_get_bottlenecks()

    @app.get("/api/graph/path")
    def get_shortest_path(start: str, end: str):
        res = handle_get_shortest_path(start, end)
        if "error" in res:
            raise HTTPException(status_code=404, detail=res["error"])
        return res

    @app.get("/api/neo4j/status")
    def get_neo4j_status():
        return handle_get_neo4j_status()

    @app.post("/api/nlp/analyze")
    def analyze_news(payload: NewsAnalysisRequest):
        return handle_analyze_news(payload.text)

    @app.get("/api/nlp/samples")
    def get_news_samples():
        return handle_get_news_samples()

    @app.post("/api/predict/ripple")
    def predict_ripple(payload: RipplePredictionRequest):
        return handle_predict_ripple(
            disrupted_nodes=payload.disrupted_nodes,
            severity=payload.severity,
            initial_delay=payload.initial_delay,
            damping_factor=payload.damping_factor
        )

    @app.get("/api/predict/metrics")
    def get_metrics():
        return handle_get_metrics()

    @app.post("/api/simulate/what-if")
    def simulate_what_if(payload: WhatIfRequest):
        return handle_simulate_what_if(
            disrupted_node_id=payload.disrupted_node_id,
            disruption_duration_days=payload.disruption_duration_days,
            mitigation_strategy=payload.mitigation_strategy,
            buffer_increase_days=payload.buffer_increase_days
        )

    # Static UI Mount
    if os.path.exists(STATIC_DIR):
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

        @app.get("/")
        def serve_index():
            index_path = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(index_path):
                return FileResponse(index_path)
            return {"message": "AtmoGraph API is running. Build static UI or access /docs"}
else:
    app = None
