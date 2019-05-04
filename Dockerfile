FROM alpine:3.9
LABEL maintainer "https://github.com/heilaaks/snippy"

ENV LANG C.UTF-8
ENV PYTHONUSERBASE=/usr/local/snippy/.local
ENV PATH=/usr/local/snippy/.local/bin:"${PATH}"

ENV SNIPPY_LOG_JSON 1
ENV SNIPPY_SERVER_HOST=container.hostname:32768
ENV SNIPPY_SERVER_BASE_PATH_REST=/api/snippy/rest/

WORKDIR /usr/local/snippy

COPY LICENSE .
COPY README.rst .
COPY setup.py .
COPY snippy/ snippy/

RUN apk add \
        python3 \
        py3-psycopg2 && \
    python3 -m pip install --upgrade \
        pip \
        setuptools && \
    python3 -m pip install --user \
        .[docker] && \
    find /usr/lib/python3.6 -type d -name __pycache__ -exec rm -r {} \+ && \
    find /usr/local/snippy/.local/lib -type d -name __pycache__ -exec rm -r {} \+ && \
    find /usr/local/snippy/.local/bin ! -regex '\(.*snippy\)' -type f -exec rm -f {} + && \
    mkdir /volume && \
    rm -f /usr/local/snippy/.local/lib/python3.6/site-packages/snippy/data/storage/snippy.db && \
    snippy import \
        --defaults \
        --scat all \
        --storage-path /volume \
        -q && \
    chmod -R go=+rX-w,u-rwx /usr/local/snippy/ && \
    chmod go=+rwX,u=-rwx /volume && \
    chmod go=+rx-w,u=-rwx .local/bin/snippy && \
    chmod go=+rw-x,u=-rwx /volume/snippy.db && \
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
            CMD snippy \
                --server-healthcheck

EXPOSE 32768

USER 232768

ENTRYPOINT ["snippy", "server", "--storage-path", "/volume"]

