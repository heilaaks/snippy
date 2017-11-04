#!/usr/bin/env python3

"""snippet_helper.py: Helper methods for snippet testing."""

import re
import sys
import six
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.editor import Editor
from snippy.content.content import Content
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class SnippetHelper(object):
    """Helper methods for snippet testing."""

    REMOVE = 0
    FORCED = 1
    EXITED = 2
    SNIPPETS = ((('docker rm --volumes $(docker ps --all --quiet)',),
                 'Remove all docker containers with volumes',
                 'docker',
                 ('docker-ce', 'docker', 'moby', 'container', 'cleanup'),
                 ('https://docs.docker.com/engine/reference/commandline/rm/',),
                 Const.SNIPPET,
                 '',
                 None,
                 '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                 None,
                 None,
                 """--content 'docker rm --volumes $(docker ps --all --quiet)'
                    --brief 'Remove all docker containers with volumes'
                    --group docker
                    --tags docker-ce,docker,moby,container,cleanup
                    --links 'https://docs.docker.com/engine/reference/commandline/rm/'"""),

                (('docker rm --force redis',),
                 'Remove docker image with force',
                 'docker',
                 ('docker-ce', 'docker', 'moby', 'container', 'cleanup'),
                 ('https://docs.docker.com/engine/reference/commandline/rm/',
                  'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'),
                 Const.SNIPPET,
                 '',
                 None,
                 '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                 None,
                 None,
                 """-c 'docker rm --force redis'
                    -b 'Remove docker image with force'
                    -g 'docker'
                    -t docker-ce,docker,moby,container,cleanup
                    -l 'https://docs.docker.com/engine/reference/commandline/rm/
                        https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'"""),

                (('docker rm $(docker ps --all -q -f status=exited)', 'docker images -q --filter dangling=true | xargs docker rmi'),
                 'Remove all exited containers and dangling images',
                 'docker',
                 ('docker-ce', 'docker', 'moby', 'container', 'cleanup', 'image'),
                 ('https://docs.docker.com/engine/reference/commandline/rm/',
                  'https://docs.docker.com/engine/reference/commandline/images/',
                  'https://docs.docker.com/engine/reference/commandline/rmi/'),
                 Const.SNIPPET,
                 '',
                 None,
                 '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                 None,
                 None,
                 """-c 'docker rm $(docker ps --all -q -f status=exited)\ndocker images -q --filter dangling=true | xargs docker rmi'
                    -b 'Remove all exited containers and dangling images'
                    -g 'docker'
                    -t docker-ce,docker,moby,container,cleanup,image
                    -l 'https://docs.docker.com/engine/reference/commandline/rm/
                        https://docs.docker.com/engine/reference/commandline/images/
                        https://docs.docker.com/engine/reference/commandline/rmi/'"""))

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
    def get_references(index=0, sliced=None):
        """Return specified snippet."""

        if sliced:
            sliced = sliced.split(':')
            snippets = SnippetHelper.SNIPPETS[int(sliced[0]):int(sliced[1])]
            snippets = [Content(x[Const.DATA:Const.TESTING]) for x in snippets]
            snippets = tuple(snippets)
        else:
            snippets = Content(SnippetHelper.SNIPPETS[index][Const.DATA:Const.TESTING])

        return snippets

    @staticmethod
    def get_command_args(snippet, regexp=r'^\'|\'$'): # ' <-- For UltraEditor code highlights problem.
        """Get command line arguments from snippets list."""

        args = [re.sub(regexp, Const.EMPTY, arg)
                for arg in re.split("('.*?'| )", SnippetHelper.SNIPPETS[snippet][Const.TESTING], flags=re.DOTALL) if arg.strip()]

        # Replace multiple spaces with one. These are coming from the snippet
        # definition that splits for example the link parameter to multiple
        # lines.
        args = [re.sub(r'\s{2,}', Const.SPACE, argument).strip() for argument in args]

        return args

    @staticmethod
    def get_command_string(snippet):
        """Return command string from snippets list."""

        command = Const.SPACE.join(SnippetHelper.get_command_args(snippet, Const.NEWLINE))

        return command

    @staticmethod
    def get_template(content):
        """Return text template from content dictionary."""

        contents = Content.load({'content': [content]})
        editor = Editor(contents[0], '2017-10-01 11:53:17')

        return editor.get_template()

    @staticmethod
    def get_edited_message(initial, updates, columns):
        """Create mocked editor default template and new content with merged updates."""

        # Merge the content from initial set based on updates data from columns
        # defined by user. Calculate the digest for merged content and convert
        # back to Content().
        merged_list = initial.get_list()
        updates_list = updates.get_list()
        for column in columns:
            merged_list[column] = updates_list[column]
        merged = Content((merged_list))
        merged_list[Const.DIGEST] = merged.compute_digest()
        merged = Content((merged_list))
        template = Editor(merged, '2017-10-01 11:53:17').get_template()

        return (template, merged)

    @staticmethod
    def compare(testcase, snippet, reference):
        """Compare two snippets."""

        # Test that all fields excluding id and onwards are equal.
        six.assertCountEqual(testcase, snippet.get_data(), reference.get_data())
        testcase.assertEqual(snippet.get_brief(), reference.get_brief())
        testcase.assertEqual(snippet.get_group(), reference.get_group())
        six.assertCountEqual(testcase, snippet.get_tags(), reference.get_tags())
        six.assertCountEqual(testcase, snippet.get_links(), reference.get_links())
        testcase.assertEqual(snippet.get_category(), reference.get_category())
        testcase.assertEqual(snippet.get_filename(), reference.get_filename())
        testcase.assertEqual(snippet.get_digest(), reference.get_digest())
        testcase.assertEqual(snippet.get_metadata(), reference.get_metadata())

        # Test that the tags and links are sorted.
        testcase.assertEqual(snippet.get_tags(), tuple(sorted(reference.get_tags())))
        testcase.assertEqual(snippet.get_links(), tuple(sorted(reference.get_links())))

        # Test that tags and links are lists and rest of the fields strings.
        assert isinstance(snippet.get_data(), tuple)
        assert isinstance(snippet.get_brief(), six.string_types)
        assert isinstance(snippet.get_group(), six.string_types)
        assert isinstance(snippet.get_tags(), tuple)
        assert isinstance(snippet.get_links(), tuple)
        assert isinstance(snippet.get_category(), six.string_types)
        assert isinstance(snippet.get_filename(), six.string_types)
        assert isinstance(snippet.get_digest(), six.string_types)

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

    @staticmethod
    def add_defaults(snippy):
        """Add default snippets for testing purposes."""

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            sys.argv = ['snippy', 'create'] + SnippetHelper.get_command_args(0)
            if not snippy:
                snippy = Snippy()
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            sys.argv = ['snippy', 'create'] + SnippetHelper.get_command_args(1)
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2

        return snippy

    @staticmethod
    def add_one(snippy, index):
        """Add one default snippet for testing purposes."""

        if not snippy:
            snippy = Snippy()

        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            sys.argv = ['snippy', 'create'] + SnippetHelper.get_command_args(index)
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1

        return snippy

    @staticmethod
    def test_content(snippy, mock_file, content):
        """Compare given content against data read with message digest."""

        for digest in content:
            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '-d', digest, '-f', 'defined-content.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-content.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(SnippetHelper.get_template(content[digest])),
                                                mock.call(Const.NEWLINE)])
