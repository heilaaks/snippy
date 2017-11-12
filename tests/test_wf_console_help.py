#!/usr/bin/env python3

"""test_wf_console_help.py: Test workflows for getting help from console."""

import sys
import unittest
import pytest
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO # pylint: disable=import-error
else:
    from StringIO import StringIO # pylint: disable=import-error


class TestWfConsoleHelp(unittest.TestCase):
    """Test getting help from console."""

    def test_console_help(self):
        """Test printing help from consoler."""

        ## Brief: Print tool help.
        cause = Cause.ALL_OK
        snippy = Snippy()
        try:
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
                      'Snippy version 0.6.0 - license Apache 2.0',
                      'Copyright 2017 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                      'Homepage https://github.com/heilaaks/snippy')
            sys.argv = ['snippy', '--help']  ## workflow
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            snippy = Snippy()
            cause = snippy.run_cli()
        except SystemExit:
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    def test_console_help_examples(self):
        """Test printing examples from consoler."""

        ## Brief: Print tool examples.
        cause = Cause.ALL_OK
        snippy = Snippy()
        try:
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
                      '      $ snippy export -d e95e9092c92e3440',
                      '      $ snippy import -d e95e9092c92e3440 -f howto-debug-elastic-beats.txt',
                      '',
                      '    Migrating content:',
                      '      $ snippy export --snippet -f snippets.yaml',
                      '      $ snippy export --snippet -f snippets.json',
                      '      $ snippy export --snippet -f snippets.text',
                      '      $ snippy import --snippet -f snippets.yaml',
                      '      $ snippy export --solution -f solutions.yaml',
                      '      $ snippy import --solution -f solutions.yaml',
                      '',
                      'Snippy version 0.6.0 - license Apache 2.0',
                      'Copyright 2017 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
                      'Homepage https://github.com/heilaaks/snippy')
            sys.argv = ['snippy', '--help', 'examples']  ## workflow
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli()
        except SystemExit:
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch('snippy.devel.reference.pkg_resources.resource_isdir')
    @mock.patch('snippy.devel.reference.pkg_resources.resource_listdir')
    def test_console_help_tests(self, mock_resource_listdir, mock_resource_isdir):
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
                    'import unittest',
                    'import json',
                    'import yaml',
                    'import mock',
                    'import pkg_resources',
                    'from snippy.snip import Snippy',
                    'from snippy.config.constants import Constants as Const',
                    'from snippy.cause.cause import Cause',
                    'from snippy.storage.database.sqlite3db import Sqlite3Db',
                    'from tests.testlib.snippet_helper import SnippetHelper as Snippet',
                    'from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database',
                    '',
                    '',
                    'class TestWfImportSnippet(unittest.TestCase):',
                    '    """Test workflows for importing snippets."""',
                    '',
                    '    @mock.patch.object(json, \'load\')',
                    '    @mock.patch.object(yaml, \'safe_load\')',
                    '    @mock.patch.object(Sqlite3Db, \'_get_db_location\')',
                    '    @mock.patch(\'snippy.migrate.migrate.os.path.isfile\')',
                    '    def test_import_all_snippets(self, mock_isfile, mock_get_db_location, mock_yaml_load, mock_json_load):',
                    '        """Import all snippets."""',
                    '',
                    '        mock_isfile.return_value = True',
                    '        mock_get_db_location.return_value = Database.get_storage()',
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
                    '            sys.argv = [\'snippy\', \'import\', \'--filter\', \'.*(\\$\\s.*)\']  ## workflow',
                    '            cause = snippy.run_cli()',
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
            snippy = Snippy()
            try:
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
                sys.argv = ['snippy', '--help', 'tests', '--no-ansi']  ## workflow
                real_stdout = sys.stdout
                sys.stdout = StringIO()
                cause = snippy.run_cli()
            except SystemExit:
                result = sys.stdout.getvalue().strip()
                sys.stdout = real_stdout
                print(result)
                print("===")
                print(Const.NEWLINE.join(output))
                assert cause == Cause.ALL_OK
                assert result == Const.NEWLINE.join(output)
                snippy.release()
                snippy = None
                Database.delete_storage()

    @mock.patch('snippy.devel.reference.pkg_resources.resource_isdir')
    @mock.patch('snippy.devel.reference.pkg_resources.resource_listdir')
    def test_console_help_tests_no_package(self, mock_resource_listdir, mock_resource_isdir):
        """Test printing test documentation when testing package does not exist."""

        mock_resource_isdir.side_effect = ModuleNotFoundError("No module named 'tests'")
        mock_resource_listdir.return_value = ['test_ut_arguments_create.py',
                                              'test_wf_console_help.py',
                                              'test_wf_export_snippet.py']

        ## Brief: Try to print tool test case reference documentation when tests are not
        ##        packaged with the release.
        testcase = ('')
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(testcase))
        with mock.patch('snippy.devel.reference.open', mocked_open, create=True):
            cause = Cause.ALL_OK
            snippy = Snippy()
            try:
                output = ('')
                sys.argv = ['snippy', '--help', 'tests']  ## workflow
                real_stdout = sys.stdout
                sys.stdout = StringIO()
                cause = snippy.run_cli()
            except SystemExit:
                result = sys.stdout.getvalue().strip()
                sys.stdout = real_stdout
                assert cause == Cause.ALL_OK  # Cause is not updated because the SystemExit exception is thrown from argparse.
                assert result == Const.NEWLINE.join(output)
                snippy.release()
                snippy = None
                Database.delete_storage()

    @pytest.mark.skip(reason="this again slows down all tests but works independently. Why?")
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    def test_console_very_verbose_option(self, mock_get_db_location):
        """Test printing logs witht the tool output."""

        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Enable short logging with -vv option. Test checks that there is more than
        ##        randomly picked largish number of logs in order to avoid matching logs
        ##        explicitly. This just verifies that the very verbose option prints more
        ##        logs.
        with mock.patch('snippy.devel.reference.open', mock.mock_open(), create=True):
            cause = Cause.ALL_OK
            sys.argv = ['snippy', 'search', '--sall', '.', '-vv']  ## workflow
            snippy = Snippy()
            real_stderr = sys.stderr
            sys.stderr = StringIO()
            cause = snippy.run_cli()
            result = sys.stderr.getvalue().strip()
            sys.stderr = real_stderr
            assert cause == Cause.ALL_OK
            assert len(result.split(Const.NEWLINE)) > 25
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
