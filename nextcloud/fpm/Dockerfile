FROM nextcloud:34.0.4-fpm@sha256:7fb41a27be12a2cd91c8a16e4c3908d18fa04b7cd58a24c371e5ec64561aebd3
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
