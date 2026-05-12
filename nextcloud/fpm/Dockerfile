FROM nextcloud:33.0.3-fpm@sha256:6d730635a2d223a75d955b33510dfc84eb7f25a0c737f973a54dea041317ab80
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
