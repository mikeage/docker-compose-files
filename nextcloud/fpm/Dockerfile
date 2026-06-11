FROM nextcloud:34.0.0-fpm@sha256:de81fba189d07038f3c4fda16ddf7e8581d87ca2674d7832a742e12d7dc57a19
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
