#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
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

"""test_api_performance.py: Verify that there are no major impacts to performance in API usage."""

from __future__ import print_function

import json
import sys
import time

from subprocess import call
from subprocess import Popen

from snippy.cause import Cause
from snippy.config.constants import Constants as Const
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

if not Const.PYTHON2:
    import http.client as httplib # pylint: disable=import-error
    from io import StringIO  # pylint: disable=import-error
else:
    import httplib  # pylint: disable=import-error
    from StringIO import StringIO  # pylint: disable=import-error


class TestApiPerformance(object):
    """Test tool performance."""

    def test_api_performance(self):
        """Test API performance."""

        # Clear the real database and run the real server.
        call(['make', 'clean-db'])
        server = Popen(['python', './runner', '--server'])
        time.sleep(1)  # Wait untill server up. TODO: Get some indicator for this.
        snippets = {'data': [{'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.FORCED]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.EXITED]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.NETCAT]}]}

        ## Brief: Verify performance of the tool on a rough scale. The intention
        ##        is to keep a reference test that is just iterated few times and
        ##        the time consumed is measured. This is more for manual analysis
        ##        than automation as of now.
        ##
        ##        Reference PC:   1 loop :  0.0973 /   55 loop :  4.7275 / 100 loop : 8.4567
        ##        Reference PC: 880 loop : 72.8752 / 1000 loop : 83.6648
        ##        Reference PC:  10 loop : 0.8260
        ##
        ##        NOTE! Vere slow. Is the reason how requests opens the connection
        ##              for every requests?
        ##
        ##        NOTE! Using http.client gives 20-30% performance boost over Python
        ##              requests. Also the latencies are more constant with this.
        ##
        ##        The reference is with sqlite database in memory as with all tests.
        ##        There is naturally jitter in results and the values are as of now
        ##        hand picked from few examples.
        ##
        ##        Note that when run on Python2, will use sqlite database in disk
        ##        that is naturally slower than memory database.
        ##
        ##        No errors should be printed and the runtime should be below 10
        ##        seconds. The runtime is intentionally set 10 times higher value
        ##        than with the reference PC.
        conn = httplib.HTTPConnection('localhost', port=8080)
        real_stderr = sys.stderr
        real_stdout = sys.stdout
        sys.stderr = StringIO()
        sys.stdout = StringIO()
        start = time.time()
        for _ in range(10):

            # POST four snippets in list context.
            conn.request('POST',
                         '/snippy/api/v1/snippets',
                         json.dumps(snippets),
                         {'content-type':'application/json; charset=UTF-8'})
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_201_CREATED

            assert len(json.loads(resp.read().decode())['data']) == 4

            # GET maximum of two snippets from whole snippet collection.
            conn.request('GET',
                         '/snippy/api/v1/snippets?limit=2&sort=-brief')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert len(json.loads(resp.read().decode())['data']) == 2

            ## GET maximum of four snippets from whole snippet collection with sall search.
            conn.request('GET',
                         '/snippy/api/v1/snippets?sall=docker,swarm&limit=4&sort=brief')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert len(json.loads(resp.read().decode())['data']) == 3

            ## DELETE all snippets one by one by first requesting only digests.
            conn.request('GET',
                         '/snippy/api/v1/snippets?limit=100&fields=digest')
            resp = conn.getresponse()
            body = json.loads(resp.read().decode())
            assert resp.status == Cause.HTTP_200_OK
            assert len(body['data']) == 4
            for resource_ in body['data']:
                conn.request('DELETE',
                             'http://localhost:8080/snippy/api/v1/snippets/' + resource_['attributes']['digest'])
                resp = conn.getresponse()
                assert resp.status == Cause.HTTP_204_NO_CONTENT

            # GET all snippets to make sure that all are deleted
            conn.request('GET',
                         '/snippy/api/v1/snippets?limit=100')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_404_NOT_FOUND

        runtime = time.time() - start
        server.terminate()
        result_stderr = sys.stderr.getvalue().strip()
        result_stdout = sys.stdout.getvalue().strip()
        sys.stderr = real_stderr
        sys.stdout = real_stdout
        print("====================================")
        print("Runtime %.4f" % runtime)
        print("There are %d rows in stdout" % len(result_stdout))
        print("There are %d rows in stderr" % len(result_stderr))
        print("====================================")

        assert not result_stderr
        assert runtime < 10

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
