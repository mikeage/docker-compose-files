FROM nextcloud:35.0.1-fpm@sha256:99758608767ddd6f6679786daa10f2ba1e234e8329e2ea265da69cf36beadd2b
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
