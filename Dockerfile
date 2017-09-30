FROM alpine:3.6
LABEL maintainer "laaksonen.heikki.j@gmail.com"

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install PyYAML && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache

WORKDIR /usr/local/snippy
COPY snippy/ snippy/
COPY setup.py .
COPY LICENSE .
RUN pip3 install .
RUN snippy import --snippet -f defaults
RUN snippy import --solution -f defaults

ENTRYPOINT ["snippy"]
CMD ["--help"]
