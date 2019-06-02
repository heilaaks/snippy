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

"""test_cli_update_solution: Test workflows for updating solutions."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.solution import Solution


class TestCliUpdateSolution(object):
    """Test workflows for updating solutions."""

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_001(snippy, edited_beats):
        """Update solution with ``--digest`` option.

        Update solution with short message digest. Only the content data is
        updated. Because the description tag was changed, the ``description``
        attribute is not read and it results an empty string.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## Description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '23312e20cb961d46b3fb0ac5a63dacfbb16f13a220b48250019977940e9720f3'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '-d', '4346ba4c79247430', '--format', 'text'])
        print(Content.output())
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_002(snippy, edited_beats):
        """Update solution with ``--digest`` option.

        Update solution with very short message digest. This must match to a
        single solution that must be updated.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## Description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '23312e20cb961d46b3fb0ac5a63dacfbb16f13a220b48250019977940e9720f3'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '--digest', '4346b', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_003(snippy, edited_beats):
        """Update solution with ``--digest`` option.

        Update solution based on long message digest. Only the content data
        is updated.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## Description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '23312e20cb961d46b3fb0ac5a63dacfbb16f13a220b48250019977940e9720f3'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '-d', '4346ba4c792474308bc66bd16d747875bef9b431044824987e302b726c1d298e', '--format', 'text'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_004(snippy, edited_beats):
        """Update solution with ``--digest`` option.

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
        content['data'][0]['data'] = tuple([line.replace('## Description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '23312e20cb961d46b3fb0ac5a63dacfbb16f13a220b48250019977940e9720f3'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'snippet', '-d', '4346ba4c79247430', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_005(snippy, edited_beats):
        """Update solution with ``--digest`` option.

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
        content['data'][0]['data'] = tuple([line.replace('## Description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '23312e20cb961d46b3fb0ac5a63dacfbb16f13a220b48250019977940e9720f3'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', '4346ba4c79247430', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_006(snippy):
        """Update solution with ``--digest`` option.

        Try to update solution with message digest that cannot be found. No
        changes must be made to stored content.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_007(snippy):
        """Update solution with ``--digest`` option.

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
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '-d', ''])
        assert cause == 'NOK: cannot use empty message digest for update operation'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_008(snippy, edited_beats):
        """Update solution with ``--content`` option.

        Update solution based on content data.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS),
                Solution.NGINX
            ]
        }
        content['data'][0]['data'] = tuple([line.replace('## Description', '## updated desc') for line in content['data'][0]['data']])
        content['data'][0]['description'] = ''
        content['data'][0]['digest'] = '23312e20cb961d46b3fb0ac5a63dacfbb16f13a220b48250019977940e9720f3'
        edited_beats.return_value = Content.dump_text(content['data'][0])
        data = Const.NEWLINE.join(Solution.BEATS['data'])
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '-c', data, '--format', 'text', '--editor'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_009(snippy):
        """Update solution with ``--content`` option.

        Try to update solution based on content data that is not found.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '--content', 'solution not existing'])
        assert cause == 'NOK: cannot find content with content data: solution not existing'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-solutions')
    def test_cli_update_solution_010(snippy):
        """Update solution with ``--content`` option.

        Try to update solution with empty content data. Nothing must be
        updated in this case because there is more than one content stored.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '-c', ''])
        assert cause == 'NOK: cannot use empty content data for update operation'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-nginx', 'update-beats-utc')
    def test_cli_update_solution_011(snippy, edited_beats):
        """Update solution with editor.

        Update existing solution by defining all values from editor. In this
        case the solution is existing and previously stored data must be set
        into editor on top of the default template. In this case the ngingx
        solution is edited to beats solution. The case verifies that editor
        shows the ngingx solution and not an empty solution template.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.BEATS)
            ]
        }
        content['data'][0]['uuid'] = Solution.NGINX_UUID
        edited_beats.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', '6cfe47a8880a8f81', '--scat', 'solution', '--editor', '--format', 'text'])
        edited_beats.assert_called_with(Content.dump_text(Solution.NGINX))
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-kafka-mkdn', 'update-beats-utc')
    def test_cli_update_solution_012(snippy, editor_data):
        """Update solution with editor.

        Update existing Markdown native solution. Editor must show existing
        Markdown native content as is. Updated content must be identified as
        Markdown native content. Editor must be used by default when the
        ``--editor`` option is not used.

        In this case the links must be empty when stored. The edited content
        did not have any links in the content data so they must be updated
        to stored content.
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
            'digest   : c54c8a896b94ea35edf6c798879957419d26268bd835328d74b19a6e9ce2324d  ',
            'filename : kubernetes-docker-log-driver-kafka.mkdn  ',
            'name     :  ',
            'source   :  ',
            'tags     : docker,driver,kafka,kubernetes,logging,logs2kafka,moby,plugin  ',
            'updated  : 2019-01-05T10:54:49.265512+00:00  ',
            'uuid     : 24cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
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
        updates['data'][0]['links'] = ()
        updates['data'][0]['updated'] = Content.BEATS_TIME
        updates['data'][0]['uuid'] = Solution.KAFKA_MKDN_UUID
        updates['data'][0]['digest'] = '7941851522a23d3651f223b6d69441f77649ccb7ae1e72c6709890f2caf6401a'
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'update', '-d', 'c54c8a896b94ea35', '--scat', 'solution'])
        editor_data.assert_called_with(Content.dump_mkdn(Solution.KAFKA_MKDN))
        assert cause == Cause.ALL_OK
        Content.assert_storage(updates)

    @staticmethod
    @pytest.mark.usefixtures('import-kafka', 'update-kafka-utc')
    def test_cli_update_solution_013(snippy, editor_data):
        """Update solution with editor.

        Update existing solution by explicitly defining content format as
        Markdown. In this case the content is not changed at all. In this
        case the solution is stored originally in text format. The content
        must be convertd to Markdown format when displayed in editor.
        """

        content = {
            'data': [
                Solution.KAFKA
            ]
        }
        template = Content.dump_mkdn(content['data'][0])
        editor_data.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', 'ee3f2ab7c63d6965', '--format', 'mkdn'])
        editor_data.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-kafka-mkdn', 'update-kafka-mkdn-utc')
    def test_cli_update_solution_014(snippy, editor_data):
        """Update solution with editor.

        Update existing solution by explicitly defining content format as
        Markdown. In this case the content is not changed at all. In this
        case the solution is stored originally in Markdown format.

        The template in this test is defined in the test in order to test
        against manually defined content. In most of the test, the refences
        are generated by the Content wrappers.
        """

        content = {
            'data': [
                Solution.KAFKA_MKDN
            ]
        }
        # pylint: disable=C0330
        template = (  # Python 2 does not support tuple unpack with star.
            '# Testing docker log drivers @docker',
            '',
            '> Investigate docker log drivers and the logs2kafka log plugin.',
            '',
            '> [1] https://github.com/MickayG/moby-kafka-logdriver  ',
            '[2] https://github.com/garo/logs2kafka  ',
            '[3] https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ',
            '') + Solution.KAFKA_MKDN['data'] + (
            '## Meta',
            '',
            '> category : solution  ',
            'created  : 2019-01-04T10:54:49.265512+00:00  ',
            'digest   : c54c8a896b94ea35edf6c798879957419d26268bd835328d74b19a6e9ce2324d  ',
            'filename : kubernetes-docker-log-driver-kafka.mkdn  ',
            'name     :  ',
            'source   :  ',
            'tags     : docker,driver,kafka,kubernetes,logging,logs2kafka,moby,plugin  ',
            'updated  : 2019-01-05T10:54:49.265512+00:00  ',
            'uuid     : 24cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            '')
        # pylint: enable=C0330
        editor_data.return_value = '\n'.join(template)
        cause = snippy.run(['snippy', 'update', '-d', 'c54c8a896b94ea35', '--format', 'mkdn'])
        editor_data.assert_called_with('\n'.join(template))
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-kafka', 'update-three-kafka-utc')
    def test_cli_update_solution_015(snippy, editor_data):
        """Update text native solution with editor.

        Update existing text formatted solution first in text format, then
        in Markdown format and then again in text format without making any
        changes. The content must not change when updated between different
        formats.

        Each update must generate different timestamp in content ``updated``
        attribute.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.KAFKA)
            ]
        }
        content['data'][0]['brief'] = 'Testing docker log drivers again'
        content['data'][0]['digest'] = '1072f9a0ddb2ab15a7f6cca0acd9f7e48903faa576fb19eca4e0ec98dc20c041'
        template = Content.dump_text(content['data'][0])
        editor_data.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', 'ee3f2ab7c63d6965', '--format', 'text', '--brief', 'Testing docker log drivers again'])
        editor_data.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

        content['data'][0]['brief'] = 'Testing docker log drivers again in mkdn'
        content['data'][0]['digest'] = '2887f455e73ad3a6040df7299e69548748db5eb208b9c7eb4717aa2527af4778'
        template = Content.dump_mkdn(content['data'][0])
        editor_data.return_value = template
        content['data'][0]['updated'] = '2017-11-20T06:16:27.000001+00:00'
        cause = snippy.run(['snippy', 'update', '-d', '1072f9a0ddb2ab15', '--format', 'mkdn', '--brief', 'Testing docker log drivers again in mkdn'])  # pylint: disable=line-too-long
        editor_data.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

        content['data'][0]['brief'] = 'Testing docker log drivers again'
        content['data'][0]['digest'] = '1072f9a0ddb2ab15a7f6cca0acd9f7e48903faa576fb19eca4e0ec98dc20c041'
        template = Content.dump_text(content['data'][0])
        editor_data.return_value = template
        content['data'][0]['updated'] = '2017-12-20T06:16:27.000001+00:00'
        cause = snippy.run(['snippy', 'update', '-d', '2887f455e73ad3a6', '--format', 'text', '--brief', 'Testing docker log drivers again'])
        editor_data.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-kafka-mkdn', 'update-three-kafka-utc')
    def test_cli_update_solution_016(snippy, editor_data):
        """Update Markdown native solution with editor.

        Update existing text formatted solution first in text format, then
        in Markdown format and then again in text format without making any
        changes. The content must not change when updated between different
        formats.

        Each update must generate different timestamp in content ``updated``
        attribute.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.KAFKA_MKDN)
            ]
        }
        content['data'][0]['brief'] = 'Testing docker log drivers again'
        content['data'][0]['digest'] = 'b5e5242d971f561675558981b4f25d1e822db282145c4246e3bd50111146096c'
        template = Content.dump_text(content['data'][0])
        editor_data.return_value = template
        content['data'][0]['updated'] = '2017-10-20T06:16:27.000001+00:00'
        cause = snippy.run(['snippy', 'update', '-d', 'c54c8a896b94ea35e', '--format', 'text', '--brief', 'Testing docker log drivers again'])
        editor_data.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

        content['data'][0]['brief'] = 'Testing docker log drivers again in mkdn'
        content['data'][0]['digest'] = '243e51c8b99c80fb73c30b8d72618f8c3bc094df04184da8209f147138067083'
        template = Content.dump_mkdn(content['data'][0])
        editor_data.return_value = template
        content['data'][0]['updated'] = '2017-11-20T06:16:27.000001+00:00'
        cause = snippy.run(['snippy', 'update', '-d', 'b5e5242d971f5616', '--format', 'mkdn', '--brief', 'Testing docker log drivers again in mkdn'])  # pylint: disable=line-too-long
        editor_data.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

        content['data'][0]['brief'] = 'Testing docker log drivers again'
        content['data'][0]['digest'] = 'b5e5242d971f561675558981b4f25d1e822db282145c4246e3bd50111146096c'
        template = Content.dump_text(content['data'][0])
        editor_data.return_value = template
        content['data'][0]['updated'] = '2017-12-20T06:16:27.000001+00:00'
        cause = snippy.run(['snippy', 'update', '-d', '243e51c8b99c80fb', '--format', 'text', '--brief', 'Testing docker log drivers again'])
        editor_data.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
