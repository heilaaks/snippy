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


class SolutionHelper(object):
    """Helper methods for solution testing."""

    BEATS = 0
    NGINX = 1
    KAFKA = 2

    BEATS_DIGEST = 'a96accc25dd23ac0'
    NGINX_DIGEST = '61a24a156f5e9d2d'
    KAFKA_DIGEST = 'eeef5ca3ec9cd364'
    DEFAULTS = ({
        'data':('################################################################################',
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
        'name': '',
        'filename' :'howto-debug-elastic-beats.txt',
        'versions': '',
        'uuid': '21cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created' :'2017-10-20T11:11:19.000001+0000',
        'updated' :'2017-10-20T11:11:19.000001+0000',
        'digest':'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'
    }, {
        'data':('################################################################################',
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
        'name': '',
        'filename': 'howto-debug-nginx.txt',
        'versions': '',
        'uuid': '22cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': '2017-10-20T06:16:27.000001+0000',
        'updated': '2017-10-20T06:16:27.000001+0000',
        'digest': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe'
    }, {
        'data':('################################################################################',
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
        'name': '',
        'filename': 'kubernetes-docker-log-driver-kafka.txt',
        'versions': '',
        'uuid': '23cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': '2017-10-20T06:16:27.000001+0000',
        'updated': '2017-10-20T06:16:27.000001+0000',
        'digest': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57'
    })

    TEMPLATE = (
        '################################################################################',
        '## BRIEF : ',
        '##',
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
        ''
    )

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
    def _get_content(source):
        """Transform text template to content."""

        timestamp = Config.utcnow()
        collection = Parser.read_content(timestamp, source)

        return collection
