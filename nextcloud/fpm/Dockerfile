FROM nextcloud:fpm@sha256:e31c86e7b68e5c6616e5d35c6b025107df4d26720414a51ba5fff925656196d2
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
