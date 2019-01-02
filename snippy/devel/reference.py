#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""reference: Development reference."""

from __future__ import print_function

import re
import sys
import textwrap
from signal import signal, getsignal, SIGPIPE, SIG_DFL

import pkg_resources

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.logger import Logger


class Reference(object):
    """Development reference."""

    TEST_SEPARATOR = ' <WF_SEPARATOR> '

    def __init__(self):
        self._logger = Logger.get_logger(__name__)
        self.tests = []

    def print_tests(self, ansi=True):
        """Print tests case documentation."""

        self.create_test_document()
        text = self.format_test_document(ansi)
        Reference.output_test_document(text)

    def create_test_document(self):
        """Create test documentation from test files."""

        # The ImportError is the parent class of ModuleNotFoundError. The later one
        # is only in Python 3.6 but the ImportError works with older Python versions.
        try:
            pkg_resources.resource_isdir('tests', '')
        except ImportError as error:
            Cause.push(Cause.HTTP_INTERNAL_SERVER_ERROR, 'test cases are not packaged with release {}'.format(error))

            return

        # Test case file mock does not support iterators. Because of this, the
        # file is read directly to list where it is parsed.
        tests = pkg_resources.resource_listdir('tests', Const.EMPTY)
        regex = re.compile(r'''
            test_wf.*\.py
            ''', re.VERBOSE)
        tests = [filename for filename in tests if regex.match(filename)]
        for filename in tests:
            testfile = pkg_resources.resource_filename('tests', filename)
            with open(testfile, 'r') as infile:
                wf_brief = Const.EMPTY
                testcase = infile.readlines()
                for line_nbr, line in enumerate(testcase):
                    brief, line = Reference.get_brief(line, line_nbr, testcase)
                    if brief:
                        wf_brief = brief
                    wf_command = Reference.get_command(line)
                    if wf_command:
                        self.tests.append(wf_command + Reference.TEST_SEPARATOR + wf_brief)

    def format_test_document(self, ansi):
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
        if text:
            text = text.rstrip()
            text = text + Const.NEWLINE

        return text

    @staticmethod
    def output_test_document(text):
        """Print test document to console."""

        # See comment from Migrate.print_stdout. This is not used
        # from Migrate() because of circular dependencies.
        if text:
            text = 'test case reference list:\n\n' + text
            signal_sigpipe = getsignal(SIGPIPE)
            signal(SIGPIPE, SIG_DFL)
            print(text)
            sys.stdout.flush()
            signal(SIGPIPE, signal_sigpipe)

    @staticmethod
    def _terminal_command(ansi=False):
        """Format test case command."""

        return '   \x1b[91m$\x1b[0m \x1b[1;92m%s\x1b[0m\n' if ansi else '   $ %s\n'

    @staticmethod
    def _terminal_brief(ansi=False):
        """Format test case command."""

        return '%s\n' if ansi else '%s\n'

    @staticmethod
    def get_brief(line, line_nbr, testcase):
        """Return test case brief description."""

        brief = Const.EMPTY
        line_brief = line
        match = re.search(r'''
            [##]{2}\sBrief:\s+  # Match brief description.
            (.*)                # Catch brief description.
            ''', line, re.VERBOSE)
        if match:
            brief = match.group(1)
            brief = brief.strip()
            line_nbr = line_nbr + 1
            for line_brief in testcase[line_nbr:]:
                # Avoid matching the '  ## workflow' tag with leading spaces.
                match = re.search(r'''
                    \s{3,}[##]{2}\s+    # Match brief description line tag.
                    (.*)                # Catch brief description line.
                    ''', line_brief, re.VERBOSE)
                if match:
                    brief = brief + ' ' + match.group(1).strip()
                else:
                    break

        return (brief, line_brief)

    @staticmethod
    def get_command(line):
        """Return workflow command."""

        command = Const.EMPTY

        # The regexp below must not match to console help test case that
        # contains example test case.
        #
        # Example 1: main(['snippy', 'search', '--sall', '.', '--profile'])  ## workflow
        # Example 2: Snippy(['snippy', 'search', '--sall', '.', '-q'])  ## workflow
        # Example 3: snippy.run(['snippy', 'search'])  ## workflow
        match = re.search(r'''
            \[(.*)\][\)\s]+     # Match anything before the workflow tag.
            [##]{2}\s+workflow  # Match workflow tag.
            ''', line, re.VERBOSE)
        if match:
            command = match.group(1).strip()
            command = command.replace('\'', Const.EMPTY).replace(',', Const.EMPTY)
            # Special characters are escaped in commands.
            command = command.replace('\\\\$', '\\$').replace('\\\\s', '\\s')

        return command
