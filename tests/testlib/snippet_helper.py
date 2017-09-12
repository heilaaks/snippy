#!/usr/bin/env python3

"""snippet_helper.py: Helper methods for snippet testing."""

import re
import unittest
from snippy.config import Constants as Const


class SnippetHelper(object):
    """Helper methods for snippet testing."""

    SNIPPETS = [('docker rm --volumes $(docker ps --all --quiet)',
                 'Remove all docker containers with volumes',
                 'docker',
                 ['docker-ce', 'docker', 'moby', 'container', 'cleanup'],
                 ['https://docs.docker.com/engine/reference/commandline/rm/'],
                 'f4852122e1aa5b28d88181f9852960cc9e991fcc263a2e17f22db2cec98c3d0b',
                 None,
                 None,
                 None,
                 """--content 'docker rm --volumes $(docker ps --all --quiet)'
                    --brief 'Remove all docker containers with volumes'
                    --group docker
                    --tags docker-ce,docker,moby,container,cleanup
                    --links 'https://docs.docker.com/engine/reference/commandline/rm/'""")]

    @staticmethod
    def get_references(snippets):
        """Return specified snippet."""

        snippets = [SnippetHelper.SNIPPETS[snippets]]

        return snippets

    @staticmethod
    def get_command_args(snippet, regexp=r'^\'|\'$|\n'): # ' <-- For UltraEditor code highlights problem.
        """Get command line arguments for the snippet."""

        args = [re.sub(regexp, Const.EMPTY, argument)
                for argument in re.split("( |'.*?')", SnippetHelper.SNIPPETS[snippet][Const.SNIPPET_TESTING]) if argument.strip()]

        return args

    @staticmethod
    def get_digest(snippet):
        """Return digest for specified snippet."""

        digest = SnippetHelper.SNIPPETS[snippet][Const.SNIPPET_DIGEST]

        return digest

    @staticmethod
    def get_command_string(snippet):
        """Return command string for specified snippet."""

        command = Const.SPACE.join(SnippetHelper.get_command_args(snippet, '\n'))

        return command

    @staticmethod
    def assert_snippets(snippet, reference):
        """Compare two snippets."""

        # pylint: disable=invalid-name
        CONTENT = Const.SNIPPET_CONTENT
        BRIEF = Const.SNIPPET_BRIEF
        GROUP = Const.SNIPPET_GROUP
        TAGS = Const.SNIPPET_TAGS
        LINKS = Const.SNIPPET_LINKS
        DIGEST = Const.SNIPPET_DIGEST
        METADATA = Const.SNIPPET_METADATA
        # pylint: enable=invalid-name

        # Test that all fields excluding id and onwards are equal.
        testcase = unittest.TestCase()
        testcase.assertEqual(snippet[CONTENT:TAGS], reference[CONTENT:TAGS])
        testcase.assertCountEqual(snippet[TAGS], reference[TAGS])
        testcase.assertCountEqual(snippet[LINKS], reference[LINKS])
        testcase.assertEqual(snippet[DIGEST], reference[DIGEST])
        testcase.assertEqual(snippet[METADATA], reference[METADATA])

        # Test that the tags and links are sorted.
        testcase.assertEqual(snippet[TAGS], sorted(reference[TAGS]))
        testcase.assertEqual(snippet[LINKS], sorted(reference[LINKS]))

        # Test that tags and links are lists and rest of the fields strings.
        assert isinstance(snippet[CONTENT], str)
        assert isinstance(snippet[BRIEF], str)
        assert isinstance(snippet[GROUP], str)
        assert isinstance(snippet[TAGS], list)
        assert isinstance(snippet[LINKS], list)
        assert isinstance(snippet[DIGEST], str)
