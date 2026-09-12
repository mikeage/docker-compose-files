FROM nextcloud:34.0.4-fpm@sha256:2ae7986bcf7f0014c4a4d143e18cd504c1d9513a8739604c9e4eeab86bbd64bf
# RUN apt-get update && \
# 	apt-get install -y ffmpeg && \
# 	apt-get clean && \
# 	rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
	apt-get install -y procps && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY zzz-www-custom.conf /usr/local/etc/php-fpm.d/zzz-www-custom.conf
