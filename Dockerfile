FROM alpine:3.8 as base
LABEL maintainer "laaksonen.heikki.j@gmail.com"

FROM base as builder

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev && \
    pip3 install --no-cache-dir psycopg2 && \
    find /usr/lib/python* -type d -name __pycache__ -exec rm -r {} \+ &&  \
    rm -Rf /usr/lib/python3.6/site-packages/psycopg2/tests/ && \
    apk del --no-cache .build-deps

FROM base
WORKDIR /usr/lib/python3.6/site-packages/
COPY --from=builder /usr/lib/python3.6/site-packages/psycopg2 ./psycopg2
COPY --from=builder /usr/lib/python3.6/site-packages/psycopg2-2.7.7-py3.6.egg-info ./psycopg2_binary-2.7.7-py3.6.egg-info

ENV LANG C.UTF-8

WORKDIR /usr/local/snippy
COPY snippy/ snippy/
COPY setup.py .
COPY LICENSE .
COPY README.rst .

RUN addgroup -g 1000 snippy && adduser -G snippy -D -H snippy

RUN apk add --no-cache python3 && \
    apk add --no-cache libpq && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install . && \
    pip3 install -e .[server] && \
    find /usr/lib/python* -type d -name __pycache__ -exec rm -r {} \+ && \
    snippy import --snippet --defaults -q && \
    snippy import --solution --defaults -q && \
    pip3 uninstall pip --yes && \
    apk del apk-tools && \
    rm -rf /etc/apk/ && \
    rm -rf /lib/apk/ && \
    rm -rf /usr/share/apk/ && \
    rm -rf /var/cache/apk/ && \
    rm -rf /root/.cache

RUN chown -R snippy:root .

USER snippy

ENTRYPOINT ["snippy"]
CMD ["--help"]
