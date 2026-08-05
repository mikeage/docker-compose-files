FROM nextcloud:34.0.2-fpm@sha256:9bbae8efae3ee63c743951326d2e1dbde92e4cd35e4e9ad2ad48b8a2b8e5504b
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
