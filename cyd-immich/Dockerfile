FROM ghcr.io/astral-sh/uv:python3.15-trixie-slim@sha256:980d6aa868431fd4ef2b32481e934ef5ee3b662c5decade3aa2d7e7ffb8075e4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock
COPY src /app/src

RUN uv sync --locked --no-dev

CMD ["uv", "run", "uvicorn", "cyd_immich_proxy.main:app", "--host", "0.0.0.0", "--port", "8080"]
