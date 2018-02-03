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

"""test_wf_create_snippet.py: Test workflows for creating snippets."""

import mock

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.editor import Editor
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfCreateSnippet(object):
    """Test workflows for creating snippets."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_create_snippet_from_cli(self, mock_isfile, mock_storage_file, mock_call_editor):
        """Create snippet from CLI."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Create new snippet by defining all content parameters from command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
            brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
            group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
            tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
            links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'create', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Create new snippet with all content parameters but only one tag.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
            brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
            group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
            tags = Snippet.DEFAULTS[Snippet.REMOVE]['tags'][0]
            links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
            snippet_remove = Snippet.DEFAULTS[Snippet.REMOVE].copy()
            snippet_remove['tags'] = [Snippet.DEFAULTS[Snippet.REMOVE]['tags'][0]]
            compare_content = {'f94cf88b1546a8fd': snippet_remove}
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'create', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create new snippet without defining mandatory content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
            group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
            tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
            links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'create', '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow
            assert cause == 'NOK: mandatory snippet data not defined'
            assert not Database.get_snippets()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create new snippet without any changes to snippet template. In
        ##        case of snippets, the error cause is always complaining about missing
        ##        content data even when no changes are made to template.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Const.NEWLINE.join(Snippet.TEMPLATE)
            mock_call_editor.return_value = template
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'create', '--editor'])  ## workflow
            assert cause == 'NOK: mandatory snippet data not defined'
            assert not Database.get_snippets()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create new snippet with empty data. In this case the whole template
        ##        is deleted and the edited solution is an empty string.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            mock_call_editor.return_value = Const.EMPTY
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'create', '--editor'])  ## workflow
            assert cause == 'NOK: could not identify edited content category - please keep tags in place'
            assert not Database.get_snippets()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create snippet again with exactly same content than already stored.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
            brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
            group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
            tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
            links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
            cause = snippy.run_cli(['snippy', 'create', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow # pylint: disable=line-too-long
            assert cause == 'NOK: content data already exist with digest 54e41e9b52a02b63'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
