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

"""test_cli_delete_reference: Test workflows for deleting references."""

import pytest

from snippy.cause import Cause
from tests.lib.content import Content
from tests.lib.reference import Reference


class TestCliDeleteReference(object):
    """Test workflows for deleting references."""

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_001(snippy):
        """Delete reference with digest.

        Delete reference with short 16 byte version of message digest.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '-d', 'cb9225a81eab8ced'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog')
    def test_cli_delete_reference_002(snippy):
        """Delete reference with digest.

        Delete reference with empty message digest when there is only one
        content stored. In this case the last content can be deleted with
        empty digest.
        """

        Content.assert_storage_size(1)
        cause = snippy.run(['snippy', 'delete', '-d', ''])
        assert cause == Cause.ALL_OK
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_003(snippy):
        """Delete reference with digest.

        Try to delete reference with message digest that cannot be found.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'delete', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_004(snippy):
        """Delete reference with uuid.

        Try to delete reference with short content UUID. Since the UUID is
        unique, this must not delete the content.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '-u', '16cd5827'])
        assert cause == 'NOK: cannot find content with content uuid: 16cd5827'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_005(snippy):
        """Delete reference with uuid.

        Try to delete content with empty uuid string.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'delete', '-u', ''])
        assert cause == 'NOK: cannot use empty content uuid for delete operation'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_006(snippy):
        """Delete reference with uuid.

        Try to delete content with uuid that does not match to any content.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'delete', '-u', '1234567'])
        assert cause == 'NOK: cannot find content with content uuid: 1234567'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_007(snippy):
        """Delete reference with uuid.

        Try to delete content with uuid that matches to more than one content.
        In this case nothing should get deleted because the operatione permits
        only one content to be deleted in one operation.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'delete', '-u', '1'])
        assert cause == 'NOK: cannot find content with content uuid: 1'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_008(snippy):
        """Delete reference with data.

        Delete reference based on content data.
        """

        content = {
            'data': [
                Reference.REGEXP
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '--content', 'https://chris.beams.io/posts/git-commit/'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_009(snippy):
        """Delete reference with data.

        Try to delete reference with content data that does not exist. In this
        case the content data is not truncated.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--content', 'not found content'])
        assert cause == 'NOK: cannot find content with content data: not found content'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.skip(reason='not supported yet')
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_010(snippy):
        """Delete reference with link.

        Delete reference based on content link.
        """

        content = {
            'data': [
                Reference.REGEXP
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '--links', 'https://chris.beams.io/posts/git-commit/'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_011(snippy):
        """Delete reference with data.

        Try to delete reference with empty content data. Nothing should be
        deleted in this case because there is more than one content left.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--content', ''])
        assert cause == 'NOK: cannot use empty content data for delete operation'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_012(snippy):
        """Delete reference with search.

        Delete reference based on search keyword that results one hit. In this
        case the content is deleted.
        """

        content = {
            'data': [
                Reference.REGEXP
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '--sall', 'chris', '--scat', 'reference'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_013(snippy):
        """Try to delete reference with search.

        Try to delete reference based on search keyword so that the category
        is left out. In this case the search keyword matches but the default
        category is snippet and content is not deleted.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--sall', 'chris'])
        assert cause == 'NOK: cannot find content with given search criteria'
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
