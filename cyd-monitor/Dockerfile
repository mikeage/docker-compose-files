FROM ghcr.io/astral-sh/uv:python3.12-alpine@sha256:714d6668cb2bcf6567d8e6f4bc3afbec15a3edfb811adea37650f8a197f3625d

WORKDIR /app
COPY metrics_exporter.py /app/metrics_exporter.py

ENV PORT=9105
ENV PROC_PATH=/host/proc
ENV SAMPLE_WINDOW=0.25

EXPOSE 9105

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD wget -q -O /dev/null "http://127.0.0.1:${PORT}/health" || exit 1

CMD ["uv", "run", "--no-project", "/app/metrics_exporter.py"]
