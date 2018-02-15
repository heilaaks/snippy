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

"""test_wf_search_solution.py: Test workflows for searching solutions."""

import sys

import mock

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database
if not Const.PYTHON2:
    from io import StringIO # pylint: disable=import-error
else:
    from StringIO import StringIO # pylint: disable=import-error


class TestWfSearchSnippet(object):
    """Test workflows for searching solutions."""

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_solution_with_sall(self, mock_isfile, mock_storage_file):
        """Search solution from all fields."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

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
            snippy = Solution.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--solution', '--sall', 'filebeat', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to search solutions with keyword that cannot be found.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            output = 'NOK: cannot find content with given search criteria'
            snippy = Solution.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--solution', '--sall', 'notfound', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == 'NOK: cannot find content with given search criteria'
            assert result == output
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_solution_with_regxp(self, mock_isfile, mock_storage_file):
        """Search solution with regexp."""

        mock_storage_file.return_value = Database.get_storage()
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
            snippy = Solution.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--solution', '--sall', '.', '--filter', '.*(\\$\\s.*)'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_searching_solution_with_digest(self, mock_isfile, mock_storage_file):
        """Search solution with --digest option."""

        mock_storage_file.return_value = Database.get_storage()
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
            snippy = Solution.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--solution', '--digest', 'a96accc25dd23ac0', '--no-ansi'])  ## workflow
            assert cause == Cause.ALL_OK
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_search_solution_with_sall_sgrp(self, mock_isfile, mock_storage_file):
        """Search solution from all field sand limit the search within specific group."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Search solutions from all fields and limit the search to specific group.
        ##        The match must not be made from other than defined group. In this case
        ##        the list all must print the content of defined group.
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
            snippy = Solution.add_defaults()
            real_stdout = sys.stdout
            sys.stdout = StringIO()
            cause = snippy.run_cli(['snippy', 'search', '--solution', '--sall', '.', '--sgrp', 'beats', '--no-ansi'])  ## workflow
            result = sys.stdout.getvalue().strip()
            sys.stdout = real_stdout
            assert cause == Cause.ALL_OK
            assert result == Const.NEWLINE.join(output)
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
