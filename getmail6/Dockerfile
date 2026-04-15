FROM debian:stable-slim@sha256:e51bfcd2226c480a5416730e0fa2c40df28b0da5ff562fc465202feeef2f1116

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates getmail6 swaks bash \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 getmail || true && useradd  -m -u 1000 -g 1000 -s /bin/bash getmail || true

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER getmail
ENTRYPOINT ["/entrypoint.sh"]
