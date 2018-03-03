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

import mock
import pytest

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.source.editor import Editor
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliUpdateSnippet(object):
    """Test workflows for updating snippets."""

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_cli_update_snippet_001(self, snippy, edited_remove, mocker):
        """Update snippet based on digest."""

        ## Brief: Update snippet based on short message digest. Only the
        ##        content data is updated.
        template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
        template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
        content_read = {
            'af8c89629dc1a531': Snippet.get_dictionary(template),
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        edited_remove.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '-d', '54e41e9b52a02b63'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_snippets()) == 2
        Content.verified(mocker, snippy, content_read)

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_update_snippet_with_digest(self, mock_isfile, mock_storage_file, mock_call_editor):
        """Update snippet based on digest."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Update snippet based on very short message digest. This must match to a single
        ##        snippet that must be updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '-d', '54e41'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'af8c89629dc1a531': Snippet.get_dictionary(template),
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update snippet based on long message digest. Only the content data is updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '-d', '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'af8c89629dc1a531': Snippet.get_dictionary(template),
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update snippet based on message digest and explicitly define the content
        ##        category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '--snippet', '-d', '54e41e9b52a02b63'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'af8c89629dc1a531': Snippet.get_dictionary(template),
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update snippet based on message digest and accidentally define solution
        ##        category. In this case the snippet is updated properly regardless of
        ##        incorrect category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', '54e41e9b52a02b63'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'af8c89629dc1a531': Snippet.get_dictionary(template),
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet with message digest that cannot be found. No changes must
        ##        be made to stored content.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '-d', '123456789abcdef0'])  ## workflow
            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet with empty message digest. Nothing should be updated
        ##        in this case because the empty digest matches to more than one snippet. Only
        ##        one content can be updated at the time.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '-d', ''])  ## workflow
            assert cause == 'NOK: cannot use empty message digest to update content'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet with one digit digest that matches two snippets. Note!
        ##        not change the snippets because this case is produced with real message digests
        ##        that just happen to have same digit starting both of the cases.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '-d', '5'])  ## workflow
            assert cause == 'NOK: given digest 5 matches (2) more than once preventing the operation'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_update_snippet_with_data(self, mock_isfile, mock_storage_file, mock_call_editor):
        """Update snippet based on content data."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Update snippet based on content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults()
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            cause = snippy.run_cli(['snippy', 'update', '-c', 'docker rm --volumes $(docker ps --all --quiet)'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'af8c89629dc1a531': Snippet.get_dictionary(template),
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet based on content data that is not found.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '-c', 'snippet not existing'])  ## workflow
            assert cause == 'NOK: cannot find content with content data \'snippet not existing\''
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update snippet with empty content data. Nothing must be updated
        ##        in this case because there is more than one content stored.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
            template = template.replace('docker rm --volumes $(docker ps --all --quiet)', 'docker images')
            mock_call_editor.return_value = template
            snippy = Snippet.add_defaults()
            cause = snippy.run_cli(['snippy', 'update', '-c', ''])  ## workflow
            assert cause == 'NOK: cannot use empty content data to update content'
            assert len(Database.get_snippets()) == 2
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
