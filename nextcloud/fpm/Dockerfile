FROM nextcloud:33.0.3-fpm@sha256:caa5445f10d29ea525073611928c681932432c8b6b03b63a4340ef20e57976ed
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
