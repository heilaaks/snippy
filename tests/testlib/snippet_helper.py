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

"""snippet_helper.py: Helper methods for snippet testing."""

import mock
import six

from snippy.cause.cause import Cause
from snippy.config.constants import Constants as Const
from snippy.config.source.parser import Parser
from snippy.content.content import Content
from snippy.metadata import __homepage__
from snippy.metadata import __version__
from snippy.migrate.migrate import Migrate
from snippy.snip import Snippy
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class SnippetHelper(object):
    """Helper methods for snippet testing."""

    UTC1 = '2017-10-14 19:56:31'
    UTC2 = '2017-10-20 07:08:45'
    REMOVE = 0
    FORCED = 1
    EXITED = 2
    NETCAT = 3
    DEFAULTS = ({'data': ('docker rm --volumes $(docker ps --all --quiet)', ),
                 'brief': 'Remove all docker containers with volumes',
                 'group': 'docker',
                 'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
                 'links': ('https://docs.docker.com/engine/reference/commandline/rm/', ),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'utc': '2017-10-14 19:56:31',
                 'digest': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'},
                {'data': ('docker rm --force redis', ),
                 'brief': 'Remove docker image with force',
                 'group': 'docker',
                 'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
                 'links': ('https://docs.docker.com/engine/reference/commandline/rm/',
                           'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-' +
                           'images-containers-and-volumes'),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'utc': '2017-10-14 19:56:31',
                 'digest': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5'},
                {'data': ('docker rm $(docker ps --all -q -f status=exited)',
                          'docker images -q --filter dangling=true | xargs docker rmi'),
                 'brief': 'Remove all exited containers and dangling images',
                 'group': 'docker',
                 'tags': ('docker-ce', 'docker', 'moby', 'container', 'cleanup', 'image'),
                 'links': ('https://docs.docker.com/engine/reference/commandline/rm/',
                           'https://docs.docker.com/engine/reference/commandline/images/',
                           'https://docs.docker.com/engine/reference/commandline/rmi/'),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'utc': '2017-10-20 07:08:45',
                 'digest': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73'},
                {'data': ('nc -v 10.183.19.189 443',
                          'nmap 10.183.19.189'),
                 'brief': 'Test if specific port is open',
                 'group': 'linux',
                 'tags': ('linux', 'netcat', 'networking', 'port'),
                 'links': ('https://www.commandlinux.com/man-page/man1/nc.1.html',),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'utc': '2017-10-20 07:08:45',
                 'digest': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d'})

    TEMPLATE = ('# Commented lines will be ignored.',
                '#',
                '# Add mandatory snippet below.',
                '',
                '',
                '# Add optional brief description below.',
                '',
                '',
                '# Add optional single group below.',
                'default',
                '',
                '# Add optional comma separated list of tags below.',
                '',
                '',
                '# Add optional links below one link per line.',
                '',
                '')

    @staticmethod
    def get_metadata(utc):
        """Return the default metadata for exported data."""

        metadata = {'utc': utc,
                    'version': __version__,
                    'homepage': __homepage__}

        return metadata

    @staticmethod
    def get_http_metadata():
        """Return the default HTTP metadata."""

        metadata = {'version': __version__,
                    'homepage': __homepage__}

        return metadata

    @staticmethod
    def get_content(text=None, snippet=None):
        """Transform text template to content."""

        if text:
            contents = Parser.read_content(Content(category=Const.SNIPPET), text, SnippetHelper.UTC1)
            content = contents[0]
            content.update_digest()
        else:
            content = Content.load({'content': [SnippetHelper.DEFAULTS[snippet]]})[0]

        return content

    @staticmethod
    def get_dictionary(template):
        """Transform template to dictinary."""

        content = SnippetHelper.get_content(text=template)
        dictionary = Migrate.get_dictionary_list([content])

        return dictionary[0]

    @staticmethod
    def get_template(dictionary):
        """Transform dictionary to text template."""

        contents = Content.load({'content': [dictionary]})

        return contents[0].convert_text()

    @staticmethod
    def add_defaults(snippy=None):
        """Add default snippets for testing purposes."""

        if not snippy:
            snippy = Snippy()

        mocked_open = mock.mock_open(read_data=SnippetHelper.get_template(SnippetHelper.DEFAULTS[SnippetHelper.REMOVE]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            cause = snippy.run_cli(['snippy', 'import', '-f', 'one-snippet.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1

        mocked_open = mock.mock_open(read_data=SnippetHelper.get_template(SnippetHelper.DEFAULTS[SnippetHelper.FORCED]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            cause = snippy.run_cli(['snippy', 'import', '-f', 'one-snippet.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2

        return snippy

    @staticmethod
    def add_one(index, snippy=None):
        """Add one default snippet for testing purposes."""

        if not snippy:
            snippy = Snippy()

        mocked_open = mock.mock_open(read_data=SnippetHelper.get_template(SnippetHelper.DEFAULTS[index]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            contents = len(Database.get_snippets())
            cause = snippy.run_cli(['snippy', 'import', '-f', 'one-snippet.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == contents + 1

        return snippy

    @staticmethod
    def sorted_json_list(json_data):
        """Sort list of JSONs but keep the oder of main level list containing JSONs."""

        json_list = []
        if isinstance(json_data, list):
            json_list = (json_data)
        else:
            json_list.append(json_data)

        jsons = []
        for json_item in json_list:
            jsons.append(SnippetHelper.sorted_json(json_item))

        return tuple(jsons)

    @staticmethod
    def sorted_json(json):
        """Sort nested JSON to allow comparison."""

        if isinstance(json, dict):
            return sorted((k, SnippetHelper.sorted_json(v)) for k, v in json.items())
        if isinstance(json, (list, tuple)):
            return sorted(SnippetHelper.sorted_json(x) for x in json)

        return json

    @staticmethod
    def test_content(snippy, mock_file, dictionary):
        """Compare given dictionary against content stored in database based on message digest."""

        for digest in dictionary:
            mock_file.reset_mock()
            cause = snippy.run_cli(['snippy', 'export', '-d', digest, '-f', 'defined-content.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-content.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(SnippetHelper.get_template(dictionary[digest])),
                                                mock.call(Const.NEWLINE)])

    @staticmethod
    def test_content2(dictionary):
        """Compare given dictionary against content stored in database based on message digest."""

        snippy = Snippy()
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            for digest in dictionary:
                mock_file.reset_mock()
                cause = snippy.run_cli(['snippy', 'export', '-d', digest, '-f', 'defined-content.txt'])
                assert cause == Cause.ALL_OK
                mock_file.assert_called_once_with('defined-content.txt', 'w')
                file_handle = mock_file.return_value.__enter__.return_value
                file_handle.write.assert_has_calls([mock.call(SnippetHelper.get_template(dictionary[digest])),
                                                    mock.call(Const.NEWLINE)])

    @staticmethod
    def compare_db(snippet, content):
        """Compare snippets in database format to content format."""

        # Test that all fields excluding id and onwards are equal.
        assert snippet[Const.DATA] == content.get_data(Const.STRING_CONTENT)
        assert snippet[Const.BRIEF] == content.get_brief(Const.STRING_CONTENT)
        assert snippet[Const.GROUP] == content.get_group(Const.STRING_CONTENT)
        assert snippet[Const.TAGS] == content.get_tags(Const.STRING_CONTENT)
        assert snippet[Const.LINKS] == content.get_links(Const.STRING_CONTENT)
        assert snippet[Const.CATEGORY] == content.get_category(Const.STRING_CONTENT)
        assert snippet[Const.FILENAME] == content.get_filename(Const.STRING_CONTENT)
        assert snippet[Const.RUNALIAS] == content.get_runalias(Const.STRING_CONTENT)
        assert snippet[Const.VERSIONS] == content.get_versions(Const.STRING_CONTENT)
        assert snippet[Const.DIGEST] == content.get_digest(Const.STRING_CONTENT)
        assert snippet[Const.METADATA] == content.get_metadata(Const.STRING_CONTENT)

        # Test that tags and links are lists and rest of the fields strings.
        assert isinstance(snippet[Const.DATA], six.string_types)
        assert isinstance(snippet[Const.BRIEF], six.string_types)
        assert isinstance(snippet[Const.GROUP], six.string_types)
        assert isinstance(snippet[Const.TAGS], six.string_types)
        assert isinstance(snippet[Const.LINKS], six.string_types)
        assert isinstance(snippet[Const.CATEGORY], six.string_types)
        assert isinstance(snippet[Const.FILENAME], six.string_types)
        assert isinstance(snippet[Const.RUNALIAS], six.string_types)
        assert isinstance(snippet[Const.VERSIONS], six.string_types)
        assert isinstance(snippet[Const.DIGEST], six.string_types)
