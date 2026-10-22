FROM nextcloud:35.0.2-fpm@sha256:7c27d9b6df1413e07c94fd7ab11333cf7c4e7d5a544b1d2ec4963587df0f6da7
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
