#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""solution_helper: Helper methods for solution testing."""

from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.config.source.parser import Parser
from snippy.content.collection import Collection
from tests.testlib.helper import Helper


class SolutionHelper(object):
    """Helper methods for solution testing."""

    BEATS = 0
    NGINX = 1
    KAFKA = 2

    # Default content must be always set so that it reflects content stored
    # into a database. For example the tags must be sorted correct here. This
    # forces creating special error cases in each test case and enforces more
    # controlled failure testing.
    BEATS_DIGEST = 'db712a82662d6932'
    NGINX_DIGEST = '7c226ee33a088381'
    KAFKA_DIGEST = 'fffeaf31e98e68a3'
    DEFAULTS = ({
        'data':('################################################################################',
                '## BRIEF  : Debugging Elastic Beats',
                '##',
                '## GROUPS : beats',
                '## TAGS   : Elastic,beats,filebeat,debug,howto',
                '## FILE   : howto-debug-elastic-beats.txt',
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
        'description': 'Debug Elastic Beats',
        'groups': ('beats',),
        'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
        'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
        'category' :'solution',
        'name': '',
        'filename' :'howto-debug-elastic-beats.txt',
        'versions': '',
        'source': '',
        'uuid': '21cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created' :'2017-10-20T11:11:19.000001+0000',
        'updated' :'2017-10-20T11:11:19.000001+0000',
        'digest':'db712a82662d693206004c2174a0bb1900e1e1307f21f79a0efb88a01add4151'
    }, {
        'data':('################################################################################',
                '## BRIEF  : Debugging nginx ',
                '##',
                '## GROUPS : nginx',
                '## TAGS   : nginx,debug,logging,howto',
                '## FILE   : howto-debug-nginx.txt',
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
        'description': 'Instructions how to debug nginx.',
        'groups': ('nginx',),
        'tags': ('debug', 'howto', 'logging', 'nginx'),
        'links': ('https://www.nginx.com/resources/admin-guide/debug/', ),
        'category': 'solution',
        'name': '',
        'filename': 'howto-debug-nginx.txt',
        'versions': '',
        'source': '',
        'uuid': '22cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': '2017-10-20T06:16:27.000001+0000',
        'updated': '2017-10-20T06:16:27.000001+0000',
        'digest': '7c226ee33a0883815f3dee7ad70f000dfeb34ed3fae78691ace5c4dca6bcb175'
    }, {
        'data':('################################################################################',
                '## BRIEF  : Testing docker log drivers',
                '##',
                '## GROUPS : docker',
                '## TAGS   : docker,moby,kubernetes,logging,plugin,driver,kafka,logs2kafka',
                '## FILE   : kubernetes-docker-log-driver-kafka.txt',
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
        'description': 'Investigating docker log driver and especially the Kafka plugin.',
        'groups': ('docker',),
        'tags': ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin'),
        'links': ('https://github.com/MickayG/moby-kafka-logdriver',
                  'https://github.com/garo/logs2kafka',
                  'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'),
        'category': 'solution',
        'name': '',
        'filename': 'kubernetes-docker-log-driver-kafka.txt',
        'versions': '',
        'source': '',
        'uuid': '23cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': '2017-10-20T06:16:27.000001+0000',
        'updated': '2017-10-20T06:16:27.000001+0000',
        'digest': 'fffeaf31e98e68a3dd063a1db0e334c0bc7e7c2f774262c5df0f95210c5ff1ee'
    })

    TEMPLATE = Helper.read_template('solution.txt').split(Const.NEWLINE)

    OUTPUT = [(
        '',
        '   # Elastic,beats,debug,filebeat,howto',
        '   > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
        '',
        '   : ################################################################################',
        '   : ## BRIEF  : Debugging Elastic Beats',
        '   : ##',
        '   : ## GROUPS : beats',
        '   : ## TAGS   : Elastic,beats,filebeat,debug,howto',
        '   : ## FILE   : howto-debug-elastic-beats.txt',
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
        '   : ################################################################################'
    )]

    @staticmethod
    def get_dictionary(template):
        """Transform template to dictinary."""

        collection = SolutionHelper._get_content(template)
        resource = next(collection.resources())

        return resource.dump_dict(Config.remove_fields)

    @staticmethod
    def get_template(dictionary):
        """Transform dictionary to text template."""

        resource = Collection.get_resource(Const.SOLUTION, '2018-10-20T06:16:27.000001+0000')
        resource.load_dict(dictionary)

        return resource.dump_text(Config.templates)

    @staticmethod
    def _get_content(text):
        """Transform text template to content."""

        collection = Parser(Const.CONTENT_FORMAT_TEXT, Config.utcnow(), text).read()

        return collection
