FROM nextcloud:fpm@sha256:8df4667df5c71edfd3ac7fda2eedd5963a5811ad7b02c63f106a5de99cad2628
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
