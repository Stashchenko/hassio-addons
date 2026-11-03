ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.0

FROM $BUILD_FROM

RUN \
    apk add --no-cache \
        avahi=0.9_rc4-r0 \
        avahi-compat-libdns_sd=0.9_rc4-r0 \
        dbus=1.16.2-r2 \
        dbus-libs=1.16.2-r2 \
        nss=3.124-r0 \
        pulseaudio=17.0-r7 \
        pulseaudio-utils=17.0-r7 \
        alsa-plugins-pulse=1.2.12-r2 \
        alsa-lib=1.2.15.3-r0 \
        python3=3.14.10-r1 \
        py3-flask=3.1.3-r2 \
        py3-waitress=3.0.2-r2 \
        curl=8.20.0-r1 \
        unzip=6.0-r16 \
    && apk add --no-cache \
        snapcast=0.35.0-r1 \
        caps=0.9.26-r0 \
        --repository=https://dl-cdn.alpinelinux.org/alpine/edge/main \
        --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community \
    && mkdir -p /usr/share/snapserver/snapweb \
    && curl -J -L https://github.com/badaix/snapweb/releases/download/v0.9.3/snapweb.zip -o /tmp/snapweb.zip \
    && unzip -o /tmp/snapweb.zip -d /usr/share/snapserver/snapweb \
    && rm /tmp/snapweb.zip \
    && rm -f \
        /etc/avahi/services/ssh.service \
        /etc/avahi/services/sftp-ssh.service \
    && rm -rf /tmp/*

COPY rootfs /

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="stashchenko" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Stashchenko's HA Apps" \
    org.opencontainers.image.authors="stashchenko" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
