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

"""test_cli_delete_snippet: Test workflows for deleting snippets."""

import pytest

from snippy.cause import Cause
from tests.lib.content import Content
from tests.lib.snippet import Snippet


class TestCliDeleteSnippet(object):
    """Test workflows for deleting snippets."""

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_001(snippy):
        """Delete snippet with digest.

        Delete snippet with short 16 byte version of message digest.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '-d', '53908d68425c61dc'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_002(snippy):
        """Delete snippet with digest.

        Delete snippet with very short version of digest that matches to one
        snippet.
        """

        content = {
            'data': [
                Snippet.FORCED
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '-d', '54e41'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_003(snippy):
        """Delete snippet with digest.

        Delete snippet with long 16 byte version of message digest.
        """

        content = {
            'data': [
                Snippet.FORCED
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '-d', '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-remove')
    def test_cli_delete_snippet_004(snippy):
        """Delete snippet with dgiest.

        Delete snippet with empty message digest when there is only one
        content stored. In this case the last content can be deleted with
        empty digest.
        """

        Content.assert_storage_size(1)
        cause = snippy.run(['snippy', 'delete', '-d', ''])
        assert cause == Cause.ALL_OK
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_005(snippy):
        """Delete snippet with digest.

        Try to delete snippet with message digest that cannot be found.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'delete', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_006(snippy):
        """Delete snippet with dgiest.

        Try to delete snippet with empty message digest. Nothing should be
        deleted in this case because there is more than one content stored.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'delete', '-d', ''])
        assert cause == 'NOK: cannot use empty message digest for delete operation'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_007(snippy):
        """Delete snippet with dgiest.

        Try to delete snippet with short version of digest that does not match
        to any existing message digest.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'delete', '-d', '123456'])
        assert cause == 'NOK: cannot find content with message digest: 123456'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_008(snippy):
        """Delete snippet with data.

        Delete snippet based on content data.
        """

        content = {
            'data': [
                Snippet.FORCED
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '--content', 'docker rm --volumes $(docker ps --all --quiet)'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_009(snippy):
        """Delete snippet with data.

        Try to delete snippet with content data that does not exist. In this
        case the content data is not truncated.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--content', 'not found content'])
        assert cause == 'NOK: cannot find content with content data: not found content'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_010(snippy):
        """Delete snippet with data.

        Try to delete snippet with content data that does not exist. In this
        case the content data is truncated.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--content', 'docker rm --volumes $(docker ps --all)'])
        assert cause == 'NOK: cannot find content with content data: docker rm --volumes $(docker p...'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_011(snippy):
        """Delete snippet with data.

        Try to delete snippet with empty content data. Nothing should be
        deleted in this case because there is more than one content left.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--content', ''])
        assert cause == 'NOK: cannot use empty content data for delete operation'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_012(snippy):
        """Delete snippet with search.

        Delete snippet based on search keyword that results one hit. In this
        case the content is deleted.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '--sall', 'redis'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_delete_snippet_013(snippy, capsys):
        """Delete snippet with search keyword matching more than once.

        Delete snippet based on search keyword that results more than one hit.
        In this case the error text is read from stdout and it must contain
        the error string.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--sall', 'docker'])
        out, _ = capsys.readouterr()
        assert cause == 'NOK: search keywords matched 2 times preventing delete operation'
        assert out == 'NOK: search keywords matched 2 times preventing delete operation\n'
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
