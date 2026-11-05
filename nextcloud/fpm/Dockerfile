FROM nextcloud:35.0.2-fpm@sha256:8fcc3b92ce27964a5c8c5f464620a0c92114b95d4ca4b97b9b4c24d2c4a55881
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
