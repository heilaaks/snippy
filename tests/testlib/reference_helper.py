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

from snippy.config.config import Config
from snippy.content.collection import Collection


class ReferenceHelper(object):  # pylint: disable=too-few-public-methods
    """Helper methods for reference testing."""

    GITLOG = 0
    REGEXP = 1
    PYTEST = 2

    GITLOG_DIGEST = '5c2071094dbfaa33'
    REGEXP_DIGEST = 'cb9225a81eab8ced'
    PYTEST_DIGEST = '1f9d9496005736ef'
    DEFAULTS = ({
        'data': ('', ),
        'brief': 'How to write commit messages',
        'group': 'git',
        'tags': ('commit', 'git', 'howto'),
        'links': ('https://chris.beams.io/posts/git-commit/', ),
        'category': 'reference',
        'name': '',
        'filename': '',
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
        'name': '',
        'filename': '',
        'versions': '',
        'created': '2018-05-21T13:11:13.678729+0000',
        'updated': '2018-05-21T13:11:13.678729+0000',
        'digest': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832'
    }, {
        'data': ('', ),
        'brief': 'Python pytest framework',
        'group': 'python',
        'tags': ('python', 'pytest', 'docs'),
        'links': ('https://docs.pytest.org/en/latest/skipping.html', ),
        'category': 'reference',
        'name': '',
        'filename': '',
        'versions': '',
        'created': '2016-04-21T12:10:11.678729+0000',
        'updated': '2016-04-21T12:10:11.678729+0000',
        'digest': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e'
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

    @staticmethod
    def get_template(dictionary):
        """Transform dictionary to text template."""

        resource = Collection.get_resource(dictionary['category'], '2018-10-20T06:16:27.000001+0000')
        resource.load_dict(dictionary)

        return resource.dump_text(Config.templates)
