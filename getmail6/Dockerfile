FROM debian:stable-slim@sha256:fbfb4059d2127120aa05b6e6064523d2102552f0cf0026ddf0701c12f1f8f3e0

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates getmail6 swaks bash \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 getmail || true && useradd  -m -u 1000 -g 1000 -s /bin/bash getmail || true

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER getmail
ENTRYPOINT ["/entrypoint.sh"]
