FROM nextcloud:33.0.3-fpm@sha256:d96341058d8026dbe7c97d7f262272bc421efaf88438b2676ea20ce3293af423
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
