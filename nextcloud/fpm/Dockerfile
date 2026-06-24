FROM nextcloud:34.0.0-fpm@sha256:69667be13bf65882110f60d6c5b20dc0fa91e44b95c0075bf72ecc45a30cfc4a
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
