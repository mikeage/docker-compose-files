FROM nextcloud:33.0.3-fpm@sha256:36226b305613cdde76ee8da89a66e8a8b4fb4ef4b673bdb7b9a9d25efa14e047
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
