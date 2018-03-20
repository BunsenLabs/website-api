FROM alpine:latest
RUN apk add --update python3
RUN pip3 install --no-cache-dir blwwwapi
EXPOSE 10000
ENTRYPOINT /bin/sh
