FROM nextcloud:33.0.5-fpm@sha256:aa5eaa9f7ccdfb5bb8f14378ef3e75e60cd3255bf161f5ab398c67b588fb4927
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
