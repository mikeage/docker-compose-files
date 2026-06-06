FROM nextcloud:33.0.5-fpm@sha256:71e95c52e19afb32f1b8d533673e2e46c1d8a9f14b94fd44188c2cf3016d76de
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
