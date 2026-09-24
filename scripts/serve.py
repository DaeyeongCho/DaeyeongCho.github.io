#!/usr/bin/env python3
"""Local static preview, including GitHub Pages-style custom 404 responses."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'index.html', '404.html', 'styles.css', 'favicon.ico', 'robots.txt', 'sitemap.xml', 'assets', 'work', 'publications'}


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parts = Path(unquote(urlsplit(self.path).path)).parts[1:]
        if '..' in parts or (parts and parts[0] not in ALLOWED):
            self.send_error(404)
            return
        super().do_GET()

    def list_directory(self, path):
        self.send_error(404)

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            body = (ROOT / '404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)
        else:
            super().send_error(code, message, explain)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(ROOT)))
    print(f'Preview: http://127.0.0.1:{args.port}', flush=True)
    server.serve_forever()
