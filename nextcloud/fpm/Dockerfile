FROM nextcloud:34.0.1-fpm@sha256:4afbc1e6a1dfb6e7235fc5f5352a8a1a17c2a0670a6f0ec4ba20386dcfcfe2d2
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
