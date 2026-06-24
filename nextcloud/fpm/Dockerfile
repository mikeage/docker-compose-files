FROM nextcloud:34.0.0-fpm@sha256:4ec4d895f51b4b029a77370ef22a73b4fff7ada1cc02b35978d036e9e7f60f68
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
