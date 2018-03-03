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

"""test_cli_delete_snippet: Test workflows for deleting snippets."""

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliDeleteSnippet(object):
    """Test workflows for deleting snippets."""

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_001(self, snippy, mocker):
        """Delete snippet with digest."""

        ## Brief: Delete snippet with short 16 byte version of message digest.
        content_read = {Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]}
        cause = snippy.run_cli(['snippy', 'delete', '-d', '53908d68425c61dc'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_002(self, snippy, mocker):
        """Delete snippet with digest."""

        ## Brief: Delete snippet with very short version of digest that
        #         matches to one snippet.
        content_read = {Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]}
        cause = snippy.run_cli(['snippy', 'delete', '-d', '54e41'])  ## workflow)
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_003(self, snippy, mocker):
        """Delete snippet with digest."""

        ## Brief: Delete snippet with long 16 byte version of message digest.
        content_read = {Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]}
        cause = snippy.run_cli(['snippy', 'delete', '-d', '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'remove')
    def test_cli_delete_snippet_004(self, snippy):
        """Delete snippet with dgiest."""

        ## Brief: Delete snippet with empty message digest when there is only
        ##        one content stored. In this case the last content can be
        ##        deleted with empty digest.
        cause = snippy.run_cli(['snippy', 'delete', '-d', ''])  ## workflow
        assert cause == Cause.ALL_OK
        assert not Database.get_snippets()

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_005(self, snippy, mocker):
        """Delete snippet with dgiest."""

        ## Brief: Try to delete snippet with message digest that cannot be
        ##        found.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run_cli(['snippy', 'delete', '-d', '123456789abcdef0'])  ## workflow
        assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_006(self, snippy, mocker):
        """Delete snippet with dgiest."""

        ## Brief: Try to delete snippet with empty message digest. Nothing
        ##        should be deleted in this case because there is more than
        ##        one content stored.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run_cli(['snippy', 'delete', '-d', ''])  ## workflow
        assert cause == 'NOK: cannot use empty message digest to delete content'
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_007(self, snippy, mocker):
        """Delete snippet with dgiest."""

        ## Brief: Try to delete snippet with short version of digest that
        ##        does not match to any existing message digest.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run_cli(['snippy', 'delete', '-d', '123456'])  ## workflow
        assert cause == 'NOK: cannot find content with message digest 123456'
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_008(self, snippy, mocker):
        """Delete snippet with data."""

        ## Brief: Delete snippet based on content data.
        content_read = {Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]}
        cause = snippy.run_cli(['snippy', 'delete', '--content', 'docker rm --volumes $(docker ps --all --quiet)'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_009(self, snippy, mocker):
        """Delete snippet with data."""

        ## Brief: Try to delete snippet with content data that does not exist.
        ##        In this case the content data is not truncated.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run_cli(['snippy', 'delete', '--content', 'not found content'])  ## workflow
        assert cause == 'NOK: cannot find content with content data \'not found content\''
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_0010(self, snippy, mocker):
        """Delete snippet with data."""

        ## Brief: Try to delete snippet with content data that does not exist.
        ##        In this case the content data is truncated.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run_cli(['snippy', 'delete', '--content', 'docker rm --volumes $(docker ps --all)'])  ## workflow
        assert cause == 'NOK: cannot find content with content data \'docker rm --volumes $(docker p...\''
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_011(self, snippy, mocker):
        """Delete snippet with data."""

        ## Brief: Try to delete snippet with empty content data. Nothing
        ##        should be deleted in this case because there is more than
        ##        one content left.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run_cli(['snippy', 'delete', '--content', ''])  ## workflow
        assert cause == 'NOK: cannot use empty content data to delete content'
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_012(self, snippy, mocker):
        """Delete snippet with search."""

        ## Brief: Delete snippet based on search keyword that results one hit.
        ##        In this case the content is deleted.
        content_read = {Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]}
        cause = snippy.run_cli(['snippy', 'delete', '--sall', 'redis'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_013(self, snippy, mocker):
        """Delete snippet with search."""

        ## Brief: Delete snippet based on search keyword that results more
        ##        than one hit. In this case the content must not be deleted.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run_cli(['snippy', 'delete', '--sall', 'docker'])  ## workflow
        assert cause == 'NOK: given search keyword matches (2) more than once preventing the operation'
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_delete_snippet_014(self, snippy, mocker, capsys):
        """Delete snippet with data."""

        ## Brief: Delete snippet based on search keyword that results more
        ##        than one hit. In this case the error text is read from
        ##        stdout and it must contain the error string.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run_cli(['snippy', 'delete', '--sall', 'docker'])  ## workflow
        out, _ = capsys.readouterr()
        assert cause == 'NOK: given search keyword matches (2) more than once preventing the operation'
        assert out == 'NOK: given search keyword matches (2) more than once preventing the operation\n'
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
