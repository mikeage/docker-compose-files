FROM nextcloud:33.0.3-fpm@sha256:891d1a4f6369dfc5a609a1d8776105b9f1a67d6e3346bcb49034e5136bbc3ca8
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
