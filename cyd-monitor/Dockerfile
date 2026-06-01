FROM ghcr.io/astral-sh/uv:python3.12-alpine@sha256:a5d58d45d45f1e9f7d492e80aee76749df33ff88f3de704e388ab62f5c7b9f50

WORKDIR /app
COPY metrics_exporter.py /app/metrics_exporter.py

ENV PORT=9105
ENV PROC_PATH=/host/proc
ENV SAMPLE_WINDOW=0.25

EXPOSE 9105

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD wget -q -O /dev/null "http://127.0.0.1:${PORT}/health" || exit 1

CMD ["uv", "run", "--no-project", "/app/metrics_exporter.py"]
