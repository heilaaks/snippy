#!/usr/bin/env python3

"""snippet_helper.py: Helper methods for snippet testing."""

import re
import unittest
from snippy.config import Constants as Const
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import


class SnippetHelper(object):
    """Helper methods for snippet testing."""

    SNIPPETS = [(('docker rm --volumes $(docker ps --all --quiet)',),
                 'Remove all docker containers with volumes',
                 'docker',
                 ('docker-ce', 'docker', 'moby', 'container', 'cleanup'),
                 ('https://docs.docker.com/engine/reference/commandline/rm/',),
                 'f4852122e1aa5b28d88181f9852960cc9e991fcc263a2e17f22db2cec98c3d0b',
                 None,
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
                 '6f9e21abdc2e4c53d04d77eff024708086c0a583f1be3dd761774353e9d2b74f',
                 None,
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

        digest = SnippetHelper.SNIPPETS[snippet][Const.SNIPPET_DIGEST]

        return digest

    @staticmethod
    def compare(snippet, reference):
        """Compare two snippets."""

        # Test that all fields excluding id and onwards are equal.
        testcase = unittest.TestCase()
        testcase.assertCountEqual(snippet[CONTENT], reference[CONTENT])
        testcase.assertEqual(snippet[BRIEF:TAGS], reference[BRIEF:TAGS])
        testcase.assertCountEqual(snippet[TAGS], reference[TAGS])
        testcase.assertCountEqual(snippet[LINKS], reference[LINKS])
        testcase.assertEqual(snippet[DIGEST], reference[DIGEST])
        testcase.assertEqual(snippet[METADATA], reference[METADATA])

        # Test that the tags and links are sorted.
        testcase.assertEqual(snippet[TAGS], tuple(sorted(reference[TAGS])))
        testcase.assertEqual(snippet[LINKS], tuple(sorted(reference[LINKS])))

        # Test that tags and links are lists and rest of the fields strings.
        assert isinstance(snippet[CONTENT], tuple)
        assert isinstance(snippet[BRIEF], str)
        assert isinstance(snippet[GROUP], str)
        assert isinstance(snippet[TAGS], tuple)
        assert isinstance(snippet[LINKS], tuple)
        assert isinstance(snippet[DIGEST], str)

    @staticmethod
    def compare_db(snippet, reference):
        """Compare snippes when they are in database format."""

        # Test that all fields excluding id and onwards are equal.
        testcase = unittest.TestCase()
        testcase.assertEqual(snippet[CONTENT], Const.DELIMITER_CONTENT.join(reference[CONTENT]))
        testcase.assertEqual(snippet[BRIEF:TAGS], reference[BRIEF:TAGS])
        testcase.assertEqual(snippet[TAGS], Const.DELIMITER_TAGS.join(reference[TAGS]))
        testcase.assertCountEqual(snippet[LINKS], Const.DELIMITER_LINKS.join(reference[LINKS]))
        testcase.assertEqual(snippet[DIGEST], reference[DIGEST])
        testcase.assertEqual(snippet[METADATA], reference[METADATA])

        # Test that tags and links are lists and rest of the fields strings.
        assert isinstance(snippet[CONTENT], str)
        assert isinstance(snippet[BRIEF], str)
        assert isinstance(snippet[GROUP], str)
        assert isinstance(snippet[TAGS], str)
        assert isinstance(snippet[LINKS], str)
        assert isinstance(snippet[DIGEST], str)
