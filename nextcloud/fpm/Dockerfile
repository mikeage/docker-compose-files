FROM nextcloud:34.0.0-fpm@sha256:7ba76e0d89f6b70984bbf97590b3785bd32be488351d80fe780ca9b5262d97cc
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
