#!/usr/bin/env python3

"""test_wf_search_solution.py: Test workflows for searching solutions."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO # pylint: disable=import-error
else:
    from StringIO import StringIO # pylint: disable=import-error


class TestWfSearchSnippet(unittest.TestCase):
    """Test workflows for searching solutions."""

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_solution_with_sall(self, mock_isfile, mock_get_db_location):
        """Search solution from all fields."""

        mock_isfile.return_value = True
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Search solutions from all fields. The match is made from one solution
        ##        content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Debugging Elastic Beats @beats [a96accc25dd23ac0]',
                      '',
                      '   # Elastic,beats,debug,filebeat,howto',
                      '   > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
                      '',
                      '   : ################################################################################',
                      '   : ## BRIEF : Debugging Elastic Beats',
                      '   : ##',
                      '   : ## DATE  : 2017-10-20 11:11:19',
                      '   : ## GROUP : beats',
                      '   : ## TAGS  : Elastic,beats,filebeat,debug,howto',
                      '   : ## FILE  : howto-debug-elastic-beats.txt',
                      '   : ################################################################################',
                      '   : ',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## description',
                      '   : ################################################################################',
                      '   : ',
                      '   :     # Debug Elastic Beats',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## references',
                      '   : ################################################################################',
                      '   : ',
                      '   :     # Enable logs from Filebeat',
                      '   :     > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## commands',
                      '   : ################################################################################',
                      '   : ',
                      '   :     # Run Filebeat with full log level',
                      '   :     $ ./filebeat -e -c config/filebeat.yml -d "*"',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## solutions',
                      '   : ################################################################################',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## configurations',
                      '   : ################################################################################',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## whiteboard',
                      '   : ################################################################################',
                      '   :',
                      '',
                      'OK')
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'search', '--solution', '--sall', 'filebeat', '--no-ansi']  ## workflow
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli()
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            print(result)
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_solution_with_regxp(self, mock_isfile, mock_get_db_location):
        """Search solution with regexp."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search all content with regexp filter. The ansi characters must be
        ##        automatically disabled in when the --filter option is used.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('$ ./filebeat -e -c config/filebeat.yml -d "*"',
                      '$ nginx -V 2>&1 | grep -- \'--with-debug\'',
                      '$ ls -al /var/log/nginx/',
                      '$ unlink /var/log/nginx/access.log',
                      '$ unlink /var/log/nginx/error.log',
                      '$ nginx -s reload',
                      '$ vi conf.d/default.conf',
                      '$ docker exec -i -t $(docker ps | egrep -m 1 \'petelk/nginx\' | awk \'{print $1}\') /bin/bash',
                      '',
                      'OK')
            snippy = Solution.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--solution', '--sall', '.', '--filter', '.*(\\$\\s.*)']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_searching_solution_with_digest(self, mock_isfile, mock_get_db_location):
        """Search solution with --digest option."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Search solution by explicitly defining short message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = ('1. Debugging Elastic Beats @beats [a96accc25dd23ac0]',
                      '',
                      '   # Elastic,beats,debug,filebeat,howto',
                      '   > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
                      '',
                      '   : ################################################################################',
                      '   : ## BRIEF : Debugging Elastic Beats',
                      '   : ##',
                      '   : ## DATE  : 2017-10-20 11:11:19',
                      '   : ## GROUP : beats',
                      '   : ## TAGS  : Elastic,beats,filebeat,debug,howto',
                      '   : ## FILE  : howto-debug-elastic-beats.txt',
                      '   : ################################################################################',
                      '   : ',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## description',
                      '   : ################################################################################',
                      '   : ',
                      '   :     # Debug Elastic Beats',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## references',
                      '   : ################################################################################',
                      '   : ',
                      '   :     # Enable logs from Filebeat',
                      '   :     > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## commands',
                      '   : ################################################################################',
                      '   : ',
                      '   :     # Run Filebeat with full log level',
                      '   :     $ ./filebeat -e -c config/filebeat.yml -d "*"',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## solutions',
                      '   : ################################################################################',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## configurations',
                      '   : ################################################################################',
                      '   : ',
                      '   : ################################################################################',
                      '   : ## whiteboard',
                      '   : ################################################################################',
                      '   :',
                      '',
                      'OK')
            snippy = Solution.add_defaults(Snippy())
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            sys.argv = ['snippy', 'search', '--solution', '--digest', 'a96accc25dd23ac0', '--no-ansi']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            print(result)
            print(Const.NEWLINE.join(output))
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
