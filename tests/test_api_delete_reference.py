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

"""test_api_delete_references: Test DELETE references API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiDeleteReference(object):
    """Test DELETE references API."""

    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_delete_reference_001(self, server, mocker):
        """Delete reference with digest.

        Call DELETE /references/1f9d9496005736ef that matches one reference
        that is deleted.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        result_headers = {}
        assert len(Database.get_references()) == 3
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/references/1f9d9496005736ef',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert result.status == falcon.HTTP_204
        assert len(Database.get_references()) == 2
        Content.verified(mocker, server, content_read)

    @pytest.mark.usefixtures('default-references', 'import-pytest', 'caller')
    def test_api_delete_reference_002(self, server):
        """Try to delete reference.

        Try to DELETE reference with resource location that does not exist.
        """
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with message digest: beefbeef'
            }]
        }
        assert len(Database.get_references()) == 3
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/references/beefbeef',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_references()) == 3

    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_delete_reference_003(self, server, mocker):
        """Try to delete reference.

        Try to call DELETE /references without digest identifying delete
        reource.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot delete content without identified resource'
            }]
        }
        assert len(Database.get_collection()) == 2
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404
        assert len(Database.get_references()) == 2
        Content.verified(mocker, server, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
