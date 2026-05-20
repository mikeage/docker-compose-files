FROM nextcloud:33.0.3-fpm@sha256:7c652adc6ba39e534c075f54e7c5a624c1f660442c7b251f9295eacd838ef620
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
