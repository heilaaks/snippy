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

"""reference: Default references for testing."""

from tests.lib.helper import Helper


class Reference(object):  # pylint: disable=too-few-public-methods
    """Default references for testing."""

    _GITLOG = 0
    _REGEXP = 1
    _PYTEST = 2

    # Default time is same for the default content. See 'Test case layouts and
    # data structures' for more information.
    DEFAULT_TIME = '2018-06-22T13:11:13.678729+00:00'

    # Default content must be always set so that it reflects content stored
    # into database. For example the tags must be sorted in correct order.
    # This forces defining erroneous content in each test case. This improves
    # the readability and maintainability of failure testing.
    _DEFAULTS = ({
        'category': 'reference',
        'data': (),
        'brief': 'How to write commit messages',
        'description': '',
        'name': '',
        'groups': ('git',),
        'tags': ('commit', 'git', 'howto'),
        'links': ('https://chris.beams.io/posts/git-commit/', ),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': '',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'uuid': '31cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f'
    }, {
        'category': 'reference',
        'data': (),
        'brief': 'Python regular expression',
        'description': '',
        'name': '',
        'groups': ('python',),
        'tags': ('howto', 'online', 'python', 'regexp'),
        'links': ('https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
                  'https://pythex.org/'),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': '',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'uuid': '32cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832'
    }, {
        'category': 'reference',
        'data': (),
        'brief': 'Python pytest framework',
        'description': '',
        'name': '',
        'groups': ('python',),
        'tags': ('docs', 'pytest', 'python'),
        'links': ('https://docs.pytest.org/en/latest/skipping.html', ),
        'source': '',
        'versions': (),
        'languages': (),
        'filename': '',
        'created': '2016-04-21T12:10:11.678729+00:00',
        'updated': '2016-04-21T12:10:11.678729+00:00',
        'uuid': '33cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'digest': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e'
    })

    GITLOG_CREATED = _DEFAULTS[_GITLOG]['created']
    GITLOG_UPDATED = _DEFAULTS[_GITLOG]['updated']
    REGEXP_CREATED = _DEFAULTS[_REGEXP]['created']
    REGEXP_UPDATED = _DEFAULTS[_REGEXP]['updated']
    PYTEST_CREATED = _DEFAULTS[_PYTEST]['created']
    PYTEST_UPDATED = _DEFAULTS[_PYTEST]['updated']

    if not DEFAULT_TIME == GITLOG_CREATED == GITLOG_UPDATED == REGEXP_CREATED == REGEXP_UPDATED:
        raise Exception('default content timestamps must be same - see \'Test case layouts and data structures\'')

    GITLOG_DIGEST = _DEFAULTS[_GITLOG]['digest']
    REGEXP_DIGEST = _DEFAULTS[_REGEXP]['digest']
    PYTEST_DIGEST = _DEFAULTS[_PYTEST]['digest']
    GITLOG_UUID = _DEFAULTS[_GITLOG]['uuid']
    REGEXP_UUID = _DEFAULTS[_REGEXP]['uuid']
    PYTEST_UUID = _DEFAULTS[_PYTEST]['uuid']

    GITLOG = _DEFAULTS[_GITLOG]
    REGEXP = _DEFAULTS[_REGEXP]
    PYTEST = _DEFAULTS[_PYTEST]
    DEFAULT_REFERENCES = (GITLOG, REGEXP)

    TEMPLATE = Helper.read_template('reference.txt').split('\n')
    TEMPLATE_DIGEST_EMPTY = 'bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d'
    TEMPLATE_TEXT = (
        '# Commented lines will be ignored.',
        '#',
        '# Add mandatory links below one link per line.',
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
        '# Add optional source reference below.',
        'https://www.example.com/source.md',
        '',
        '# Add optional comma separated list of key-value versions below.',
        'example=3.9.0,python>=3',
        '',
        '# Add optional comma separated list of languages below.',
        'example-language',
        '',
        '# Add optional filename below.',
        'example-content.md',
        '',
        '# Meta',
        'category : reference',
        'created  : 2018-02-02T02:02:02.000001+00:00',
        'digest   : f5693f66ec42e8f42687e8639df806e79aead1dad1a6c1b5448b6220995518bd',
        'updated  : 2018-02-02T02:02:02.000001+00:00',
        'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        ''
    )
    TEMPLATE_MKDN = (
        '# Add brief title for content @groups',
        '',
        '> Add a description that defines the content in one chapter.',
        '',
        '> [1] https://www.example.com/add-links-here.html',
        '',
        '## Meta',
        '',
        '> category  : reference  ',
        'created   : 2018-02-02T02:02:02.000001+00:00  ',
        'digest    : bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d  ',
        'filename  : example-content.md  ',
        'languages : example-language  ',
        'name      : example content handle  ',
        'source    : https://www.example.com/source.md  ',
        'tags      : example,tags  ',
        'updated   : 2018-02-02T02:02:02.000001+00:00  ',
        'uuid      : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
        'versions  : example=3.9.0,python>=3  ',
        ''
    )
