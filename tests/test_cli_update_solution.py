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

"""test_cli_update_solution: Test workflows for updating solutions."""

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.solution import Solution


class TestCliUpdateSolution(object):
    """Test workflows for updating solutions."""

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_001(self, snippy, edited_beats):
        """Update solution with digest.

        Update solution based on short message digest. Only content data
        is updated. Because the description tag was changed, the description
        itself is not read and it results an empty string.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '19baa35ea3751e7fb66a810fb20b766601dc7c61512a36a8378be7c6b0063acc'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--solution', '-d', 'db712a82662d6932'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_002(self, snippy, edited_beats):
        """Update solution with digest.

        Update solution based on very short message digest. This must match
        to a single solution that must be updated.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '19baa35ea3751e7fb66a810fb20b766601dc7c61512a36a8378be7c6b0063acc'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--solution', '--digest', 'db712'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_003(self, snippy, edited_beats):
        """Update solution with digest.

        Update solution based on long message digest. Only the content data
        is updated.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '19baa35ea3751e7fb66a810fb20b766601dc7c61512a36a8378be7c6b0063acc'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--solution', '-d', 'db712a82662d693206004c2174a0bb1900e1e1307f21f79a0efb88a01add4151']) # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_004(self, snippy, edited_beats):
        """Update solution with digest.

        Update solution based on message digest and accidentally define
        snippet category explicitly from command line. In this case the
        solution is updated properly regardless of incorrect category.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '19baa35ea3751e7fb66a810fb20b766601dc7c61512a36a8378be7c6b0063acc'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--snippet', '-d', 'db712a82662d6932'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_005(self, snippy, edited_beats):
        """Update solution with digest.

        Update solution based on message digest and accidentally implicitly
        use snippet category by not using content category option that
        defaults to snippet category. In this case the solution is updated
        properly regardless of incorrect category.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '19baa35ea3751e7fb66a810fb20b766601dc7c61512a36a8378be7c6b0063acc'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', 'db712a82662d6932'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_006(self, snippy):
        """Update solution with digest.

        Try to update solution with message digest that cannot be found. No
        changes must be made to stored content.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'update', '--solution', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_007(self, snippy):
        """Update solution with digest.

        Try to update solution with empty message digest. Nothing should be
        updated in this case because the empty digest matches to more than
        one solution. Only one content can be updated at the time.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'update', '--solution', '-d', ''])
        assert cause == 'NOK: cannot use empty message digest for: update :operation'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_008(self, snippy, edited_beats):
        """Update solution with data.

        Update solution based on content data.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '19baa35ea3751e7fb66a810fb20b766601dc7c61512a36a8378be7c6b0063acc'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        data = Content.dump_text(Solution.BEATS)
        cause = snippy.run(['snippy', 'update', '--solution', '-c', data])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_009(self, snippy):
        """Update solution with data.

        Try to update solution based on content data that is not found.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'update', '--solution', '--content', 'solution not existing'])
        assert cause == 'NOK: cannot find content with content data: solution not existing'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_010(self, snippy):
        """Update solution with data.

        Try to update solution with empty content data. Nothing must be
        updated in this case because there is more than one content stored.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'update', '--solution', '-c', ''])
        assert cause == 'NOK: cannot use empty content data for: update :operation'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-nginx', 'update-beats-utc')
    def test_cli_update_solution_011(self, snippy, edited_beats):
        """Update existing solution from editor.

        Update existing solution by defining all values from editor. In this
        case the solution is existing and previously stored data must be set
        into editor on top of the default template. In this case the ngingx
        solution is edited to beats solution. The case verifies that editor
        shows the ngingx solution and not an empty solution template.
        """

        content = {
            'data': [
                Solution.BEATS
            ]
        }
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', '5dee85bedb7f4d3a', '--solution', '--editor'])
        edited_beats.assert_called_with(Content.dump_text(Solution.NGINX))
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-kafka-mkdn', 'update-beats-utc')
    def test_cli_update_solution_012(self, snippy, editor_data):
        """Update existing solution from editor.

        Update existing Markdown native solution. Editor must show existing
        Markdown native content as is. Updated content must be identified as
        Markdown native content. Editor must be used by default when
        the --editor option is not used.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.KAFKA_MKDN)
            ]
        }
        edited = (
            '# Testing docker log drivers @docker',
            '',
            '> Investigate docker log drivers and the logs2kafka log plugin',
            '',
            '> [1] https://github.com/MickayG/moby-kafka-logdriver  ',
            '[2] https://github.com/garo/logs2kafka  ',
            '[3] https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
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
            'name     :   ',
            'source   :   ',
            'tags     : docker,driver,kafka,kubernetes,logging,logs2kafka,moby,plugin  ',
            'updated  : 2019-01-05T10:54:49.265512+00:00  ',
            'uuid     : 24cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            '')
        updates = content
        updates['data'][0]['data'] = (
            '## Description',
            '',
            'Investigate docker log drivers.',
            '',
            '## Solutions',
            '',
            '## Whiteboard',
            ''
        )
        updates['data'][0]['description'] = 'Investigate docker log drivers and the logs2kafka log plugin'
        updates['data'][0]['updated'] = Content.BEATS_TIME
        updates['data'][0]['uuid'] = '11cd5827-b6ef-4067-b5ac-3ceac07dde9f'
        updates['data'][0]['digest'] = '9286207e33cd8cc78446b4e6d070a76fadda8fb304afb6e5f4fad0cf66e491bc'
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'update', '-d', '18473ec207798670', '--solution'])
        editor_data.assert_called_with(Content.dump_mkdn(Solution.KAFKA_MKDN))
        assert cause == Cause.ALL_OK
        Content.assert_storage(updates)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
