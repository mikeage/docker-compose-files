FROM debian:stable-slim@sha256:04634311a8d5fc442b6eb06d792293c4f3e2268652ca7634e00ce8ef5cc0a28a

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates getmail6 swaks bash \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 getmail || true && useradd  -m -u 1000 -g 1000 -s /bin/bash getmail || true

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER getmail
ENTRYPOINT ["/entrypoint.sh"]
