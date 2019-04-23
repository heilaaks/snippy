FROM alpine:3.9
LABEL maintainer "laaksonen.heikki.j@gmail.com"

ENV LANG C.UTF-8
ENV PYTHONUSERBASE=/usr/local/snippy/.local
ENV PATH=/usr/local/snippy/.local/bin:"${PATH}"

ENV SNIPPY_GID=61999
ENV SNIPPY_UID=61999
ENV SNIPPY_LOG_JSON 1
ENV SNIPPY_SERVER_HOST=container.hostname:32768
ENV SNIPPY_SERVER_BASE_PATH_REST=/api/snippy/rest

WORKDIR /usr/local/snippy

COPY snippy/ snippy/
COPY docker-entrypoint.sh .
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
        curl \
        python3 \
        py3-psycopg2 && \
    python3 -m pip install --upgrade \
        pip \
        setuptools && \
    python3 -m pip install \
        --user .[docker] && \
    find /usr/local/snippy/.local/lib -type d -name __pycache__ -exec rm -r {} \+ && \
    find /usr/local/snippy/.local/bin ! -regex '\(.*snippy\)' -type f -exec rm -f {} + && \
    mkdir -p /volume && \
    rm -f /usr/local/snippy/.local/lib/python3.6/site-packages/snippy/data/storage/snippy.db && \
    snippy import \
        --defaults \
        --all \
        --server-host "" \
        --storage-path /volume \
        -q && \
    touch snippy-server-host && \
    chown -R noname:root /usr/local/snippy/ && \
    chown -R noname:root /volume/ && \
    chmod -R ug=+rX-w,o-rwx /usr/local/snippy/ && \
    chmod ug=+rX,o=-rwx /usr/local/snippy/.local/lib/python3.6/site-packages/snippy/data/server/openapi/schema && \
    chmod ug=+rx-w,o=-rwx docker-entrypoint.sh && \
    chmod ug=+rw-x,o=-rwx snippy-server-host && \
    chmod ug=+rx-w,o=-rwx .local/bin/snippy && \
    chmod ug=+rwX,o=-rwx /volume/snippy.db && \
    find /usr/lib/python3.6 -type d -name __pycache__ -exec rm -r {} \+ && \
    python3 -m pip uninstall pip --yes && \
    apk del apk-tools && \
    rm -f /usr/local/snippy/setup.py && \
    rm -rf /etc/apk/ && \
    rm -rf /usr/local/snippy/.cache && \
    rm -rf /usr/local/snippy/snippy && \
    rm -rf /lib/apk/ && \
    rm -rf /root/.cache && \
    rm -rf /usr/lib/python3.6/site-packages/psycopg2/tests && \
    rm -rf /usr/lib/python3.6/distutils/ && \
    rm -rf /usr/share/apk/ && \
    rm -rf /var/cache/apk/ && \
    find / -perm +6000 -type f -exec chmod a-s {} \; || true

HEALTHCHECK --interval=10s \
            --timeout=3s \
            CMD curl \
                --fail \
                --insecure \
                --proto http,https \
                $(cat snippy-server-host)${SNIPPY_SERVER_BASE_PATH_REST} || exit 1

EXPOSE 32768

USER noname


ENTRYPOINT ["./docker-entrypoint.sh"]
#ENTRYPOINT ["tail", "-f","/dev/null"]

