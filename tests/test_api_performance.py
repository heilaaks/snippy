#!/usr/bin/env python3

"""test_api_performance.py: Verify that there are no major impacts to performance in API usage."""

from __future__ import print_function
from subprocess import call
from subprocess import Popen
import sys
import time
import json
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
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
        snippets = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED],
                    Snippet.DEFAULTS[Snippet.EXITED], Snippet.DEFAULTS[Snippet.NETCAT]]

        ## Brief: Verify performance of the tool on a rough scale. The intention
        ##        is to keep a reference test that is just iterated few times and
        ##        the time consumed is measured. This is more for manual analysis
        ##        than automation as of now.
        ##
        ##        NOTE! There seems to be quite much variation in results that shows
        ##              in shorter runs. E.g. 1 iteration can be 0.0584 - 0.1304.
        ##              There seems to be variation of 5-20%. With short runs the
        ##              variation percentage is larger.
        ##
        ##        Reference PC:   1 loop :  0.0843 /   55 loop :  4.3813 / 100 loop : 7.8849
        ##        Reference PC: 880 loop : 69.4168 / 1000 loop : 79.0004
        ##        Reference PC:  10 loop : 0.7955
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
                         '/api/v1/snippets',
                         json.dumps(snippets),
                         {'content-type':'application/json; charset=UTF-8'})
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_201_CREATED
            assert len(json.loads(resp.read().decode())) == 4

            # GET maximum of two snippets from whole snippet collection.
            conn.request('GET',
                         '/api/v1/snippets?limit=2&sort=-brief')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert len(json.loads(resp.read().decode())) == 2

            ## GET maximum of four snippets from whole snippet collection with sall search.
            conn.request('GET',
                         '/api/v1/snippets?sall=docker,swarm&limit=4&sort=brief')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert len(json.loads(resp.read().decode())) == 3

            ## DELETE all snippets one by one by first requesting only digests.
            conn.request('GET',
                         '/api/v1/snippets?limit=100&fields=digest')
            resp = conn.getresponse()
            body = json.loads(resp.read().decode())
            assert resp.status == Cause.HTTP_200_OK
            assert len(body) == 4
            for member in body:
                print(member['digest'])
                conn.request('DELETE',
                             'http://localhost:8080/api/v1/snippets/' + member['digest'])
                resp = conn.getresponse()
                assert resp.status == Cause.HTTP_204_NO_CONTENT

            # GET all snippets to make sure that all are deleted
            conn.request('GET',
                         '/api/v1/snippets?limit=100')
            resp = conn.getresponse()
            assert resp.status == Cause.HTTP_200_OK
            assert not json.loads(resp.read().decode())

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
