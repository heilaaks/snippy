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

"""test_cli_update_reference: Test workflows for updating references."""

import pytest

from snippy.cause import Cause
from tests.lib.content import Content
from tests.lib.reference import Reference


class TestCliUpdateReference(object):
    """Test workflows for updating references."""

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_001(snippy, edited_gitlog):
        """Update reference with ``digest`` option.

        Update reference based on short message digest. Only content links
        are updated. The update is made with editor.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Reference.REGEXP
            ]
        }
        content['data'][0]['links'] = ('https://docs.docker.com', )
        content['data'][0]['digest'] = '1fc34e79a4d2bac51a039b7265da464ad787da41574c3d6651dc6a128d4c7c10'
        edited_gitlog.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '-d', '5c2071094dbfaa33', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_002(snippy, edited_gitlog):
        """Update reference with ``digest`` option.

        Update reference based on very short message digest. This must match
        to a single reference that must be updated.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Reference.REGEXP
            ]
        }
        content['data'][0]['links'] = ('https://docs.docker.com', )
        content['data'][0]['digest'] = '1fc34e79a4d2bac51a039b7265da464ad787da41574c3d6651dc6a128d4c7c10'
        edited_gitlog.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '--digest', '5c2071', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_003(snippy, edited_gitlog):
        """Update reference with ``digest`` option.

        Update reference based on message digest and accidentally define
        solution category explicitly from command line. In this case the
        reference is updated properly regardless of incorrect category.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Reference.REGEXP
            ]
        }
        content['data'][0]['links'] = ('https://docs.docker.com', )
        content['data'][0]['digest'] = '1fc34e79a4d2bac51a039b7265da464ad787da41574c3d6651dc6a128d4c7c10'
        edited_gitlog.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'solution', '-d', '5c2071094dbfaa33', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_004(snippy, edited_gitlog):
        """Update reference with ``digest`` option.

        Update reference based on message digest and accidentally implicitly
        use snippet category by not using content category option that
        defaults to snippet category. In this case the reference is updated
        properly regardless of incorrect category.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Reference.REGEXP
            ]
        }
        content['data'][0]['links'] = ('https://docs.docker.com', )
        content['data'][0]['digest'] = '1fc34e79a4d2bac51a039b7265da464ad787da41574c3d6651dc6a128d4c7c10'
        edited_gitlog.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', '5c2071094dbfaa33', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_005(snippy):
        """Update reference with ``digest`` option.

        Try to update reference with message digest that cannot be found. No
        changes must be made to stored content.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_006(snippy):
        """Update reference with ``digest`` option.

        Try to update reference with empty message digest. Nothing should be
        updated in this case because the empty digest matches to more than
        one reference. Only one content can be updated at the time.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '-d', ''])
        assert cause == 'NOK: cannot use empty message digest for update operation'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_007(snippy, edited_gitlog):
        """Update reference with ``uuid`` option.

        Update reference based on uuid. The content must be updated so that
        only links get updated.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Reference.REGEXP
            ]
        }
        content['data'][0]['links'] = ('https://docs.docker.com', )
        content['data'][0]['digest'] = '1fc34e79a4d2bac51a039b7265da464ad787da41574c3d6651dc6a128d4c7c10'
        edited_gitlog.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '-u', '31cd5827-b6ef-4067-b5ac-3ceac07dde9f', '--format', 'text'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_008(snippy):
        """Update reference with ``uuid`` option.

        Try to update reference based on uuid that cannot be found.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '-u', '9999994'])
        assert cause == 'NOK: cannot find content with content uuid: 9999994'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.skip(reason='not supported yet')
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_009(snippy, edited_gitlog):
        """Update reference with ``content`` option.

        Update reference based on content links.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG),
                Reference.REGEXP
            ]
        }
        content['data'][0]['links'] = ('https://docs.docker.com', )
        content['data'][0]['digest'] = '1fc34e79a4d2bac51a039b7265da464ad787da41574c3d6651dc6a128d4c7c10'
        edited_gitlog.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '-l', 'https://chris.beams.io/posts/git-commit/'])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.skip(reason='not supported yet')
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_010(snippy):
        """Update reference with ``content`` option.

        Try to update reference based on content links that is not found.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '--links', 'links-not-exist'])
        assert cause == 'NOK: cannot find content with content data: reference not existing'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_011(snippy, edited_gitlog):
        """Update reference with ``content`` option.

        Try to update reference with empty content links. Nothing must be
        updated in this case because links are mandatory item in reference
        content.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        updates = Content.deepcopy(Reference.GITLOG)
        updates['links'] = ()
        edited_gitlog.return_value = Content.dump_text(updates)
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '-d', '5c2071094dbfaa33'])
        assert cause == 'NOK: content was not stored because mandatory content field links is empty'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-regexp', 'update-gitlog-utc')
    def test_cli_update_reference_012(snippy, edited_gitlog):
        """Update reference with editor.

        Update existing reference by defining all values from editor. In this
        case the reference is existing and previously stored data must be set
        into editor on top of the default template. In this case the regexp
        reference is edited to gitlog reference. The case verifies that editor
        shows the regexp reference and not an empty reference template.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['uuid'] = Reference.REGEXP_UUID
        edited_gitlog.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', 'cb9225a81eab8ced', '--scat', 'reference', '--editor', '--format', 'text'])
        edited_gitlog.assert_called_with(Content.dump_text(Reference.REGEXP))
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_013(snippy, edited_gitlog):
        """Update reference with ``digest`` option.

        Try to update reference with empty string read from editor.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        edited_gitlog.return_value = ''
        cause = snippy.run(['snippy', 'update', '--scat', 'reference', '-d', '5c2071094dbfaa33', '--format', 'text'])
        assert cause == 'NOK: could not identify content category - please keep template tags in place'
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-regexp', 'update-regexp-utc')
    def test_cli_update_reference_014(snippy, editor_data):
        """Update reference with editor.

        Update existing reference by explicitly defining content format as
        Markdown. In this case the content is not changed at all.
        """

        content = {
            'data': [
                Reference.REGEXP
            ]
        }
        template = (
            '# Python regular expression @python',
            '',
            '> ',
            '',
            '> [1] https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/  ',
            '[2] https://pythex.org/',
            '',
            '## Meta',
            '',
            '> category : reference  ',
            'created  : 2018-06-22T13:11:13.678729+00:00  ',
            'digest   : cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832  ',
            'filename :  ',
            'name     :  ',
            'source   :  ',
            'tags     : howto,online,python,regexp  ',
            'updated  : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid     : 32cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            ''
        )
        editor_data.return_value = '\n'.join(template)
        cause = snippy.run(['snippy', 'update', '-d', 'cb9225a81eab8ced', '--format', 'mkdn'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-three-gitlog-utc')
    def test_cli_update_reference_015(snippy, edited_gitlog):
        """Update reference with editor.

        Update existing Mkdn formatted reference first in text format, then
        in Text format and then again in Markdown format without making any
        changes. The content must not change when updated between different
        formats.

        Each update must generate different timestamp in content ``updated``
        attribute. Also the last update must produce the same resource as
        the first update.

        The content in editor is explicitly defined in the test to avoid
        false positives from the test helpers that actually use the code
        itself.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['tags'] = ('commit',)
        content['data'][0]['digest'] = '2dcb254063ccb5bbc27796df96033f89dae33dde53dbc038d4532e1a798c97c0'
        template = Content.dump_mkdn(content['data'][0])
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', '5c2071094dbfaa33', '--editor', '--format', 'mkdn', '--tags', 'commit'])
        edited_gitlog.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

        content['data'][0]['tags'] = ('git',)
        content['data'][0]['digest'] = 'b2228e2cc6e3d7fe01257f615175a1f33e617b0cfba55199a93e7e48dcdbecf1'
        template = Content.dump_text(content['data'][0])
        edited_gitlog.return_value = template
        content['data'][0]['updated'] = '2018-07-22T13:11:13.678729+00:00'
        cause = snippy.run(['snippy', 'update', '-d', '2dcb254063ccb5bbc', '--editor', '--format', 'text', '--tags', 'git'])
        edited_gitlog.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

        content['data'][0]['tags'] = ('commit',)
        content['data'][0]['digest'] = '2dcb254063ccb5bbc27796df96033f89dae33dde53dbc038d4532e1a798c97c0'
        template = Content.dump_mkdn(content['data'][0])
        edited_gitlog.return_value = template
        content['data'][0]['updated'] = '2018-08-22T13:11:13.678729+00:00'
        cause = snippy.run(['snippy', 'update', '-d', 'b2228e2cc6e3d7fe', '--editor', '--format', 'mkdn', '--tags', 'commit'])
        edited_gitlog.assert_called_with(template)
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('import-gitlog', 'update-pytest-utc')
    def test_cli_update_reference_016(snippy, edited_gitlog):
        """Update reference with editor.

        Update existing resource without doing any changes to the resource.
        The ``updated`` timestamp must not be changed because the resource
        was not changed.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        edited_gitlog.return_value = Content.dump_text(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', '5c2071094dbfaa', '--format', 'text'])
        edited_gitlog.assert_called_with(Content.dump_text(Reference.GITLOG))
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
