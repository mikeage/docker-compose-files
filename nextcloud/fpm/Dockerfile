FROM nextcloud:33.0.5-fpm@sha256:636f94b54ca1c57ed11e7e36fbdf209088739bf262eb2b5307cdb18eba09ad3f
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
