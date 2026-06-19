FROM ghcr.io/astral-sh/uv:python3.12-alpine@sha256:af42a377a30c429320016ce58aaa017cb8f3b2e67999d63b8a39a0cb8d25402d

WORKDIR /app
COPY metrics_exporter.py /app/metrics_exporter.py

ENV PORT=9105
ENV PROC_PATH=/host/proc
ENV SAMPLE_WINDOW=0.25

EXPOSE 9105

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD wget -q -O /dev/null "http://127.0.0.1:${PORT}/health" || exit 1

CMD ["uv", "run", "--no-project", "/app/metrics_exporter.py"]
