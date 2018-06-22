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

    GITLOG_DIGEST = '2459998d3b556b9e'
    REGEXP_DIGEST = '2459998d3b556b9e'
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
        'digest': '2459998d3b556b9e8a5b640e84426e05046b5235fe34a5958dcfdbfabad7efbb'
    }, {
        'data': ('', ),
        'brief': 'Python regular expression',
        'group': 'python',
        'tags': (' python ', ' regexp  ', '  online   '),
        'links': ('https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
                  'https://pythex.org/'),
        'category': 'reference',
        'filename': '',
        'runalias': '',
        'versions': '',
        'created': '2018-05-21T13:11:13.678729+0000',
        'updated': '2018-05-21T13:11:13.678729+0000',
        'digest': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5'
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
