FROM ghcr.io/astral-sh/uv:python3.12-alpine@sha256:f672ffce65d48a2c8b3079d9f0479856f3a70d08ab09f89d56f56f4f6d7cfe5a

WORKDIR /app
COPY metrics_exporter.py /app/metrics_exporter.py

ENV PORT=9105
ENV PROC_PATH=/host/proc
ENV SAMPLE_WINDOW=0.25

EXPOSE 9105

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD wget -q -O /dev/null "http://127.0.0.1:${PORT}/health" || exit 1

CMD ["uv", "run", "--no-project", "/app/metrics_exporter.py"]
