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

"""test_cli_create_solution: Test workflows for creating solutions."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution


class TestCliCreateSolution(object):
    """Test workflows for creating solutions."""

    @pytest.mark.usefixtures('snippy', 'edit-beats')
    def test_cli_create_solution_001(self, snippy):
        """Create solution from CLI.

        Create new solution by defining all content parameters from command
        line. Creating solution from command line will always use editor to
        create the content.
        """

        content = {
            'data': [
                Solution.DEFAULTS[Solution.BEATS]
            ]
        }
        data = Const.DELIMITER_DATA.join(content['data'][0]['data'])
        brief = content['data'][0]['brief']
        groups = Const.DELIMITER_GROUPS.join(content['data'][0]['groups'])
        tags = Const.DELIMITER_TAGS.join(content['data'][0]['tags'])
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links'])
        cause = snippy.run(['snippy', 'create', '--solution', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions', 'edit-beats')
    def test_cli_create_solution_002(self, snippy):
        """Try to create solution from CLI.

        Try to create same solution again with exactly the same content data.
        """

        content = {
            'data': [
                Solution.DEFAULTS[Solution.BEATS],
                Solution.DEFAULTS[Solution.NGINX]
            ]
        }
        cause = snippy.run(['snippy', 'create', '--solution'])
        assert cause == 'NOK: content data already exist with digest: db712a82662d6932'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('edit-solution-template')
    def test_cli_create_solution_003(self, snippy):
        """Try to create solution from CLI.

        Try to create new solution without any changes to template.
        """

        cause = snippy.run(['snippy', 'create', '--solution'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('edit-empty')
    def test_cli_create_solution_004(self, snippy):
        """Try to create solution from CLI.

        Try to create new solution with empty data. In this case the whole
        template is deleted and the edited solution is an empty string.
        """

        cause = snippy.run(['snippy', 'create', '--solution'])
        assert cause == 'NOK: could not identify edited content category - please keep tags in place'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('edit-unknown-solution-template')
    def test_cli_create_solution_005(self, snippy):
        """Try to create solution from CLI.

        Try to create new solution with a template that cannot be identified.
        In this case the user has changed the input template completely and
        it has lost tags that identify it as a solution content.
        """

        cause = snippy.run(['snippy', 'create', '--solution'])
        assert cause == 'NOK: could not identify edited content category - please keep tags in place'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('snippy', 'edit-beats')
    def test_cli_create_solution_006(self, snippy):
        """Create solution from editor.

        Create new solution by defining all values from editor.
        """

        content = {
            'data': [
                Solution.DEFAULTS[Solution.BEATS]
            ]
        }
        cause = snippy.run(['snippy', 'create', '--solution', '--editor'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
