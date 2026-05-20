FROM nextcloud:33.0.3-fpm@sha256:7a8b7b16f29d431643a038981f573ec60e2c46e115ebce5527e4320c55604af0
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
