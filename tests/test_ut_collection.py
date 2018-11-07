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

"""test_ut_collection: Test Collection() class."""

import pytest

from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from tests.testlib.helper import Helper


class TestUtCollection(object):
    """Test Collection() class."""

    def test_collection_operations_001(self, snippy, capsys):
        """Test collection data class operations.

        Verify that collection class implements the data class properties
        correctly. In this case there are no resources in collection.
        """

        collection = Collection()

        # Collection with len().
        assert len(collection) == 0

        # Collection with condition.
        if collection:
            assert 0
        else:
            assert 1

        # Collection with negative condition.
        if not collection:
            assert 1
        else:
            assert 0

        # Equality of two emtpy collections.
        collection2 = Collection()
        if collection == collection2:
            assert 1
        else:
            assert 0

        # Non equality of two empty collections.
        if collection != collection2:
            assert 0
        else:
            assert 1

        # Collection with loop.
        for resource in collection:
            assert 0

        # Printing collection.
        output = (
            '# collection meta',
            '   ! total : 0',
            '',
            ''
        )
        print(collection)
        out, err = capsys.readouterr()
        out = Helper.remove_ansi(out)
        print(out)
        assert out == Const.NEWLINE.join(output)
        assert not err

        with pytest.raises(Exception):
            collection[0]

    def test_collection_operations_002(self, snippy, capsys):
        """Test collection data class operations.

        Verify that collection class implements the data class properties
        correctly. In this case there is only one resource in collection.
        """

        collection = Collection()
        collection.load_dict({
            'data': [{
                'data': [
                    'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./',
                    'tar xfO mytar.tar.gz manifest.json# Cat file in compressed tar.'],
                'brief': 'Manipulate compressed tar files',
                'groups': ['linux'],
                'tags': ['howto', 'linux', 'tar', 'untar'],
                'category': Const.SNIPPET
            }]
        })
        assert len(collection) == 1

        #for resource in collection:
        #    print("HERE")
        #    print(resource)
        #print(collection)

        #assert 0
