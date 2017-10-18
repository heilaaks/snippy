FROM alpine:3.6
LABEL maintainer "laaksonen.heikki.j@gmail.com"

WORKDIR /usr/local/snippy
COPY snippy/ snippy/
COPY setup.py .
COPY LICENSE .

RUN addgroup -g 1000 snippy && adduser -G snippy -D -H snippy

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install . && \
    snippy import --snippet --defaults -q && \
    snippy import --solution --defaults -q && \
    rm -r /root/.cache

RUN chown -R snippy:root . && \
    chown -R snippy:root /usr/lib/python3.6/site-packages/snippy

USER snippy

ENTRYPOINT ["snippy"]
CMD ["--help"]
