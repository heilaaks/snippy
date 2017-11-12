#!/usr/bin/env python3

"""test_wf_console_help.py: Test workflows for getting help from console."""

import sys
import unittest
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO # pylint: disable=import-error
else:
    from StringIO import StringIO # pylint: disable=import-error


class TestWfConsoleHelp(unittest.TestCase):
    """Test getting help from console."""

    def test_console_help(self):
        """Test getting help from consoler."""

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
            sys.argv = ['snippy', '--help']
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
        """Test getting help from consoler."""

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
            sys.argv = ['snippy', '--help', 'examples']
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

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
