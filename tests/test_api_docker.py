# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

from snippy.constants import Constants as Const


class TestApiDocker(object):  # pylint: disable=too-few-public-methods
    """Test server in Docker.

    The tests require external ``dockerd`` installed correctly and usable by
    the user who runs the test cases. Usually the ``dockerd`` daemon has been
    installed by the root and tests are run by different user. You may either:

    1) Add current user to docker group that can execute Docker

       # https://docs.docker.com/install/linux/linux-postinstall/
       sudo groupadd docker
       sudo usermod -aG docker $USER
       # Log out and log back in so that your group membership is re-evaluated.

    2) Unsecurely add read and write permissions to other users for the docker
       socket.

       sudo chmod o+rw /var/run/docker.sock

    These instructions may break security rules and there is no guarantees that
    the instructions work on various operating systems.
    """

    @pytest.mark.docker
    def test_docker_server_001(self, docker):
        """Test server in Docker.

        Verify use case to start container with local backend (Sqlite) and
        no mounted volume on host. Container must have the default content
        imported.

        This does not verify container healthceck command.

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
            ports={'32768/tcp': '32768'},
            image='heilaaks/snippy:latest')
        self._wait_server(container)
        result = requests.get('http://127.0.0.1:32768/api/snippy/rest/snippets')
        container.stop()
        logs = container.logs().decode().splitlines()
        container.remove()
        assert result.status_code == 200
        assert result.json()['meta']['count'] == 20
        assert result.json()['meta']['limit'] == 20
        assert len(logs) == 2

    @pytest.mark.docker
    def test_docker_server_002(self, docker):
        """Test server in Docker.

        Verify use case to start container with local backend (Sqlite) and
        no mounted volume on host. Container must have the default content
        imported. In this case the user has been set explicitly from host
        and it is different than the user UID that starts the container.

        This does not verify container healthceck command.

        This corresponds to use case:

        ```shell
        docker run \
            --user 1000 \
            --publish=127.0.0.1:8080:32768/tcp \
            --name snippy \
            --detach \
            heilaaks/snippy -vv
        ```
        """

        container = docker.containers.run(
            detach=True,
            user=1000,
            ports={'32768/tcp': '32769'},
            image='heilaaks/snippy:latest')
        self._wait_server(container)
        result = requests.get('http://127.0.0.1:32769/api/snippy/rest/snippets')
        container.stop()
        logs = container.logs().decode().splitlines()
        container.remove()
        assert result.status_code == 200
        assert result.json()['meta']['count'] == 20
        assert result.json()['meta']['limit'] == 20
        assert len(logs) == 2

    @pytest.mark.docker
    def test_docker_server_003(self, docker):
        """Test server in Docker.

        Verify use case to start container with local backend (Sqlite) and
        no mounted volume on host. Container must have the default content
        imported. In this case the server REST API base path has been set
        to other than default value.

        This does not verify container healthceck command.

        This corresponds to use case:

        ```shell
        docker run \
            --env SNIPPY_SERVER_BASE_PATH_REST=/api/ \
            --publish=127.0.0.1:8080:32768/tcp \
            --name snippy \
            --detach \
            heilaaks/snippy -vv
        ```
        """

        container = docker.containers.run(
            detach=True,
            environment={'SNIPPY_SERVER_BASE_PATH_REST': '/api/'},
            ports={'32768/tcp': '32770'},
            image='heilaaks/snippy:latest')
        self._wait_server(container)
        result = requests.get('http://127.0.0.1:32770/api/snippets')
        container.stop()
        logs = container.logs().decode().splitlines()
        container.remove()
        assert result.status_code == 200
        assert result.json()['meta']['count'] == 20
        assert result.json()['meta']['limit'] == 20
        assert len(logs) == 2

    @staticmethod
    @pytest.mark.docker
    def test_docker_server_004(docker):
        """Test server in Docker.

        Verify docker container usage as a command line tool. In thi case
        the server must not be started. The command output must be visible
        in stdout

        This corresponds to use case:

        ```shell
        docker run \
            --rm \
            --env SNIPPY_LOG_JSON=0 \
            heilaaks/snippy search --sall docker
        ```
        """

        output = (
            '1. Manage Elasticsearch plugins @elasticsearch [93ee5c79e510dd65]',
            '',
            '   $ curl -XGET -u elastic:changeme "http://${HOSTNAME}:9200/_cat/plugins"',
            '   $ curl -XGET -u elastic:changeme "http://${HOSTNAME}:9200/_nodes/plugins?filter_path=**.plugins.name&pretty"',
            '',
            '   # api,elastic,elasticsearch,plugin,rest,x-pack',
            '   > https://www.elastic.co/guide/en/elasticsearch/plugins/current/intro.html',
            '',
            'OK',
            ''
        )
        stdout = docker.containers.run(
            detach=False,
            remove=True,
            stdout=True,
            environment={'SNIPPY_LOG_JSON': '0'},
            image='heilaaks/snippy:latest',
            command=['search', '--sgrp', 'elasticsearch', '--sall', 'plugins', '--no-ansi'])
        assert stdout.decode() == Const.NEWLINE.join(output)

    @pytest.mark.docker
    def test_docker_server_005(self, docker):
        """Test server in Docker.

        Verify that docker container can be run when the container filesystem
        is set to readonly. The server requires always a remporary folder where
        to write server healthcheck. Because of this, there must be the tmpfs.

        This is related to Gunigorn server and functionality related to [1].

        This corresponds to use case:

        ```shell
        docker run \
            --user 1000 \
            --publish=127.0.0.1:8080:32768/tcp \
            --name snippy \
            --read-only \
            --tmpfs /tmp \
            --detach \
            heilaaks/snippy --server-readonly
        ```

        [1] http://docs.gunicorn.org/en/stable/faq.html#blocking-os-fchmod
        """

        container = docker.containers.run(
            detach=True,
            user=1000,
            read_only=True,
            tmpfs={'/tmp': 'size=1M,uid=1000'},
            ports={'32768/tcp': '32771'},
            image='heilaaks/snippy:latest',
            command=['--server-readonly'])
        self._wait_server(container)
        result = requests.get('http://127.0.0.1:32771/api/snippy/rest/snippets?limit=20')
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
