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

"""test_wf_console_help.py: Test workflows for getting help from console."""

from __future__ import print_function

import re
import sys

import mock
import pytest

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.meta import __homepage__
from snippy.meta import __version__
from snippy.snip import Snippy
from snippy.snip import main
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO  # pylint: disable=import-error
else:
    from StringIO import StringIO  # pylint: disable=import-error


class TestWfConsoleHelp(object):
    """Test getting help from console."""

    def test_console_help(self):
        """Test printing help from console."""

        output = ('usage: snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]',
                  '',
                  'positional arguments:',
                  '    {create,search,update,delete,export,import}',
                  '',
                  'content category:',
                  '    --snippet                     operate snippets (default)',
                  '    --solution                    operate solutions',
                  '    --all                         operate all content (search only)',
                  '',
                  'edit options:',
                  '    -e, --editor                  use vi editor to add content',
                  '    -c, --content CONTENT         define example content',
                  '    -b, --brief BRIEF             define content brief description',
                  '    -g, --group GROUP             define content group',
                  '    -t, --tags [TAG,...]          define comma separated list of tags',
                  '    -l, --links [LINK ...]        define space separated list of links',
                  '    -d, --digest DIGEST           idenfity content with digest',
                  '',
                  'search options:',
                  '    --sall [KW,...]               search keywords from all fields',
                  '    --stag [KW,...]               search keywords only from tags',
                  '    --sgrp [KW,...]               search keywords only from groups',
                  '    --filter REGEXP               filter search output with regexp',
                  '    --no-ansi                     remove ANSI characters from output',
                  '',
                  'migration options:',
                  '    -f, --file FILE               define file for operation',
                  '    --defaults                    migrate category specific defaults',
                  '    --template                    migrate category specific template',
                  '',
                  'symbols:',
                  '    $    snippet',
                  '    :    solution',
                  '    @    group',
                  '    #    tag',
                  '    >    url',
                  '',
                  'examples:',
                  '    Import default content.',
                  '      $ snippy import --snippet --defaults',
                  '      $ snippy import --solution --defaults',
                  '',
                  '    List all snippets.',
                  '      $ snippy search --snippet --sall .',
                  '',
                  '    List more examples.',
                  '      $ snippy --help examples',
                  '',
                  'Snippy version ' + __version__ + ' - license GNU AGPLv3',
                  'Copyright 2017-2018 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                  'Homepage ' + __homepage__)

        ## Brief: Print tool help with long option.
        cause = Cause.ALL_OK
        real_stdout = sys.stdout
        real_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        snippy = Snippy(['snippy', '--help'])  ## workflow
        snippy.release()
        result_stdout = sys.stdout.getvalue().strip()
        result_stderr = sys.stderr.getvalue().strip()
        sys.stdout = real_stdout
        sys.stderr = real_stderr
        assert cause == Cause.ALL_OK
        assert result_stdout == Const.NEWLINE.join(output)
        assert not result_stderr
        snippy = None
        Database.delete_storage()

        ## Brief: Print tool help with short option.
        cause = Cause.ALL_OK
        real_stdout = sys.stdout
        real_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        snippy = Snippy(['snippy', '-h'])  ## workflow
        snippy.release()
        result_stdout = sys.stdout.getvalue().strip()
        result_stderr = sys.stderr.getvalue().strip()
        sys.stdout = real_stdout
        sys.stderr = real_stderr
        assert cause == Cause.ALL_OK
        assert result_stdout == Const.NEWLINE.join(output)
        assert not result_stderr
        snippy = None
        Database.delete_storage()

    def test_console_help_examples(self):
        """Test printing examples from console."""

        ## Brief: Print tool command examples from help.
        output = ('examples:',
                  '    Creating new content:',
                  '      $ snippy create --snippet --editor',
                  '      $ snippy create --snippet -c \'docker ps\' -b \'list containers\' -t docker,moby',
                  '',
                  '    Searching and filtering content:',
                  '      $ snippy search --snippet --sall docker,moby',
                  '      $ snippy search --snippet --sall .',
                  '      $ snippy search --snippet --sall . --no-ansi | grep \'\\$\' | sort',
                  '      $ snippy search --solution --sall .',
                  '      $ snippy search --solution --sall . | grep -Ev \'[^\\s]+:\'',
                  '      $ snippy search --all --sall . --filter \'.*(\\$\\s.*)\'',
                  '      $ snippy search --all --sall . --no-ansi | grep -E \'[0-9]+\\.\\s\'',
                  '',
                  '    Updating content:',
                  '      $ snippy update --snippet -d 44afdd0c59e17159',
                  '      $ snippy update --snippet -c \'docker ps\'',
                  '',
                  '    Deleting content:',
                  '      $ snippy delete --snippet -d 44afdd0c59e17159',
                  '      $ snippy delete --snippet -c \'docker ps\'',
                  '',
                  '    Migrating default content:',
                  '      $ snippy import --snippet --defaults',
                  '      $ snippy import --solution --defaults',
                  '',
                  '    Migrating content templates:',
                  '      $ snippy export --solution --template',
                  '      $ snippy import --solution --template',
                  '      $ snippy import --solution -f solution-template.txt',
                  '',
                  '    Migrating specific content:',
                  '      $ snippy export -d 76a1a02951f6bcb4',
                  '      $ snippy import -d 76a1a02951f6bcb4 -f howto-debug-elastic-beats.txt',
                  '',
                  '    Migrating content:',
                  '      $ snippy export --snippet -f snippets.yaml',
                  '      $ snippy export --snippet -f snippets.json',
                  '      $ snippy export --snippet -f snippets.text',
                  '      $ snippy import --snippet -f snippets.yaml',
                  '      $ snippy export --solution -f solutions.yaml',
                  '      $ snippy import --solution -f solutions.yaml',
                  '',
                  'Snippy version ' + __version__ + ' - license GNU AGPLv3',
                  'Copyright 2017-2018 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                  'Homepage ' + __homepage__)
        cause = Cause.ALL_OK
        real_stdout = sys.stdout
        real_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        sys.argv = ['snippy', '--help', 'examples']
        snippy = Snippy(['snippy', '--help', 'examples'])  ## workflow
        snippy.release()
        result_stdout = sys.stdout.getvalue().strip()
        result_stderr = sys.stderr.getvalue().strip()
        sys.stdout = real_stdout
        sys.stderr = real_stderr
        assert cause == Cause.ALL_OK
        assert result_stdout == Const.NEWLINE.join(output)
        assert not result_stderr
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.devel.reference.pkg_resources.resource_isdir')
    @mock.patch('snippy.devel.reference.pkg_resources.resource_listdir')
    def test_console_help_tests_list(self, mock_resource_listdir, mock_resource_isdir):
        """Test printing test documentation from consoler."""

        mock_resource_isdir.return_value = True
        mock_resource_listdir.return_value = ['test_ut_arguments_create.py',
                                              'test_wf_console_help.py',
                                              'test_wf_export_snippet.py']

        ## Brief: Print tool examples.
        testcase = ('#!/usr/bin/env python3',
                    '',
                    '"""test_wf_import_snippet.py: Test workflows for importing snippets."""',
                    '',
                    'import re',
                    'import sys',
                    'import copy',
                    'import json',
                    'import yaml',
                    'import mock',
                    'import pkg_resources',
                    'from snippy.snip import Snippy',
                    'from snippy.config.config import Config',
                    'from snippy.config.constants import Constants as Const',
                    'from snippy.cause import Cause',
                    'from tests.testlib.snippet_helper import SnippetHelper as Snippet',
                    'from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database',
                    '',
                    '',
                    'class TestWfImportSnippet(object):',
                    '    """Test workflows for importing snippets."""',
                    '',
                    '    @mock.patch.object(json, \'load\')',
                    '    @mock.patch.object(yaml, \'safe_load\')',
                    '    @mock.patch.object(Config, \'_storage_file\')',
                    '    @mock.patch(\'snippy.migrate.migrate.os.path.isfile\')',
                    '    def test_import_all_snippets(self, mock_isfile, mock_storage_file, mock_yaml_load, mock_json_load):',
                    '        """Import all snippets."""',
                    '',
                    '        mock_isfile.return_value = True',
                    '        mock_storage_file.return_value = Database.get_storage()',
                    '        import_dict = {\'content\': [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.NETCAT]]}',
                    '        mock_yaml_load.return_value = import_dict',
                    '        mock_json_load.return_value = import_dict',
                    '        compare_content = {\'54e41e9b52a02b63\': import_dict[\'content\'][0],',
                    '                           \'f3fd167c64b6f97e\': import_dict[\'content\'][1]}',
                    '',
                    '        ## Brief: Import all snippets. File name is not defined in commmand line. This should',
                    '        ##        result tool internal default file name ./snippets.yaml being used by default.',
                    '        with mock.patch(\'snippy.migrate.migrate.open\', mock.mock_open(), create=True) as mock_file:',
                    '            snippy = Snippy()',
                    '            cause = snippy.run_cli([\'snippy\', \'import\', \'--filter\', \'.*(\\$\\s.*)\'])  ## workflow',
                    '            assert cause == Cause.ALL_OK',
                    '            assert len(Database.get_snippets()) == 2',
                    '            mock_file.assert_called_once_with(\'./snippets.yaml\', \'r\')',
                    '            Snippet.test_content(snippy, mock_file, compare_content)',
                    '            snippy.release()',
                    '            snippy = None',
                    '            Database.delete_storage()')
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(testcase))
        with mock.patch('snippy.devel.reference.open', mocked_open, create=True):
            cause = Cause.ALL_OK
            output = ('test case reference list:',
                      '',
                      '   $ snippy import --filter .*(\\$\\s.*)',
                      '   # Import all snippets. File name is not defined in commmand line.',
                      '   # This should result tool internal default file name',
                      '   # ./snippets.yaml being used by default.',
                      '',
                      '   $ snippy import --filter .*(\\$\\s.*)',
                      '   # Import all snippets. File name is not defined in commmand line.',
                      '   # This should result tool internal default file name',
                      '   # ./snippets.yaml being used by default.')
            cause = Cause.ALL_OK
            real_stdout = sys.stdout
            real_stderr = sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            sys.argv = ['snippy', '--help', 'tests', '--no-ansi']
            snippy = Snippy(['snippy', '--help', 'tests', '--no-ansi'])  ## workflow
            snippy.release()
            result_stdout = sys.stdout.getvalue().strip()
            result_stderr = sys.stderr.getvalue().strip()
            sys.stdout = real_stdout
            sys.stderr = real_stderr
            assert cause == Cause.ALL_OK
            assert result_stdout == Const.NEWLINE.join(output)
            assert not result_stderr
            snippy = None
            Database.delete_storage()

    @mock.patch('snippy.devel.reference.pkg_resources.resource_isdir')
    @mock.patch('snippy.devel.reference.pkg_resources.resource_listdir')
    def test_console_help_tests_no_package(self, mock_resource_listdir, mock_resource_isdir):
        """Test printing test documentation when testing package does not exist."""

        # The exception in Python 3.6 is ModuleNotFoundError but this is not
        # available in earlier Python versions. The used ImportError is a partent
        # class of ModuleNotFoundError and it works with older Python versions.
        mock_resource_isdir.side_effect = [ImportError("No module named 'tests'"), mock.DEFAULT]
        mock_resource_listdir.return_value = ['test_ut_arguments_create.py',
                                              'test_wf_console_help.py',
                                              'test_wf_export_snippet.py']

        ## Brief: Try to print tool test case reference documentation when tests
        ##        are not packaged with the release.
        testcase = ('')
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(testcase))
        with mock.patch('snippy.devel.reference.open', mocked_open, create=True):
            try:
                output = ('')
                cause = Cause.ALL_OK
                real_stdout = sys.stdout
                real_stderr = sys.stderr
                sys.stdout = StringIO()
                sys.stderr = StringIO()
                sys.argv = ['snippy', '--help', 'tests']
                snippy = Snippy(['snippy', '--help', 'tests'])  ## workflow
                cause = snippy.run_cli()
            except SystemExit:
                result_stdout = sys.stdout.getvalue().strip()
                result_stderr = sys.stderr.getvalue().strip()
                sys.stdout = real_stdout
                sys.stderr = real_stderr
                assert cause == Cause.ALL_OK  # Cause is not updated because the SystemExit exception is thrown from argparse.
                assert result_stdout == Const.NEWLINE.join(output)
                assert not result_stderr
                snippy = None
                Database.delete_storage()
        mock_resource_isdir.side_effect = None

    @pytest.mark.parametrize('snippy', [['-vv']], indirect=True)
    def test_very_verbose_option_001(self, snippy, caplog, capsys):
        """Test printing logs with the very verbose option."""

        ## Brief: Enable verbose logging with -vv option. Test checks that
        ##        there is more than randomly picked largish number of logs
        ##        in order to avoid matching logs explicitly. Nothing must
        ##        be printed to stderr. TODO: Why the stdout container few
        ##        lines in this test?
        cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '-vv'])  ## workflow
        _, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert len(caplog.records[:]) > 30
        assert not err

    @pytest.mark.usefixtures('default-snippets')
    @pytest.mark.parametrize('snippy', [['--debug', '--no-ansi']], indirect=True)
    def test_debug_option_001(self, snippy, capsys, caplog):
        """Test printing logs with debug option."""

        ## Brief: Enable full logging with --debug option. In this case the
        ##        debug option must print all fields from stored snippets.
        ##        TODO: Why the stderr container log exceptions with 'I/O
        ##        operation on closed file'?
        output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
                  '   $ docker rm --volumes $(docker ps --all --quiet)',
                  '',
                  '   # cleanup,container,docker,docker-ce,moby',
                  '   > https://docs.docker.com/engine/reference/commandline/rm/',
                  '',
                  '   ! category : snippet',
                  '   ! filename : ',
                  '   ! runalias : ',
                  '   ! versions : ',
                  '   ! created  : 2017-10-14 19:56:31',
                  '   ! updated  : 2017-10-14 19:56:31',
                  '   ! digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319 (True)',
                  '   ! metadata : None',
                  '   ! key      : 1',
                  '',
                  '2. Remove docker image with force @docker [53908d68425c61dc]',
                  '   $ docker rm --force redis',
                  '',
                  '   # cleanup,container,docker,docker-ce,moby',
                  '   > https://docs.docker.com/engine/reference/commandline/rm/',
                  '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
                  '',
                  '   ! category : snippet',
                  '   ! filename : ',
                  '   ! runalias : ',
                  '   ! versions : ',
                  '   ! created  : 2017-10-14 19:56:31',
                  '   ! updated  : 2017-10-14 19:56:31',
                  '   ! digest   : 53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5 (True)',
                  '   ! metadata : None',
                  '   ! key      : 2')
        cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '--debug', '--no-ansi'])  ## workflow
        out, _ = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert Const.NEWLINE.join(output) in out
        assert len(caplog.records[:]) > 30
        #assert not err

    @pytest.mark.parametrize('snippy', [['-q']], indirect=True)
    def test_quiet_option_001(self, snippy, capsys, caplog):
        """Test supressing all output from tool."""

        ## Brief: Disable all logging and output to terminal. Only the printed
        ##        content is displayed on the screen.
        cause = snippy.run_cli(['snippy', 'search', '--sall', '.', '-q'])  ## workflow
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert not out
        assert not err
        assert not caplog.records[:]

    def test_version_option_001(self, capsys, caplog):
        """Test printing tool version."""

        ## Brief: Output tool version with long option. Only the version must
        ##        be printed and nothing else. The print must be send to
        ##        stdout.
        snippy = Snippy(['snippy', '--version'])  ## workflow
        snippy.run()
        out, err = capsys.readouterr()
        assert out == __version__ + Const.NEWLINE
        assert not err
        assert not caplog.records[:]
        Database.delete_storage()

    def test_version_option_002(self, capsys, caplog):
        """Test printing tool version."""

        ## Brief: Output tool version with short option. Only the version must
        ##        be printed and nothing else. The print must be send to
        ##        stdout.
        snippy = Snippy(['snippy', '-v'])  ## workflow
        snippy.run()
        out, err = capsys.readouterr()
        assert out == __version__ + Const.NEWLINE
        assert not err
        assert not caplog.records[:]
        Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    def test_snippy_main(self, mock_storage_file):
        """Test running program main with profile option."""

        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Run program main with profile option. Test checks that
        ##        there is more than randomly picked largish number of rows.
        ##        This just verifies that the profile option prints lots for
        ##        data.
        with mock.patch('snippy.devel.reference.open', mock.mock_open(), create=True):
            sys.argv = ['snippy', 'search', '--sall', '.', '--profile']  ## workflow
            real_stdout = sys.stdout
            real_stderr = sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            main()
            result_stdout = sys.stdout.getvalue().strip()
            result_stderr = sys.stderr.getvalue().strip()
            sys.stdout = real_stdout
            sys.stderr = real_stderr
            assert len(result_stdout.split(Const.NEWLINE)) > 100
            assert not result_stderr
            Database.delete_storage()

    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_debug_print_001(self, capsys):
        """Test printing the content."""

        ## Brief: Test printing content with print. This is a development
        ##        test which must directly print the snippet.
        output = ('1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
                  '   $ docker rm --volumes $(docker ps --all --quiet)',
                  '',
                  '   # cleanup,container,docker,docker-ce,moby',
                  '   > https://docs.docker.com/engine/reference/commandline/rm/',
                  '',
                  '   ! category : snippet',
                  '   ! filename : ',
                  '   ! runalias : ',
                  '   ! versions : ',
                  '   ! created  : 2017-10-14 19:56:31',
                  '   ! updated  : 2017-10-14 19:56:31',
                  '   ! digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319 (True)',
                  '   ! metadata : None',
                  '   ! key      : 1',
                  '',
                  '1. Remove docker image with force @docker [53908d68425c61dc]',
                  '   $ docker rm --force redis',
                  '',
                  '   # cleanup,container,docker,docker-ce,moby',
                  '   > https://docs.docker.com/engine/reference/commandline/rm/',
                  '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
                  '',
                  '   ! category : snippet',
                  '   ! filename : ',
                  '   ! runalias : ',
                  '   ! versions : ',
                  '   ! created  : 2017-10-14 19:56:31',
                  '   ! updated  : 2017-10-14 19:56:31',
                  '   ! digest   : 53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5 (True)',
                  '   ! metadata : None',
                  '   ! key      : 2')
        print(Database.get_snippets()[0])  # Part of the test.
        print(Database.get_snippets()[1])  # Part of the test.
        out, err = capsys.readouterr()
        out = re.sub(r'\x1b[^m]*m', '', out)  # Remove all color codes from output for comparison.
        assert Const.NEWLINE.join(output) in out
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
