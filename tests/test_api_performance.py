#!/usr/bin/env python3

"""test_api_performance.py: Verify that there are no major impacts to performance in API usage."""

from __future__ import print_function
from subprocess import call
from subprocess import Popen
import sys
import time
import http.client
import json
import requests
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO  # pylint: disable=import-error
else:
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
        ##        Reference PC:   1 loop :   0.1256 /   55 loop : 6.1329 / 100 loop : 10.9246
        ##        Reference PC: 880 loop : 100.9132 / 1000 loop : 115.9591
        ##        Reference PC:  10 loop : 1.0813
        ##
        ##        NOTE! Vere slow. Is the reason how requests opens the connection
        ##              for every requests?
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
        session = requests.Session()
        real_stderr = sys.stderr
        real_stdout = sys.stdout
        sys.stderr = StringIO()
        sys.stdout = StringIO()
        start = time.time()
        for _ in range(10):

            # POST four snippets in list context.
            resp = session.post(url='http://127.0.0.1:8080/api/v1/snippets',
                                headers={'content-type':'application/json; charset=UTF-8'},
                                data=json.dumps(snippets))
            assert resp.status_code == Cause.HTTP_201_CREATED
            assert len(json.loads(resp.text)) == 4

            # GET maximum of two snippets from whole snippet collection.
            resp = session.get(url='http://127.0.0.1:8080/api/v1/snippets?limit=2&sort=-brief',
                               headers={'content-type':'application/json; charset=UTF-8'})
            assert resp.status_code == Cause.HTTP_200_OK
            assert len(json.loads(resp.text)) == 2

            # GET maximum of four snippets from whole snippet collection with sall search.
            resp = session.get(url='http://127.0.0.1:8080/api/v1/snippets?sall=docker,swarm&limit=4&sort=brief',
                               headers={'content-type':'application/json; charset=UTF-8'})
            assert resp.status_code == Cause.HTTP_200_OK
            assert len(json.loads(resp.text)) == 3

            # DELETE all snippets one by one by first requesting only digests.
            resp = session.get(url='http://127.0.0.1:8080/api/v1/snippets?limit=100&fields=digest',
                               headers={'content-type':'application/json; charset=UTF-8'})
            assert resp.status_code == Cause.HTTP_200_OK
            assert len(json.loads(resp.text)) == 4
            for member in json.loads(resp.text):
                print(member['digest'])
                resp = session.delete(url='http://127.0.0.1:8080/api/v1/snippets/' + member['digest'],
                                      headers={'content-type':'application/json; charset=UTF-8'})
                assert resp.status_code == Cause.HTTP_204_NO_CONTENT

            # GET all snippets to make sure that all are deleted
            resp = session.get(url='http://127.0.0.1:8080/api/v1/snippets?limit=100',
                               headers={'content-type':'application/json; charset=UTF-8'})
            assert resp.status_code == Cause.HTTP_200_OK
            assert not json.loads(resp.text)

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
