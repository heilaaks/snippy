# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_cli_options: Test command line options."""

from __future__ import print_function

import sys

import mock
import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.meta import __homepage__
from snippy.meta import __version__
from snippy.snip import Snippy
from snippy.snip import main
from tests.lib.content import Content
from tests.lib.helper import Helper


class TestCliOptions(object):  # pylint: disable=too-many-public-methods
    """Test CLI command options."""

    HELP = (
        'usage: snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]',
        '',
        'positional arguments:',
        '    {create,search,update,delete,export,import}',
        '',
        'content category:',
        '    --scat [CATEGORY,...]         operate content categories',
        '',
        'edit options:',
        '    -c, --content CONTENT         define example content',
        '    -b, --brief BRIEF             define content brief description',
        '    -g, --groups [GROUP,...]      define comma separated list of groups',
        '    -t, --tags [TAG,...]          define comma separated list of tags',
        '    -l, --links [LINK ...]        define space separated list of links',
        '    -d, --digest DIGEST           idenfity content with digest',
        '    -u, --uuid UUID               idenfity content with uuid',
        '    --editor                      use vi editor to manage content',
        '    --no-editor                   do not use vi editor',
        '',
        'search options:',
        '    --sall [KW,...]               search keywords from all fields',
        '    --stag [KW,...]               search keywords only from tags',
        '    --sgrp [KW,...]               search keywords only from groups',
        '    --filter REGEXP               filter search result with regexp',
        '    --limit INT                   maximum number of search results',
        '    --sort FIELD                  sort search result based on fields',
        '    --headers                     print only content headers',
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
        '    >    reference',
        '    ' + Helper.to_bytes(u'\u2713') + '    todo',
        '    @    group',
        '    #    tag',
        '',
        'examples:',
        '    Import default content.',
        '      $ snippy import --defaults --scat snippet',
        '      $ snippy import --defaults --scat solution',
        '      $ snippy import --defaults --scat reference',
        '      $ snippy import --defaults --scat all',
        '',
        '    List all snippets.',
        '      $ snippy search --scat snippet --sall .',
        '',
        '    List more examples.',
        '      $ snippy --help examples',
        '',
        'Copyright 2017-2020 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
        'Snippy ' + __version__ + ' licensed under GNU Affero General Public License v3.0 or later',
        'Homepage ' + __homepage__,
        ''
    )
    EXAMPLES = (
        'examples:',
        '    Creating new content:',
        '      $ snippy create --scat snippet --editor',
        '      $ snippy create --scat snippet -c \'docker ps\' -b \'list containers\' -t docker,moby',
        '',
        '    Searching and filtering content:',
        '      $ snippy search --scat snippet --sall docker,moby',
        '      $ snippy search --scat snippet --sall .',
        '      $ snippy search --scat snippet --sall . --no-ansi | grep \'\\$\' | sort',
        '      $ snippy search --scat solution --sall .',
        '      $ snippy search --scat solution --sall . | grep -Ev \'[^\\s]+:\'',
        '      $ snippy search --scat all --sall . --filter \'\\$?.*docker\'',
        '      $ snippy search --scat all --sall . --no-ansi | grep -E \'[0-9]+\\.\\s\'',
        '',
        '    Updating content:',
        '      $ snippy update --scat snippet -d 44afdd0c59e17159',
        '      $ snippy update --scat snippet -c \'docker ps\'',
        '',
        '    Deleting content:',
        '      $ snippy delete --scat snippet -d 44afdd0c59e17159',
        '      $ snippy delete --scat snippet -c \'docker ps\'',
        '',
        '    Migrating default content:',
        '      $ snippy import --scat snippet --defaults',
        '      $ snippy import --scat solution --defaults',
        '      $ snippy import --scat reference --defaults',
        '',
        '    Migrating content templates:',
        '      $ snippy export --scat solution --template',
        '      $ snippy import --scat solution --template',
        '      $ snippy import --scat solution -f solution-template.txt',
        '',
        '    Migrating specific content:',
        '      $ snippy export -d eb792f8015ace749',
        '      $ snippy import -d eb792f8015ace749 -f howto-debug-elastic-beats.mkdn',
        '',
        '    Migrating content:',
        '      $ snippy export --scat snippet -f snippets.yaml',
        '      $ snippy export --scat snippet -f snippets.json',
        '      $ snippy export --scat snippet -f snippets.text',
        '      $ snippy import --scat snippet -f snippets.yaml',
        '      $ snippy export --scat solution -f solutions.yaml',
        '      $ snippy import --scat solution -f solutions.yaml',
        '',
        'Copyright 2017-2020 Heikki Laaksonen <laaksonen.heikki.j@gmail.com>',
        'Snippy ' + __version__ + ' licensed under GNU Affero General Public License v3.0 or later',
        'Homepage ' + __homepage__,
        ''
    )

    @staticmethod
    def test_help_option_001(capsys, caplog):
        """Test printing help from console.

        Print help with long option.
        """

        snippy = Snippy(['snippy', '--help'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert Helper.to_bytes(out) == Const.NEWLINE.join(TestCliOptions.HELP)
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    def test_help_option_002(capsys, caplog):
        """Test printing help from console.

        Print help with short option.
        """

        snippy = Snippy(['snippy', '-h'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert Helper.to_bytes(out) == Const.NEWLINE.join(TestCliOptions.HELP)
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    def test_help_option_003(capsys, caplog):
        """Test printing help from console.

        Generate help text by giving only the tool name.
        """

        snippy = Snippy(['snippy'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert Helper.to_bytes(out) == Const.NEWLINE.join(TestCliOptions.HELP)
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    @pytest.mark.skipif(sys.platform == "win32", reason="does not work on windows")
    @pytest.mark.usefixtures('mock-server')
    def test_help_option_004(capsys, caplog, osenviron):
        """Test running only the snippy.

        In this case the SNIPPY_SERVER_HOST configuration variable is set.
        This should just start the server without printing help. This is a
        use case for server installation in Docker containers where all
        variables are coming from environment variables.
        """

        osenviron.setenv('SNIPPY_SERVER_HOST', '127.0.0.1:8081')
        snippy = Snippy(['snippy'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == Const.EMPTY
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    def test_help_option_005(capsys, caplog):
        """Test printing help from console.

        Suppress tool help text with quiet mode even when there are no other
        parameters and the help should be printed.
        """

        snippy = Snippy(['snippy', '-q'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == Const.EMPTY
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    def test_help_option_006(capsys, caplog):
        """Test invalid command line option.

        Try to run snippy with invalid command line option.
        """

        output = (
            'usage: snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]',
            'snippy: error: unrecognized arguments: -a',
            ''
        )
        snippy = Snippy(['snippy', '-a'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == Const.EMPTY
        assert err == Const.NEWLINE.join(output)
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    def test_help_option_007(capsys, caplog):
        """Test printing examples from console.

        Print command examples from help.
        """

        snippy = Snippy(['snippy', '--help', 'examples'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == Const.NEWLINE.join(TestCliOptions.EXAMPLES)
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('devel_file_list', 'devel_file_data')
    def test_help_option_008(capsys, caplog):
        """Test printing test documentation from console.

        Print test cases. The ``--no-ansi`` option must work when set before
        the ``--help`` option. There are two files out of three where tests
        are read.
        """

        output = (
            'test case reference list:',
            '',
            '   $ snippy import --filter .*(\\$\\s.*)',
            '   # Import all snippets. File name is not defined in commmand line.',
            '   # This should result tool internal default file name',
            '   # ./snippets.yaml being used by default.',
            '',
            '   $ snippy import --filter .*(\\$\\s.*)',
            '   # Import all snippets. File name is not defined in commmand line.',
            '   # This should result tool internal default file name',
            '   # ./snippets.yaml being used by default.',
            '',
            ''
        )
        snippy = Snippy(['snippy', '--no-ansi', '--help', 'tests'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == Const.NEWLINE.join(output)
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('devel_file_list', 'devel_file_data')
    def test_help_option_009(capsys, caplog):
        """Test printing test documentation from console.

        Print test cases. The ``--no-ansi`` option must work when set after
        the ``--help`` option.
        """

        output = (
            'test case reference list:',
            '',
            '   $ snippy import --filter .*(\\$\\s.*)',
            '   # Import all snippets. File name is not defined in commmand line.',
            '   # This should result tool internal default file name',
            '   # ./snippets.yaml being used by default.',
            '',
            '   $ snippy import --filter .*(\\$\\s.*)',
            '   # Import all snippets. File name is not defined in commmand line.',
            '   # This should result tool internal default file name',
            '   # ./snippets.yaml being used by default.',
            '',
            ''
        )
        snippy = Snippy(['snippy', '--help', 'tests', '--no-ansi'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == Const.NEWLINE.join(output)
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('devel_no_tests')
    def test_help_option_010(capsys, caplog):
        """Print test documentation when testing package does not exist.

        Try to print tool test case reference documentation when tests are
        not packaged with the release.
        """

        snippy = Snippy(['snippy', '--help', 'tests'])
        cause = snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert cause == 'NOK: test cases are not packaged with release No module named \'tests\''
        assert out == 'NOK: test cases are not packaged with release No module named \'tests\'' + Const.NEWLINE
        assert not err
        assert not caplog.records[:]
        snippy.release()
        Content.delete()

    @staticmethod
    def test_help_option_011(capsys, caplog):
        """Test invalid command line option.

        Try to run snippy with ``--scat`` option without any value.
        """

        output = (
            'usage: snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]',
            'snippy: error: argument --scat: expected at least one argument',
            ''
        )
        snippy = Snippy(['snippy', '--scat'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == Const.EMPTY
        assert err == Const.NEWLINE.join(output)
        assert not caplog.records[:]
        Content.delete()


    @staticmethod
    @pytest.mark.parametrize('snippy', [['-vv']], indirect=True)
    def test_very_verbose_option_001(snippy, caplog, capsys):
        """Test printing logs with the very verbose option.

        Enable verbose logging with ``-vv`` option. Test checks that there are
        more than a randomly picked largish number of logs in order to avoid
        matching logs count explicitly.

        Nothing must be printed to the stderr.
        """

        cause = snippy.run(['snippy', 'search', '--sall', '.', '-vv'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert len(out.splitlines()) > 10
        assert len(caplog.records) > 10
        assert not err

    @staticmethod
    @pytest.mark.parametrize('snippy', [['-vv', '--log-msg-max', '200']], indirect=True)
    def test_very_verbose_option_002(snippy, caplog, capsys):
        """Test printing logs with the very verbose option.

        Enable verbose logging with ``-vv`` option. In this case the message
        lenght is defined from command line. Test checks that there are more
        than a randomly picked largish number of logs to avoid matching log
        count explicitly.

        Nothing must be printed to stderr.
        """

        cause = snippy.run(['snippy', 'search', '--sall', '.', '-vv', '--log-msg-max', '200'])
        snippy.release()
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert 'log msg max: 200' in out
        assert len(out.splitlines()) > 10
        assert len(caplog.records) > 10
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    @pytest.mark.parametrize('snippy', [['--debug', '--no-ansi']], indirect=True)
    def test_debug_option_001(snippy, capsys, caplog):
        """Test printing logs with debug option.

        Enable full length log messages with the ``--debug`` option. In this
        case all the attributes from stored resources must be printed.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '   ! category    : snippet',
            '   ! created     : 2017-10-14T19:56:31.000001+00:00',
            '   ! description : ',
            '   ! digest      : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319 (True)',
            '   ! filename    : ',
            '   ! id          : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! languages   : ',
            '   ! name        : ',
            '   ! source      : ',
            '   ! updated     : 2017-10-14T19:56:31.000001+00:00',
            '   ! uuid        : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! versions    : ',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            '   ! category    : snippet',
            '   ! created     : 2017-10-14T19:56:31.000001+00:00',
            '   ! description : ',
            '   ! digest      : 53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5 (True)',
            '   ! filename    : ',
            '   ! id          : a2cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! languages   : ',
            '   ! name        : ',
            '   ! source      : ',
            '   ! updated     : 2017-10-14T19:56:31.000001+00:00',
            '   ! uuid        : 12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! versions    :'
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--debug', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert Const.NEWLINE.join(output) in out
        assert len(caplog.records) > 20
        assert not err

    @staticmethod
    def test_quiet_option_001(snippy, capsys, caplog):
        """Test supressing all output from tool.

        Disable all logging and output to terminal. Only the printed content
        is displayed on the screen.
        """

        snippy = Snippy(['snippy', 'search', '--sall', '.', '-q'])
        cause = snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert not out
        assert not err
        assert not caplog.records[:]

    @staticmethod
    def test_version_option_001(capsys, caplog):
        """Test printing tool version.

        Output tool version with long option. Only the version must be printed
        and nothing else. The print must be send to stdout.
        """

        snippy = Snippy(['snippy', '--version'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == __version__ + Const.NEWLINE
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    def test_version_option_002(capsys, caplog):
        """Test printing tool version.

        Output tool version with short option. Only the version must be
        printed and nothing else. The print must be send to stdout.
        """

        snippy = Snippy(['snippy', '-v'])
        snippy.run()
        snippy.release()
        out, err = capsys.readouterr()
        assert out == __version__ + Const.NEWLINE
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    def test_snippy_main(capsys, caplog):
        """Test running program main with profile option.

        Run program main with the profile option. Test checks that there is
        more than randomly picked largish number of rows. This just verifies
        that the profile option prints lots for data.
        """

        with pytest.raises(SystemExit):
            main(['snippy', 'search', '--sall', '.', '--profile'])
        out, err = capsys.readouterr()
        assert 'Ordered by: cumulative time' in out
        assert not err
        assert not caplog.records[:]
        Content.delete()

    @staticmethod
    @pytest.mark.usefixtures('snippy', 'default-snippets')
    def test_debug_print_001(capsys):
        """Test printing the content.

        Test printing content with print. This is a development test which
        must directly print the snippets with the test case helper method.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '   ! category    : snippet',
            '   ! created     : 2017-10-14T19:56:31.000001+00:00',
            '   ! description : ',
            '   ! digest      : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319 (True)',
            '   ! filename    : ',
            '   ! id          : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! languages   : ',
            '   ! name        : ',
            '   ! source      : ',
            '   ! updated     : 2017-10-14T19:56:31.000001+00:00',
            '   ! uuid        : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! versions    : ',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            '   ! category    : snippet',
            '   ! created     : 2017-10-14T19:56:31.000001+00:00',
            '   ! description : ',
            '   ! digest      : 53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5 (True)',
            '   ! filename    : ',
            '   ! id          : a2cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! languages   : ',
            '   ! name        : ',
            '   ! source      : ',
            '   ! updated     : 2017-10-14T19:56:31.000001+00:00',
            '   ! uuid        : 12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! versions    : ',
            '',
            '# collection meta',
            '   ! total : 2'
        )
        print(Content.output())  # Part of the test.
        out, err = capsys.readouterr()
        out = Helper.remove_ansi(out)
        assert Const.NEWLINE.join(output) in out
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('exists_true', 'access_true')
    def test_export_shell_completion_001(snippy):
        """Export bash completion script.

        Export Bash completion script. In this case the ``--file`` option is
        not defined and a default filename is used.
        """

        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            cause = snippy.run(['snippy', 'export', '--complete', 'bash'])
            assert cause == Cause.ALL_OK
            Content.assert_arglist(mock_file, './snippy.bash-completion', mode='w', encoding='utf-8')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Content.COMPLETE_BASH)

    @staticmethod
    @pytest.mark.usefixtures('exists_true', 'access_true')
    def test_export_shell_completion_002(snippy):
        """Export bash completion script.

        Export Bash completion script. In this case the ``--file`` option is
        set to local path so that only the filename is changed from the
        default.
        """

        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            cause = snippy.run(['snippy', 'export', '--complete', 'bash', '-f', './snippy'])
            assert cause == Cause.ALL_OK
            Content.assert_arglist(mock_file, './snippy', mode='w', encoding='utf-8')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_called_with(Content.COMPLETE_BASH)

    @staticmethod
    @pytest.mark.usefixtures('exists_false', 'access_true')
    def test_export_shell_completion_003(snippy):
        """Try to export bash completion script.

        Try to export Bash completion script. In this case the ``--file``
        option is set to a file path that does not exist.
        """

        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            cause = snippy.run(['snippy', 'export', '--complete', 'bash', '-f', '/root/noaccess/snippy'])
            assert cause == 'NOK: cannot export bash completion file because path is not writable /root/noaccess/snippy'
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('exists_true', 'access_false')
    def test_export_shell_completion_004(snippy):
        """Try to export bash completion script.

        Try to export Bash completion script. In this case the ``--file``
        option is set to a file path is not writable.
        """

        with mock.patch('snippy.content.migrate.io.open') as mock_file:
            cause = snippy.run(['snippy', 'export', '--complete', 'bash', '-f', '/root/noaccess/snippy'])
            assert cause == 'NOK: cannot export bash completion file because path is not writable /root/noaccess/snippy'
            mock_file.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures('exists_true', 'access_false')
    def test_export_shell_completion_005(snippy, capsys):
        """Try to export shell completion script.

        Try to export unknown shell completion script.
        """

        output = (
            'usage: snippy [-v, --version] [-h, --help] <operation> [<options>] [-vv] [-q]',
            "snippy: error: argument --complete: invalid choice: 'notfound' (choose from 'bash')",
            ''
        )
        with mock.patch('snippy.content.migrate.io.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'export', '--complete', 'notfound'])
            out, err = capsys.readouterr()
            assert not out
            assert err == Const.NEWLINE.join(output)
            assert cause == Cause.ALL_OK
            mock_file.assert_not_called()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
