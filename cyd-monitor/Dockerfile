FROM ghcr.io/astral-sh/uv:python3.12-alpine@sha256:f39c313b3dcdec1f8e24d098af69c65e6f6fd5bc3a909bf386d54a7a92e3388e

WORKDIR /app
COPY metrics_exporter.py /app/metrics_exporter.py

ENV PORT=9105
ENV PROC_PATH=/host/proc
ENV SAMPLE_WINDOW=0.25

EXPOSE 9105

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD wget -q -O /dev/null "http://127.0.0.1:${PORT}/health" || exit 1

CMD ["uv", "run", "--no-project", "/app/metrics_exporter.py"]
