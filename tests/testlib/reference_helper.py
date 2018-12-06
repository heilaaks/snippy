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
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from tests.testlib.helper import Helper


class ReferenceHelper(object):
    """Helper methods for reference testing."""

    GITLOG = 0
    REGEXP = 1
    PYTEST = 2

    DEFAULT_TIME = '2018-06-22T13:11:13.678729+0000'
    DEFAULT_SOLUTIONS = (GITLOG, REGEXP)

    # Default content must be always set so that it reflects content stored
    # into database. For example the tags must be sorted in correct order.
    # This forces defining erroneous content in each test case. This improves
    # the readability and maintainability of failure testing.
    DEFAULTS = ({
        'data': (),
        'brief': 'How to write commit messages',
        'description': '',
        'groups': ('git',),
        'tags': ('commit', 'git', 'howto'),
        'links': ('https://chris.beams.io/posts/git-commit/', ),
        'category': 'reference',
        'name': '',
        'filename': '',
        'versions': '',
        'source': '',
        'uuid': '31cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'digest': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f'
    }, {
        'data': (),
        'brief': 'Python regular expression',
        'description': '',
        'groups': ('python',),
        'tags': ('howto', 'online', 'python', 'regexp'),
        'links': ('https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
                  'https://pythex.org/'),
        'category': 'reference',
        'name': '',
        'filename': '',
        'versions': '',
        'source': '',
        'uuid': '32cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': DEFAULT_TIME,
        'updated': DEFAULT_TIME,
        'digest': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832'
    }, {
        'data': (),
        'brief': 'Python pytest framework',
        'description': '',
        'groups': ('python',),
        'tags': ('docs', 'pytest', 'python'),
        'links': ('https://docs.pytest.org/en/latest/skipping.html', ),
        'category': 'reference',
        'name': '',
        'filename': '',
        'versions': '',
        'source': '',
        'uuid': '33cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': '2016-04-21T12:10:11.678729+0000',
        'updated': '2016-04-21T12:10:11.678729+0000',
        'digest': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e'
    })

    GITLOG_CREATED = DEFAULTS[GITLOG]['created']
    GITLOG_UPDATED = DEFAULTS[GITLOG]['updated']
    REGEXP_CREATED = DEFAULTS[REGEXP]['created']
    REGEXP_UPDATED = DEFAULTS[REGEXP]['updated']
    PYTEST_CREATED = DEFAULTS[PYTEST]['created']
    PYTEST_UPDATED = DEFAULTS[PYTEST]['updated']

    if not DEFAULT_TIME == GITLOG_CREATED == GITLOG_UPDATED == REGEXP_CREATED == REGEXP_UPDATED:
        raise Exception('default content timestamps must be same - see \'Test case layouts and data structures\'')

    GITLOG_DIGEST = DEFAULTS[GITLOG]['digest']
    REGEXP_DIGEST = DEFAULTS[REGEXP]['digest']
    PYTEST_DIGEST = DEFAULTS[PYTEST]['digest']

    TEMPLATE = Helper.read_template('reference.txt').split(Const.NEWLINE)

    @staticmethod
    def get_dictionary(template):
        """Transform template to dictinary."""

        collection = Collection()
        collection.load(Const.CONTENT_FORMAT_TEXT, Config.utcnow(), template)
        resource = next(collection.resources())

        return resource.dump_dict(Config.remove_fields)

    @staticmethod
    def dump(content, content_format):
        """Dump content in requested format.

        Args:
            content (dict): Content in dictionary.
            content_format (str): Content format.

        Returns:
            str: Content in requested format.
        """

        dump = Const.EMPTY
        resource = Collection.get_resource(content['category'], '2018-10-20T06:16:27.000001+0000')
        resource.load_dict(content)
        if content_format == Const.CONTENT_FORMAT_TEXT:
            dump = resource.dump_text(Config.templates)
        elif content_format == Const.CONTENT_FORMAT_MKDN:
            dump = resource.dump_mkdn(Config.templates)

        return dump
