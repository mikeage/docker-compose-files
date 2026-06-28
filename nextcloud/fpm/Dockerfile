FROM nextcloud:34.0.0-fpm@sha256:52f7bf89bb308616c8dfd9cbc7f5b26877309a6a553e0664254a7153dcb9c414
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
