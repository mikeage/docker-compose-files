FROM nextcloud:33.0.4-fpm@sha256:a249247a8725d11209226d111d74f1f3222ecd195ab3077d2c849fe81155b766
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
