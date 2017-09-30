FROM alpine:3.6
LABEL maintainer "laaksonen.heikki.j@gmail.com"

WORKDIR /usr/local/snippy
COPY snippy/ snippy/
COPY setup.py .
COPY LICENSE .

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install PyYAML && \
    pip3 install . && \
    snippy import --snippet -f defaults && \
    snippy import --solution -f defaults && \
    rm -r /root/.cache && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

ENTRYPOINT ["snippy"]
CMD ["--help"]
