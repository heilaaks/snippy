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

"""api_rest_client: Snippy REST API client."""

from __future__ import print_function

import json
import time

from tests.testlib.snippet_helper import SnippetHelper as Snippet

try:
    import http.client as httplib
except ImportError:
    import httplib


class RestApiPerformance(object):
    """Test REST API performance."""

    def run(self, iterations):
        """Test REST API server performance.

        This is external client not intended to integrate to Snippy tool
        in any way. There is no connection to Snippy test suite with this
        client. This is just a play around client to verify things like
        perfromance of PyPy based server.
        
        No documentation provided for this client.

        Reference PC: N/A loop : N/A / N/A loop : N/A / 100 loop : N/A
        Reference PC: N/A loop : N/A / N/A loop : N/A
        Reference PC: N/A loop : N/A
        """

        snippets = {'data': [{'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.REMOVE]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.FORCED]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.EXITED]},
                             {'type': 'snippet', 'attributes': Snippet.DEFAULTS[Snippet.NETCAT]}]}

        conn = httplib.HTTPConnection('localhost', port=8080)
        start = time.time()
        for _ in range(iterations):

            ## DELETE all snippets one by one by first requesting only digests.
            conn.request('GET',
                         '/snippy/api/app/v1/snippets?limit=100&fields=digest')
            resp = conn.getresponse()
            body = json.loads(resp.read().decode())
            assert resp.status in (200, 404)
            if 'data' in body:
                for resource_ in body['data']:
                    conn.request('DELETE',
                                 'http://localhost:8080/snippy/api/app/v1/snippets/' + resource_['attributes']['digest'])
                    resp = conn.getresponse()
                    assert resp.status == 204

            # GET all snippets to make sure that all are deleted
            conn.request('GET',
                         '/snippy/api/app/v1/snippets?limit=100')
            resp = conn.getresponse()
            assert resp.status == 404

            # POST four snippets in list context.
            conn.request('POST',
                         '/snippy/api/app/v1/snippets',
                         json.dumps(snippets),
                         {'content-type':'application/json; charset=UTF-8'})
            resp = conn.getresponse()
            assert resp.status == 201
            assert len(json.loads(resp.read().decode())['data']) == 4

            # GET maximum of two snippets from whole snippet collection.
            conn.request('GET',
                         '/snippy/api/app/v1/snippets?limit=2&sort=-brief')
            resp = conn.getresponse()
            assert resp.status == 200
            assert len(json.loads(resp.read().decode())['data']) == 2

            ## GET maximum of four snippets from whole snippet collection with sall search.
            conn.request('GET',
                         '/snippy/api/app/v1/snippets?sall=docker,swarm&limit=4&sort=brief')
            resp = conn.getresponse()
            assert resp.status == 200
            assert len(json.loads(resp.read().decode())['data']) == 3

        runtime = time.time() - start
        print("====================================")
        print("Runtime %.4f" % runtime)
        print("====================================")


# Warming
perf = RestApiPerformance()
perf.run(1000)

# Testing
perf.run(1000)
