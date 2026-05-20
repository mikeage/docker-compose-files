FROM debian:stable-slim@sha256:5012d0517aa0075a7150a45aae67586641e898913b7af3b08228108565b5f90c

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates getmail6 swaks bash \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 getmail || true && useradd  -m -u 1000 -g 1000 -s /bin/bash getmail || true

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER getmail
ENTRYPOINT ["/entrypoint.sh"]
