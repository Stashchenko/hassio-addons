import http.server
import os
import socketserver

PORT = int(os.environ.get("WEB_PORT", 8080))
LEASES_FILE = "/var/lib/misc/dnsmasq.leases"

# It will find it locally during Mac testing, or at /web/index.html in the container
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "index.html")
if not os.path.exists(HTML_FILE):
    HTML_FILE = "/web/index.html"


class LeaseHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        try:
            with open(HTML_FILE, "r") as f:
                html_template = f.read()
        except Exception:
            html_template = "<html><body><h2>Error loading template</h2></body></html>"

        rows = ""
        if os.path.exists(LEASES_FILE):
            try:
                with open(LEASES_FILE, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 4:
                            ip = parts[2]
                            mac = parts[1]
                            hostname = parts[3]
                            rows += f"<tr><td><span class='badge'>{ip}</span></td><td><code>{mac}</code></td><td>{hostname}</td></tr>"
            except Exception:
                pass

        if not rows:
            rows = "<tr><td colspan='3' style='text-align: center; color: #94a3b8;'>No active clients connected.</td></tr>"

        final_html = html_template.replace("{{CLIENT_ROWS}}", rows)
        self.wfile.write(final_html.encode("utf-8"))

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        allow_reuse_address = True


    server = ThreadingHTTPServer(("", PORT), LeaseHandler)
    try:
        print(f"Starting Status Web Server on port {PORT}...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Status Web Server...")
        server.server_close()

    print(f"Starting Status Web Server on port {PORT}...")
