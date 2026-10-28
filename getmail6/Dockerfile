FROM debian:stable-slim@sha256:9e3624ad785d0d322f0c69194c2c0ebba7bc5fda3e2c6523ac095b4f08a12ba7

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates getmail6 swaks bash \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 getmail || true && useradd  -m -u 1000 -g 1000 -s /bin/bash getmail || true

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER getmail
ENTRYPOINT ["/entrypoint.sh"]
