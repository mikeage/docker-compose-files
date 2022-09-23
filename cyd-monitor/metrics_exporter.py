#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""Tiny HTTP exporter for CPU usage and load average."""

import http.server
import json
import os
import socketserver
import time
from dataclasses import dataclass
from typing import Final

HOST: Final = "0.0.0.0"
PORT: Final = int(os.environ.get("PORT", "9105"))
PROC_PATH: Final = os.environ.get("PROC_PATH", "/proc")
SAMPLE_WINDOW: Final = float(os.environ.get("SAMPLE_WINDOW", "0.25"))


@dataclass(frozen=True)
class Snapshot:
    cpu_percent: float
    load1: float
    load5: float
    load15: float
    load_percent: float
    cpu_cores: int


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().strip()


def _read_cpu_totals() -> tuple[int, int]:
    stat = _read_file(f"{PROC_PATH}/stat").splitlines()[0]
    parts = stat.split()[1:]
    values = [int(value) for value in parts]
    idle = values[3] + values[4]
    total = sum(values)
    return total, idle


def _read_load() -> tuple[float, float, float]:
    first_three = _read_file(f"{PROC_PATH}/loadavg").split()[:3]
    return float(first_three[0]), float(first_three[1]), float(first_three[2])


def _read_cpu_cores() -> int:
    cores = 0
    for line in _read_file(f"{PROC_PATH}/stat").splitlines():
        name = line.split(maxsplit=1)[0]
        if name.startswith("cpu") and name[3:].isdigit():
            cores += 1
    return max(1, cores)


def collect_snapshot() -> Snapshot:
    total_1, idle_1 = _read_cpu_totals()
    time.sleep(SAMPLE_WINDOW)
    total_2, idle_2 = _read_cpu_totals()

    total_delta = max(1, total_2 - total_1)
    idle_delta = max(0, idle_2 - idle_1)
    cpu_percent = (total_delta - idle_delta) * 100.0 / total_delta

    load1, load5, load15 = _read_load()
    cpu_cores = _read_cpu_cores()
    load_percent = (load1 / cpu_cores) * 100.0

    return Snapshot(
        cpu_percent=round(cpu_percent, 2),
        load1=round(load1, 2),
        load5=round(load5, 2),
        load15=round(load15, 2),
        load_percent=round(load_percent, 2),
        cpu_cores=cpu_cores,
    )


class MetricsHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        # Keep container logs clean. Errors still show from exceptions.
        return

    def _send_text(self, body: str, status: int = 200) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_json(self, payload: dict[str, object], status: int = 200) -> None:
        body = json.dumps(payload, separators=(",", ":"))
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]

        if path == "/health":
            self._send_text("ok\n")
            return

        if path in ("/snapshot", "/metrics", "/metrics.json"):
            snap = collect_snapshot()

            if path == "/snapshot":
                # Compact format for ESPHome parsing: cpu_percent,load1,load_percent
                self._send_text(
                    f"{snap.cpu_percent:.2f},{snap.load1:.2f},{snap.load_percent:.2f}\n"
                )
                return

            if path == "/metrics":
                self._send_text(
                    "\n".join(
                        [
                            "# TYPE host_cpu_usage_percent gauge",
                            f"host_cpu_usage_percent {snap.cpu_percent:.2f}",
                            "# TYPE host_load_1 gauge",
                            f"host_load_1 {snap.load1:.2f}",
                            "# TYPE host_load_5 gauge",
                            f"host_load_5 {snap.load5:.2f}",
                            "# TYPE host_load_15 gauge",
                            f"host_load_15 {snap.load15:.2f}",
                            "# TYPE host_load_percent gauge",
                            f"host_load_percent {snap.load_percent:.2f}",
                            "# TYPE host_cpu_cores gauge",
                            f"host_cpu_cores {snap.cpu_cores}",
                            "",
                        ]
                    )
                )
                return

            self._send_json(
                {
                    "cpu_percent": snap.cpu_percent,
                    "load1": snap.load1,
                    "load5": snap.load5,
                    "load15": snap.load15,
                    "load_percent": snap.load_percent,
                    "cpu_cores": snap.cpu_cores,
                }
            )
            return

        self._send_text("not found\n", status=404)


def main() -> None:
    with socketserver.ThreadingTCPServer((HOST, PORT), MetricsHandler) as server:
        server.allow_reuse_address = True
        print(
            f"metrics_exporter listening on http://{HOST}:{PORT} "
            f"(proc={PROC_PATH}, sample_window={SAMPLE_WINDOW}s)",
            flush=True,
        )
        server.serve_forever()


if __name__ == "__main__":
    main()
