#!/usr/bin/env python3

"""snippet_helper.py: Helper methods for snippet testing."""

import re
import six
from snippy.config import Constants as Const
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import


class SnippetHelper(object):
    """Helper methods for snippet testing."""

    SNIPPETS = [(('docker rm --volumes $(docker ps --all --quiet)',),
                 'Remove all docker containers with volumes',
                 'docker',
                 ('docker-ce', 'docker', 'moby', 'container', 'cleanup'),
                 ('https://docs.docker.com/engine/reference/commandline/rm/',),
                 Const.SNIPPET,
                 '',
                 None,
                 '467cdee334da208d403d3d9eb326829a3e1b8ee5980e5159f665eb77882c50bc',
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
                 'None',
                 '6f9e21abdc2e4c53d04d77eff024708086c0a583f1be3dd761774353e9d2b74f',
                 None,
                 None,
                 """-c 'docker rm --force redis'
                    -b 'Remove docker image with force'
                    -g 'docker'
                    -t docker-ce,docker,moby,container,cleanup
                    -l 'https://docs.docker.com/engine/reference/commandline/rm/
                        https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'""")]



    @staticmethod
    def get_references(index=0, sliced=None):
        """Return specified snippet."""

        if sliced:
            sliced = sliced.split(':')
            snippets = SnippetHelper.SNIPPETS[int(sliced[0]):int(sliced[1])]
        else:
            snippets = [SnippetHelper.SNIPPETS[index]]

        return snippets

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
        SnippetHelper._assert_count_equal(testcase, snippet[DATA], reference[DATA])
        testcase.assertEqual(snippet[BRIEF:TAGS], reference[BRIEF:TAGS])
        SnippetHelper._assert_count_equal(testcase, snippet[TAGS], reference[TAGS])
        SnippetHelper._assert_count_equal(testcase, snippet[LINKS], reference[LINKS])
        testcase.assertEqual(snippet[CATEGORY], reference[CATEGORY])
        testcase.assertEqual(snippet[FILENAME], reference[FILENAME])
        testcase.assertEqual(snippet[DIGEST], reference[DIGEST])
        testcase.assertEqual(snippet[METADATA], reference[METADATA])

        # Test that the tags and links are sorted.
        testcase.assertEqual(snippet[TAGS], tuple(sorted(reference[TAGS])))
        testcase.assertEqual(snippet[LINKS], tuple(sorted(reference[LINKS])))

        # Test that tags and links are lists and rest of the fields strings.
        assert isinstance(snippet[DATA], tuple)
        assert isinstance(snippet[BRIEF], six.string_types)
        assert isinstance(snippet[GROUP], six.string_types)
        assert isinstance(snippet[TAGS], tuple)
        assert isinstance(snippet[LINKS], tuple)
        assert isinstance(snippet[CATEGORY], six.string_types)
        assert isinstance(snippet[FILENAME], six.string_types)
        assert isinstance(snippet[DIGEST], six.string_types)

    @staticmethod
    def compare_db(testcase, snippet, reference):
        """Compare snippes when they are in database format."""

        # Test that all fields excluding id and onwards are equal.
        testcase.assertEqual(snippet[DATA], Const.DELIMITER_DATA.join(reference[DATA]))
        testcase.assertEqual(snippet[BRIEF:TAGS], reference[BRIEF:TAGS])
        testcase.assertEqual(snippet[TAGS], Const.DELIMITER_TAGS.join(sorted(reference[TAGS])))
        SnippetHelper._assert_count_equal(testcase, snippet[LINKS], Const.DELIMITER_LINKS.join(sorted(reference[LINKS])))
        testcase.assertEqual(snippet[CATEGORY], reference[CATEGORY])
        testcase.assertEqual(snippet[FILENAME], reference[FILENAME])
        testcase.assertEqual(snippet[DIGEST], reference[DIGEST])
        testcase.assertEqual(snippet[METADATA], reference[METADATA])

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
