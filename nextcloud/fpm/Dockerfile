FROM nextcloud:33.0.5-fpm@sha256:711b3fb718cd1fc205eb49afa712beed297191fa5506b05ac7d18f68a79102e4
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
