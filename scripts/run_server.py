"""
AtmoGraph Universal Server Launcher
Automatically boots FastAPI / Uvicorn if installed, or falls back to standard Python
HTTP server handling identical REST API endpoints and serving the visual dashboard.
"""

import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
sys.path.append(BACKEND_DIR)

from app.config import HOST, PORT, STATIC_DIR
from app.api.routes_graph import (
    handle_get_graph, handle_get_node, handle_get_downstream,
    handle_get_bottlenecks, handle_get_shortest_path, handle_get_neo4j_status
)
from app.api.routes_nlp import handle_analyze_news, handle_get_news_samples
from app.api.routes_predict import handle_predict_ripple, handle_get_metrics
from app.api.routes_simulation import handle_simulate_what_if


class AtmoGraphRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Static files & Dashboard
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            index_file = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(index_file):
                with open(index_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>AtmoGraph Backend Running</h1><p>Static index.html not found.</p>")
            return

        if path.startswith("/static/"):
            rel_path = path[len("/static/"):]
            full_path = os.path.join(STATIC_DIR, rel_path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                self.send_response(200)
                if full_path.endswith(".css"):
                    self.send_header("Content-Type", "text/css")
                elif full_path.endswith(".js"):
                    self.send_header("Content-Type", "application/javascript")
                self.end_headers()
                with open(full_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # REST API Routes
        response_data = None

        if path == "/api/graph":
            response_data = handle_get_graph()
        elif path.startswith("/api/graph/node/"):
            node_id = path.split("/api/graph/node/")[1]
            response_data = handle_get_node(node_id)
        elif path == "/api/graph/downstream":
            node_ids = query.get("node_ids", [""])[0].split(",")
            response_data = handle_get_downstream(node_ids)
        elif path == "/api/graph/bottlenecks":
            response_data = handle_get_bottlenecks()
        elif path == "/api/graph/path":
            start = query.get("start", [""])[0]
            end = query.get("end", [""])[0]
            response_data = handle_get_shortest_path(start, end)
        elif path == "/api/neo4j/status":
            response_data = handle_get_neo4j_status()
        elif path == "/api/nlp/samples":
            response_data = handle_get_news_samples()
        elif path == "/api/predict/metrics":
            response_data = handle_get_metrics()

        if response_data is not None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length).decode("utf-8")
        payload = {}
        if post_body:
            try:
                payload = json.loads(post_body)
            except Exception:
                payload = {}

        response_data = None

        if path == "/api/nlp/analyze":
            text = payload.get("text", "")
            response_data = handle_analyze_news(text)
        elif path == "/api/predict/ripple":
            nodes = payload.get("disrupted_nodes", [])
            sev = float(payload.get("severity", 0.85))
            delay = int(payload.get("initial_delay", 21))
            damping = float(payload.get("damping_factor", 0.82))
            response_data = handle_predict_ripple(nodes, sev, delay, damping)
        elif path == "/api/simulate/what-if":
            nid = payload.get("disrupted_node_id", "")
            duration = int(payload.get("disruption_duration_days", 21))
            strat = payload.get("mitigation_strategy", "none")
            buffer_inc = int(payload.get("buffer_increase_days", 10))
            response_data = handle_simulate_what_if(nid, duration, strat, buffer_inc)

        if response_data is not None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": f"Endpoint {path} not found"}).encode("utf-8"))


def run():
    try:
        import uvicorn
        print("Uvicorn detected! Launching high-performance FastAPI server...")
        uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True, app_dir=BACKEND_DIR)
    except ImportError:
        print("=" * 65)
        print("  AtmoGraph: Supply Chain Ripple Effect Predictor")
        print("  Running with Built-In HTTP Server (No external dependencies)")
        print(f"  Interactive Dashboard: http://localhost:{PORT}")
        print(f"  API Endpoint:          http://localhost:{PORT}/api/graph")
        print("=" * 65)
        server = HTTPServer((HOST, PORT), AtmoGraphRequestHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down AtmoGraph server...")
            server.server_close()


if __name__ == "__main__":
    run()
