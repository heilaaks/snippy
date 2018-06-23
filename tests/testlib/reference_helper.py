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

"""reference_helper: Helper methods for reference testing."""


class ReferenceHelper(object):  # pylint: disable=too-few-public-methods
    """Helper methods for reference testing."""

    GITLOG = 0
    REGEXP = 1

    GITLOG_DIGEST = '5c2071094dbfaa33'
    REGEXP_DIGEST = 'd65a6322aef85e63'
    DEFAULTS = ({
        'data': ('', ),
        'brief': 'How to write commit messages',
        'group': 'git',
        'tags': ('commit', 'git', 'howto'),
        'links': ('https://chris.beams.io/posts/git-commit/', ),
        'category': 'reference',
        'filename': '',
        'runalias': '',
        'versions': '',
        'created': '2018-06-22T13:11:13.678729+0000',
        'updated': '2018-06-22T13:11:13.678729+0000',
        'digest': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f'
    }, {
        'data': ('', ),
        'brief': 'Python regular expression',
        'group': 'python',
        'tags': (' python ', ' regexp  ', '  online   ', 'howto'),
        'links': ('https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
                  'https://pythex.org/'),
        'category': 'reference',
        'filename': '',
        'runalias': '',
        'versions': '',
        'created': '2018-05-21T13:11:13.678729+0000',
        'updated': '2018-05-21T13:11:13.678729+0000',
        'digest': 'd65a6322aef85e637162a8ec3ed2dae1c5ac00a6413b60d04da64ffea40e74ab'
    })

    TEMPLATE = (
        '# Commented lines will be ignored.',
        '#',
        '# Add mandatory links below one link per line.',
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
        ''
    )
