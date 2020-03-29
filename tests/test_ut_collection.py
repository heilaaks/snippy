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

"""test_ut_collection: Test Collection() class."""

from __future__ import print_function

import pytest

from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from tests.lib.helper import Helper


class TestUtCollection(object):
    """Test Collection() class."""

    @staticmethod
    def test_collection_operations_001(capsys):
        """Test collection data class operations.

        Verify that collection class implements data class methods correctly.
        In this case there are no resources in collection.
        """

        collection = Collection()

        # Collection with len().
        assert not collection

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

        # Equality of two empty collections.
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

        # Iterate resources in collection.
        for resource in collection:
            resource.digest = resource.digest
            assert 0

        # Get list of keys (digest) from collection.
        assert not collection.keys()

        # Get list of values (resources) from collection.
        assert not collection.values()

        # Test generator.
        resources = collection.resources()
        with pytest.raises(StopIteration):
            next(resources)

        # Printing collection.
        output = (
            '# collection meta',
            '   ! total : 0',
            '',
            ''
        )
        print(collection)  # Part of the test.
        out, err = capsys.readouterr()
        out = Helper.remove_ansi(out)
        assert out == Const.NEWLINE.join(output)
        assert not err

        # Access non existent resource from collection.
        with pytest.raises(KeyError):
            resource = collection[0]

        # Delete non existent resource from collection with string.
        with pytest.raises(KeyError):
            del collection['012123']

        # Delete non existent resource from collection with number.
        with pytest.raises(KeyError):
            del collection[0]

        # Two created objects must not point ot same reference.
        if collection is collection2:
            assert 0

        # Reference of object must be to the same object.
        collection3 = collection
        if collection3 is not collection:
            assert 0

    @staticmethod
    @pytest.mark.usefixtures('uuid')
    def test_collection_operations_002(capsys):  # pylint: disable=too-many-branches
        """Test collection data class operations.

        Verify that collection class implements data class methods correctly.
        In this case there is only one resource in collection.
        """

        collection = Collection()
        collection.load_dict(Helper.EXPORT_TIME, {
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

        # Collection with len().
        assert len(collection) == 1

        # Collection with condition.
        if collection:
            assert 1
        else:
            assert 0

        # Collection with negative condition.
        if not collection:
            assert 0
        else:
            assert 1

        # Equality of two different collections where the UUID differs.
        collection2 = Collection()
        collection2.load_dict(Helper.EXPORT_TIME, {
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
        if collection == collection2:
            assert 0
        else:
            assert 1

        # Non equality of two different collections.
        if collection != collection2:
            assert 1
        else:
            assert 0

        # Equality of two same collections.
        collection2 = collection
        if collection == collection2:
            assert 1
        else:
            assert 0

        # Non equality of same collections.
        if collection != collection2:
            assert 0
        else:
            assert 1

        # Equality of two collection with different length.
        collection2 = Collection()
        if collection == collection2:
            assert 0
        else:
            assert 1

        # Equality collection and random type.
        if collection == 1:
            assert 0
        else:
            assert 1

        # Iterate resources in collection.
        i = 0
        for resource in collection:
            resource.digest = resource.digest
            i = i + 1
        assert i == 1

        # Get list of keys (digest) from collection.
        assert len(collection.keys()) == 1
        assert collection.keys() == list(['e79ae51895908c5a40e570dc60a4dd594febdecf781c77c7b3cad37f9e0b7240'])

        # Get list of values (resources) from collection.
        assert len(collection.values()) == 1
        assert collection.values()[0] == collection['e79ae51895908c5a40e570dc60a4dd594febdecf781c77c7b3cad37f9e0b7240']

        # Test generator.
        resources = collection.resources()
        assert next(resources) == collection['e79ae51895908c5a40e570dc60a4dd594febdecf781c77c7b3cad37f9e0b7240']
        with pytest.raises(StopIteration):
            next(resources)

        # Printing collection.
        output = (
            '1. Manipulate compressed tar files @linux [e79ae51895908c5a]',
            '',
            '   $ tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./',
            '   $ tar xfO mytar.tar.gz manifest.json# Cat file in compressed tar.',
            '',
            '   # howto,linux,tar,untar',
            '',
            '   ! category    : snippet',
            '   ! created     : 2018-02-02T02:02:02.000001+00:00',
            '   ! description : ',
            '   ! digest      : e79ae51895908c5a40e570dc60a4dd594febdecf781c77c7b3cad37f9e0b7240 (True)',
            '   ! filename    : ',
            '   ! id          : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! languages   : ',
            '   ! name        : ',
            '   ! source      : ',
            '   ! updated     : 2018-02-02T02:02:02.000001+00:00',
            '   ! uuid        : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            '   ! versions    : ',
            '',
            '# collection meta',
            '   ! total : 1',
            '',
            ''
        )
        print(collection)  # Part of the test.
        out, err = capsys.readouterr()
        out = Helper.remove_ansi(out)
        assert out == Const.NEWLINE.join(output)
        assert not err

        with pytest.raises(KeyError):
            resource = collection[0]

    @staticmethod
    @pytest.mark.usefixtures('uuid')
    def test_collection_operations_003():
        """Test merging resources and collections.

        Verify that merging collection or resource to collection works.
        """

        collection1 = Collection()
        collection2 = Collection()
        collection1.load_dict(Helper.EXPORT_TIME, {
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

        # Try to merge two collections that is not supported.
        assert len(collection1) == 1
        assert not collection2
        digest = collection2.merge(collection1)
        assert not collection2
        assert digest is None

        # Merge resource to collection.
        digest = collection2.merge(collection1['e79ae51895908c5a40e570dc60a4dd594febdecf781c77c7b3cad37f9e0b7240'])
        assert len(collection2) == 1
        assert digest == 'e79ae51895908c5a40e570dc60a4dd594febdecf781c77c7b3cad37f9e0b7240'

        # Merge already existing resource to collection.
        digest = collection2.merge(collection1['e79ae51895908c5a40e570dc60a4dd594febdecf781c77c7b3cad37f9e0b7240'])
        assert len(collection2) == 1
        assert digest == 'e79ae51895908c5a40e570dc60a4dd594febdecf781c77c7b3cad37f9e0b7240'

        # Try to migrate random type to collection.
        collection2.migrate('string')
        assert len(collection2) == 1

    @staticmethod
    @pytest.mark.usefixtures('uuid')
    def test_collection_operations_004():
        """Test collection data class operations.

        Verify values with None generate default values for resource. For
        example a None for brief must generate empty string for resource
        brief attribute.
        """

        collection = Collection()
        collection.load_dict(Helper.EXPORT_TIME, {
            'data': [{
                'category': Const.SNIPPET,
                'data': [
                    'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./',
                    'tar xfO mytar.tar.gz manifest.json# Cat file in compressed tar.'],
                'brief': None,
                'description': None,
                'name': None,
                'groups': None,
                'tags': None,
                'links': None,
                'source': None,
                'versions': None,
                'languages': None,
                'filename': None
            }]
        })
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == (
            'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./',
            'tar xfO mytar.tar.gz manifest.json# Cat file in compressed tar.'
        )
        assert resource.brief == ''
        assert resource.description == ''
        assert resource.name == ''
        assert resource.groups == ()
        assert resource.tags == ()
        assert resource.links == ()
        assert resource.source == ''
        assert resource.versions == ()
        assert resource.languages == ()
        assert resource.filename == ''
        assert resource.digest == '6dae3799010719ca694b86514ec404cd6b6047a2979b3dbaf75fa51576ad269c'
