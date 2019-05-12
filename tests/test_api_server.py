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

"""test_api_server: Test real REST API server process."""

from __future__ import print_function

import json
import re
import time

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.content import Request

pytest.importorskip('gunicorn')


class TestApiServer(object):
    """Test real REST API server performance."""

    RE_MATCH_SERVER_PORT = re.compile(r'''
        (127\.0\.0\.1):\d{1,5}    # Match server port running locally.
        ''', re.MULTILINE | re.VERBOSE)

    @pytest.mark.server
    @pytest.mark.parametrize('process', [['--server-minify-json']], indirect=True)
    def test_server_performance(self, process):  # pylint: disable=too-many-locals
        """Test API server performance.

        Note! These were invalidated when the in-memory database was
              taken into use for parallel server testing.

        Verify performance of the tool on a rough scale. The intention
        is to keep a reference test that is just iterated few times and
        the time consumed is measured. This is more for manual analysis
        than automation as of now.

        Reference PC:   1 loop :  0.0585 /   55 loop :  0.8221 / 100 loop : 1.4674
        Reference PC: 880 loop : 12.5211 / 1000 loop : 14.1784
        Reference PC:  10 loop : 0.1851

        NOTE! Vere slow. Is the reason how requests opens the connection
              for every requests?

        NOTE! Using http.client gives 20-30% performance boost over Python
              requests. Also the latencies are more constant with this.

        The reference is with sqlite database in memory as with all tests.
        There is naturally jitter in results and the values are as of now
        hand picked from few examples.

        Note that when run on Python2, will use sqlite database in disk
        that is naturally slower than memory database.

        No errors should be printed and the runtime should be below 10
        seconds. The runtime is intentionally set 10 times higher value
        than with the reference PC to cope with slow test envrironments
        """

        server = process[0]
        http = process[1]
        snippets = {
            'data': [
                {'type': 'snippet', 'attributes': Request.remove},
                {'type': 'snippet', 'attributes': Request.forced},
                {'type': 'snippet', 'attributes': Request.exited},
                {'type': 'snippet', 'attributes': Request.netcat}
            ]
        }
        start = time.time()
        for _ in range(10):

            # POST four snippets in list context.
            http.request(
                'POST',
                '/api/snippy/rest/snippets',
                json.dumps(snippets),
                {'content-type':'application/json; charset=UTF-8'}
            )
            resp = http.getresponse()
            assert resp.status == Cause.HTTP_201_CREATED
            assert len(json.loads(resp.read().decode())['data']) == 4

            # GET maximum of two snippets from whole snippet collection.
            http.request(
                'GET',
                '/api/snippy/rest/snippets?limit=2&sort=-brief'
            )
            resp = http.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert len(json.loads(resp.read().decode())['data']) == 2

            # GET maximum of four snippets from whole snippet collection with
            # sall search.
            http.request(
                'GET',
                '/api/snippy/rest/snippets?sall=docker,swarm&limit=4&sort=brief'
            )
            resp = http.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert len(json.loads(resp.read().decode())['data']) == 3

            # DELETE all snippets one by one by first requesting only digests.
            http.request(
                'GET',
                '/api/snippy/rest/snippets?limit=100&fields=digest'
            )
            resp = http.getresponse()
            body = json.loads(resp.read().decode())
            assert resp.status == Cause.HTTP_200_OK
            assert len(body['data']) == 4
            for resource_ in body['data']:
                http.request(
                    'DELETE',
                    '/api/snippy/rest/snippets/' + resource_['attributes']['digest']
                )
                resp = http.getresponse()
                assert resp.status == Cause.HTTP_204_NO_CONTENT

            # GET all snippets to make sure that all are deleted
            http.request(
                'GET',
                '/api/snippy/rest/snippets?limit=100'
            )
            resp = http.getresponse()
            assert resp.status == Cause.HTTP_404_NOT_FOUND

        runtime = time.time() - start
        server.terminate()
        server.wait()
        raw = server.stdout.readlines()
        # Convert array of byte strings to string and replace random
        # port with static port for comparison.
        out = Const.EMPTY.join(line.decode() for line in raw)
        out = self.RE_MATCH_SERVER_PORT.sub(r'\1:80', out)
        err = server.stderr.readlines()
        output = (
            'snippy server stopped at: http://127.0.0.1:80',
            ''
        )
        print("====================================")
        print("Runtime %.4f" % runtime)
        print("There are %d rows in stdout" % len(raw))
        print("There are %d rows in stderr" % len(err))
        print("====================================")
        assert out == Const.NEWLINE.join(output)
        assert not err
        assert runtime < 10

    @staticmethod
    @pytest.mark.server
    @pytest.mark.parametrize('process', [['-vv']], indirect=True)
    def test_server_logging(process):
        """Test server log configuration.

        Test that server initial log configuration is used for whole the whole
        server lifetime. The log configuration must not get reset after the
        first operation.
        """

        server = process[0]
        http = process[1]
        snippets = {
            'data': [
                {'type': 'snippet', 'attributes': Request.remove},
                {'type': 'snippet', 'attributes': Request.forced},
                {'type': 'snippet', 'attributes': Request.exited},
                {'type': 'snippet', 'attributes': Request.netcat}
            ]
        }
        start = time.time()

        http.request(
            'POST',
            '/api/snippy/rest/snippets',
            json.dumps(snippets),
            {'content-type':'application/json; charset=UTF-8'}
        )
        resp = http.getresponse()
        assert resp.status == Cause.HTTP_201_CREATED
        assert len(json.loads(resp.read().decode())['data']) == 4

        runtime = time.time() - start
        server.terminate()
        server.wait()
        out = server.stdout.readlines()
        err = server.stderr.readlines()
        print("====================================")
        print("Runtime %.4f" % runtime)
        print("There are %d rows in stdout" % len(out))
        print("There are %d rows in stderr" % len(err))
        print("====================================")
        assert sum('creating new: snippet' in str(s) for s in out) == 4
        assert not err
        assert runtime < 10

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
