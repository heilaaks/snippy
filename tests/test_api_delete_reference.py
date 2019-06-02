# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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

"""test_api_delete_references: Test DELETE /references API endpoint."""

from falcon import testing
import falcon
import pytest

from tests.lib.content import Content
from tests.lib.content import Storage
from tests.lib.reference import Reference

pytest.importorskip('gunicorn')


class TestApiDeleteReference(object):
    """Test DELETE /references API endpoint."""

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_delete_reference_001(server):
        """Delete reference with digest.

        Send DELETE /references/{id} to remove a resource. The ``id`` in
        URI matches to one resource that is deleted.
        """

        storage = {
            'data': [
                Storage.gitlog,
                Storage.regexp
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/api/snippy/rest/references/1f9d9496005736ef',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest', 'caller')
    def test_api_delete_reference_002(server):
        """Try to delete reference.

        Try to send DELETE /reference{id} with ``id`` in URI does not exist.
        """

        storage = {
            'data': [
                Storage.pytest,
                Storage.gitlog,
                Storage.regexp
            ]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '370'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with content identity: beefbeef'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/api/snippy/rest/references/beefbeef',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_delete_reference_003(server):
        """Try to delete reference.

        Try to send DELETE /references without ``id`` in URI that identifies
        the deleted resource.
        """

        storage = {
            'data': [
                Storage.gitlog,
                Storage.regexp
            ]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '368'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot delete content without identified resource'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/api/snippy/rest/references',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(storage)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_delete_reference_004(server):
        """Delete reference with UUID.

        Send DELETE /references/{id} to remove one resource. The ``id``
        in URI matches to one resource that is deleted.
        """

        storage = {
            'data': [
                Storage.pytest,
                Storage.regexp
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/api/snippy/rest/references/' + Reference.GITLOG_UUID,
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(storage)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
