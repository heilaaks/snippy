#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
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

"""test_cli_delete_solution: Test workflows for deleting solutions."""

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliDeleteSolution(object):
    """Test workflows for deleting solutions."""

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_001(self, snippy, mocker):
        """Delete solution with digest.

        Delete solution with short 16 byte version of message digest.
        """

        content_read = {Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS]}
        cause = snippy.run(['snippy', 'delete', '--solution', '-d', '61a24a156f5e9d2d'])
        assert cause == Cause.ALL_OK
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_002(self, snippy, mocker):
        """Delete solution with digest.

        Delete solution with without explicitly specifying solution category.
        """

        content_read = {Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS]}
        cause = snippy.run(['snippy', 'delete', '-d', '61a24a156f5e9d2d'])
        assert cause == Cause.ALL_OK
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_003(self, snippy, mocker):
        """Delete solution with digest.

        Delete solution with very short version of digest that matches to
        one solution.
        """

        content_read = {Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS]}
        cause = snippy.run(['snippy', 'delete', '--solution', '-d', '61a24'])
        assert cause == Cause.ALL_OK
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_004(self, snippy, mocker):
        """Delete solution with digest.

        Delete solution with long 16 byte version of message digest.
        """

        content_read = {Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS]}
        cause = snippy.run(['snippy', 'delete', '--solution', '-d', '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-nginx')
    def test_cli_delete_solution_005(self, snippy):
        """Delete solution with digest.

        Delete solution with empty message digest when there is only one
        content stored. In this case the last content can be deleted with
        empty digest.
        """

        cause = snippy.run(['snippy', 'delete', '--solution', '-d', ''])
        assert cause == Cause.ALL_OK
        assert not Database.get_solutions().size()

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_006(self, snippy, mocker):
        """Delete solution with digest.

        Try to delete solution with message digest that cannot be found.
        """

        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX],
        }
        cause = snippy.run(['snippy', 'delete', '--solution', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_007(self, snippy, mocker):
        """Delete solution with digest.

        Try to delete solution with empty message digest. Nothing should be
        deleted in this case because there is more than one content stored.
        """

        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX],
        }
        cause = snippy.run(['snippy', 'delete', '--solution', '-d', ''])
        assert cause == 'NOK: cannot use empty message digest for: delete :operation'
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_008(self, snippy, mocker):
        """Delete solution with digest.

        Try to delete solution with short version of digest that does not
        match to any existing message digest.
        """

        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX],
        }
        cause = snippy.run(['snippy', 'delete', '--solution', '-d', '123456'])
        assert cause == 'NOK: cannot find content with message digest: 123456'
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_009(self, snippy, mocker):
        """Delete solution with data.

        Delete solution based on content data.
        """

        content_read = {Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS]}
        data = Solution.get_template(Solution.DEFAULTS[Solution.NGINX])
        cause = snippy.run(['snippy', 'delete', '--solution', '--content', data])
        assert cause == Cause.ALL_OK
        assert Database.get_solutions().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_010(self, snippy, mocker):
        """Delete solution with data.

        Try to delete solution with content data that does not exist. In this
        case the content data is not truncated.
        """

        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX],
        }
        cause = snippy.run(['snippy', 'delete', '--solution', '--content', 'not-exists'])
        assert cause == 'NOK: cannot find content with content data: not-exists'
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_011(self, snippy, mocker):
        """Delete solution with data.

        Try to delete solution with content data that does not exist. In this
        case the content data is truncated.
        """

        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX],
        }
        data = Solution.get_template(Solution.DEFAULTS[Solution.KAFKA])
        cause = snippy.run(['snippy', 'delete', '--solution', '--content', data])
        assert cause == 'NOK: cannot find content with content data: ##############################...'
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_delete_solution_012(self, snippy, mocker):
        """Delete solution with data.

        Try to delete solution with empty content data. Nothing should be
        deleted in this case because there is more than ne content left.
        """

        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX],
        }
        cause = snippy.run(['snippy', 'delete', '--solution', '--content', ''])
        assert cause == 'NOK: cannot use empty content data for: delete :operation'
        assert Database.get_solutions().size() == 2
        Content.verified(mocker, snippy, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
