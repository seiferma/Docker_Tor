FROM alpine:3.23

ARG TOR_VERSION=

RUN apk add --no-cache tor=${TOR_VERSION} su-exec curl
COPY ./overlay/ /

ENTRYPOINT ["/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=60s --start-period=15s --retries=3 CMD /usr/bin/curl --socks5-hostname 127.0.0.1:9050 http://google.com/generate_204 || exit 1
CMD ["-f", "/etc/tor/torrc"]
