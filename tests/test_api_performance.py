#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_api_performance: Test REST API server performance."""

from __future__ import print_function

import json
import time
from subprocess import call
from subprocess import Popen
from subprocess import PIPE

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet

try:
    import http.client as httplib
except ImportError:
    import httplib

pytest.importorskip('gunicorn')


class TestApiPerformance(object):
    """Test REST API server performance."""

    @pytest.mark.serial
    def test_server_performance(self):
        """Test API server performance.

        Verify performance of the tool on a rough scale. The intention
        is to keep a reference test that is just iterated few times and
        the time consumed is measured. This is more for manual analysis
        than automation as of now.

        Reference PC:   1 loop :  0.1493 /   55 loop :  5.6273 / 100 loop : 9.5056
        Reference PC: 880 loop : 89.7575 / 1000 loop : 102.4989
        Reference PC:  10 loop : 1.0330

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

        # Clear the real database and run the real server.
        call(['make', 'clean-db'])
        server = Popen(['python', './runner', '--server', '--compact-json'], stdout=PIPE, stderr=PIPE)
        time.sleep(1)  # Wait untill server is up.
        snippets = {'data': [{'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.FORCED]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.EXITED]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.NETCAT]}]}

        conn = httplib.HTTPConnection('localhost', port=8080)
        start = time.time()
        for _ in range(10):

            # POST four snippets in list context.
            conn.request('POST',
                         '/snippy/api/app/v1/snippets',
                         json.dumps(snippets),
                         {'content-type':'application/json; charset=UTF-8'})
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_201_CREATED
            assert len(json.loads(resp.read().decode())['data']) == 4

            # GET maximum of two snippets from whole snippet collection.
            conn.request('GET',
                         '/snippy/api/app/v1/snippets?limit=2&sort=-brief')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert len(json.loads(resp.read().decode())['data']) == 2

            ## GET maximum of four snippets from whole snippet collection with sall search.
            conn.request('GET',
                         '/snippy/api/app/v1/snippets?sall=docker,swarm&limit=4&sort=brief')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert len(json.loads(resp.read().decode())['data']) == 3

            ## DELETE all snippets one by one by first requesting only digests.
            conn.request('GET',
                         '/snippy/api/app/v1/snippets?limit=100&fields=digest')
            resp = conn.getresponse()
            body = json.loads(resp.read().decode())
            assert resp.status == Cause.HTTP_200_OK
            assert len(body['data']) == 4
            for resource_ in body['data']:
                conn.request('DELETE',
                             'http://localhost:8080/snippy/api/app/v1/snippets/' + resource_['attributes']['digest'])
                resp = conn.getresponse()
                assert resp.status == Cause.HTTP_204_NO_CONTENT

            # GET all snippets to make sure that all are deleted
            conn.request('GET',
                         '/snippy/api/app/v1/snippets?limit=100')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_404_NOT_FOUND

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
        assert out == [b'snippy server running at 127.0.0.1:8080\n', b'snippy server stopped at 127.0.0.1:8080\n']
        assert not err
        assert runtime < 10

    @pytest.mark.serial
    def test_server_logging(self):
        """Test server log configuration.

        Test that server initial log configuration is used for whole the whole
        server lifetime. The log configuration must not get reset after the
        first operation.
        """

        # Clear the real database and run the real server.
        call(['make', 'clean-db'])
        server = Popen(['python', './runner', '--server', '-vv'], stdout=PIPE, stderr=PIPE)
        time.sleep(1)  # Wait untill server up.
        snippets = {'data': [{'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.FORCED]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.EXITED]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.NETCAT]}]}
        conn = httplib.HTTPConnection('localhost', port=8080)
        start = time.time()

        # POST four snippets.
        conn.request('POST',
                     '/snippy/api/app/v1/snippets',
                     json.dumps(snippets),
                     {'content-type':'application/json; charset=UTF-8'})
        resp = conn.getresponse()
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
        """Teardown class."""

        Content.delete()
