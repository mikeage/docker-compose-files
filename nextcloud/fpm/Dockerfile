FROM nextcloud:34.0.0-fpm@sha256:8b1e72bfa92deda9baa5fb0b4e9aade17a240a49902a3e442880edff29e735be
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
