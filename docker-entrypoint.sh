#!/bin/sh
set -e

# Create a file that contains IP:port for the server.
# See Dockefile documentation for reasons to do this.
SERVER_HOST="${SNIPPY_SERVER_HOST}"
case ${SNIPPY_SERVER_HOST} in
  *"container.hostname"*)
  SERVER_HOST=$(echo "${SNIPPY_SERVER_HOST}" | sed -e "s/container.hostname/$(hostname -i)/g")
esac
export SNIPPY_SERVER_HOST=${SERVER_HOST}
echo "${SERVER_HOST}" > snippy-server-host

# Do not let user to configure storage path. There is
# no need for it because 'docker run --volume' always
# sets the host volume path.
exec snippy --storage-path /volume "$@"
