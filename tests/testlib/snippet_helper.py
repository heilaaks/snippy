#!/usr/bin/env python3

"""snippet_helper.py: Helper methods for snippet testing."""

import sys
import six
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.editor import Editor
from snippy.content.content import Content
from snippy.migrate.migrate import Migrate
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class SnippetHelper(object):
    """Helper methods for snippet testing."""

    UTC = '2017-10-14 19:56:31'
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
                 'utc': '2017-10-20 07:08:45',
                 'digest': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5'})

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
    def get_content(text=None, snippet=None):
        """Transform text template to content."""

        if text:
            content = Content(content=(Const.EMPTY,)*11, category=Const.SNIPPET)
            editor = Editor(Content(content=(Const.EMPTY,)*11, category=Const.SNIPPET), SnippetHelper.UTC, text)
            content.set((editor.get_edited_data(),
                         editor.get_edited_brief(),
                         editor.get_edited_group(),
                         editor.get_edited_tags(),
                         editor.get_edited_links(),
                         editor.get_edited_category(),
                         editor.get_edited_filename(),
                         editor.get_edited_date(),
                         content.get_digest(),
                         content.get_metadata(),
                         content.get_key()))
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
        editor = Editor(contents[0], SnippetHelper.UTC)

        return editor.get_template()

    @staticmethod
    def add_defaults(snippy):
        """Add default snippets for testing purposes."""

        if not snippy:
            snippy = Snippy()

        mocked_open = mock.mock_open(read_data=SnippetHelper.get_template(SnippetHelper.DEFAULTS[SnippetHelper.REMOVE]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            sys.argv = ['snippy', 'import', '-f', 'one-snippet.txt']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1

        mocked_open = mock.mock_open(read_data=SnippetHelper.get_template(SnippetHelper.DEFAULTS[SnippetHelper.FORCED]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            sys.argv = ['snippy', 'import', '-f', 'one-snippet.txt']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2

        return snippy

    @staticmethod
    def add_one(snippy, index):
        """Add one default snippet for testing purposes."""

        if not snippy:
            snippy = Snippy()

        mocked_open = mock.mock_open(read_data=SnippetHelper.get_template(SnippetHelper.DEFAULTS[index]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            sys.argv = ['snippy', 'import', '-f', 'one-snippet.txt']
            contents = len(Database.get_snippets())
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == contents + 1

        return snippy

    @staticmethod
    def test_content(snippy, mock_file, dictionary):
        """Compare given dictionary against content stored in database based on message digest."""

        for digest in dictionary:
            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '-d', digest, '-f', 'defined-content.txt']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-content.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(SnippetHelper.get_template(dictionary[digest])),
                                                mock.call(Const.NEWLINE)])

    @staticmethod
    def compare_db(testcase, snippet, reference):
        """Compare snippes when they are in database format."""

        # Test that all fields excluding id and onwards are equal.
        testcase.assertEqual(snippet[Const.DATA], reference.get_data(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[Const.BRIEF], reference.get_brief(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[Const.GROUP], reference.get_group(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[Const.TAGS], reference.get_tags(Const.STRING_CONTENT))
        six.assertCountEqual(testcase, snippet[Const.LINKS], reference.get_links(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[Const.CATEGORY], reference.get_category(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[Const.FILENAME], reference.get_filename(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[Const.DIGEST], reference.get_digest(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[Const.METADATA], reference.get_metadata(Const.STRING_CONTENT))

        # Test that tags and links are lists and rest of the fields strings.
        assert isinstance(snippet[Const.DATA], six.string_types)
        assert isinstance(snippet[Const.BRIEF], six.string_types)
        assert isinstance(snippet[Const.GROUP], six.string_types)
        assert isinstance(snippet[Const.TAGS], six.string_types)
        assert isinstance(snippet[Const.LINKS], six.string_types)
        assert isinstance(snippet[Const.CATEGORY], six.string_types)
        assert isinstance(snippet[Const.FILENAME], six.string_types)
        assert isinstance(snippet[Const.DIGEST], six.string_types)
