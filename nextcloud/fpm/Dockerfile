FROM nextcloud:35.0.1-fpm@sha256:1a334f3b53abc80505deb4fd28397aae5b0f479abb483b1ba47cc2fdc6d49a5c
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
