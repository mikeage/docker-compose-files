FROM nextcloud:34.0.3-fpm@sha256:3f37d1d829c6fbb2a2d0fc1f1b849f9caa01a5c97be412150ebc984571667815
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
