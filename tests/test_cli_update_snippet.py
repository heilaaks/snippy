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

"""test_cli_update_snippet: Test workflows for updating snippets."""

import pytest

from snippy.cause import Cause
from tests.lib.content import Content
from tests.lib.snippet import Snippet


class TestCliUpdateSnippet(object):
    """Test workflows for updating snippets."""

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_001(snippy, edited_remove):
        """Update snippet with ``--digest`` option.

        Update snippet based on short message digest. Only the content data
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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_002(snippy, edited_remove):
        """Update snippet with ``--digest`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_003(snippy, edited_remove):
        """Update snippet with ``--digest`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_004(snippy, edited_remove):
        """Update snippet with ``--digest`` option.

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
        cause = snippy.run(['snippy', 'update', '--scat', 'snippet', '-d', '54e41e9b52a02b63', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_005(snippy, edited_remove):
        """Update snippet with ``--digest`` option.

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
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '-d', '54e41e9b52a02b63', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_006(snippy):
        """Update snippet with ``--digest`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_007(snippy):
        """Update snippet with ``--digest`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_008(snippy):
        """Update snippet with ``--digest`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_009(snippy, edited_remove):
        """Update snippet with ``--content`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_010(snippy):
        """Update snippet with ``--content`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_011(snippy):
        """Update snippet with ``--content`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_update_snippet_012(snippy):
        """Update snippet with ``--content`` option.

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

    @staticmethod
    @pytest.mark.usefixtures('import-remove', 'update-forced-utc')
    def test_cli_update_snippet_013(snippy, editor_data):
        """Update snippet with editor.

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
        content['data'][0]['groups'] = ('cli-group',)
        content['data'][0]['tags'] = ('cli-tag',)
        content['data'][0]['links'] = ('https://cli-link',)
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
            '> category  : snippet  ',
            'created   : 2017-10-14T19:56:31.000001+00:00  ',
            'digest    : 613e163028a17645a7dfabbe159f05d14db7588259229dd8d08e949cdc668373  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cli-tag  ',
            'updated   : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid      : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  :  ',
            ''
        )
        editor_data.return_value = '\n'.join(template)
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63', '-t', 'cli-tag', '-b', 'brief cli', '-g', 'cli-group', '-l', 'https://cli-link'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-remove', 'update-forced-utc')
    def test_cli_update_snippet_014(snippy, editor_data):
        """Update snippet from command line.

        Update existing snippet directly from command line. In this case,
        editor is not used because of '--no-editor' option which updates
        given content directly without user interaction.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['brief'] = 'brief cli'
        content['data'][0]['groups'] = ('cli-group',)
        content['data'][0]['tags'] = ('cli-tag',)
        content['data'][0]['links'] = ('https://cli-link',)
        content['data'][0]['digest'] = '613e163028a17645a7dfabbe159f05d14db7588259229dd8d08e949cdc668373'
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63', '-t', 'cli-tag', '-b', 'brief cli', '-g', 'cli-group', '-l', 'https://cli-link', '--no-editor'])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        editor_data.assert_not_called()
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-remove', 'update-remove-utc')
    def test_cli_update_snippet_015(snippy, editor_data):
        """Update snippet with editor.

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
            '> category  : snippet  ',
            'created   : 2017-10-14T19:56:31.000001+00:00  ',
            'digest    : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup,container,docker,docker-ce,moby  ',
            'updated   : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid      : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  :  ',
            ''
        )
        editor_data.return_value = '\n'.join(template)
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63', '--format', 'mkdn'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-remove', 'update-remove-utc')
    def test_cli_update_snippet_016(snippy, editor_data):
        """Update snippet from command line.

        Update existing snippet directly from command line. In this case the
        given field values are duplicated and thus they must not affect to
        existing content.
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
            '> category  : snippet  ',
            'created   : 2017-10-14T19:56:31.000001+00:00  ',
            'digest    : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : cleanup,container,docker,docker-ce,moby  ',
            'updated   : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid      : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  :  ',
            ''
        )
        editor_data.return_value = '\n'.join(template)
        cause = snippy.run(['snippy', 'update', '-d', '54e41e9b52a02b63', '-t', 'moby,container,docker,docker-ce,cleanup'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures()
    def test_cli_update_snippet_017(snippy, editor_data):
        """Update snippet with editor.

        Update existing snippet directly from command line. In this case the
        snippet contains multiple comments which are same. The update is made
        in Markdown format and editor must be able to show the content. There
        are no changes and the parser must notice that the content was not
        updated.
        """

        Content.store({
            'category': Content.SNIPPET,
            'data': [
                "find . -iregex '.*\\(py\\|robot\\)'  #  Find files.",
                "find . -iregex '.*\\(py\\|robot\\)' -print0 | wc -l --files0-from=-  #  Find files and count lines.",
                "find . -iregex '.*\\(py\\|robot\\)' -print0 | wc -l --files0-from=- | tail -n 1",
                "find . -name '*.py' -print0 | wc -l --files0-from=-  #  Find files and count lines.",
                "find . -name '*.py' -print0 | wc -l --files0-from=- | tail -n 1",
                "find . -name '*.py' -exec cat {} + | wc -l  #  Find files and count lines."],
            'brief': 'Find files and count lines',
            'description': 'Find files with or without regexp pattern and count lines.',
            'groups': ['linux'],
            'tags': ['find', 'linux', 'regexp'],
            'digest': 'dae4e22c3c3858b5616a29be11916112a16994e30bc3e4b93b069bc9a772d889'
        })
        content = {
            'data': [{
                'category': 'snippet',
                'data': ("find . -iregex '.*\\(py\\|robot\\)'  #  Find files.",
                         "find . -iregex '.*\\(py\\|robot\\)' -print0 | wc -l --files0-from=-  #  Find files and count lines.",
                         "find . -iregex '.*\\(py\\|robot\\)' -print0 | wc -l --files0-from=- | tail -n 1",
                         "find . -name '*.py' -print0 | wc -l --files0-from=-  #  Find files and count lines.",
                         "find . -name '*.py' -print0 | wc -l --files0-from=- | tail -n 1",
                         "find . -name '*.py' -exec cat {} + | wc -l  #  Find files and count lines."),
                'brief': 'Find files and count lines',
                'description': 'Find files with or without regexp pattern and count lines.',
                'name': '',
                'groups': ('linux', ),
                'tags': ('find', 'linux', 'regexp'),
                'links': (),
                'source': '',
                'versions': (),
                'languages': (),
                'filename': '',
                'created': '2018-03-02T02:02:02.000001+00:00',
                'updated': '2018-03-02T02:02:02.000001+00:00',
                'uuid': 'a1cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'digest': 'dae4e22c3c3858b5616a29be11916112a16994e30bc3e4b93b069bc9a772d889'
            }]
        }
        template = (
            '# Find files and count lines @linux',
            '',
            '> Find files with or without regexp pattern and count lines.',
            '',
            '> ',
            '',
            '- Find files.',
            '',
            '    `$ find . -iregex \'.*\\(py\\|robot\\)\'`',
            '',
            '- Find files and count lines.',
            '',
            '    `$ find . -iregex \'.*\\(py\\|robot\\)\' -print0 | wc -l --files0-from=-`',
            '',
            '- <not documented>',
            '',
            '    `$ find . -iregex \'.*\\(py\\|robot\\)\' -print0 | wc -l --files0-from=- | tail -n 1`  ',
            '',
            '- Find files and count lines.',
            '',
            '    `$ find . -name \'*.py\' -print0 | wc -l --files0-from=-`',
            '',
            '- <not documented>',
            '',
            '    `$ find . -name \'*.py\' -print0 | wc -l --files0-from=- | tail -n 1`  ',
            '',
            '- Find files and count lines.',
            '',
            '    `$ find . -name \'*.py\' -exec cat {} + | wc -l`',
            '',
            '## Meta',
            '',
            '> category  : snippet  ',
            'created   : 2018-03-02T02:02:02.000001+00:00  ',
            'digest    : dae4e22c3c3858b5616a29be11916112a16994e30bc3e4b93b069bc9a772d889  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : find,linux,regexp  ',
            'updated   : 2018-03-02T02:02:02.000001+00:00  ',
            'uuid      : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  :  ',
            ''
        )
        editor_data.return_value = '\n'.join(template)
        cause = snippy.run(['snippy', 'update', '-d', 'dae4e22c3c3858b5'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-remove', 'update-three-forced-utc')
    def test_cli_update_snippet_018(snippy, edited_remove):
        """Update snippet with editor.

        Update existing text formatted snippet first in text format, then
        in Markdown format and then again in text format without making any
        changes. The content must not change when updated between different
        formats.

        Each update must generate different timestamp in content ``updated``
        attribute. In this case the updates are given from editor and the
        last update must produce the same content as the first update.

        The content in editor is explicitly defined in the test to avoid
        false positives from the test helpers that actually use the code
        itself.
        """

        edited_text = (
            '# Commented lines will be ignored.',
            '#',
            '# Add mandatory snippet below.',
            'docker rm --volumes $(docker ps --all --quiet)',
            '',
            '# Add optional brief description below.',
            'Remove all docker containers',
            '',
            '# Add optional description below.',
            '',
            '',
            '# Add optional name below.',
            '',
            '',
            '# Add optional comma separated list of groups below.',
            'docker',
            '',
            '# Add optional comma separated list of tags below.',
            'cleanup,container,docker,docker-ce,moby',
            '',
            '# Add optional links below one link per line.',
            'https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '# Add optional source reference below.',
            '',
            '',
            '# Add optional comma separated list of key-value versions below.',
            '',
            '',
            '# Add optional filename below.',
            ''
        )
        edited_mkdn = (
            '# Remove all docker containers again @docker',
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
            'uuid     : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            ''
        )

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE),
            ]
        }
        content['data'][0]['brief'] = 'Remove all docker containers'
        content['data'][0]['digest'] = 'ef734194f551eaa165767fc6aa081ca0c66894fd51eef5cfbc5a26ab3e808d06'
        edited_remove.return_value = '\n'.join(edited_text)
        cause = snippy.run(['snippy', 'update', '--digest', '54e41e9b52a0', '--format', 'text', '--editor'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

        content['data'][0]['brief'] = 'Remove all docker containers again'
        content['data'][0]['digest'] = 'ff16d0f4fdbe1f863e6b81189672d33d29fb436235f3a2243449aca651e8eb49'
        edited_remove.return_value = '\n'.join(edited_mkdn)
        content['data'][0]['updated'] = '2017-11-14T19:56:31.000001+00:00'
        cause = snippy.run(['snippy', 'update', '--digest', 'ef734194f551', '--format', 'mkdn', '--editor'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

        content['data'][0]['brief'] = 'Remove all docker containers'
        content['data'][0]['digest'] = 'ef734194f551eaa165767fc6aa081ca0c66894fd51eef5cfbc5a26ab3e808d06'
        edited_remove.return_value = '\n'.join(edited_text)
        content['data'][0]['updated'] = '2017-12-14T19:56:31.000001+00:00'
        cause = snippy.run(['snippy', 'update', '--digest', 'ff16d0f4fdbe', '--format', 'text', '--editor'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
