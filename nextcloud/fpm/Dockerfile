FROM nextcloud:34.0.1-fpm@sha256:6ef5e9ce28e1d77a793698a5c08c7c6df8d7d177071c0289eb916586dc47db48
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
