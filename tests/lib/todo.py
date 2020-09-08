# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""todo: Default snippets for testing."""


class Todo(object):  # pylint: disable=too-few-public-methods
    """Default todos for testing."""

    _DEFMKD = 0
    _DEPLOY = 1

    # Default time is same for the default content. See 'Test case layouts and
    # data structures' for more information.
    DEFAULT_TIME = '2017-10-14T19:56:31.000001+00:00'

    _DEFAULTS = ({
        'category': 'todo',
        'data': ('[ ] Add todo item.  # No Timeline [95a832]', ),
        'brief': '',
        'description': '',
        'name': '',
        'groups': ('default',),
        'tags': (),
        'links': (),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': '',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'uuid': 'a1cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': 'fb0544e8817b654994a1295dc47a46af616350c35c468a3084699f8579d1546e'
    }, {
        'category': 'todo',
        'data': ('docker rm --volumes $(docker ps --all --quiet)',),
        'brief': 'Remove all docker containers with volumes',
        'description': '',
        'name': '',
        'groups': ('testing',),
        'tags': ('todo', 'testing'),
        'links': (),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': '',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319'
    })

    DEFMKD_CREATED = _DEFAULTS[_DEFMKD]['created']
    DEFMKD_UPDATED = _DEFAULTS[_DEPLOY]['updated']
    DEPLOY_CREATED = _DEFAULTS[_DEFMKD]['created']
    DEPLOY_UPDATED = _DEFAULTS[_DEPLOY]['updated']

    if not DEFAULT_TIME == DEFMKD_CREATED == DEFMKD_UPDATED == DEPLOY_CREATED == DEPLOY_UPDATED:
        raise Exception('default content timestamps must be same - see \'Test case layouts and data structures\'')

    DEFMKD = _DEFAULTS[_DEFMKD]
    DEPLOY = _DEFAULTS[_DEPLOY]

    TEMPLATE_MKDN = (
        '# Add brief title for content @groups',
        '',
        '> Add a description that defines the content in one chapter.',
        '',
        '## Todo',
        '',
        '- [ ] Add todo item.',
        '',
        '## Whiteboard',
        '',
        '## Meta',
        '',
        '> category  : todo  ',
        'created   : 2017-10-14T19:56:31.000001+00:00  ',
        'digest    : fe2e819adb53cada064ebd0e22697ae04d3248e34d77f8c7a4c346c4c5d43d0b  ',
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
