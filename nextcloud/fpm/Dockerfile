FROM nextcloud:35.0.2-fpm@sha256:2556e045d57fff50d2b50ddd160d2d0730e6d5b6f71c33b903d491baa8444f03
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
