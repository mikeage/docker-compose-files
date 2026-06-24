FROM nextcloud:34.0.0-fpm@sha256:9a7d2012563290fe621080d412ef31ddfef28f7b1072b4e4a439d7115186f6e6
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
