FROM nextcloud:fpm@sha256:4d6015c7ddd537522abbdb9ee6b10c0a6b667bfbe5d4a16ed0e58a3c4f844017
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
