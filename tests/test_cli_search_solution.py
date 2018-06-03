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

"""test_cli_search_solution: Test workflows for searching solutions."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliSearchSolution(object):
    """Test workflows for searching solutions."""

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_001(self, snippy, capsys):
        """Search solution from all fields."""

        ## Brief: Search solutions from all fields. The match is made from one
        ##        solution content data.
        output = (
            '1. Debugging Elastic Beats @beats [a96accc25dd23ac0]',
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
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--solution', '--sall', 'filebeat', '--no-ansi'])  ## workflow
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_002(self, snippy, capsys):
        """Search solution from all fields."""

        ## Brief: Try to search solutions with keyword that cannot be found.
        output = 'NOK: cannot find content with given search criteria' + Const.NEWLINE
        cause = snippy.run(['snippy', 'search', '--solution', '--sall', 'notfound', '--no-ansi'])  ## workflow
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_003(self, snippy, capsys):
        """Search solution with regexp."""

        ## Brief: Search all content with regexp filter. The ansi characters
        ##        must be automatically disabled in when the --filter option
        ##        is used.
        output = (
            '$ ./filebeat -e -c config/filebeat.yml -d "*"',
            '$ nginx -V 2>&1 | grep -- \'--with-debug\'',
            '$ ls -al /var/log/nginx/',
            '$ unlink /var/log/nginx/access.log',
            '$ unlink /var/log/nginx/error.log',
            '$ nginx -s reload',
            '$ vi conf.d/default.conf',
            '$ docker exec -i -t $(docker ps | egrep -m 1 \'petelk/nginx\' | awk \'{print $1}\') /bin/bash',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--solution', '--sall', '.', '--filter', '.*(\\$\\s.*)'])  ## workflow
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_004(self, snippy, capsys):
        """Search solution with --digest option."""

        ## Brief: Search solution by explicitly defining short message digest.
        output = (
            '1. Debugging Elastic Beats @beats [a96accc25dd23ac0]',
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
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--solution', '--digest', 'a96accc25dd23ac0', '--no-ansi'])  ## workflow
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_search_solution_005(self, snippy, capsys):
        """Search solution from all field sand limit the search within specific group."""

        ## Brief: Search solutions from all fields and limit the search to
        ##        specific group. The match must not be made from other than
        ##        defined group. In this case the list all must print the
        ##        content of defined group.
        output = (
            '1. Debugging Elastic Beats @beats [a96accc25dd23ac0]',
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
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--solution', '--sall', '.', '--sgrp', 'beats', '--no-ansi'])  ## workflow
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
