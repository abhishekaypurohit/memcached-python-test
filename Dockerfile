FROM alpine:3.7

COPY init.sh /init.sh
RUN apk --no-cache add memcached && chmod +x /init.sh

USER memcached
CMD ["/init.sh"]
