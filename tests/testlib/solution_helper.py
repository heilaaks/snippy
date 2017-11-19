#!/usr/bin/env python3

"""solution_helper.py: Helper methods for solution testing."""

import sys
import mock
from snippy.snip import Snippy
from snippy.version import __version__
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.editor import Editor
from snippy.content.content import Content
from snippy.migrate.migrate import Migrate
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class SolutionHelper(object):
    """Helper methods for solution testing."""

    UTC = '2017-10-01 11:53:17'
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
                 'utc' :'2017-10-20 11:11:19',
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
                 'utc': '2017-10-20 06:16:27',
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
                 'utc': '2017-10-20 06:16:27',
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

        metadata = {'utc': utc,
                    'version': __version__,
                    'homepage': 'https://github.com/heilaaks/snippy'}

        return metadata

    @staticmethod
    def get_content(text=None, solution=None):
        """Transform text template to content."""

        if text:
            content = Content(content=(Const.EMPTY,)*13, category=Const.SOLUTION)
            editor = Editor(Content(content=(Const.EMPTY,)*13, category=Const.SOLUTION), SolutionHelper.UTC, text)
            content.set((editor.get_edited_data(),
                         editor.get_edited_brief(),
                         editor.get_edited_group(),
                         editor.get_edited_tags(),
                         editor.get_edited_links(),
                         editor.get_edited_category(),
                         editor.get_edited_filename(),
                         content.get_runalias(),
                         content.get_versions(),
                         editor.get_edited_date(),
                         content.get_digest(),
                         content.get_metadata(),
                         content.get_key()))
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
        editor = Editor(contents[0], SolutionHelper.UTC)

        return editor.get_template()

    @staticmethod
    def add_defaults(snippy):
        """Add default solutions for testing purposes."""

        if not snippy:
            snippy = Snippy()

        mocked_open = mock.mock_open(read_data=SolutionHelper.get_template(SolutionHelper.DEFAULTS[SolutionHelper.BEATS]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            sys.argv = ['snippy', 'import', '-f', 'howto-debug-elastic-beats.txt']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1

        mocked_open = mock.mock_open(read_data=SolutionHelper.get_template(SolutionHelper.DEFAULTS[SolutionHelper.NGINX]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            sys.argv = ['snippy', 'import', '-f', 'howto-debug-nginx.txt']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2

        return snippy

    @staticmethod
    def add_one(snippy, index):
        """Add one default solution for testing purposes."""

        if not snippy:
            snippy = Snippy()

        mocked_open = mock.mock_open(read_data=SolutionHelper.get_template(SolutionHelper.DEFAULTS[index]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True):
            sys.argv = ['snippy', 'import', '-f', 'one-solution.txt']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1

        return snippy

    @staticmethod
    def test_content(snippy, mock_file, dictionary):
        """Compare given dictionary against content stored in database based on message digest."""

        for digest in dictionary:
            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '-d', digest, '-f', 'defined-content.txt']
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-content.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(SolutionHelper.get_template(dictionary[digest])),
                                                mock.call(Const.NEWLINE)])
