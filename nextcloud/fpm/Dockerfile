FROM nextcloud:34.0.1-fpm@sha256:4eb70728fafd09d1c192c940adb50495bd7ba47bbb807cc8970e4851b551dfd8
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
