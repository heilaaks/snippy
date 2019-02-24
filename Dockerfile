FROM alpine:3.9 as base
LABEL maintainer "laaksonen.heikki.j@gmail.com"

ENV LANG C.UTF-8
ENV SNIPPY_LOG_JSON 1

WORKDIR /usr/local/snippy
COPY snippy/ snippy/
COPY setup.py .
COPY LICENSE .
COPY README.rst .

RUN addgroup -g 1000 snippy && adduser -G snippy -D -H snippy

RUN apk add python3 && \
    apk add py3-psycopg2 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -e .[docker] && \
    find /usr/lib/python* -type d -name __pycache__ -exec rm -r {} \+ && \
    snippy import --snippet --defaults -q && \
    snippy import --solution --defaults -q && \
    pip3 uninstall pip --yes && \
    apk del apk-tools && \
    rm -rf /etc/apk/ && \
    rm -rf /lib/apk/ && \
    rm -rf /root/.cache && \
    rm -rf /usr/lib/python3.6/distutils/ && \
    rm -rf /usr/share/apk/ && \
    rm -rf /var/cache/apk/

RUN chown -R snippy:root .

USER snippy

ENTRYPOINT ["snippy"]
CMD ["--help"]
