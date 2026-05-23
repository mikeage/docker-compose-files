FROM nextcloud:33.0.3-fpm@sha256:f19148bd5c7f3a59b1dd848b8a70cd613640251d5e322964fa0c3356249cece2
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
