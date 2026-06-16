FROM nextcloud:34.0.0-fpm@sha256:043ad29d7423bc750c3bff8210413d8ca591f971c98680ee1edd1367b950cc49
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
