FROM nextcloud:33.0.5-fpm@sha256:bd547cf969cd4b6e34523ddeb468766b67cc06bc20cc0c23c2631e85487ca7f1
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
