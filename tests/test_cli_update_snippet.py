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

"""test_cli_update_snippet: Test workflows for updating snippets."""

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliUpdateSnippet(object):
    """Test workflows for updating snippets."""

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_001(self, snippy, edited_remove, mocker):
        """Update snippet based on digest.

        Update snippet based on short message digest. Only the content data
        is updated.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            'af8c89629dc1a531': Snippet.get_dictionary(template),
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_002(self, snippy, edited_remove, mocker):
        """Update snippet based on digest.

        Update snippet based on very short message digest. This must match to
        a single snippet that must be updated.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            'af8c89629dc1a531': Snippet.get_dictionary(template),
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', '54e41'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_003(self, snippy, edited_remove, mocker):
        """Update snippet based on digest.

        Update snippet based on long message digest. Only the content data is
        updated.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            'af8c89629dc1a531': Snippet.get_dictionary(template),
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_004(self, snippy, edited_remove, mocker):
        """Update snippet based on digest.

        Update snippet based on message digest and explicitly define the
        content category.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            'af8c89629dc1a531': Snippet.get_dictionary(template),
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '--snippet', '-d', '54e41e9b52a02b63'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_005(self, snippy, edited_remove, mocker):
        """Update snippet based on digest.

        Update snippet based on message digest and accidentally define
        solution category. In this case the snippet is updated properly
        regardless of incorrect category.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            'af8c89629dc1a531': Snippet.get_dictionary(template),
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '--solution', '-d', '54e41e9b52a02b63'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_006(self, snippy, edited_remove, mocker):
        """Update snippet based on digest.

        Try to update snippet with message digest that cannot be found. No
        changes must be made to stored content.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_007(self, snippy, edited_remove, mocker):
        """Update snippet based on digest.

        Try to update snippet with empty message digest. Nothing should be
        updated in this case because the empty digest matches to more than
        one snippet. Only one content can be updated at the time.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', ''])
        assert cause == 'NOK: cannot use empty message digest for: update :operation'
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_008(self, snippy, edited_remove, mocker):
        """Update snippet based on digest.

        Try to update snippet with one digit digest that matches two snippets.
        Note! Don't not change the test snippets because this case is produced
        with real digests that just happen to have same digit starting both of
        the cases.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', '5'])
        assert cause == 'NOK: content digest: 5 :matched more than once: 2 :preventing: update :operation'
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_009(self, snippy, edited_remove, mocker):
        """Update snippet based on content data.

        Update snippet based on content data.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            'af8c89629dc1a531': Snippet.get_dictionary(template),
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-c', 'docker rm --volumes $(docker ps --all --quiet)'])
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_010(self, snippy, edited_remove, mocker):
        """Update snippet based on content data.

        Try to update snippet based on content data that is not found.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-c', 'snippet not existing'])
        assert cause == 'NOK: cannot find content with content data: snippet not existing'
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_011(self, snippy, edited_remove, mocker):
        """Update snippet based on content data.

        Try to update snippet with empty content data. Nothing must be updated
        in this case because there is more than one content stored.
        """

        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run(['snippy', 'update', '-c', ''])
        assert cause == 'NOK: cannot use empty content data for: update :operation'
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_012(self, snippy, mocker):
        """Update snippet based on content data.

        Try to update snippet with content data that matches to two different
        snippets. Nothing must be updated in this case because content can be
        updated only if it is uniquely identified.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        cause = snippy.run(['snippy', 'update', '-c', 'docker'])
        assert cause == 'NOK: content data: docker :matched more than once: 2 :preventing: update :operation'
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)
    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
