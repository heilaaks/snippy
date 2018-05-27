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

"""snippet_helper: Helper methods for snippet testing."""

from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.parser import Parser
from snippy.content.collection import Collection


class SnippetHelper(object):
    """Helper methods for snippet testing."""

    REMOVE = 0
    FORCED = 1
    EXITED = 2
    NETCAT = 3
    UMOUNT = 4

    REMOVE_DIGEST = '54e41e9b52a02b63'
    FORCED_DIGEST = '53908d68425c61dc'
    EXITED_DIGEST = '49d6916b6711f13d'
    NETCAT_DIGEST = 'f3fd167c64b6f97e'
    UMOUNT_DIGEST = '490c913cf941a0be'
    DEFAULTS = ({'data': ('docker rm --volumes $(docker ps --all --quiet)', ),
                 'brief': 'Remove all docker containers with volumes',
                 'group': 'docker',
                 'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
                 'links': ('https://docs.docker.com/engine/reference/commandline/rm/', ),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'created': '2017-10-14T19:56:31.000001+0000',
                 'updated': '2017-10-14T19:56:31.000001+0000',
                 'digest': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'},
                {'data': ('docker rm --force redis', ),
                 'brief': 'Remove docker image with force',
                 'group': 'docker',
                 'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
                 'links': ('https://docs.docker.com/engine/reference/commandline/rm/',
                           'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-' +
                           'images-containers-and-volumes'),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'created': '2017-10-14T19:56:31.000001+0000',
                 'updated': '2017-10-14T19:56:31.000001+0000',
                 'digest': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5'},
                {'data': ('docker rm $(docker ps --all -q -f status=exited)',
                          'docker images -q --filter dangling=true | xargs docker rmi'),
                 'brief': 'Remove all exited containers and dangling images',
                 'group': 'docker',
                 'tags': ('docker-ce', 'docker', 'moby', 'container', 'cleanup', 'image'),
                 'links': ('https://docs.docker.com/engine/reference/commandline/rm/',
                           'https://docs.docker.com/engine/reference/commandline/images/',
                           'https://docs.docker.com/engine/reference/commandline/rmi/'),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'created': '2017-10-20T07:08:45.000001+0000',
                 'updated': '2017-10-20T07:08:45.000001+0000',
                 'digest': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73'},
                {'data': ('nc -v 10.183.19.189 443',
                          'nmap 10.183.19.189'),
                 'brief': 'Test if specific port is open',
                 'group': 'linux',
                 'tags': ('linux', 'netcat', 'networking', 'port'),
                 'links': ('https://www.commandlinux.com/man-page/man1/nc.1.html',),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'created': '2017-10-20T07:08:45.000001+0000',
                 'updated': '2017-10-20T07:08:45.000001+0000',
                 'digest': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d'},
                {'data': ('lsof | grep \'/tmp/overlayfs/overlay\'',
                          'kill <pid>',
                          'umount /tmp/overlayfs/overlay'),
                 'brief': 'Umount a busy device',
                 'group': 'linux',
                 'tags': ('device', 'linux', 'umount'),
                 'links': ('https://stackoverflow.com/a/7878763',),
                 'category': 'snippet',
                 'filename': '',
                 'runalias': '',
                 'versions': '',
                 'created': '2018-05-07T11:11:55.000001+0000',
                 'updated': '2018-05-07T11:11:55.000001+0000',
                 'digest': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d'})

    TEMPLATE = ('# Commented lines will be ignored.',
                '#',
                '# Add mandatory snippet below.',
                '',
                '',
                '# Add optional brief description below.',
                '',
                '',
                '# Add optional single group below.',
                'default',
                '',
                '# Add optional comma separated list of tags below.',
                '',
                '',
                '# Add optional links below one link per line.',
                '',
                '')

    @staticmethod
    def get_collection(snippet=None):
        """Transform text template to content."""

        collection = Collection()
        resource = collection.get_resource(Const.SNIPPET, Config.utcnow())
        resource.load_dict(SnippetHelper.DEFAULTS[snippet])
        collection.migrate(resource)

        return collection

    @staticmethod
    def get_dictionary(template):
        """Transform template to dictinary."""

        collection = SnippetHelper._get_content(template)
        resource = next(collection.resources())

        return resource.dump_dict(Config.remove_fields)

    @staticmethod
    def get_template(dictionary):
        """Transform dictionary to text template."""

        resource = Collection.get_resource(Const.SNIPPET, '2018-10-20T06:16:27.000001+0000')
        resource.load_dict(dictionary)

        return resource.dump_text(Config.templates)

    @staticmethod
    def _get_content(source):
        """Transform text template to content."""

        collection = Parser.read_content(Config.utcnow(), source)

        return collection
