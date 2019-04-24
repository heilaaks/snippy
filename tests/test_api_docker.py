#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""test_api_docker: Test server in Docker."""

import pytest
import requests


class TestApiDocker(object):  # pylint: disable=too-few-public-methods
    """Test server in Docker.

    The tests require external ``dockerd`` installed correctly and usable by
    the user who runs the test cases. Usually the ``dockerd`` daemon has been
    installed by the root. You may either:

    1) Add current user to docker group that can execute Docker

       # https://docs.docker.com/install/linux/linux-postinstall/
       sudo groupadd docker
       sudo usermod -aG docker $USER
       # Log out and log back in so that your group membership is re-evaluated.

    2) Unsecurely add read and write permissions to other users for the docker
       socket.

       sudo chmod o+rw /var/run/docker.sock

    These instructions may break security rules and there is no quarantees that
    then instructions work on various operating systems.
    """

    @pytest.mark.docker
    def test_server_performance(self, docker):
        """Test server in Docker.

        Verify use case to start container with local backend (Sqlite) and
        no mounted volume on host. Container must have the default content
        imported.

        This corresponds to use case:

        ```shell
        docker run \
            --publish=127.0.0.1:8080:32768/tcp \
            --name snippy \
            --detach \
            heilaaks/snippy -vv
        ```
        """

        container = docker.containers.run(
            detach=True,
            ports={'32768/tcp': '8080'},
            image='heilaaks/snippy:latest')
        self._wait_server(container)
        result = requests.get('http://127.0.0.1:8080/api/snippy/rest/snippets')
        container.stop()
        logs = container.logs().decode().splitlines()
        container.remove()
        assert result.status_code == 200
        assert result.json()['meta']['count'] == 20
        assert result.json()['meta']['limit'] == 20
        assert len(logs) == 2

    @staticmethod
    def _wait_server(container):
        """Wait untill the server has started.

        Currently this blocks forever.

        Args:
            container (obj): Python Docker SDK Container() object.
        """

        for message in container.logs(stream=True):  # Get generator with streams=True.
            if 'snippy server running at' in message.decode():
                return
