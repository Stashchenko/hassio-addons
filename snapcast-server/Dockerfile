ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.0

FROM $BUILD_FROM

RUN \
    apk add --no-cache \
        avahi \
        avahi-compat-libdns_sd \
        dbus \
        dbus-libs \
        nss \
        pulseaudio \
        alsa-plugins-pulse \
        alsa-lib \
        curl \
        unzip \
    \
    && apk add --no-cache \
        snapcast \
        --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main \
        --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
    \
    && mkdir -p /usr/share/snapserver/snapweb \
    && curl -J -L https://github.com/badaix/snapweb/releases/download/v0.9.3/snapweb.zip -o /tmp/snapweb.zip \
    && unzip -o /tmp/snapweb.zip -d /usr/share/snapserver/snapweb \
    && rm /tmp/snapweb.zip \
    && rm -fr /tmp/*

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
