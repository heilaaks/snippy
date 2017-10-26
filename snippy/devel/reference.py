#!/usr/bin/env python3

"""reference.py: Development reference."""

import re
import textwrap
import pkg_resources
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger


class Reference(object):
    """Development reference."""

    TEST_SEPARATOR = ' <WF_SEPARATOR> '

    def __init__(self):
        self.logger = Logger(__name__).get()
        self.tests = []

    def print_tests(self):
        """Print tests case documentation."""

        self.create_test_document()
        text = self.format_test_document()
        Reference.output_test_document(text)

    def create_test_document(self):
        """Create test documentation from test files."""

        files = []
        files.append(pkg_resources.resource_filename('tests', 'test_wf_export_solution.py'))
        for file in files:
            with open(file, 'r') as infile:
                wf_brief = ''
                for line in infile:
                    brief = Reference.get_brief(line, infile)
                    if brief:
                        wf_brief = brief
                    wf_command = Reference.get_command(line)
                    if wf_command:
                        self.tests.append(wf_command + Reference.TEST_SEPARATOR + wf_brief)

    def format_test_document(self, ansi=True):
        """Output test documentation."""

        text = Const.EMPTY
        self.tests.sort()
        for test in self.tests:
            wf_command, wf_brief = test.split(Reference.TEST_SEPARATOR)
            text = text + Reference._terminal_command(ansi) % wf_command
            dedented_text = textwrap.dedent(wf_brief).strip()
            brief = textwrap.fill(dedented_text, initial_indent='   # ', subsequent_indent='   # ')
            text = text + Reference._terminal_brief(ansi) % brief
            text = text + Const.NEWLINE

        # Set only one empty line at the end of string for beautified output.
        text = text.rstrip()
        text = text + Const.NEWLINE

        return text

    @staticmethod
    def output_test_document(text):
        """Print test document to console."""

        print(text)

    @staticmethod
    def _terminal_command(ansi=False):
        """Format test case command."""

        return '   \x1b[91m$\x1b[0m \x1b[1;92m%s\x1b[0m\n' if ansi else '%s   $ %s\n'

    @staticmethod
    def _terminal_brief(ansi=False):
        """Format test case command."""

        return '%s\n' if ansi else '%s\n'

    @staticmethod
    def get_brief(line, infile):
        """Return test case brief description."""

        brief = ''
        match = re.search(r'## Brief:\s+(.*)', line)
        if match:
            brief = match.group(1)
            brief = brief.strip()
            while True:
                line = infile.readline()
                match = re.search(r'\s+##\s+(.*)', line)
                if match:
                    brief = brief + ' ' + match.group(1).strip()
                else:
                    break

        return brief

    @staticmethod
    def get_command(line):
        """Return workflow command."""

        command = Const.EMPTY
        match = re.search(r'(.*)##\s+workflow', line)
        if match:
            command = match.group(1).strip()
            command = re.search(r'\[(.*)\]', command)
            command = command.group(1).replace('\'', Const.EMPTY).replace(',', Const.EMPTY)

        return command