#
# SECURITY HARDENING
#
#   Note that the author is not a security or Linux expert. This is a
#   hobby project. If the reasons that justify the Dockerfile and the
#   security design aspects are not correct, it is a sign that can be
#   a security vulnerability or subpar user experience.
#
#   The most critical parts from the container security hardening have
#   to be done in host that runs the container runtime.
#
#
# TERMS
#
#   The documentation always refers to 'Docker' even though the correct
#   term is 'The Moby Project' these days. The 'Docker' is the name of
#   the company that created the Docker.
#
#   The documentation always refers to 'Docker' as a generic term. This
#   covers 'containerd' runtime as well as the 'docker run' command. The
#   goal is just to get the software running.
#
#   A 'host' always refers to the operating system that starts and runs
#   Docker images.
#
#   A 'container' always refer to the Docker container itself.
#
#
# TARGET GROUP
#
#   The target group is a casual user who just wants to run the Snippy
#   Docker image with the same Linux user as the user who starts the
#   container. This enables an easy way to mount a persistent volume
#   from host.
#
#
# MINIMUM VERSIONS
#
#   The examples are tested with Docker version 18.05.0-ce. They likely
#   work with other relatively recent versions as well.
#
#   Examples have been tested with Fedora 26 and Bash.
#
#
# CONTAINER UID/GID
#
#   By default, all docker image haave non-deterministic UID and GID. The
#   non-deterministic values are allocated at image compile time [2].
#
#   Non-deterministic UID and GID are problems only when container mounts
#   a volume from host. If there is a non-deterministic UID, it is not
#   trivial to maintain file access rights in host for containers that
#   require file access. For example if a host is a multi-tenant runtime
#   environment with many containers, maintaining volume access rights
#   based on non-deterministic UID and GID values is not feasible.
#
#   If Docker user namespaces feature is activated in host ``dockerd`` [3],
#   it is possible to start a container with UID 0 (root). The UID 0 maps
#   to specific UID range in host that does not have root privileges.
#
#   UID ranges are Linux kernel and distribution specific [4] and they can
#   be configured to have different ranges. This means it is not feasible
#   to know in advance which ranges user prefers.
#
#   For example OpenShift runs containers using an arbitrarily assigned
#   user ID [1].
#
#
# USE CASES:
#
#   1. Running container with the same UID as in the host (unsecure)
#
#      In this case the user who starts the Docker container is the same
#      as the the user who runs the Snippy server in the Docker container.
#      That is, the user in the Docker image has the same privileges as
#      the user in the host. This means that if there is a breach within
#      the Docker container to the host, a malicious user will gain the
#      same user privileges as the user who started the Docker container.
#
#      This is unsecure because user starting the container may be a root
#      user. If the command example below is run as a root user, it starts
#      the container with almost the same privileges as the root user in
#      host. In this case only some of the Linux security capabilities are
#      removed from the running container [5].
#
#
#      ```shell
#      # Example 1: No persistent volume from host.
#      docker run \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy -vv
#      ```
#
#      ```shell
#
#      In order to maintain stored data over restarts, a persistent volume
#      must be mounted from the host. The directory path in the host must
#      be absolute path. The example below will create new folder under
#      user home directory. The Docker container is started with the same
#      user (UID) that the user running the containers. This makes it
#      possible to access the host volume from container. If different UID
#      would be used in the container to run the Snippy server, it would
#      not be able to access the volume mount from the host.
#
#      Because this creates a volume outside the Docker container, there
#      are no default content in storage unless explicitly told. Because
#      of this, there is the ``--defaults`` flag. This tells the Snippy
#      server to import the default content when the server is started.
#      If you do not want to use the default content, just leave the
#      ``--defaults`` out from the command example.
#
#      # Example 2: Persistent volume is reserved from host.
#      mkdir -p /home/$(whoami)/.local/share/snippy
#      docker run \
#          --user $(id -u $(whoami)) \
#          --volume /home/$(whoami)/.local/share/snippy:/volume \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy --defaults -vv
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
#      If persisted volume is needed in this use case, you can follow the
#      example in the unsecure use case. Just define the user UID and neede
#      volume permission for the user that is going to be used to run the
#      Docker container. You must define the ``--user`  in the ``docker
#      run`` command. Otherwise the Docker container user UID would be
#      different which would prevent the container to access to the host
#      volume.
#
#   3. Running container with UID allocated from host with user namespaces
#
#      In this use case the UID in container does not map to UID in host.
#      This use case assumes that container name user namespaces feature in
#      host dockerd [3] is activated.
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
#   4. Change the IP and port visible in host that runs the container
#
#      The ``--publish`` command line option defines what is the IP and port
#      that is visible in host. The example below shows how the exposed port
#      and IP address in the host can be changed to 173.23.22.212:80.
#
#      The ``/tcp`` in the ``publish`` option means that only TCP port in
#      running container is mapped to 173.23.22.212:80. Because Snippy is a
#      HTTP server, only TCP protocol is needed.
#
#      ```shell
#      docker run \
#          --publish=173.23.22.212:80:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy -vv
#      ```
#
#   5. Change REST API server base path
#
#      It is possible to change Snippy REST API server base path. Configured
#      base path must always start and end with a slash
#
#      ```shell
#      docker run \
#          --env SNIPPY_SERVER_BASE_PATH_REST=/api/ \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy -vv
#      ```
#
#   6. Use host network
#
#      This is not recommended configuration because it is not secure and
#      breaks the container native design "assume nothing from host".
#
#      It is possible to bind the server IP directly from the host that runs
#      the Snippy Docker continer. This configuration is prone to port
#      conflicts since some other service in host may already use required
#      port.
#
#      This example is the only valid reason to modify the Snippy server
#      host and port in the container.
#
#      ```shell
#      docker run \
#          --env SNIPPY_SERVER_HOST=127.0.0.1:8080 \
#          --net=host \
#          --name snippy \
#          --detach \
#          heilaaks/snippy -vv
#      ```
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
#      The reason is likely that each intermediate RUN layer contains the
#      files that are only removed last. It would be awkward to delete all
#      the temporay files with each RUN layer.
#
#   2. Dockerfile configuration
#
#      There is no know use case to justify users to be able to modify
#      following settings in the Dockerfile:
#
#      - User and user group names. All that matters are the UID and GID.
#
#      - Server installation location in container. It would be a security
#        risk and unnecessary complication to define where the server is
#        installed in Docker container.
#
#      - Server storage location. If user wants to mount a volume from the
#        host for persisnten storage, the ``--volume`` option defines the
#        host directly. It would be a security risk and unnecessary
#        complication to let user to define what directory Docker container
#        uses for storage.
#
#      The design principle is to allow configuration through environment
#      variables if there is a supported use case.
#
#
#   3. Special tag to read container runtime IP address.
#
#      There are no other ways to get the container runtime IP address
#      than doing a startup script that extracts the container IP address
#      or resolving the address in code.
#
#      The problem would be much easier if the container would always bind
#      to 0.0.0.0. But this is considered as a security risk since it is
#      likely that security hardening is not done for host that runs the
#      containers. Also it is likely that user may start the server with
#      ``--net=host`` without changing the server IP which would lead the
#      server to listen all the addresses in host.
#
#      In order to get both 1 and 2 to work simultaneously with the above
#      security assumption, the startup script is the only option.
#
#         1. Server started with
#            A) container defaults
#            B) using --net=host and changing the SNIPPY_SERVER_HOST
#         2. Container healthcheck working properly
#
#      - If user does not want to change the default and does not use host
#        networking with ``--net=host``, it is not possible to set the
#        server host environment variable without startup script or reading
#        the hostname from code. If code reads the hostname, this is not
#        available for the healtcheck without writing the information into
#        a file. The code cannot update environment variables in runtime
#        so that they would be visible for container that runs healthcheck.
#
#      - It would work through environment variables if the user would
#        always define SNIPPY_SERVER_HOST environment variable. But this
#        is considered too difficult to be practical without running the
#        container with ``--net=host``.
#
#      - It could be possible to provide new hostname with ``--add-host``
#        from ``docker run`` command. But this is again considered too
#        difficult to be practical for target use case.
#
#      - The special tag ``container.hostname`` tells for the script that
#        user did not set set the server IP and it must be read from the
#        container runtime hostname IP.
#
#      The area itself is complicated so there can be issues with this
#      approach. See ``The Snippy server in the container can bind to
#      0.0.0.0.`` for security advisory. For example when Kubernetes or
#      Swarm is taken into use with different networking models, it is
#      suspected that there will be issues.
#
#      ```shell
#      ENV SNIPPY_SERVER_HOST=container.hostname:32768
#      ```
#
#   4. Container UID and GID are not defined by default
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
#   5. The container user is created as system user
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
#      ```shell
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
#      ```
#
#   6. Container user file access privileges
#
#      "For an image to support running as an arbitrary user, directories and
#       files that may be written to by processes in the image should be owned
#       by the root group and be read/writable by that group. Files to be
#       executed should also have group execute permissions." [1]
#
#      "Because the container user is always a member of the root group, the
#       container user can read and write these files. The root group does
#       not have any special permissions (unlike the root user) so there are
#       no security concerns with this arrangement." [1]
#
#      Because of the above, all files needed by the server in Docker container
#      are owned by user ``noname`` or ``root``. If other user (GID) than the
#      default user with defined GID in container, the user is still always
#      parth of the root group.
#
#
#      By default, only read for files and folders and execution for folders
#      is granted for ``user`` and ``group`` file permissions. Then the files
#      and folders are granted write and execution permission if needed.
#
#      ```shell
#      chown -R noname:root /usr/local/snippy/ && \
#      chown -R noname:root /volume/ && \
#      chmod -R ug=+rX-w,o-rwx /usr/local/snippy/ && \
#      chmod ug=+rX,o=-rwx /usr/local/snippy/.local/lib/python3.6/site-packages/snippy/data/server/openapi/schema && \
#      chmod ug=+rx-w,o=-rwx docker-entrypoint.sh && \
#      chmod ug=+rw-x,o=-rwx snippy-server-host && \
#      chmod ug=+rx-w,o=-rwx .local/bin/snippy && \
#      chmod ug=+rwX,o=-rwx /volume/snippy.db && \
#      ```
#
#   7. Remove setuid/setgid bit from all binaries (defang)
#
#      There is no need to allow binaries to run with these privileges in
#      container. Because ofthis, the bit is removed from all binaries.
#
#      ```shell
#      find / -perm +6000 -type f -exec chmod a-s {} \; || true && \
#      ```
#
#   8. Container user is operated only with UID and GID
#
#      There is no user name allocated for the container. Only the UID and
#      GID are relevant from security point of view and allocating specific
#      user name for the container can give misleading information about the
#      security hardening.
#
#      Because of this, there is only a fixed noname allocated for the user
#      in container.
#
#      ```shell
#      USER noname
#      ```
#
#   9. Periodic healthcheck
#
#      Healthcheck is made with curl that allows using either http or https
#      as protocol. A ``nc`` command line tool is one option. The problem
#      with the ``nc`` tool is that it requires IP address and port as a
#      separate parameters. In case of Snippy command line options, the IP
#      address and port are defined in one string which is not supported by
#      the ``nc`` tool.
#
#      The server host with port is read from a file. See the ``Special tag
#      to read container runtime IP address.`` for more information.
#
#      ```shell
#      HEALTHCHECK --interval=10s \
#                  --timeout=3s \
#                  CMD curl \
#                      --fail \
#                      --insecure \
#                      --proto http,https \
#                      $(cat snippy-server-host)${SNIPPY_SERVER_BASE_PATH_REST} || exit 1
#      ```
#
#
#  10. Exposed container port can not be configured
#
#      The Snippy server in container image binds on port 32768 by default.
#      The server port is exposed statically in the Dockerfile. The exposed
#      port in the Dockefile serves only two purposes:
#
#        1. Default value for dockerd ``--publish`` option.
#        2. Documentation to user about the container bind port.
#
#      The default port is chosen to have different value than 80 or 8080
#      because this clearly separates container port from the host port. The
#      author always have problems to remember which was the host port and
#      which the quest port in command examples like ``--publish=8080:8080``.
#
#      The port is just the first port from the ephemeral range. By default
#      this does not matter because the Snippy container is never recommended
#      to be run with the ``--net=host`` option. This command option shares
#      host network to container and exposes possible security and port clash
#      problems. If user for some reason wants to do this, it can be done.
#      See the ``Use host network`` example for more information.
#
#      It is not possible to configure privileged ports below 1024 without
#      running the container without ``--privileged`` option for dockerd. It
#      is never recommended to use the ``--privileged`` when running Snippy
#      container because it exposes security risk.
#
#      The exposed port is hard coded because when the ``--net=host`` option
#      is used, published ports are discarded the the exposed default is not
#      used in any way.
#
#      ```shell
#      EXPOSE 32768
#      ```
#
#  11. No default command
#
#      Do not add default command ``--help``. This causes problems when the
#      server configuration is defined only from environment variables that
#      is the most common use case when running server from container.
#
#      From Snippy point of view, this implememntation makes the CLI and
#      server side work in a similar manner. This helps to avoid container
#      specific solutions in code and makes testing easier.
#
#      ```shell
#      ENTRYPOINT ["./docker-entrypoint.sh"]
#      ```
#
# KNOWN SECURITY VULNERABILITIES AND PROBLEMS:
#
#   1. The Snippy server in the container can bind to 0.0.0.0.
#
#      If there is a problem reading the container hostname and IP, the
#      Snippy container still runs on the IP address 0.0.0.0. This is a
#      security risk that should not be done in production.
#
#      If there are no problems reading the container address, the server
#      binds to correct address.
#
#      There is a security level log message printed in case reading the
#      container IP address failed and the server is run on 0.0.0.0.
#
#   2. Because Alpine ``adduser`` does not support ``--no-log-init``, the
#      Snippy container is prone to disk exhaustion if used UID is very
#      large [2]. It is recommended to run the container with UID values
#      below 65534.
#
#   3. Alpine base image is not able to support UID values over 256000 [6].
#
#
# TODO
#
#   2. Fix TODO comment about the UID/GID not set by default.
#
#   3. Add examples for --privileged to bind with --net=host to ports below 1024.
#
#   4. Add examples to connect the server to another container that runs PostgreSQL.
#
#   5. Add examples to connect the CLI to another container that runs PostgreSQL.
#
#   6. Add script that tests all the combinations.
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
# [1] https://docs.openshift.com/enterprise/3.2/creating_images/guidelines.html
#
# [2] https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
#     "Users and groups in an image are assigned a non-deterministic UID/GID"
#
# [3] https://docs.docker.com/engine/security/userns-remap/
#
# [4] http://www.linfo.org/uid.html
#
# [5] https://docs.docker.com/engine/security/security/#linux-kernel-capabilities
#     "By default Docker drops all capabilities except those needed."
#
# [6] https://bugs.busybox.net/show_bug.cgi?id=9811
#