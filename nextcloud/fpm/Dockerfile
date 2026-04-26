FROM nextcloud:33.0.2-fpm@sha256:349f8d1ddf04e15fd4e854a094899511f4e1b05b8b0187d1f7173a7c41fac7cf
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
