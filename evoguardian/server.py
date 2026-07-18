import http.server
import socketserver
import json
import os
import urllib.parse
from agent import ScamGuardianAgent, EvoSkillOptimizer, DEFAULT_PROMPT, DATASET

PORT = 8000

# Keep global states for simulation simplicity
optimizer = EvoSkillOptimizer()
current_iteration = 0

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow CORS for easy debugging if necessary
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        global optimizer, current_iteration
        
        parsed_url = urllib.parse.urlparse(self.path)
        
        if parsed_url.path == "/api/analyze":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            text = data.get("text", "")
            agent = ScamGuardianAgent(optimizer.current_config)
            result = agent.analyze(text)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            return

        elif parsed_url.path == "/api/evolve":
            current_iteration += 1
            step_result = optimizer.run_evolution_step(current_iteration)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(step_result).encode('utf-8'))
            return

        elif parsed_url.path == "/api/reset":
            optimizer = EvoSkillOptimizer()
            current_iteration = 0
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "config": DEFAULT_PROMPT,
                "accuracy": 0.375 # initial dataset accuracy (3/8 correct on default rules)
            }).encode('utf-8'))
            return
            
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        
        # Serve API GET status info
        if parsed_url.path == "/api/status":
            agent = ScamGuardianAgent(optimizer.current_config)
            acc, failures = optimizer.evaluate(optimizer.current_config)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status_data = {
                "config": optimizer.current_config,
                "iteration": current_iteration,
                "accuracy": acc,
                "failures_count": len(failures),
                "dataset": DATASET
            }
            self.wfile.write(json.dumps(status_data).encode('utf-8'))
            return
            
        # Serve static files locally
        # Fallback to serving index.html if request is root
        if parsed_url.path == "/" or parsed_url.path == "":
            self.path = "/index.html"
            
        # Ensure we are serving files from the evoguardian directory
        super().do_GET()

# Change working directory to the evoguardian folder to serve files correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"EvoGuardian server running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
