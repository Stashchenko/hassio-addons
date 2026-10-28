ARG BUILD_FROM
FROM $BUILD_FROM

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV LANG=C.UTF-8

RUN apk update && \
    apk add --no-cache \
        iw \
        hostapd \
        networkmanager \
        networkmanager-cli \
        net-tools \
        sudo \
        dnsmasq \
        iptables \
        python3 \
        py3-flask \
        py3-waitress \
        py3-humanize && \
    apk add --no-cache --virtual .build-deps gcc make musl-dev git && \
    git clone https://github.com/geekman/mdns-repeater.git /tmp/mdns-repeater && \
    cd /tmp/mdns-repeater && \
    make && \
    cp mdns-repeater /usr/bin/ && \
    cd / && \
    rm -rf /tmp/mdns-repeater && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*

COPY hostapd.conf /
COPY dnsmasq.conf /

# Copy web files
COPY web/ /web/

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
