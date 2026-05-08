FROM nextcloud:33.0.3-fpm@sha256:6e0f011432d56c80fc2ccea8deeb47bd276431bb1209a626ddfc67650c801883
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
