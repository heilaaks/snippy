FROM alpine:3.8
LABEL maintainer "laaksonen.heikki.j@gmail.com"

ENV LANG C.UTF-8

WORKDIR /usr/local/snippy
COPY snippy/ snippy/
COPY setup.py .
COPY LICENSE .
COPY README.rst .

RUN addgroup -g 1000 snippy && adduser -G snippy -D -H snippy

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install . && \
    pip3 install -e .[server] && \
    find /usr/lib/python* -type d -name __pycache__ -exec rm -r {} \+ && \
    snippy import --snippet --defaults -q && \
    snippy import --solution --defaults -q && \
    pip3 uninstall pip --yes && \
    rm -rf /root/.cache

RUN chown -R snippy:root .

USER snippy

ENTRYPOINT ["snippy"]
CMD ["--help"]
