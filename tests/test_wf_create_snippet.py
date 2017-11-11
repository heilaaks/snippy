#!/usr/bin/env python3

"""test_wf_create_snippet.py: Test workflows for creating snippets."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.editor import Editor
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfCreateSnippet(unittest.TestCase):
    """Test workflows for creating snippets."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_create_snippet_from_console(self, mock_isfile, mock__get_db_location, mock_call_editor):
        """Create snippet from console."""

        mock_isfile.return_value = True
        mock__get_db_location.return_value = Database.get_storage()

        ## Brief: Create new snippet by defining all content parameters from command line.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
            brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
            group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
            tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
            links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
            sys.argv = ['snippy', 'create', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links]  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create new snippet without defining the mandatory content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
            group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
            tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
            links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
            sys.argv = ['snippy', 'create', '--brief', brief, '--group', group, '--tags', tags, '--links', links]  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
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
            sys.argv = ['snippy', 'create', '--editor']  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
            assert cause == 'NOK: mandatory snippet data not defined'
            assert not Database.get_snippets()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create new snippet with empty data. In this case the whole template
        ##        is deleted and the edited solution is an empty string.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            mock_call_editor.return_value = Const.EMPTY
            sys.argv = ['snippy', 'create', '--editor']  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
            assert cause == 'NOK: mandatory snippet data not defined'
            assert not Database.get_snippets()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create snippet again with exactly same content than already stored.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
            brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
            group = Snippet.DEFAULTS[Snippet.REMOVE]['group']
            tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
            links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
            compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
            sys.argv = ['snippy', 'create', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links]  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: content data already exist with digest 54e41e9b52a02b63'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
