FROM alpine:3.9
LABEL maintainer "laaksonen.heikki.j@gmail.com"

ARG SNIPPY_SERVER_HOST

ENV SNIPPY_USER=snippy
ENV SNIPPY_HOME="/home/${SNIPPY_USER}"
ENV SNIPPY_GID=61999
ENV SNIPPY_UID=61999
ENV SNIPPY_LOG_JSON 1
ENV SNIPPY_PYTHON=python3.6
ENV SNIPPY_SERVER_IP=0.0.0.0
ENV SNIPPY_SERVER_PORT=9090
ENV SNIPPY_SERVER_HOST=${SNIPPY_SERVER_HOST:-${SNIPPY_SERVER_IP}:${SNIPPY_SERVER_PORT}}

ENV LANG C.UTF-8
ENV PYTHONUSERBASE=${SNIPPY_HOME}/.local
ENV PATH="${PATH}":"${PYTHONUSERBASE}/bin"

WORKDIR "${SNIPPY_HOME}"
COPY snippy/ snippy/
COPY setup.py .
COPY LICENSE .
COPY README.rst .

RUN addgroup --gid ${SNIPPY_GID} "${SNIPPY_USER}" && \
    adduser \
        --disabled-password \
        --gecos "" \
        --ingroup "${SNIPPY_USER}" \
        --uid ${SNIPPY_UID} \
        --shell /bin/false \
        --home "${SNIPPY_HOME}" \
        "${SNIPPY_USER}" && \
    find / -perm +6000 -type f -exec chmod a-s {} \; || true && \
    apk add \
        python3 \
        py3-psycopg2 && \
    python3 -m pip install --upgrade pip setuptools && \
    find /usr/lib/python* -type d -name __pycache__ -exec rm -r {} \+ && \
    pip3 install --user .[docker] && \
    find ${SNIPPY_HOME}* -type d -name __pycache__ -exec rm -r {} \+ && \
    snippy import --defaults --all -q --server-host "" && \
    chown -R snippy:snippy /home/snippy/ && \
    chmod -R 700 /home/snippy/ && \
    python3 -m pip uninstall pip --yes && \
    apk del apk-tools && \
    rm -rf /home/snippy/.cache && \
    rm -rf /home/snippy/setup.py && \
    rm -rf /home/snippy/snippy && \
    rm -rf /usr/lib/"${SNIPPY_PYTHON}"/site-packages/psycopg2/tests && \
    rm -rf /etc/apk/ && \
    rm -rf /lib/apk/ && \
    rm -rf /root/.cache && \
    rm -rf /usr/lib/"${SNIPPY_PYTHON}"/distutils/ && \
    rm -rf /usr/share/apk/ && \
    rm -rf /var/cache/apk/

HEALTHCHECK --interval=10s --timeout=5s CMD nc -zv ${SNIPPY_SERVER_IP} ${SNIPPY_SERVER_PORT} || exit 1

EXPOSE ${SNIPPY_SERVER_PORT}

USER ${SNIPPY_USER}

ENTRYPOINT ["snippy"]
CMD ["--help"]
