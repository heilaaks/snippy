FROM alpine:3.9
LABEL maintainer "laaksonen.heikki.j@gmail.com"

ENV LANG C.UTF-8
ENV PYTHONUSERBASE=/usr/local/snippy/.local
ENV PATH=/usr/local/snippy/.local/bin:"${PATH}"

ENV SNIPPY_GID=61999
ENV SNIPPY_UID=61999
ENV SNIPPY_LOG_JSON 1
ENV SNIPPY_SERVER_IP=0.0.0.0
ENV SNIPPY_SERVER_PORT=32768
ENV SNIPPY_SERVER_HOST=${SNIPPY_SERVER_IP}:${SNIPPY_SERVER_PORT}

WORKDIR /usr/local/snippy

COPY snippy/ snippy/
COPY setup.py .
COPY LICENSE .
COPY README.rst .

RUN addgroup \
        --gid ${SNIPPY_GID} \
        snippy && \
    adduser \
        --system \
        --disabled-password \
        --no-create-home \
        --shell /bin/false \
        --gecos "" \
        --uid ${SNIPPY_UID} \
        --ingroup snippy \
        noname && \
    apk add \
        python3 \
        py3-psycopg2 && \
    python3 -m pip install --upgrade \
        pip \
        setuptools && \
    python3 -m pip install \
        --user .[docker] && \
    # Clean pycache before installing Snippy. This leaves only the needed cache files.
    find /usr/local/snippy/.local/lib -type d -name __pycache__ -exec rm -r {} \+ && \
    snippy import \
        --defaults \
        --all \
        --server-host "" \
        -q && \
    chown -R noname:root /usr/local/snippy/ && \
    chmod -R g+rwX /usr/local/snippy/ && \
    find /usr/lib/python3.6 -type d -name __pycache__ -exec rm -r {} \+ && \
    find /usr/local/snippy/.local/bin ! -regex '\(.*snippy\|.*gunicorn\)' -type f -exec rm -f {} + && \
    python3 -m pip uninstall pip --yes && \
    apk del apk-tools && \
    rm -rf /etc/apk/ && \
    rm -rf /usr/local/snippy/.cache && \
    rm -rf /usr/local/snippy/setup.py && \
    rm -rf /usr/local/snippy/snippy && \
    rm -rf /lib/apk/ && \
    rm -rf /root/.cache && \
    rm -rf /usr/lib/python3.6/site-packages/psycopg2/tests && \
    rm -rf /usr/lib/python3.6/distutils/ && \
    rm -rf /usr/share/apk/ && \
    rm -rf /var/cache/apk/ && \
    find / -perm +6000 -type f -exec chmod a-s {} \; || true

HEALTHCHECK --interval=10s --timeout=5s CMD nc -zv ${SNIPPY_SERVER_IP} ${SNIPPY_SERVER_PORT} || exit 1

EXPOSE ${SNIPPY_SERVER_PORT}

USER noname

ENTRYPOINT ["snippy"]
CMD ["--help"]

