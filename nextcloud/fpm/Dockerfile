FROM nextcloud:34.0.3-fpm@sha256:3a631e1a48aaf0191b047460b95a10d5a4baf02982a21ab2f23f5c5134b7d75e
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
