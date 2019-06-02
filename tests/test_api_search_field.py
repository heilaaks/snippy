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

"""test_api_search_field: Test search fields API endpoint."""

from falcon import testing
import falcon
import pytest

from tests.lib.content import Content

pytest.importorskip('gunicorn')


class TestApiSearchField(object):  # pylint: disable=too-many-public-methods
    """Test GET resource attribute API."""

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_001(server):
        """Get unique content based on ``groups`` attribute.

        Send GET /groups to get unique groups from all content categories.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '82'
        }
        expect_body = {
            'data': {
                'type': 'groups',
                'attributes': {
                    'groups': {
                        'docker': 3,
                        'python': 1
                    }
                }
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_002(server):
        """Get unique content based on ``groups`` attribute.

        Send GET /groups to get unique groups only from solution category.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '69'
        }
        expect_body = {
            'data': {
                'type': 'groups',
                'attributes': {
                    'groups': {
                        'docker': 1
                    }
                }
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups',
            headers={'accept': 'application/vnd.api+json'},
            query_string='scat=solution')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_003(server):
        """Get unique content based on ``groups`` attribute.

        Send GET /groups to get unique groups. In this case the ``limit``
        query parameter is set to zero. The limit parameter does not have
        any effect in the groups API endpoint.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '82'
        }
        expect_body = {
            'data': {
                'type': 'groups',
                'attributes': {
                    'groups': {
                        'docker': 3,
                        'python': 1
                    }
                }
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups',
            headers={'accept': 'application/vnd.api+json'},
            query_string='limit=0')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_groups_004(server):
        """Get specific content based on ``groups`` attribute.

        Send GET /groups to get unique groups. In this case the ``sall``
        query parameter is used to limit the search. The search is made
        from all categories by default.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '69'
        }
        expect_body = {
            'data': {
                'type': 'groups',
                'attributes': {
                    'groups': {
                        'python': 1
                    }
                }
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=pytest')
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_groups_005(server):
        """Try to get unique content based on ``groups`` attribute.

        Try to send GET /groups to get unique groups. In this case the ``scat``
        query parameter limits the search to solution category. There are no
        resources stored in the searched category.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '365'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find unique fields for groups attribute'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/groups',
            headers={'accept': 'application/vnd.api+json'},
            query_string='scat=solution')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-kafka', 'import-pytest')
    def test_api_search_tags_001(server):
        """Get unique content based on ``tags`` attribute.

        Send GET /tags to get unique groups from all content categories.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '245'
        }
        expect_body = {
            'data': {
                'type': 'tags',
                'attributes': {
                    'tags': {
                        'docker': 3,
                        'moby': 3,
                        'cleanup': 2,
                        'container': 2,
                        'docker-ce': 2,
                        'driver': 1,
                        'kafka': 1,
                        'kubernetes': 1,
                        'logging': 1,
                        'logs2kafka': 1,
                        'plugin': 1,
                        'docs': 1,
                        'pytest': 1,
                        'python': 1
                    }
                }
            }
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_200
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_tags_002(server):
        """Try to get unique content based on ``tags`` attribute.

        Try to send GET /groups to get unique groups. In this case the ``scat``
        query parameter limits the search to solution category. There are no
        resources stored in the searched category.
        """

        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '363'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find unique fields for tags attribute'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_get(
            path='/api/snippy/rest/tags',
            headers={'accept': 'application/vnd.api+json'},
            query_string='scat=solution')
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)

    @classmethod
    def teardown_class(cls):
        """Teardown tests."""

        Content.delete()