#
# CONTAINER IMAGE SECURITY HARDENING
#
#   Author is not a security or Linux expert. This is just a hobby project.
#   If this documentation for the Snippy container security hardening does
#   not sound correct, it indicates security vulnerability or a problem to
#   run the container. Feel free to make an issue at [1].
#
#   The most critical aspects from container security hardening has to be
#   made in the host that runs containers.
#
#   You can run the Snippy container with root privileges. There is nothing
#   that prevents this.
#
#
# TERMS
#
#   The documentation uses 'docker' as a generic term. When there is no
#   need to be explicit, this term covers the 'containerd' runtime as well
#   as the 'docker run' command. In general, 'docker' referes to services
#   that are run in 'host' that are required to run 'containers'.
#
#   A 'host' always refers to the host operating system that starts and
#   runs container images.
#
#   A 'container' always refer to the Docker container itself.
#
#
# TARGET GROUP
#
#   The target group is a casual user who wants to run the Snippy Docker
#   container with the same Linux user (UID) as the user who starts the
#   container. This allows an easy way to mount a persistent volume from
#   host.
#
#   This documentation considers only docker/moby as a container runtime
#   environment. That is, there are no considerations for example for
#   configurations in Kubernetes/Swarm/Mesos or LXC/LXD. The assumption
#   is that all these are somehow based on similar techonologies on top
#   of Linux os the basic principles in this documentation should apply.
#
#
# MINIMUM VERSIONS
#
#   The examples are tested with Docker version 18.05.0-ce. They likely
#   work with other relatively recent versions from Docker.
#
#   Examples have been tested with Fedora 26 and Bash. There is a test
#   case ``test_api_docker`` that verifies some of the use cases from
#   functionality point of view, not from security point of view.
#
#
# CONTAINER UID/GID AND USERS
#
#   This is the most imporant thing to understand from container security
#   and resource management point of view. This also explains why host is
#   in a critical position to securely run a container based application.
#
#   The user name visible in a container does not matter. The only things
#   that matters are the user UID and GID. In order to avoid misleading
#   what is the container user from security point of view, a Dockerfile
#   should always use numerical UID and GID values.
#
#   Host and the docker that starts a container dictate what are the UID
#   and GID values in container to run service(s). This is done by:
#
#     1. Explicitly set by the ``--user``` option for docker run command.
#     2. Explicitly set by Docker Linux 'user namespaces' feature [4].
#     3. Implicitly set to the same value as the user who runs container.
#
#   By default, all docker images have non-deterministic UID and GID. The
#   non-deterministic values are allocated at image compile time [2].
#
#   If host does not define the UID and GID with options 1 or 2, container
#   can change the UID with explicit ``USER`` instruction in a Dockerfile.
#   If the ``USER`` instruction is set to a specific UID value, container
#   is run with that UID (if host did not explicitly define the UID). The
#   explicitly set UID in Dockerfile may or may not exist in the host. If
#   the used UID value exists by accident in the host, user in container
#   will gain almost the same privileges as the user in host [6]. It is
#   'almost' because docker drops some of the Linux capabilities from
#   containers. In case of a security breach from running container to
#   host, user will gain same privileges as the user in host.
#
#   Security hardening guidelines for host recommend that the ``dockerd``
#   is run by the root user in host. When the ``dockerd`` is run by the
#   root (UID 0), the default UID and GID are from the root user (UID and
#   GID 0) to run containers. This explains why the user in container is
#   always part of the root group if host did not explicitly define GID
#   to something else than the root group with options 1 or 2.
#
#   There is a feature ``rootles mode`` [10] which brings a non-root mode
#   for the ``dockerd``. When this feature is in use, the UID and GID in
#   container can be something else than root (0) by default. It is not
#   know how this impacts the Dockerfile security hardening. For example
#   when multiple hosts are run with different user (UID and GID). In this
#   case the GID is not a root group anymore and it can be different for
#   every container. How ever, this should not be a different case than
#   the option 1 where host sets the ``--user`` with GID for other group
#   than a root group.
#
#   The UID and GID are problems only (mainly?) because of:
#
#     1. Security breach where user (UID) breaks out from a container.
#     2. Allocating resources like volumes from host for containers.
#
#   From security point of view, it is important that the UID used in the
#   container does not match to any privileged user in the host. From a
#   resource management point of view for multi-tenant environments, it is
#   important to have deterministic UID and GID that can be managed by the
#   operator who runs the infrastructure.
#
#   Non-deterministic UID and GID are problems only when container mounts
#   a volume from host. If there is a non-deterministic UID, it is not
#   trivial to maintain file access rights in host for containers that
#   require file access. For example if a host is a multi-tenant runtime
#   environment with many containers, maintaining volume access rights
#   based on non-deterministic UID and GID values is not feasible.
#
#   If Docker 'user namespaces' feature is activated in host Docker [4],
#   it is possible to start a container with UID 0 (root) without mapping
#   directly to a root user in host. The UID 0 in this case maps to a
#   specific UID range in host that does not have root privileges.
#
#   UID ranges are Linux kernel and distribution specific [5] and they can
#   be configured to have different ranges. This means it is not feasible
#   to know in advance to which ranges user should be allocated.
#
#   For example OpenShift runs containers using an arbitrarily assigned
#   UIDs [3].
#
#
# USE CASES:
#
#   1. Starting the server without specifying UID and GID
#
#      Because the ``USER`` is explicity set in the Dockerfiel the UID that
#      runs services in the container does not have the same UID as the user
#      in the host. The container GID is the same as the user who started
#      the container. Because the ``dockerd`` security hardening principles
#      define that it is run as a root, the container user is very likely
#      part of root group (GID 0).
#
#      This means that in case of a security breach from container to host,
#      the user is likely unknown but will be part of the root group. "The
#      root group does not have any special permissions (unlike the root
#      user) so there are no security concerns with this arrangement." [3
#
#      The ``USER`` in the Docker image can be considered random even though
#      it is fixed. Do not rely to the UID defined in Dockerfile to allocate
#      volume from the host. This means that this use case does not support
#      persistent volume mount from host.
#
#      ```shell
#      docker run \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy --debug
#      ```
#
#   2. Starting the server with UID or GID defined from host
#
#      In this use case the UID defined by host will override the value set
#      in the ``USER`` instruction in the Dockerfile. This allows defining
#      a volume from host with the help of deterministic UID.
#
#      ```shell
#      # Example 1: Run container services with UID 1000.
#      docker run \
#          --user 1000 \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy --debug
#      ```
#
#      It is also possible to defined the GID with UID when starting the
#      server container.
#
#      ```shell
#      # Example 2: Run container services with UID 1000 and GID 1001.
#      docker run \
#          --user 1000:1001 \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy --debug
#      ```
#
#      In order be able to maintain the updated content in Snippy container,
#      a persistent volume must be mounted from the host. The directory path
#      in the host must be absolute path for the ``docker run`` command.
#
#      The example below will create new folder under user's home directory.
#      The container is started with the same user (UID) than user starting
#      the containers. This makes it possible to access a volume from the
#      container. If different UID would be used in the container to run the
#      Snippy server, it would not be able to access the volume from the host.
#
#      Because this creates a volume outside the Docker container, there are
#      no default content in storage unless explicitly told. Because of this,
#      there is the ``--defaults`` flag. This tells the server to import the
#      default content when the server is started. If you do not want to use
#      the default content, leave the ``--defaults`` option from the example.
#
#      # Example 3: Persistent volume is reserved from host.
#      mkdir -p /home/$(whoami)/.local/share/snippy
#      docker run \
#          --user $(id -u) \
#          --volume /home/$(whoami)/.local/share/snippy:/volume \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy --defaults --debug
#      ```
#
#   3. Starting the service with UID allocated by 'user namespaces' feature
#
#      In this use case the UID in container does not map to UID in host.
#      This use case assumes that the docker ``user namespaces`` feature
#      is activated in host that runs the containers [4].
#
#      This is the use case suited for multi-tenant environments and running
#      multiple containers.
#
#      In this case the UID is not explicitly set from host. It is assumed
#      that in this case the container is started with UID 0 (root).
#
#      ```shell
#      docker run \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy --debug
#      ```
#
#   4. Running container with a readonly filesystem
#
#      It is possible to run the server with readonly filesystem if the
#      container is started with ``--tmpfs /tmp``. The server must have a
#      temporary folder to write a server own heartbeat [8].
#
#      The ``--tmpfs`` option does not allow any configuration like size of
#      the tmpfs or file permissions. The option also does not work with the
#      Docker swarm. If there is a use case where the ``--tmpfs`` cannot be
#      used, the same can be done with the ``--mount`` option which allows
#      limits in size, file permissions and works with Docker swarm. The
#      ``--tmpfs`` is used here because it is easier to configure.
#
#      ```shell
#      # Example 1: Run with the same UID as the user who starts the container.
#      docker run \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --read-only \
#          --tmpfs /tmp \
#          --detach \
#          heilaaks/snippy --server-readonly
#      ```
#
#      ```shell
#      # Example 2: Run with UID defined from host.
#      docker run \
#          --user 1000 \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --read-only \
#          --tmpfs /tmp \
#          --detach \
#          heilaaks/snippy --server-readonly
#      ```
#
#   5. Change the IP and port visible in host that runs the container
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
#          heilaaks/snippy --debug
#      ```
#
#   6. Change REST API server base path
#
#      It is possible to change the Snippy REST API server base path. The
#      server API base path must always start and end with a slash.
#
#      ```shell
#      docker run \
#          --env SNIPPY_SERVER_BASE_PATH_REST=/api/ \
#          --publish=127.0.0.1:8080:32768/tcp \
#          --name snippy \
#          --detach \
#          heilaaks/snippy --debug
#      ```
#
#   7. Use host network
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
#          heilaaks/snippy --debug
#      ```
#
#   8. Use Docker container as a command line tool
#
#      It is possible search content with the help of Docker container like
#      with the CLI version of the tool.
#
#      The procedure is different depending on the Snippy server storage:
#
#      1) Snippy server running local (Sqlite) storage inside container.
#
#         This example uses only the immutable container. This means that
#         only the content imported by default into the Docker image can
#         be searched.
#
#         In this use case the container is alive only during the command.
#         Use the ``--rm`` option to remove the exited container after the
#         command has been run.
#
#         There is no need to add a name for the the container. The name is
#         just an extra parameter that is not needed and which may clash
#         with existing names and fail the Docker command.
#
#         The Docker container will write JSON logs by default. The example
#         below disables this so that the last 'OK' or 'NOK: *' is printed
#         as normal text instead of JSON log.
#
#         ```shell
#         # Example 1: Connect to a volume mount used by Snippy server.
#         docker run \
#             --rm \
#             --env SNIPPY_LOG_JSON=0 \
#             heilaaks/snippy search --sall docker
#         ```
#
#      2) Snippy server running local (Sqlite) storage mounted from host.
#
#         If there is a Snippy server running and the container has mounted
#         a volume from host, it is possible to access another server data
#         by directly reading it's volume from the host. The ``--user`` and
#         ``--volume`` must be defined correctly so that the container is
#         able to read the volume allocated for the sever.
#
#         ```shell
#         # Example 1: Connect to a volume mount used by Snippy server.
#         docker run \
#             --rm \
#             --user $(id -u) \
#             --volume /home/$(whoami)/.local/share/snippy:/volume \
#             --env SNIPPY_LOG_JSON=0 \
#             heilaaks/snippy search --sall docker
#         ```
#
# DESIGN DECISIONS
#
#   1. Dockerfile layers
#
#      There is only one RUN layer in order to keep the image size as small
#      as possible. This increases Docker image compilation time because the
#      source code is copied before the RUN layer which fist install all the
#      third party dependencies which usually do not change. This is accepted
#      because compiling the Dockerfile is relative fast and container small
#      size is considered more imporant.
#
#   2. Dockerfile configuration
#
#      The design principle is to allow configuration through an environment
#      variables if there is a use case for it. There is no know use case to
#      justify users to be able to modify following settings:
#
#      - User and user group names to add a new user. Only GID and ID matter.
#
#      - Server install location. It would be unnecessary complication and
#        thus a security risk to allow users to define where the server is
#        installed in docker image.
#
#      - Server storage location. Again, unnecessary complication and thus a
#        security risk to manage file permissions in container. If there is
#        a need to mount a volume from the host for persisnten storage, the
#        ``--volume`` option defines the host and container directories.
#
#      - Configuring the container user UID and GID. There is no use case to
#        allow user to set the UID and GID in the Dockerfile. These values
#        must be configured from host because of the security and resource
#        management reasons explained in the 'CONTAINER UID/GID AND USERS'
#        chapter.
#
#      Default values:
#
#      - The server produces JSON formatted logs to stdout. It is assumed
#        that logs from services running in containers are post processes
#        by host infrastructure. JSON is a common format and it allows for
#        example JSON schema that defines the log format. This is managed
#        with environment parameter ``SNIPPY_LOG_JSON``.
#
#   3. Special tag 'container.hostname' is the server host default
#
#      The special tag ``container.hostname`` tells for the server that user
#      did not set set the server IP address where to bind when the container
#      was started. It means that the server must resolve the address from
#      the container hostname.
#
#      The problem is that there are two processes in container that need
#      the server IP address. One is the server itself and the second is the
#      server healthcheck implemented by the ``HEALTHCECHK`` instruction in
#      the Dockerfile.
#
#      Below mentioned requirements must be be fullfilled to support the
#      required use cases:
#
#         1. Server started with container defaults.
#         2. Server started with the docker ``--net=host`` option.
#         3. Container healthcheck working properly with options 1 and 2.
#
#      There are no other ways to read the container runtime server IP by
#      two processes than 1) implementing a startup script that extracts
#      the correct container IP address and updates an environment variable
#      or a file or 2) resolving the address in code.
#
#      There is no support to change the container internal IP address where
#      the server was bind other than restarting the container.
#
#      The problem would be much easier if the container would always bind
#      to 0.0.0.0. But this is considered as a security risk since it is
#      likely that security hardening is not done for a host that runs the
#      containers. Also it is likely that user may start the server with
#      ``--net=host`` without changing the server IP which would lead the
#      server to listen all the IPv4 addresses in host.
#
#      - If user does not want to change the default and does not use host
#        networking with ``--net=host``, it is not possible to set the
#        server host environment variable without startup script or reading
#        the hostname from code. If code reads the hostname, this is not
#        available for the healtcheck without writing the information into
#        a file. The code cannot update environment variables in runtime
#        so that they would be visible for the  other processes that runs
#        the healtcheck.
#
#      - This would work by using only one environment variable if users
#        would always define the ``SNIPPY_SERVER_HOST`` variable when the
#        containers is started. This is considered too difficult to be
#        practical in case that user does not use the host network with
#        the ``--net=host`` option.
#
#      - It would be possible to provide a new well-known hostname with the
#        ``--add-host`` from the ``docker run`` command. But this is again
#        considered too difficult to be practical for simple use cases.
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
#   4. Container user file access privileges
#
#      Changing the file permissions in container is not as critical as it
#      sounds. The design is to understand what is needed an why and try to
#      set a minimal permissions for the files. The most important from the
#      file permission point of view is that if malicious user gains access
#      to the container filesystem, there are no additional tools to try to
#      break to host that runs the container.
#
#      The processes in container can be run with any UID or GID. By default
#      the GID is the root GID 0. The only cases when the GID can be other
#      than the root GID:
#
#      1) When user defines the GID explicitly with ``--user`` option.
#      2) When Docker ``user namespaces`` feature is used. [4]
#      3) When Docker ``rootles mode`` feature is used. [10]
#
#      Because of the above, all the files needed by the server in container
#      are owned by ``group`` and ``others``. The only reason why files are
#      owned by ``others`` is a case when the GID is changed to a different
#      value than allocated for the ``dockerd`` in host. In this case the
#      user in the container is not part of ``group`` file permission set.
#      This scenario to require ``others`` file permissions is possible only
#      with above options 1) and 2).
#
#      If other UID than the default value defined in the Dockerfile with
#      the ``USER`` instruction is used, the user in container is still
#      part of the root group (GID 0) in most cases.
#
#      Note that if a volume is mounted from host, the host directory file
#      permissions are visible in container, not the ones that are defined
#      in the Dockerfile.
#
#      ```shell
#      chmod -R go=+rX-w,u-rwx /usr/local/snippy/
#      chmod go=+rwX,u=-rwx /volume
#      chmod go=+rx-w,u=-rwx .local/bin/snippy
#      chmod go=+rw-x,u=-rwx /volume/snippy.db
#      ```
#
#   5. Remove setuid/setgid bit from all binaries (defang)
#
#      There is no need to allow binaries to run with these privileges in
#      container. Because ofthis, the bit is removed from all binaries.
#
#      ```shell
#      find / -perm +6000 -type f -exec chmod a-s {} \; || true
#      ```
#
#   6. Periodic healthcheck
#
#      The Docker healthcheck is made with own implementation. This allows
#      the healthcheck to discover the running server exactly as the server
#      code itself. This also removes the need to add new command line tools
#      into the container.
#
#      The problem is that the sever bind IP is:
#
#        1) Not know in Docker image compile time.
#        2) Not easily available for user when Docker container is started.
#        3) Not secured when server binds to 0.0.0.0.
#        4) Not available easily inside container from hostname.
#        5) Not easily available for curl/nc based healthcheck.
#
#      Option 2: Use external command line tools - curl/nc
#
#      Curl command would have to parse the container IP from host. This is
#      likely a problem as well if DNS based IP discover is needed. This
#      requires in practise a external script to parse the IP for curl to
#      a file where curl reads it. This forces to have two implementations
#      to read the container IP: one in script and one in code.
#
#      Also for example the ``nc`` command does not support host format
#      IP:port.
#
#      The server supports HTTP and HTTPS and the HTTP scheme would have to
#      be discovered somehow in external script.
#
#      There are two aspects in the problem: Server IP bind when user does
#      not define the IP (container internal IP) and when the ``--net=host``
#      is used. It is not easy to know when user defined the IP and when a
#      default was used. There was a special tag in environment variable
#      for the server host: 'container.host'. But this was awkward because
#      it required external script, file management and starting the server
#      with docker-entrypoint script.
#
#      Also when external tools like curl were used to do periodic health
#      check, they failed when the server was loaded. It seems that the
#      current implementation which uses the embedded healthceck survives
#      the load tests. [TODO: Reason for this is not understood.]
#
#      ```shell
#      HEALTHCHECK --interval=10s \
#                  --timeout=3s \
#                  CMD snippy \
#                      --server-healthcheck
#      ```
#
#  7. Exposed container port can not be configured
#
#     The Snippy server in container image binds on port 32768 by default.
#     The server port is exposed statically in the Dockerfile. The exposed
#     port in the Dockefile serves only two purposes:
#
#       1. Default value for dockerd ``--publish`` option.
#       2. Documentation to user about the container bind port.
#
#     The default port is chosen to have different value than 80 or 8080
#     because this clearly separates container port from the host port. The
#     author always have problems to remember which was the host port and
#     which the quest port in command examples like ``--publish=8080:8080``.
#
#     The port is just the first port from the ephemeral range. By default
#     this does not matter because the Snippy container is never recommended
#     to be run with the ``--net=host`` option. This command option shares
#     host network to container and exposes possible security and port clash
#     problems. If user for some reason wants to do this, it can be done.
#     See the ``Use host network`` example for more information.
#
#     It is not possible to configure privileged ports below 1024 without
#     running the container without ``--privileged`` option for dockerd. It
#     is never recommended to use the ``--privileged`` when running Snippy
#     container because it exposes security risk.
#
#     The exposed port is hard coded because when the ``--net=host`` option
#     is used, published ports are discarded the the exposed default is not
#     used in any way.
#
#     ```shell
#     EXPOSE 32768
#     ```
#
#   8. Dockerfile does not create new user or group
#
#      Because of the reasons presented in 'CONTAINER UID/GID AND USERS',
#      the user name does not matter. There is no need to create user or
#      gourp.
#
#      The only user related action in the Dockerfile is to set the ``USER``
#      to arbitrary high UID value outside of normal Linux UID ranges [5]
#      and below Alpine base image supported UID range [7]. This forces the
#      container to run with other than root user (UID 0) by default. The
#      default value is unlikely used in the host for normal users and thus
#      it should be safe in case of a security breach.
#
#      Also some services like OpenShift use the ``USER`` in Dockerfile to
#      determine if a container runs with a root [11]. Therefore the value
#      for the ``USER`` must be set to non-zero (root).
#
#      From security point of view, the most beneficial security hardening
#      step for a semi-professional use is to define the UID from the host
#      that starts the container with ``--user`` option. If the UID would
#      be hardcoded or set with an environment variable, user _may_ have
#      to recompile the Dockerfile or set a environment variable to unset
#      the default UID in container. Whether this fails or not depends on
#      how the file permissions are set in container.
#
#      When the UID of the container is generated by user, the container
#      will not have an associated entry in /etc/passwd to map user and UID.
#      This is not a problem because the Dockerfile operates only with UID.
#      The Snippy server does not care what is the UID or GID as long as
#      there are correct file permissions set in the container.
#
#      ```shell
#      USER 232768
#      ```
#
#  9. No default command
#
#     Do not add default command ``--help``. This causes problems when the
#     server configuration is defined only from environment variables that
#     is the most common use case when running server from container.
#
#     From Snippy point of view, this implememntation makes the CLI and
#     server side work in a similar manner. This helps to avoid container
#     specific solutions in code and makes testing easier.
#
#     The storage path is not configurable for user. User can override the
#     Dockerfile ENTRYPOINT but this won't work unless the new ENTRYPOINT
#     defines the same ``--storage-path`` pointing to ``/volume``. See the
#     ``Dockerfile configuration`` for configuration desing.
#
#     ```shell
#     ENTRYPOINT ["snippy", "--storage-path", "/volume"]
#     ```
#
# KNOWN SECURITY VULNERABILITIES AND PROBLEMS
#
#   1. The Snippy server in the container can bind to 0.0.0.0.
#
#      If there is a problem reading the container hostname and IP, the
#      Snippy container still runs on the IP address 0.0.0.0. This is a
#      security risk that should not be done in production.
#
#      If there are no problems reading the container address, the server
#      binds to correct address based on container hostname.
#
#      There is a security level log message printed in case reading the
#      container IP address failed and the server is run on 0.0.0.0. It is
#      recommended to post process and analyze security events (logs) from
#      the server.
#
#   2. Because Alpine ``adduser`` does not support ``--no-log-init``, the
#      Snippy container is prone to disk exhaustion if used UID is very
#      large [2]. It is recommended to run the container with UID values
#      below 65534.
#
#   3. Alpine base image is not able to support UID values over 256000 [7].
#
#
# TODO
#
#   1. Fix TODO comment related to curl vs. Snippy healthcheck during load test.
#
#   2. Add excample of option z|Z for volumes if host uses SELinux [12].
#
#   3. Add examples for --privileged to bind with --net=host to ports below 1024.
#
#   4. Add examples to connect the server to another container that runs PostgreSQL.
#
#   5. Add examples to connect the CLI to another container that runs PostgreSQL.
#
#   6. Add script more tests to ``test_api_docker``.
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
# [1] https://github.com/heilaaks/snippy/issues
#
# [2] https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
#
# [3] https://docs.openshift.com/enterprise/3.2/creating_images/guidelines.html
#
# [4] https://docs.docker.com/engine/security/userns-remap/
#
# [5] http://www.linfo.org/uid.html
#
# [6] https://docs.docker.com/engine/security/security/#linux-kernel-capabilities
#
# [7] https://bugs.busybox.net/show_bug.cgi?id=9811
#
# [8] http://docs.gunicorn.org/en/stable/faq.html#blocking-os-fchmod
#
# [9] https://docs.docker.com/storage/tmpfs/
#
# [10] https://github.com/moby/moby/issues/37375
#
# [11] https://docs.openshift.com/container-platform/3.11/creating_images/guidelines.html
#
# [12] https://stackoverflow.com/a/54787364
#