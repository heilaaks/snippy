#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""test_cli_create_solution: Test workflows for creating solutions."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.solution import Solution


class TestCliCreateSolution(object):
    """Test workflows for creating solutions."""

    @staticmethod
    @pytest.mark.usefixtures('snippy', 'create-beats-utc')
    def test_cli_create_solution_001(snippy):
        """Create solution from CLI.

        Create new solution by defining all content parameters from command
        line. Creating solution uses editor by default only if the data field
        is not defined. In this case editor is not used.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['description'] = ''
        content['data'][0]['filename'] = ''
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][0]['digest'] = 'b8dfd78b2f92caac57469acda50bebf4dca9fd3e85bb9083c8408f430fc83f52'
        data = Const.DELIMITER_DATA.join(content['data'][0]['data'])
        brief = content['data'][0]['brief']
        groups = Const.DELIMITER_GROUPS.join(content['data'][0]['groups'])
        tags = Const.DELIMITER_TAGS.join(content['data'][0]['tags'])
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links'])
        cause = snippy.run(['snippy', 'create', '--scat', 'solution', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links, '--format', 'text'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions', 'edit-beats')
    def test_cli_create_solution_002(snippy):
        """Try to create solution from CLI.

        Try to create same solution again with exactly the same content data.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'create', '--scat', 'solution', '--format', 'text'])
        assert cause == 'NOK: content data already exist with digest db712a82662d6932'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('edit-solution-template')
    def test_cli_create_solution_003(snippy):
        """Try to create solution from CLI.

        Try to create new solution without any changes to template.
        """

        cause = snippy.run(['snippy', 'create', '--scat', 'solution', '--format', 'text'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('edit-empty')
    def test_cli_create_solution_004(snippy):
        """Try to create solution from CLI.

        Try to create new solution with empty data. In this case the whole
        template is deleted and the edited solution is an empty string.
        """

        cause = snippy.run(['snippy', 'create', '--scat', 'solution', '--format', 'text'])
        assert cause == 'NOK: could not identify content category - please keep template tags in place'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('edit-unknown-solution-template')
    def test_cli_create_solution_005(snippy):
        """Try to create solution from CLI.

        Try to create new solution with a template that cannot be identified.
        In this case the user has changed the input template completely and
        it has lost tags that identify it as a solution content.
        """

        cause = snippy.run(['snippy', 'create', '--scat', 'solution', '--format', 'text'])
        assert cause == 'NOK: could not identify content category - please keep template tags in place'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('snippy', 'edit-beats')
    def test_cli_create_solution_006(snippy):
        """Create solution from editor.

        Create new solution by defining all values from editor.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID2
        cause = snippy.run(['snippy', 'create', '--scat', 'solution', '--editor', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('snippy', 'create-kafka-mkdn-utc')
    def test_cli_create_solution_007(snippy, editor_data):
        """Create solution from editor.

        Create a new solution by using the prefilled default Markdown template
        in editor. The template presented in editor is manually defined in this
        test case on purpose. This tries to verity that the testing framework
        does not hide problems compared to situation where the template would
        be generated automatically by the testing framework.

        When content is created, the timestamp is allocated once for created
        and updated timestamps. The timestamp must not be updated from what
        is presented in the editor.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.KAFKA_MKDN)
            ]
        }
        template = (
            '# Add brief title for content @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> ',
            '',
            '## Description',
            '',
            '## References',
            '',
            '## Commands',
            '',
            '## Configurations',
            '',
            '## Solutions',
            '',
            '## Whiteboard',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2019-01-04T10:54:49.265512+00:00  ',
            'digest   : 5facdc16dc81851c2f65b112a0921eb2f2db206c7756714efb45ba0026471f11  ',
            'filename : example-content.md  ',
            'name     : example content handle  ',
            'source   : https://www.example.com/source.md  ',
            'tags     : example,tags  ',
            'updated  : 2019-01-04T10:54:49.265512+00:00  ',
            'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : example=3.9.0,python>=3  ',
            ''
        )
        edited = (
            '# Testing docker log drivers @docker',
            '',
            '> Investigate docker log drivers and the logs2kafka log plugin',
            '',
            '>',
            '',
            '## Description',
            '',
            'Investigate docker log drivers.',
            '',
            '## Solutions',
            '',
            '## Whiteboard',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2019-01-04T10:54:49.265512+00:00  ',
            'digest   : 18473ec207798670c302fb711a40df6555e8973e26481e4cd6b2ed205f5e633c  ',
            'filename : kubernetes-docker-log-driver-kafka.mkdn  ',
            'name     :  ',
            'source   :  ',
            'tags     : docker,driver,kafka,kubernetes,logging,logs2kafka,moby,plugin  ',
            'updated  : 2019-01-04T10:54:49.265512+00:00  ',
            'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            '')
        content['data'][0]['data'] = (
            '## Description',
            '',
            'Investigate docker log drivers.',
            '',
            '## Solutions',
            '',
            '## Whiteboard',
            ''
        )
        content['data'][0]['description'] = 'Investigate docker log drivers and the logs2kafka log plugin'
        content['data'][0]['links'] = ()
        content['data'][0]['updated'] = '2019-01-04T10:54:49.265512+00:00'
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][0]['digest'] = '7941851522a23d3651f223b6d69441f77649ccb7ae1e72c6709890f2caf6401a'
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '--scat', 'solution'])
        editor_data.assert_called_with('\n'.join(template))
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('snippy', 'create-kafka-mkdn-utc')
    def test_cli_create_solution_008(snippy, editor_data):
        """Try to create solution from editor.

        Try to create a new solution by using the prefilled default Markdown
        template in editor. In this case there are no any changes made in
        editor on top of the displayed template.
        """

        template = (
            '# Add brief title for content @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> ',
            '',
            '## Description',
            '',
            '## References',
            '',
            '## Commands',
            '',
            '## Configurations',
            '',
            '## Solutions',
            '',
            '## Whiteboard',
            '',
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2019-01-04T10:54:49.265512+00:00  ',
            'digest   : 5facdc16dc81851c2f65b112a0921eb2f2db206c7756714efb45ba0026471f11  ',
            'filename : example-content.md  ',
            'name     : example content handle  ',
            'source   : https://www.example.com/source.md  ',
            'tags     : example,tags  ',
            'updated  : 2019-01-04T10:54:49.265512+00:00  ',
            'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : example=3.9.0,python>=3  ',
            ''
        )
        edited = template
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '--scat', 'solution'])
        editor_data.assert_called_with('\n'.join(template))
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_solution_009(snippy):
        """Try to create solution from CLI.

        Try to create new solution by from command line with --no-editor
        option when the mandatory data is not defined.
        """

        cause = snippy.run(['snippy', 'create', '--scat', 'solution', '--brief', 'Short brief', '--no-editor'])
        assert cause == 'NOK: content was not stored because mandatory content field data is empty'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('snippy', 'create-beats-utc')
    def test_cli_create_solution_010(snippy):
        """Create solution from command line.

        Create new solution by defining all content parameters from command
        line. In this case content field values contain duplicates that must
        not be used when the content is stored. Only unique values must be
        used.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['description'] = ''
        content['data'][0]['filename'] = ''
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][0]['digest'] = 'b8dfd78b2f92caac57469acda50bebf4dca9fd3e85bb9083c8408f430fc83f52'
        data = Const.DELIMITER_DATA.join(content['data'][0]['data'])
        brief = content['data'][0]['brief']
        groups = Const.DELIMITER_GROUPS.join(content['data'][0]['groups']) + ',beats'
        tags = Const.DELIMITER_TAGS.join(content['data'][0]['tags']) + ',howto,filebeat'
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links']) + ' https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html'  # pylint: disable=line-too-long
        cause = snippy.run(['snippy', 'create', '--scat', 'solution', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links, '--format', 'text'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
