FROM nextcloud:33.0.3-fpm@sha256:e4df8f7f83ecdf477cd4a8ae9cdd857f975fef6ca47ce896296f7aef18263d37
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
