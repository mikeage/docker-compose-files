FROM nextcloud:33.0.3-fpm@sha256:b30ac4e9852cf7c5fb4ce3925ec0e50ed8cbe4e84a68cf19658d0b1d5983f83d
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
