# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""solution: Default solutions for testing."""

from tests.lib.helper import Helper


class Solution(object):  # pylint: disable=too-few-public-methods
    """Default solutions for testing."""

    _BEATS = 0
    _NGINX = 1
    _KAFKA = 2
    _KAFKA_MKDN = 3

    # Default time is same for the default content. See 'Test case layouts and
    # data structures' for more information.
    DEFAULT_TIME = '2017-10-20T11:11:19.000001+00:00'

    # Default content must be always set so that it reflects content stored
    # into database. For example the tags must be sorted in correct order.
    # This forces defining erroneous content in each test case. This improves
    # the readability and maintainability of failure testing.
    _DEFAULTS = ({
        'category': 'solution',
        'data':('################################################################################',
                '## Description',
                '################################################################################',
                '',
                '    # Debug Elastic Beats',
                '',
                '################################################################################',
                '## References',
                '################################################################################',
                '',
                '    # Enable logs from Filebeat',
                '    > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
                '',
                '################################################################################',
                '## Commands',
                '################################################################################',
                '',
                '    # Run Filebeat with full log level',
                '    $ ./filebeat -e -c config/filebeat.yml -d "*"',
                '',
                '################################################################################',
                '## Solutions',
                '################################################################################',
                '',
                '################################################################################',
                '## Configurations',
                '################################################################################',
                '',
                '################################################################################',
                '## Whiteboard',
                '################################################################################',
                ''),
        'brief': 'Debugging Elastic Beats',
        'description': 'Debug Elastic Beats',
        'name': '',
        'groups': ('beats',),
        'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
        'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': 'howto-debug-elastic-beats.txt',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'uuid': '21cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '4346ba4c792474308bc66bd16d747875bef9b431044824987e302b726c1d298e'
    }, {
        'category': 'solution',
        'data':('################################################################################',
                '## Description',
                '################################################################################',
                '',
                '    # Instructions how to debug nginx.',
                '',
                '################################################################################',
                '## References',
                '################################################################################',
                '',
                '    # Official nginx debugging',
                '    > https://www.nginx.com/resources/admin-guide/debug/',
                '',
                '################################################################################',
                '## Commands',
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
                '## Solutions',
                '################################################################################',
                '',
                '################################################################################',
                '## Configurations',
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
                '## Whiteboard',
                '################################################################################',
                '',
                '    # Change nginx configuration',
                "    $ docker exec -i -t $(docker ps | egrep -m 1 'petelk/nginx' | awk '{print $1}') /bin/bash",
                ''),
        'brief': 'Debugging nginx',
        'description': 'Instructions how to debug nginx.',
        'name': '',
        'groups': ('nginx',),
        'tags': ('debug', 'howto', 'logging', 'nginx'),
        'links': ('https://www.nginx.com/resources/admin-guide/debug/', ),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': 'howto-debug-nginx.txt',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'uuid': '22cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '6cfe47a8880a8f81b66ff6bd71e795069ed1dfdd259c9fd181133f683c7697eb'
    }, {
        'category': 'solution',
        'data':('################################################################################',
                '## Description',
                '################################################################################',
                '',
                '    # Investigating docker log driver and especially the Kafka plugin.',
                '',
                '################################################################################',
                '## References',
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
                '## Commands',
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
                '## Solutions',
                '################################################################################',
                '',
                '################################################################################',
                '## Configurations',
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
                '## Whiteboard',
                '################################################################################',
                ''),
        'brief': 'Testing docker log drivers',
        'description': 'Investigating docker log driver and especially the Kafka plugin.',
        'name': '',
        'groups': ('docker',),
        'tags': ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin'),
        'links': ('https://github.com/MickayG/moby-kafka-logdriver',
                  'https://github.com/garo/logs2kafka',
                  'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': 'kubernetes-docker-log-driver-kafka.txt',
        'created': '2017-10-20T06:16:27.000001+00:00',
        'updated': '2017-10-20T06:16:27.000001+00:00',
        'uuid': '23cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': 'ee3f2ab7c63d6965ac2531003807f00caee178f6e1cbb870105c7df86e6d5be2'
    }, {
        'category': 'solution',
        'data':('## Description',
                '',
                'Investigate docker log drivers and the logs2kafka log plugin.',
                '',
                '## References',
                '',
                '   ```',
                '   # Kube Kafka log driver',
                '   > https://github.com/MickayG/moby-kafka-logdriver',
                '   ```',
                '',
                '   ```',
                '   # Logs2Kafka',
                '   > https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
                '   > https://github.com/garo/logs2kafka',
                '   ```',
                '',
                '## Commands',
                '',
                '   ```',
                '   # Get logs from pods',
                '   $ kubectl get pods',
                '   $ kubectl logs kafka-0',
                '   ```',
                '',
                '   ```',
                '   # Install docker log driver for Kafka',
                '   $ docker ps --format "{{.Names}}" | grep -E \'kafka|logstash\'',
                '   $ docker inspect k8s_POD_kafka-0...',
                '   $ docker inspect --format \'{{ .NetworkSettings.IPAddress }}\' k8s_POD_kafka-0...',
                '   $ docker plugin install --disable mickyg/kafka-logdriver:latest',
                '   $ docker plugin set mickyg/kafka-logdriver:latest KAFKA_BROKER_ADDR="10.2.28.10:9092"',
                '   $ docker plugin inspect mickyg/kafka-logdriver',
                '   $ docker plugin enable mickyg/kafka-logdriver:latest',
                '   $ docker run --log-driver mickyg/kafka-logdriver:latest hello-world',
                '   $ docker plugin disable mickyg/kafka-logdriver:latest',
                '   ```',
                '',
                '   ```',
                '   # Get current docker log driver',
                '   $ docker info |grep \'Logging Driver\' # Default driver',
                '   $ docker ps --format "{{.Names}}" | grep -E \'kafka|logstash\'',
                '   $ docker inspect k8s_POD_kafka-0...',
                '   $ docker inspect --format \'{{ .NetworkSettings.IPAddress }}\' k8s_POD_logstash...',
                '   $ docker inspect --format \'{{ .NetworkSettings.IPAddress }}\' k8s_POD_kafka-0...',
                '   $ docker inspect $(docker ps | grep POD | awk \'{print $1}\') | grep -E "Hostname|NetworkID',
                '   $ docker inspect $(docker ps | grep POD | awk \'{print $1}\') | while read line ; do egrep -E \'"Hostname"|"IPAddress"\' ; done | while read line ; do echo $line ; done',  # noqa pylint: disable=line-too-long
                '   ```',
                '',
                '## Configurations',
                '',
                '   ```',
                '   # Logstash configuration',
                '   $ vi elk-stack/logstash/build/pipeline/kafka.conf',
                '     input {',
                '         gelf {}',
                '     }',
                '',
                '     output {',
                '         elasticsearch {',
                '           hosts => ["elasticsearch"]',
                '         }',
                '         stdout {}',
                '     }',
                '   ```',
                '',
                '   ```',
                '   # Kafka configuration',
                '   $ vi elk-stack/logstash/build/pipeline/kafka.conf',
                '   kafka {',
                '       type => "argus.docker"',
                '       topics => ["dockerlogs"]',
                '       codec => "plain"',
                '       bootstrap_servers => "kafka:9092"',
                '       consumer_threads => 1',
                '   }',
                '   ```',
                '',
                '## Solutions',
                '',
                '## Whiteboard',
                ''),
        'brief': 'Testing docker log drivers',
        'description': 'Investigate docker log drivers and the logs2kafka log plugin.',
        'name': '',
        'groups': ('docker',),
        'tags': ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin'),
        'links': ('https://github.com/MickayG/moby-kafka-logdriver',
                  'https://github.com/garo/logs2kafka',
                  'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': 'kubernetes-docker-log-driver-kafka.mkdn',
        'created': '2019-01-04T10:54:49.265512+00:00',
        'updated': '2019-01-05T10:54:49.265512+00:00',
        'uuid': '24cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': 'c54c8a896b94ea35edf6c798879957419d26268bd835328d74b19a6e9ce2324d'
    })

    BEATS_CREATED = _DEFAULTS[_BEATS]['created']
    BEATS_UPDATED = _DEFAULTS[_BEATS]['updated']
    NGINX_CREATED = _DEFAULTS[_NGINX]['created']
    NGINX_UPDATED = _DEFAULTS[_NGINX]['updated']
    KAFKA_CREATED = _DEFAULTS[_KAFKA]['created']
    KAFKA_UPDATED = _DEFAULTS[_KAFKA]['updated']
    KAFKA_MKDN_CREATED = _DEFAULTS[_KAFKA_MKDN]['created']
    KAFKA_MKDN_UPDATED = _DEFAULTS[_KAFKA_MKDN]['updated']

    if not DEFAULT_TIME == BEATS_CREATED == BEATS_UPDATED == NGINX_CREATED == NGINX_UPDATED:
        raise Exception('default content timestamps must be same - see \'Test case layouts and data structures\'')

    BEATS_DIGEST = _DEFAULTS[_BEATS]['digest']
    NGINX_DIGEST = _DEFAULTS[_NGINX]['digest']
    KAFKA_DIGEST = _DEFAULTS[_KAFKA]['digest']
    KAFKA_MKDN_DIGEST = _DEFAULTS[_KAFKA_MKDN]['digest']
    BEATS_UUID = _DEFAULTS[_BEATS]['uuid']
    NGINX_UUID = _DEFAULTS[_NGINX]['uuid']
    KAFKA_UUID = _DEFAULTS[_KAFKA]['uuid']
    KAFKA_MKDN_UUID = _DEFAULTS[_KAFKA_MKDN]['uuid']

    BEATS = _DEFAULTS[_BEATS]
    NGINX = _DEFAULTS[_NGINX]
    KAFKA = _DEFAULTS[_KAFKA]
    KAFKA_MKDN = _DEFAULTS[_KAFKA_MKDN]
    DEFAULT_SOLUTIONS = (BEATS, NGINX)

    TEMPLATE = Helper.read_template('solution.txt').split('\n')
    TEMPLATE_DIGEST_TEXT = 'be2ec3ade0e984463c1d3346910a05625897abd8d3feae4b2e54bfd6aecbde2d'
    TEMPLATE_DIGEST_MKDN = '073ea152d867cf06b2ee993fb1aded4c8ccbc618972db5c18158b5b68a5da6e4'

    TEMPLATE_TEXT = (
        '################################################################################',
        '## BRIEF  : Add brief title for content',
        '##',
        '## GROUPS : groups',
        '## TAGS   : example,tags',
        '## FILE   : example-content.md',
        '################################################################################',
        '',
        '',
        '################################################################################',
        '## Description',
        '################################################################################',
        '',
        '################################################################################',
        '## References',
        '################################################################################',
        '',
        '################################################################################',
        '## Commands',
        '################################################################################',
        '',
        '################################################################################',
        '## Configurations',
        '################################################################################',
        '',
        '################################################################################',
        '## Solutions',
        '################################################################################',
        '',
        '################################################################################',
        '## Whiteboard',
        '################################################################################',
        '',
        '################################################################################',
        '## Meta',
        '################################################################################',
        '',
        'category  : solution',
        'created   : 2017-10-14T19:56:31.000001+00:00',
        'digest    : 50c37862816a197c63b2ae72c511586c3463814509c0d5c7ebde534ce0209935',
        'languages : example-language',
        'name      : example content handle',
        'source    : https://www.example.com/source.md',
        'updated   : 2017-10-14T19:56:31.000001+00:00',
        'uuid      : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'versions  : example=3.9.0,python>=3',
        ''
    )
    TEMPLATE_MKDN = (
        '# Add brief title for content @groups',
        '',
        '> Add a description that defines the content in one chapter.',
        '',
        '> ',
        '',
        '## Description',
        '',
        '## References',
        '',
        '## Commands',
        '',
        '## Configurations',
        '',
        '## Solutions',
        '',
        '## Whiteboard',
        '',
        '## Meta',
        '',
        '> category  : solution  ',
        'created   : 2017-10-14T19:56:31.000001+00:00  ',
        'digest    : 5facdc16dc81851c2f65b112a0921eb2f2db206c7756714efb45ba0026471f11  ',
        'filename  : example-content.md  ',
        'languages : example-language  ',
        'name      : example content handle  ',
        'source    : https://www.example.com/source.md  ',
        'tags      : example,tags  ',
        'updated   : 2017-10-14T19:56:31.000001+00:00  ',
        'uuid      : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
        'versions  : example=3.9.0,python>=3  ',
        ''
    )

    _OUTPUTS = [(
        '',
        '   # Elastic,beats,debug,filebeat,howto',
        '   > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
        '',
        '   : ################################################################################',
        '   : ## Description',
        '   : ################################################################################',
        '   : ',
        '   :     # Debug Elastic Beats',
        '   : ',
        '   : ################################################################################',
        '   : ## References',
        '   : ################################################################################',
        '   : ',
        '   :     # Enable logs from Filebeat',
        '   :     > https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',
        '   : ',
        '   : ################################################################################',
        '   : ## Commands',
        '   : ################################################################################',
        '   : ',
        '   :     # Run Filebeat with full log level',
        '   :     $ ./filebeat -e -c config/filebeat.yml -d "*"',
        '   : ',
        '   : ################################################################################',
        '   : ## Solutions',
        '   : ################################################################################',
        '   : ',
        '   : ################################################################################',
        '   : ## Configurations',
        '   : ################################################################################',
        '   : ',
        '   : ################################################################################',
        '   : ## Whiteboard',
        '   : ################################################################################'
    )]
    BEATS_OUTPUT = _OUTPUTS[_BEATS]
