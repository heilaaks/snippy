#!/usr/bin/env python3

"""snippet_helper.py: Helper methods for snippet testing."""

import re
import six
from snippy.config import Constants as Const
from snippy.content import Content
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import


class SnippetHelper(object):
    """Helper methods for snippet testing."""

    SNIPPETS = ((('docker rm --volumes $(docker ps --all --quiet)',),
                 'Remove all docker containers with volumes',
                 'docker',
                 ('docker-ce', 'docker', 'moby', 'container', 'cleanup'),
                 ('https://docs.docker.com/engine/reference/commandline/rm/',),
                 Const.SNIPPET,
                 '',
                 None,
                 'cf2a161acb1195bb425efc5b09ef92783af41be914bf196a3c8e07e6fc08debd',
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
                 '6f9e21abdc2e4c53d04d77eff024708086c0a583f1be3dd761774353e9d2b74f',
                 None,
                 None,
                 """-c 'docker rm --force redis'
                    -b 'Remove docker image with force'
                    -g 'docker'
                    -t docker-ce,docker,moby,container,cleanup
                    -l 'https://docs.docker.com/engine/reference/commandline/rm/
                        https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'"""))



    @staticmethod
    def get_references(index=0, sliced=None):
        """Return specified snippet."""

        if sliced:
            sliced = sliced.split(':')
            snippets = SnippetHelper.SNIPPETS[int(sliced[0]):int(sliced[1])]
            snippets = [Content(x[DATA:TESTING]) for x in snippets]
        else:
            snippets = [Content(SnippetHelper.SNIPPETS[index][DATA:TESTING])]

        return tuple(snippets)

    @staticmethod
    def get_command_args(snippet, regexp=r'^\'|\'$|\n'): # ' <-- For UltraEditor code highlights problem.
        """Get command line arguments from snippets list."""

        args = [re.sub(regexp, Const.EMPTY, arg)
                for arg in re.split("('.*?'| )", SnippetHelper.SNIPPETS[snippet][TESTING], flags=re.DOTALL) if arg.strip()]

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
    def get_digest(snippet):
        """Return digest for specified snippet."""

        digest = SnippetHelper.SNIPPETS[snippet][DIGEST]

        return digest

    @staticmethod
    def compare(testcase, snippet, reference):
        """Compare two snippets."""

        # Test that all fields excluding id and onwards are equal.
        SnippetHelper._assert_count_equal(testcase, snippet.get_data(), reference.get_data())
        testcase.assertEqual(snippet.get_brief(), reference.get_brief())
        testcase.assertEqual(snippet.get_group(), reference.get_group())
        SnippetHelper._assert_count_equal(testcase, snippet.get_tags(), reference.get_tags())
        SnippetHelper._assert_count_equal(testcase, snippet.get_links(), reference.get_links())
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
        testcase.assertEqual(snippet[DATA], reference.get_data(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[BRIEF], reference.get_brief(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[GROUP], reference.get_group(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[TAGS], reference.get_tags(Const.STRING_CONTENT))
        SnippetHelper._assert_count_equal(testcase, snippet[LINKS], reference.get_links(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[CATEGORY], reference.get_category(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[FILENAME], reference.get_filename(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[DIGEST], reference.get_digest(Const.STRING_CONTENT))
        testcase.assertEqual(snippet[METADATA], reference.get_metadata(Const.STRING_CONTENT))

        # Test that tags and links are lists and rest of the fields strings.
        assert isinstance(snippet[DATA], six.string_types)
        assert isinstance(snippet[BRIEF], six.string_types)
        assert isinstance(snippet[GROUP], six.string_types)
        assert isinstance(snippet[TAGS], six.string_types)
        assert isinstance(snippet[LINKS], six.string_types)
        assert isinstance(snippet[CATEGORY], six.string_types)
        assert isinstance(snippet[FILENAME], six.string_types)
        assert isinstance(snippet[DIGEST], six.string_types)

    @staticmethod
    def _assert_count_equal(testcase, snippet, reference):
        """Compare lists."""

        if not Const.PYTHON2:
            testcase.assertCountEqual(snippet, reference)
        else:
            testcase.assertItemsEqual(snippet, reference)
