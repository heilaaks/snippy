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

"""test_cli_update_snippet: Test workflows for updating snippets."""

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.snippet import Snippet


class TestCliUpdateSnippet(object):
    """Test workflows for updating snippets."""

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_001(self, snippy, edited_remove):
        """Update snippet based on digest.

        Update snippet based on short message digest. Only content data
        is updated.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Snippet.FORCED
            ]
        }
        content['data'][0]['data'] = ('docker images', )
        content['data'][0]['digest'] = 'af8c89629dc1a5313fd15c95fa9c1199b2b99874426e0b2532a952f40dcf980d'
        edited_remove.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_002(self, snippy, edited_remove):
        """Update snippet based on digest.

        Update snippet based on very short message digest. This must match to
        a single snippet that must be updated.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Snippet.FORCED
            ]
        }
        content['data'][0]['data'] = ('docker images', )
        content['data'][0]['digest'] = 'af8c89629dc1a5313fd15c95fa9c1199b2b99874426e0b2532a952f40dcf980d'
        edited_remove.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', '54e41', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_003(self, snippy, edited_remove):
        """Update snippet based on digest.

        Update snippet based on long message digest. Only the content data is
        updated.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Snippet.FORCED
            ]
        }
        content['data'][0]['data'] = ('docker images', )
        content['data'][0]['digest'] = 'af8c89629dc1a5313fd15c95fa9c1199b2b99874426e0b2532a952f40dcf980d'
        edited_remove.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_004(self, snippy, edited_remove):
        """Update snippet based on digest.

        Update snippet based on message digest and explicitly define the
        content category.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Snippet.FORCED
            ]
        }
        content['data'][0]['data'] = ('docker images', )
        content['data'][0]['digest'] = 'af8c89629dc1a5313fd15c95fa9c1199b2b99874426e0b2532a952f40dcf980d'
        edited_remove.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--snippets', '-d', '54e41e9b52a02b63', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_005(self, snippy, edited_remove):
        """Update snippet based on digest.

        Update snippet based on message digest and accidentally define
        solution category. In this case the snippet is updated properly
        regardless of incorrect category.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Snippet.FORCED
            ]
        }
        content['data'][0]['data'] = ('docker images', )
        content['data'][0]['digest'] = 'af8c89629dc1a5313fd15c95fa9c1199b2b99874426e0b2532a952f40dcf980d'
        edited_remove.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--solution', '-d', '54e41e9b52a02b63', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_006(self, snippy):
        """Update snippet based on digest.

        Try to update snippet with message digest that cannot be found. No
        changes must be made to stored content.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'update', '-d', '123456789abcdef0', '--format', 'text'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_007(self, snippy):
        """Update snippet based on digest.

        Try to update snippet with empty message digest. Nothing should be
        updated in this case because the empty digest matches to more than
        one snippet. Only one content can be updated at the time.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'update', '-d', '', '--format', 'text'])
        assert cause == 'NOK: cannot use empty message digest for update operation'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_008(self, snippy):
        """Update snippet based on digest.

        Try to update snippet with one digit digest that matches two snippets.

        NOTE! Don't not change the test snippets because this case is produced
        with real digests that just happen to have same digit starting both of
        the cases.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'update', '-d', '5', '--format', 'text'])
        assert cause == 'NOK: content digest 5 matched 2 times preventing update operation'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_009(self, snippy, edited_remove):
        """Update snippet based on content data.

        Update snippet based on content data.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
                Snippet.FORCED
            ]
        }
        content['data'][0]['data'] = ('docker images', )
        content['data'][0]['digest'] = 'af8c89629dc1a5313fd15c95fa9c1199b2b99874426e0b2532a952f40dcf980d'
        edited_remove.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-c', 'docker rm --volumes $(docker ps --all --quiet)', '--format', 'text', '--editor'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_010(self, snippy):
        """Update snippet based on content data.

        Try to update snippet based on content data that is not found.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'update', '-c', 'snippet not existing'])
        assert cause == 'NOK: cannot find content with content data: snippet not existing'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_011(self, snippy):
        """Update snippet based on content data.

        Try to update snippet with empty content data. Nothing must be updated
        in this case because there is more than one content stored.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'update', '-c', ''])
        assert cause == 'NOK: cannot use empty content data for update operation'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_012(self, snippy):
        """Update snippet based on content data.

        Try to update snippet with content data that matches to two different
        snippets. Nothing must be updated in this case because content can be
        updated only if it is uniquely identified.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        cause = snippy.run(['snippy', 'update', '-c', 'docker'])
        assert cause == 'NOK: content data docker matched 2 times preventing update operation'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-remove', 'update-forced-utc')
    def test_cli_update_snippet_013(self, snippy, editor_data):
        """Update existing snippet from editor.

        Update existing snippet from editor so that content fields are given
        from command line. Editor must show the content template with field
        values received from command line parameters.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['brief'] = 'brief cli'
        content['data'][0]['tags'] = ('cli-tag',)
        content['data'][0]['links'] = ('https://cli-link',)
        content['data'][0]['groups'] = ('cli-group',)
        content['data'][0]['digest'] = '613e163028a17645a7dfabbe159f05d14db7588259229dd8d08e949cdc668373'
        template = (
            '# brief cli @cli-group',
            '',
            '> ',
            '',
            '> [1] https://cli-link',
            '',
            '`$ docker rm --volumes $(docker ps --all --quiet)`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : 613e163028a17645a7dfabbe159f05d14db7588259229dd8d08e949cdc668373  ',
            'filename :  ',
            'name     :  ',
            'source   :  ',
            'tags     : cli-tag  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 12cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            ''
        )
        editor_data.return_value = '\n'.join(template)
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63', '-t', 'cli-tag', '-b', 'brief cli', '-g', 'cli-group', '-l', 'https://cli-link'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-remove', 'update-forced-utc')
    def test_cli_update_snippet_014(self, snippy, editor_data):
        """Update existing snippet from command line.

        Update existing snippet from directly from command line. In this case
        editor is not used because of '--no-editor' option which updates the
        content without editor.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['brief'] = 'brief cli'
        content['data'][0]['tags'] = ('cli-tag',)
        content['data'][0]['links'] = ('https://cli-link',)
        content['data'][0]['groups'] = ('cli-group',)
        content['data'][0]['digest'] = '613e163028a17645a7dfabbe159f05d14db7588259229dd8d08e949cdc668373'
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63', '-t', 'cli-tag', '-b', 'brief cli', '-g', 'cli-group', '-l', 'https://cli-link', '--no-editor'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        editor_data.assert_not_called()
        Content.assert_storage(content)

    @pytest.mark.usefixtures('import-remove', 'update-remove-utc')
    def test_cli_update_snippet_015(self, snippy, editor_data):
        """Update existing snippet from editor.

        Update existing snippet by explicitly defining content format as
        Markdown. In this case the content is not changed at all.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        template = (
            '# Remove all docker containers with volumes @docker',
            '',
            '> ',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '`$ docker rm --volumes $(docker ps --all --quiet)`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename :  ',
            'name     :  ',
            'source   :  ',
            'tags     : cleanup,container,docker,docker-ce,moby  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 12cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            ''
        )
        editor_data.return_value = '\n'.join(template)
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63', '--format', 'mkdn'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
