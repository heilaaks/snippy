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

"""solution_helper.py: Helper methods for solution testing."""

import mock

from snippy.cause import Cause
from snippy.config.constants import Constants as Const
from snippy.config.source.parser import Parser
from snippy.content.content import Content
from snippy.meta import __homepage__
from snippy.meta import __version__
from snippy.migrate.migrate import Migrate
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class SolutionHelper(object):
    """Helper methods for solution testing."""

    UTC1 = '2017-10-20 11:11:19'
    UTC2 = '2017-10-20 06:16:27'
    UTC3 = '2017-10-20 06:16:27'
    BEATS = 0
    NGINX = 1
    KAFKA = 2
    DEFAULTS = ({'data':('################################################################################',
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
                         ''),
                 'brief': 'Debugging Elastic Beats',
                 'group': 'beats',
                 'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                 'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                 'category' :'solution',
                 'filename' :'howto-debug-elastic-beats.txt',
                 'runalias': '',
                 'versions': '',
                 'created' :'2017-10-20 11:11:19',
                 'updated' :'2017-10-20 11:11:19',
                 'digest':'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'},
                {'data':('################################################################################',
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
                         "    $ nginx -V 2>&1 | grep -- '--with-debug'",
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
                         "    $ docker exec -i -t $(docker ps | egrep -m 1 'petelk/nginx' | awk '{print $1}') /bin/bash",
                         ''),
                 'brief': 'Debugging nginx',
                 'group': 'nginx',
                 'tags': ('debug', 'howto', 'logging', 'nginx'),
                 'links': ('https://www.nginx.com/resources/admin-guide/debug/', ),
                 'category': 'solution',
                 'filename': 'howto-debug-nginx.txt',
                 'runalias': '',
                 'versions': '',
                 'created': '2017-10-20 06:16:27',
                 'updated': '2017-10-20 06:16:27',
                 'digest': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe'},
                {'data':('################################################################################',
                         '## BRIEF : Testing docker log drivers',
                         '##',
                         '## DATE  : 2017-10-20 06:16:27',
                         '## GROUP : docker',
                         '## TAGS  : docker,moby,kubernetes,logging,plugin,driver,kafka,logs2kafka',
                         '## FILE  : kubernetes-docker-log-driver-kafka.txt',
                         '################################################################################',
                         '',
                         '################################################################################',
                         '## description',
                         '################################################################################',
                         '',
                         '    # Investigating docker log driver and especially the Kafka plugin.',
                         '',
                         '################################################################################',
                         '## references',
                         '################################################################################',
                         '',
                         '    # Kube Kafka log driver',
                         '    > https://github.com/MickayG/moby-kafka-logdriver',
                         '',
                         '    # Logs2Kafka',
                         '    > https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
                         '    > https://github.com/garo/logs2kafka',
                         '',
                         '################################################################################',
                         '## commands',
                         '################################################################################',
                         '',
                         '    # Get logs from pods',
                         '    $ kubectl get pods',
                         '    $ kubectl logs kafka-0',
                         '',
                         '    # Install docker log driver for Kafka',
                         '    $ docker ps --format "{{.Names}}" | grep -E \'kafka|logstash\'',
                         '    $ docker inspect k8s_POD_kafka-0...',
                         "    $ docker inspect --format '{{ .NetworkSettings.IPAddress }}' k8s_POD_kafka-0...",
                         '    $ docker plugin install --disable mickyg/kafka-logdriver:latest',
                         '    $ docker plugin set mickyg/kafka-logdriver:latest KAFKA_BROKER_ADDR="10.2.28.10:9092"',
                         '    $ docker plugin inspect mickyg/kafka-logdriver',
                         '    $ docker plugin enable mickyg/kafka-logdriver:latest',
                         '    $ docker run --log-driver mickyg/kafka-logdriver:latest hello-world',
                         '    $ docker plugin disable mickyg/kafka-logdriver:latest',
                         '',
                         '    # Get current docker log driver',
                         "    $ docker info |grep 'Logging Driver' # Default driver",
                         '    $ docker ps --format "{{.Names}}" | grep -E \'kafka|logstash\'',
                         '    $ docker inspect k8s_POD_kafka-0...',
                         "    $ docker inspect --format '{{ .NetworkSettings.IPAddress }}' k8s_POD_logstash...",
                         "    $ docker inspect --format '{{ .NetworkSettings.IPAddress }}' k8s_POD_kafka-0...",
                         '    $ docker inspect $(docker ps | grep POD | awk \'{print $1}\') | grep -E "Hostname|NetworkID',
                         '    $ docker inspect $(docker ps | grep POD | awk \'{print $1}\') | while read line ; do egrep -E ' +
                         '\'"Hostname"|"IPAddress"\' ; done | while read line ; do echo $line ; done',
                         '',
                         '################################################################################',
                         '## solutions',
                         '################################################################################',
                         '',
                         '################################################################################',
                         '## configurations',
                         '################################################################################',
                         '',
                         '    # Logstash configuration',
                         '    $ vi elk-stack/logstash/build/pipeline/kafka.conf',
                         '      input {',
                         '          gelf {}',
                         '      }',
                         '',
                         '      output {',
                         '          elasticsearch {',
                         '            hosts => ["elasticsearch"]',
                         '          }',
                         '          stdout {}',
                         '      }',
                         '',
                         '    # Kafka configuration',
                         '    $ vi elk-stack/logstash/build/pipeline/kafka.conf',
                         '    kafka {',
                         '        type => "argus.docker"',
                         '        topics => ["dockerlogs"]',
                         '        codec => "plain"',
                         '        bootstrap_servers => "kafka:9092"',
                         '        consumer_threads => 1',
                         '    }',
                         '',
                         '################################################################################',
                         '## whiteboard',
                         '################################################################################',
                         ''),
                 'brief': 'Testing docker log drivers',
                 'group': 'docker',
                 'tags': ('docker', 'moby', 'kubernetes', 'logging', 'plugin', 'driver', 'kafka', 'logs2kafka'),
                 'links': ('https://github.com/MickayG/moby-kafka-logdriver',
                           'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
                           'https://github.com/garo/logs2kafka'),
                 'category': 'solution',
                 'filename': 'kubernetes-docker-log-driver-kafka.txt',
                 'runalias': '',
                 'versions': '',
                 'created': '2017-10-20 06:16:27',
                 'updated': '2017-10-20 06:16:27',
                 'digest': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57'})

    TEMPLATE_UTC = '2017-10-14 19:56:31'
    TEMPLATE = ('################################################################################',
                '## BRIEF : ',
                '##',
                '## DATE  : 2017-10-14 19:56:31',
                '## GROUP : default',
                '## TAGS  : ',
                '## FILE  : ',
                '################################################################################',
                '',
                '',
                '################################################################################',
                '## description',
                '################################################################################',
                '',
                '################################################################################',
                '## references',
                '################################################################################',
                '',
                '################################################################################',
                '## commands',
                '################################################################################',
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
                '')

    @staticmethod
    def get_metadata(utc):
        """Return the default metadata for exported data."""

        return Snippet.get_metadata(utc)

    @staticmethod
    def get_http_metadata():
        """Return the default HTTP metadata."""

        return Snippet.get_http_metadata()

    @staticmethod
    def get_content(text=None, solution=None):
        """Transform text template to content."""

        if text:
            contents = Parser.read_content(Content(category=Const.SOLUTION), text, SolutionHelper.UTC1)
            content = contents[0]
            content.update_digest()
        else:
            content = Content.load({'content': [SolutionHelper.DEFAULTS[solution]]})[0]

        return content

    @staticmethod
    def get_dictionary(template):
        """Transform template to dictinary."""

        content = SolutionHelper.get_content(template)
        dictionary = Migrate.get_dictionary_list([content])

        return dictionary[0]

    @staticmethod
    def get_template(dictionary):
        """Transform dictionary to text template."""

        contents = Content.load({'content': [dictionary]})

        return contents[0].convert_text()

    @staticmethod
    def add_defaults(snippy=None):
        """Add default solutions for testing purposes."""

        if not snippy:
            snippy = Snippy()

        mocked_open = mock.mock_open(read_data=SolutionHelper.get_template(SolutionHelper.DEFAULTS[SolutionHelper.BEATS]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            cause = snippy.run_cli(['snippy', 'import', '-f', 'howto-debug-elastic-beats.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1

        mocked_open = mock.mock_open(read_data=SolutionHelper.get_template(SolutionHelper.DEFAULTS[SolutionHelper.NGINX]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            cause = snippy.run_cli(['snippy', 'import', '-f', 'howto-debug-nginx.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2

        return snippy

    @staticmethod
    def add_one(index, snippy=None):
        """Add one default solution for testing purposes."""

        if not snippy:
            snippy = Snippy()

        mocked_open = mock.mock_open(read_data=SolutionHelper.get_template(SolutionHelper.DEFAULTS[index]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            contents = len(Database.get_solutions())
            cause = snippy.run_cli(['snippy', 'import', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == contents + 1

        return snippy

    @staticmethod
    def sorted_json_list(json_data):
        """Sort list of JSONs but keep the oder of main level list containing JSONs."""

        return Snippet.sorted_json_list(json_data)

    @staticmethod
    def error_body(body):
        """Make Python2 and Python3 compatible error body."""

        return Snippet.error_body(body)

    @staticmethod
    def test_content(snippy, mock_file, dictionary):
        """Compare given dictionary against content stored in database based on message digest."""

        for digest in dictionary:
            mock_file.reset_mock()
            cause = snippy.run_cli(['snippy', 'export', '-d', digest, '-f', 'defined-content.txt'])
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-content.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(SolutionHelper.get_template(dictionary[digest])),
                                                mock.call(Const.NEWLINE)])

    @staticmethod
    def test_content2(dictionary):
        """Compare given dictionary against content stored in database based on message digest."""

        Snippet.test_content2(dictionary)
