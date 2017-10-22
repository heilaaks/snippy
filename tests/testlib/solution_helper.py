#!/usr/bin/env python3

"""solution_helper.py: Helper methods for solution testing."""

import sys
import mock
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class SolutionHelper(object):  # pylint: disable=too-few-public-methods
    """Helper methods for solution testing."""

    SOLUTIONS_TEXT = (['################################################################################',
                       '## BRIEF : Debugging Elastic Beats',
                       '##',
                       '## DATE  : 2017-10-20 11:11:19',
                       '## GROUP : beats',
                       '## TAGS  : Elastic,beats,filebeat,debug,howto',
                       '## FILE  : howto-debug-elastic-beats.txt',
                       '################################################################################',
                       '',
                       '',
                       '################################################################################',
                       '## description',
                       '################################################################################',
                       '',
                       '    # Debug Elastic Beats',
                       '',
                       '################################################################################',
                       '## references',
                       '################################################################################',
                       '',
                       '    # Enable logs from Filebeat',
                       '    > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
                       '',
                       '################################################################################',
                       '## commands',
                       '################################################################################',
                       '',
                       '    # Run Filebeat with full log level',
                       '    $ ./filebeat -e -c config/filebeat.yml -d "*"',
                       '',
                       '################################################################################',
                       '## solutions',
                       '################################################################################',
                       '',
                       '################################################################################',
                       '## configurations',
                       '################################################################################',
                       '',
                       '################################################################################',
                       '## whiteboard',
                       '################################################################################',
                       ''],
                      ['################################################################################',
                       '## BRIEF : Debugging nginx ',
                       '##',
                       '## DATE  : 2017-10-20 06:16:27',
                       '## GROUP : nginx',
                       '## TAGS  : nginx,debug,logging,howto',
                       '## FILE  : howto-debug-nginx.txt',
                       '################################################################################',
                       '',
                       '',
                       '################################################################################',
                       '## description',
                       '################################################################################',
                       '',
                       '    # Instructions how to debug nginx.',
                       '',
                       '################################################################################',
                       '## references',
                       '################################################################################',
                       '',
                       '    # Official nginx debugging',
                       '    > https://www.nginx.com/resources/admin-guide/debug/',
                       '',
                       '################################################################################',
                       '## commands',
                       '################################################################################',
                       '',
                       '    # Test if nginx is configured with --with-debug',
                       '    $ nginx -V 2>&1 | grep -- \'--with-debug\'',
                       '',
                       '    # Check the logs are forwarded to stdout/stderr and remove links',
                       '    $ ls -al /var/log/nginx/',
                       '    $ unlink /var/log/nginx/access.log',
                       '    $ unlink /var/log/nginx/error.log',
                       '',
                       '    # Reloading nginx configuration',
                       '    $ nginx -s reload',
                       '',
                       '################################################################################',
                       '## solutions',
                       '################################################################################',
                       '',
                       '################################################################################',
                       '## configurations',
                       '################################################################################',
                       '',
                       '    # Configuring nginx default.conf',
                       '    $ vi conf.d/default.conf',
                       '      upstream kibana_servers {',
                       '          server kibana:5601;',
                       '      }',
                       '      upstream elasticsearch_servers {',
                       '          server elasticsearch:9200;',
                       '      }',
                       '',
                       '################################################################################',
                       '## whiteboard',
                       '################################################################################',
                       '',
                       '    # Change nginx configuration',
                       '    $ docker exec -i -t $(docker ps | egrep -m 1 \'petelk/nginx\' | awk \'{print $1}\') /bin/bash',
                       ''])

    @staticmethod
    def add_solutions(snippy):
        """Add two default solutions for testing purposes."""

        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(SolutionHelper.SOLUTIONS_TEXT[0]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            sys.argv = ['snippy', 'import', '-f', 'howto-debug-elastic-beats.txt']
            snippy.reset()
            cause = snippy.run_cli()
            print(cause)
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1

        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(SolutionHelper.SOLUTIONS_TEXT[1]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            sys.argv = ['snippy', 'import', '-f', 'howto-debug-elastic-beats.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2

        return snippy
