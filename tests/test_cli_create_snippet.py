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

"""test_cli_create_snippet: Test workflows for creating snippets."""

import pytest

from snippy.cause import Cause
from snippy.config.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliCreateSnippet(object):
    """Test workflows for creating snippets."""

    @pytest.mark.usefixtures('snippy')
    def test_cli_create_snippet_001(self, snippy, mocker):
        """Create snippet from CLI."""

        ## Brief: Create new snippet by defining all content parameters from
        ##        command line.
        content_read = {Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]}
        data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
        tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run_cli(['snippy', 'create', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy')
    def test_cli_create_snippet_002(self, snippy, mocker):
        """Create snippet from CLI."""

        ## Brief: Create new snippet with all content parameters but only
        ##        one tag.
        snippet_remove = Snippet.DEFAULTS[Snippet.REMOVE].copy()
        snippet_remove['tags'] = [Snippet.DEFAULTS[Snippet.REMOVE]['tags'][0]]
        content_read = {'f94cf88b1546a8fd': snippet_remove}
        data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
        tags = Snippet.DEFAULTS[Snippet.REMOVE]['tags'][0]
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run_cli(['snippy', 'create', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy')
    def test_cli_create_snippet_003(self, snippy):
        """Try to create snippet from CLI."""

        ## Brief: Try to create new snippet without defining mandatory
        ##        content data.
        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
        tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run_cli(['snippy', 'create', '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow
        assert cause == 'NOK: mandatory snippet data not defined'
        assert not Database.get_snippets()

    @pytest.mark.usefixtures('snippy', 'edit-snippet-template')
    def test_cli_create_snippet_004(self, snippy):
        """Try to create snippet from CLI."""

        ## Brief: Try to create new snippet without any changes to snippet
        ##        template. In case of snippets, the error cause is always
        ##        complaining about missing content data even when no changes
        ##        are made to template.
        cause = snippy.run_cli(['snippy', 'create', '--editor'])  ## workflow
        assert cause == 'NOK: mandatory snippet data not defined'
        assert not Database.get_snippets()

    @pytest.mark.usefixtures('snippy', 'edit-empty')
    def test_cli_create_snippet_005(self, snippy):
        """Try to create snippet from CLI."""

        ## Brief: Try to create new snippet with empty data. In this case the
        ##        whole template is deleted and the edited solution is an
        ##        empty string.
        cause = snippy.run_cli(['snippy', 'create', '--editor'])  ## workflow
        assert cause == 'NOK: could not identify edited content category - please keep tags in place'
        assert not Database.get_snippets()

    @pytest.mark.usefixtures('snippy', 'default-snippets', 'edit-remove')
    def test_cli_create_snippet_006(self, snippy, mocker):
        """Try to create snippet from CLI."""

        ## Brief: Try to create snippet again with exactly same content than
        ##        already stored.
        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
        tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run_cli(['snippy', 'create', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow # pylint: disable=line-too-long
        assert cause == 'NOK: content data already exist with digest 54e41e9b52a02b63'
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
