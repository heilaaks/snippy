#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""snippet: Default snippets for testing."""

from tests.lib.helper import Helper


class Snippet(object):  # pylint: disable=too-few-public-methods
    """Default snippets for testing."""

    _REMOVE = 0
    _FORCED = 1
    _EXITED = 2
    _NETCAT = 3
    _UMOUNT = 4
    _INTERP = 5

    # Default time is same for the default content. See 'Test case layouts and
    # data structures' for more information.
    DEFAULT_TIME = '2017-10-14T19:56:31.000001+00:00'

    # Default content must be always set so that it reflects content stored
    # into database. For example the tags must be sorted in correct order.
    # This forces defining erroneous content in each test case. This improves
    # the readability and maintainability of failure testing.
    _DEFAULTS = ({
        'category': 'snippet',
        'data': ('docker rm --volumes $(docker ps --all --quiet)',),
        'brief': 'Remove all docker containers with volumes',
        'description': '',
        'name': '',
        'groups': ('docker',),
        'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
        'links': ('https://docs.docker.com/engine/reference/commandline/rm/', ),
        'source': '',
        'versions': (),
        'filename': '',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
    }, {
        'category': 'snippet',
        'data': ('docker rm --force redis', ),
        'brief': 'Remove docker image with force',
        'description': '',
        'name': '',
        'groups': ('docker',),
        'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'moby'),
        'links': ('https://docs.docker.com/engine/reference/commandline/rm/',
                  'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-' +
                  'images-containers-and-volumes'),
        'source': '',
        'versions': (),
        'filename': '',
        'uuid': '12cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'digest': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5'
    }, {
        'category': 'snippet',
        'data': ('docker rm $(docker ps --all -q -f status=exited)',
                 'docker images -q --filter dangling=true | xargs docker rmi'),
        'brief': 'Remove all exited containers and dangling images',
        'description': '',
        'name': '',
        'groups': ('docker',),
        'tags': ('cleanup', 'container', 'docker', 'docker-ce', 'image', 'moby'),
        'links': ('https://docs.docker.com/engine/reference/commandline/images/',
                  'https://docs.docker.com/engine/reference/commandline/rm/',
                  'https://docs.docker.com/engine/reference/commandline/rmi/'),
        'source': '',
        'versions': (),
        'filename': '',
        'created': '2017-10-20T07:08:45.000001+00:00',
        'updated': '2017-10-20T07:08:45.000001+00:00',
        'uuid': '13cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73'
    }, {
        'category': 'snippet',
        'data': ('nc -v 10.183.19.189 443',
                 'nmap 10.183.19.189'),
        'brief': 'Test if specific port is open',
        'description': '',
        'name': '',
        'groups': ('linux',),
        'tags': ('linux', 'netcat', 'networking', 'port'),
        'links': ('https://www.commandlinux.com/man-page/man1/nc.1.html',),
        'source': '',
        'versions': (),
        'filename': '',
        'created': '2017-10-20T07:08:45.000001+00:00',
        'updated': '2017-10-20T07:08:45.000001+00:00',
        'uuid': '14cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d'
    }, {
        'category': 'snippet',
        'data': ('lsof | grep \'/tmp/overlayfs/overlay\'',
                 'kill <pid>',
                 'umount /tmp/overlayfs/overlay'),
        'brief': 'Umount a busy device',
        'description': '',
        'name': '',
        'groups': ('linux',),
        'tags': ('device', 'linux', 'umount'),
        'links': ('https://stackoverflow.com/a/7878763',),
        'source': '',
        'versions': (),
        'filename': '',
        'created': '2018-05-07T11:11:55.000001+00:00',
        'updated': '2018-05-07T11:11:55.000001+00:00',
        'uuid': '15cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '490c913cf941a0bedc14e3d390894958b3db4220dc2b1b856454403c888df17f'
    }, {
        'category': 'snippet',
        'data': ('find . -type d -name \'.git\' | while read dir ; do sh -c "cd $dir/../ && echo -e \\"\\nGIT STATUS IN ${dir//\\.git/}\\" && git status -s" ; done',),  # pylint: disable=line-too-long
        'brief': 'Perform recursive git status on subdirectories',
        'description': '',
        'name': '',
        'groups': ('git',),
        'tags': ('git', 'status'),
        'links': ('https://gist.github.com/tafkey/664266c00387c98631b3',),
        'source': '',
        'versions': (),
        'filename': '',
        'created': '2018-01-11T07:59:46.000001+00:00',
        'updated': '2018-01-11T07:59:46.000001+00:00',
        'uuid': '16cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '9e1949c2810df2a50137f0a4056b7992529b37632d9db0da7040d17bf16f5bd3'
    })

    REMOVE_CREATED = _DEFAULTS[_REMOVE]['created']
    REMOVE_UPDATED = _DEFAULTS[_REMOVE]['updated']
    FORCED_CREATED = _DEFAULTS[_FORCED]['created']
    FORCED_UPDATED = _DEFAULTS[_FORCED]['updated']
    EXITED_CREATED = _DEFAULTS[_EXITED]['created']
    EXITED_UPDATED = _DEFAULTS[_EXITED]['updated']
    NETCAT_CREATED = _DEFAULTS[_NETCAT]['created']
    NETCAT_UPDATED = _DEFAULTS[_NETCAT]['updated']
    UMOUNT_CREATED = _DEFAULTS[_UMOUNT]['created']
    UMOUNT_UPDATED = _DEFAULTS[_UMOUNT]['updated']
    INTERP_CREATED = _DEFAULTS[_INTERP]['created']
    INTERP_UPDATED = _DEFAULTS[_INTERP]['updated']

    if not DEFAULT_TIME == REMOVE_CREATED == REMOVE_UPDATED == FORCED_CREATED == FORCED_UPDATED:
        raise Exception('default content timestamps must be same - see \'Test case layouts and data structures\'')

    REMOVE_DIGEST = _DEFAULTS[_REMOVE]['digest']
    FORCED_DIGEST = _DEFAULTS[_FORCED]['digest']
    EXITED_DIGEST = _DEFAULTS[_EXITED]['digest']
    NETCAT_DIGEST = _DEFAULTS[_NETCAT]['digest']
    UMOUNT_DIGEST = _DEFAULTS[_UMOUNT]['digest']
    INTERP_DIGEST = _DEFAULTS[_INTERP]['digest']
    REMOVE_UUID = _DEFAULTS[_REMOVE]['uuid']
    FORCED_UUID = _DEFAULTS[_FORCED]['uuid']
    EXITED_UUID = _DEFAULTS[_EXITED]['uuid']
    NETCAT_UUID = _DEFAULTS[_NETCAT]['uuid']
    UMOUNT_UUID = _DEFAULTS[_UMOUNT]['uuid']
    INTERP_UUID = _DEFAULTS[_INTERP]['uuid']


    REMOVE = _DEFAULTS[_REMOVE]
    FORCED = _DEFAULTS[_FORCED]
    EXITED = _DEFAULTS[_EXITED]
    NETCAT = _DEFAULTS[_NETCAT]
    UMOUNT = _DEFAULTS[_UMOUNT]
    INTERP = _DEFAULTS[_INTERP]
    DEFAULT_SNIPPETS = (REMOVE, FORCED)

    TEMPLATE = Helper.read_template('snippet.txt').split('\n')
    TEMPLATE_DIGEST_EMPTY = 'b4bedc2603e3b9ea95bcf53cb7b8aa6efa31eabb788eed60fccf3d8029a6a6cc'
    TEMPLATE_TEXT = (
        '# Commented lines will be ignored.',
        '#',
        '# Add mandatory snippet below.',
        '',
        '',
        '# Add optional brief description below.',
        'Add brief title for content',
        '',
        '# Add optional description below.',
        'Add a description that defines the content in one chapter.',
        '',
        '# Add optional name below.',
        'example content handle',
        '',
        '# Add optional comma separated list of groups below.',
        'groups',
        '',
        '# Add optional comma separated list of tags below.',
        'example,tags',
        '',
        '# Add optional links below one link per line.',
        'https://www.example.com/add-links-here.html',
        '',
        '# Add optional source reference below.',
        'https://www.example.com/source.md',
        '',
        '# Add optional comma separated list of key-value versions below.',
        'example=3.9.0,python>=3',
        '',
        '# Add optional filename below.',
        'example-content.md',
        ''
    )
    TEMPLATE_MKDN = (
        '# Add brief title for content @groups',
        '',
        '> Add a description that defines the content in one chapter.',
        '',
        '> [1] https://www.example.com/add-links-here.html',
        '',
        '`$ Markdown commands are defined between backtics and prefixed by a dollar sign`',
        '',
        '## Meta',
        '',
        '> category : snippet  ',
        'created  : 2018-02-02T02:02:02.000001+00:00  ',
        'digest   : 8d5193fea452d0334378a73ded829cfa27debea7ee87714d64b1b492d1a4601a  ',
        'filename : example-content.md  ',
        'name     : example content handle  ',
        'source   : https://www.example.com/source.md  ',
        'tags     : example,tags  ',
        'updated  : 2018-02-02T02:02:02.000001+00:00  ',
        'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
        'versions : example=3.9.0,python>=3  ',
        ''
    )
