import json
import os
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def _write_json(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        now = datetime.now(UTC).isoformat()

        if self.path in ("/", "/health", "/ready"):
            self._write_json(
                200,
                {
                    "status": "ok",
                    "service": "ci-test-app",
                    "path": self.path,
                    "timestamp": now,
                },
            )
            return

        self._write_json(
            404,
            {
                "status": "not_found",
                "path": self.path,
                "timestamp": now,
            },
        )

    def log_message(self, format: str, *args) -> None:
        return


def run() -> None:
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"ci-test-app listening on {port}")
    server.serve_forever()
