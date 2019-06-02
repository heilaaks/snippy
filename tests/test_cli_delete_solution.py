# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
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

"""test_cli_delete_solution: Test workflows for deleting solutions."""

import pytest

from snippy.cause import Cause
from tests.lib.content import Content
from tests.lib.solution import Solution


class TestCliDeleteSolution(object):
    """Test workflows for deleting solutions."""

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_001(snippy):
        """Delete solution with digest.

        Delete solution with short 16 byte version of message digest.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '-d', '6cfe47a8880a8f81'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_002(snippy):
        """Delete solution with digest.

        Delete solution with without explicitly specifying solution category.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '-d', '6cfe47a8880a8f81'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_003(snippy):
        """Delete solution with digest.

        Delete solution with very short version of digest that matches to
        one solution.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '-d', '6cfe4'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_004(snippy):
        """Delete solution with digest.

        Delete solution with long 16 byte version of message digest.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        Content.assert_storage_size(2)
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '-d', '6cfe47a8880a8f81b66ff6bd71e795069ed1dfdd259c9fd181133f683c7697eb'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-nginx')
    def test_cli_delete_solution_005(snippy):
        """Delete solution with digest.

        Delete solution with empty message digest when there is only one
        content stored. In this case the last content can be deleted with
        empty digest.
        """

        Content.assert_storage_size(1)
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '-d', ''])
        assert cause == Cause.ALL_OK
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_006(snippy):
        """Delete solution with digest.

        Try to delete solution with message digest that cannot be found.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_007(snippy):
        """Delete solution with digest.

        Try to delete solution with empty message digest. Nothing should be
        deleted in this case because there is more than one content stored.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '-d', ''])
        assert cause == 'NOK: cannot use empty message digest for delete operation'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_008(snippy):
        """Delete solution with digest.

        Try to delete solution with short version of digest that does not
        match to any existing message digest.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '-d', '123456'])
        assert cause == 'NOK: cannot find content with message digest: 123456'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_009(snippy):
        """Delete solution with data.

        Delete solution based on content data.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        Content.assert_storage_size(2)
        data = '\n'.join(Solution.NGINX['data'])
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '--content', data])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_010(snippy):
        """Delete solution with data.

        Try to delete solution with content data that does not exist. In this
        case the content data is not truncated.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '--content', 'not-exists'])
        assert cause == 'NOK: cannot find content with content data: not-exists'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_011(snippy):
        """Delete solution with data.

        Try to delete solution with content data that does not exist. In this
        case the content data is truncated.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        data = Content.dump_text(Solution.KAFKA)
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '--content', data])
        assert cause == 'NOK: cannot find content with content data: ##############################...'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_012(snippy):
        """Delete solution with data.

        Try to delete solution with empty content data. Nothing should be
        deleted in this case because there is more than ne content left.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'delete', '--scat', 'solution', '--content', ''])
        assert cause == 'NOK: cannot use empty content data for delete operation'
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