#
# SECURITY HARDENING
#
#   The most critical parts from Snippy container security hardening has
#   to be made in host that runs dockerd daemon and starts the container.
#
#   Note that the author is not a security or Linux specialist. This is
#   just a hobby project. If the explanations here are not correct, it
#   indicates that there can be security problems when running Snippy
#   container image.
#
#
# TARGET GROUP
#
#   Defaults are defined for a casual user who want's to run Snippy with
#   the same UID as in host to mount persistent storage volume without
#   giving additional user permissions for the mount point in host.
#
#
# MINIMUM VERSION
#
#   The minimum Docker version to run these examples is Docker 17.06. The
#   examples use ``--mount`` option that has been available for standalone
#   containers only from Docker 17.06 [1].
#
#
# CONTAINER UID/GID
#
#   By default the Snippy docker image has non-deterministic UID and GID.
#   The non-deterministic values are allocated at image compile time [2].
#
#   A non-deterministic UID and GID are problems only when the container
#   mounts a volume from host. If there is a non-deterministic UID, it is
#   not trivial to give access rights from host to a process runing in
#   container.
#
#   If a host is a multi-tenant runtime environment with many containers,
#   maintaining volume access rights based on non-deterministic UID and
#   GID values is not feasible.
#
#   If container user namespaces feature is activated in host dockerd [3],
#   it is possible to start a container with UID 0 (root). The UID 0 maps
#   to specific UID range in host that does not have root privileges.
#
#   UID ranges are Linux kernel and distribution specific [4] and they can
#   be configured. This means it is not feasible to know from which range
#   to allocate container UID by default.
#
#   For example OpenShift Enterprise runs containers using an arbitrarily
#   assigned user ID [2].
#
#
# USE CASES:
#
#   1. Running container with the same UID as in the host (unsecure)
#
#      This is unsecure because user starting the container may be a root
#      user. If the command example below is run as a root user, it starts
#      the container with almost the same privileges as the root user in
#      host. In this case only some of the Linux security capabilities are
#      removed [6].
#
#      ```shell
#      docker run \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy -vv
#      ```
#
#   2. Running container with UID allocated from host without user namespaces
#
#      In this use case the UID in container directly maps to UID in host.
#      The host UID that runs the container is assumed to be unprivileged
#      non root user that has access rights to specific mount point.
#
#      When UID is set when the container is started, it will override UID
#      defined in container. In this example the UID is 1000 but it can be
#      any UID wich is created in host running the Snippy container.
#
#      ```shell
#      docker run \
#          --user 1000 \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy -vv
#      ```
#
#   3. Running container with UID allocated from host with user namespaces
#
#      In this use case the UID in container does not map to UID in host.
#      This use case assumes that container name user namespaces feature in
#      host dockerd [4] is activated.
#
#      This is the use case suited for multi-tenant environments and running
#      multiple containers.
#
#      In this case the UID is not set from the host dockerd. It is assumed
#      that the container is started with UID 0 (root) in this case.
#
#      ```shell
#      docker run \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy -vv
#      ```
#
#   4. Set IP and port visible in host that runs the container
#
#      The ``--publish`` command line option defines what is the IP and port
#      that is visible in host. In these examples the host IP is configured
#      to 127.0.0.1 and port to 8080.
#
#
# IMPLEMENTATION
#
#   1. Dockerfile layers
#
#      There is only one RUN layer in order to keep the image size roughly
#      at 38MB. For example separating the same into three RUN layers, the
#      image size would be 71MB.
#
#   2. Dockerfile configuration
#
#      There is no need to allow configuration of user and group names.
#      Also the server installation location in container is not relevant
#      for runtime environment. Because of this, there are no environment
#      variables that can be used to configure these options.
#
#      This causes for example the installation location to be set in
#      two different places. But it is considered better than revealing
#      this to user through ARG or ENV variable.
#
#   3. Container UID and GID are not defined by default
#
#      Because of the supported use cases for default tager users and
#      UID values being unpredictable, the container image does not set
#      explicit UID and GID by default.
#
#      From security point of view, the most beneficial security hardening
#      step for a semi-professional use is to define the UID from the host
#      that starts the container with ``--user`` option. If the UID would
#      be hardcoded or set with an environment variable, user would have
#      to recompile the Dockerfile or set a environment variable to unset
#      the default UID in container.
#
#      When the UID of the container is generated by user, the container
#      will not have an associated entry in /etc/passwd. This is not a
#      problem for Snippy server because it does not look it's user ID.
#
#      TODO: This is not quite true. The default cannot be avoided because
#            adduser and addgroups always need the UID and GID? But even
#            when those are set, the ``docker run`` with ``--user`` and
#            without it works?
#
#   4. The container user is created as system user
#
#      Minimal user privileges are created with a system user that does
#      not have home directory. Also user shell is set to /bin/false.
#
#      The Alpine ``adduser`` would set for example the disabled password
#      by default if no arguments are provided or ``-D`` option would be
#      used. The used syntax explicitly documents and quarantees the used
#      values without relying to defaults.
#
#      The ``gecos`` option with empty string value prevents additional
#      information to be added in /etc/password file.
#
#      The host Linux kernel does not care about user name or group name.
#      Only the UID and GID are important. Because of this, adduser ``user``
#      and addgroup ``group`` are hardcoded to ``snippy``. The user and
#      group names must be unique only withing the running container.
#
#      addgroup \
#          --gid ${SNIPPY_GID} \
#          snippy
#
#      adduser \
#          --system
#          --disabled-password \
#          --no-create-home \
#          --shell /bin/false \
#          --gecos "" \
#          --uid ${SNIPPY_UID} \
#          --ingroup snippy \
#          noname
#
#   5. Container user file access privileges
#
#      "For an image to support running as an arbitrary user, directories and
#       files that may be written to by processes in the image should be owned
#       by the root group and be read/writable by that group. Files to be
#       executed should also have group execute permissions." [2]
#
#      "Because the container user is always a member of the root group, the
#       container user can read and write these files. The root group does
#       not have any special permissions (unlike the root user) so there are
#       no security concerns with this arrangement." [2]
#
#      chown -R noname:root /usr/local/snippy/ && \
#      chmod -R g+rwX /usr/local/snippy/
#
#   6. Remove setuid/setgid bit from all binaries (defang)
#
#      There is no need to allow binaries to run with these privileges in
#      container. Because ofthis, the bit is removed from all binaries.
#
#      find / -perm +6000 -type f -exec chmod a-s {} \; || true && \
#
#   7. Container user is operated only with UID and GID
#
#      There is no user name allocated for the container. Only the UID and
#      GID are relevant from security point of view and allocating specific
#      user name for the container can give misleading information about the
#      security hardening.
#
#      Because of this, there is only a fixed noname allocated for the user
#      in container.
#
#      USER noname
#
#   8. Exposed container port can be configured
#
#      The Snippy server in container image binds on port 32768 by default.
#      The server port is exposed in the Dockerfile. The exposed port in the
#      Dockefile serves only two purposes:
#
#        1. Default value for dockerd --publish option.
#        2. Documentation to user about the container bind port.
#
#      The default port is chosen to have different value than 80 or 8080
#      because this clearly separates container port from the host port. The
#      author always have problems to know which was the host port and which
#      the quest port in command examples like ``--publish=8080:8080``.
#
#      The port is just the first port from the ephemeral range. By default
#      this does not matter because the Snippy container is never recommended
#      to be run with ``--net=host``. This command option shares host network
#      to container and exposes a risk for a port clash. If for some reason
#      user wants to do this, the configuration option for the port is left
#      open for user.
#
#      It is not possible to configured privileged port below 1024 without
#      running the container without ``--privileged`` option for dockerd. It
#      is never recommended to use the ``--privileged`` when running Snippy
#      container.
#
#      EXPOSE ${32768:-SNIPPY_SERVER_PORT}
#
#
# KNOWN SECURITY VULNERABILITIES AND PROBLEMS:
#
#   1. The Snippy server in the container binds to 0.0.0.0.
#
#      The Snippy server should bind to the hostname of the container.
#
#   2. Because Alpine ``adduser`` does not support ``--no-log-init``, the
#      Snippy container is prone to disk exhaustion if used UID is very
#      large [3]. It is recommended to run the container with UID values
#      below 65534.
#
#   3. Alpine base image is not able to support UID values over 256000 [6].
#
#
# TODO
#
#   1. Add mount examples to store persistent volume on host.
#
#   2. Fix Snippy server bind to container IP 0.0.0.0.
#
#   3. Fix TODO comment about the UID/GID not set by default.
#
#   4. Add examples for --net=host and --privileged.
#
#   5. Add example to configured the exposed with with --net=host.
#
#   6. Add examples to connect the server to another container that runs PostgreSQL.
#
#   7. Add examples to connect the CLI to another container that runs PostgreSQL.
#
#   8. Add script that tests all the combinations.
#
#
# LINTING IMAGES
#
#   1. Docker bench for security
#
#      Most of the analyses are for host that runs the dockerd daemon since
#      it is the most critical piece from container security point of view.
#
#      docker run -it --net host --pid host --userns host --cap-add audit_control \
#          -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
#          -v /etc:/etc \
#          -v /usr/bin/docker-containerd:/usr/bin/docker-containerd \
#          -v /usr/bin/docker-runc:/usr/bin/docker-runc \
#          -v /usr/lib/systemd:/usr/lib/systemd \
#          -v /var/lib:/var/lib \
#          -v /var/run/docker.sock:/var/run/docker.sock \
#          --label docker_bench_security \
#          docker/docker-bench-security
#
#   2. Anchore
#
#      Was not able to read localhost images and always tried to pull from
#      DockerHub by default. No instructions found within one minute to set
#      localhost registry. Analysis not done.
#
#      https://github.com/anchore/anchore-engine
#
#      mkdir anchore
#      cd anchore
#      curl https://raw.githubusercontent.com/anchore/anchore-engine/master/scripts/docker-compose/docker-compose.yaml > docker-compose.yaml
#      mkdir config
#      curl https://raw.githubusercontent.com/anchore/anchore-engine/master/scripts/docker-compose/config.yaml > config/config.yaml
#      mkdir db
#      docker-compose up -d
#      anchore-cli image add heilaaks/snippy:latest
#      anchore-cli image vuln heilaaks/snippy:latest
#      anchore-cli image content heilaaks/snippy:latest
#
#
# REFERENCES
#
# [1] https://docs.docker.com/storage/volumes/#choose-the--v-or---mount-flag
#
# [2] https://docs.openshift.com/enterprise/3.2/creating_images/guidelines.html
#
# [3] https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
#     "Users and groups in an image are assigned a non-deterministic UID/GID"
#
# [4] https://docs.docker.com/engine/security/userns-remap/
#
# [5] http://www.linfo.org/uid.html
#
# [6] https://docs.docker.com/engine/security/security/#linux-kernel-capabilities
#     "By default Docker drops all capabilities except those needed."
#
# [7] https://bugs.busybox.net/show_bug.cgi?id=9811
#