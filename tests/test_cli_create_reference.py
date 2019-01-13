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

"""test_cli_create_reference: Test workflows for creating references."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference import Reference


class TestCliCreateReferece(object):
    """Test workflows for creating references."""

    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_cli_create_reference_001(self, snippy):
        """Create reference from CLI.

        Create new reference by defining all content parameters from command
        line. Content data is must not be used at all in case of reference
        content.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        data = 'must not be used'
        brief = content['data'][0]['brief']
        groups = content['data'][0]['groups']
        tags = content['data'][0]['tags']
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links'])
        cause = snippy.run(['snippy', 'create', '--references', '--links', links, '-b', brief, '-g', groups, '-t', tags, '-c', data])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    def test_cli_create_reference_002(self, snippy):
        """Try to create reference from CLI.

        Try to create new reference without defining mandatory content link.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        data = 'must not be used'
        brief = content['data'][0]['brief']
        groups = Reference.GITLOG['groups']
        tags = content['data'][0]['tags']
        cause = snippy.run(['snippy', 'create', '--references', '--brief', brief, '--groups', groups, '--tags', tags, '-c', data, '--no-editor'])
        assert cause == 'NOK: content was not stored because mandatory content field links is empty'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('edit-reference-template')
    def test_cli_create_reference_003(self, snippy):
        """Try to create reference from CLI.

        Try to create new reference without any changes to reference template.
        """

        cause = snippy.run(['snippy', 'create', '--editor', '--format', 'text'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('edit-empty')
    def test_cli_create_reference_004(self, snippy):
        """Try to create reference from CLI.

        Try to create new reference with empty data. In this case the whole
        template is deleted and the edited reference is an empty string.
        """

        cause = snippy.run(['snippy', 'create', '--editor', '--format', 'text'])
        assert cause == 'NOK: could not identify content category - please keep template tags in place'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_cli_create_reference_005(self, snippy, editor_data):
        """Create reference with editor.

        Create new reference by using the default Markdown template. All values
        are set with editor. The template is defined in this on purpose. This
        tries to make sure that the testing framework does not hide possible
        problems if the template would be generated automatically.
        """

        content = {
            'data': [
                Reference.GITLOG
            ]
        }
        template = (
            '# Add brief title for content @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> [1] https://www.example.com/add-links-here.html',
            '',
            '## Meta',
            '',
            '> category : reference  ',
            'created  : 2018-06-22T13:11:13.678729+00:00  ',
            'digest   : ' + Reference.TEMPLATE_DIGEST_MKDN + '  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : comma,separated,tags  ',
            'updated  : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid     : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            ''
        )
        edited = (
            '# How to write commit messages @git',
            '',
            '> ',
            '',
            '> [1] https://chris.beams.io/posts/git-commit/',
            '',
            '`$ docker rm --volumes $(docker ps --all --quiet)`',
            '',
            '## Meta',
            '',
            '> category : reference  ',
            'created  : 2018-06-22T13:11:13.678729+00:00  ',
            'digest   : ' + Reference.TEMPLATE_DIGEST_MKDN + '  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : commit,git,howto  ',
            'updated  : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid     : 24cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            '')
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '--reference', '--editor'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_cli_create_reference_006(self, snippy, editor_data):
        """Try to create reference with editor.

        Try to create new reference by using the default Markdown template. In
        this case there are no any changes to the template.
        """

        template = (
            '# Add brief title for content @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> [1] https://www.example.com/add-links-here.html',
            '',
            '## Meta',
            '',
            '> category : reference  ',
            'created  : 2018-06-22T13:11:13.678729+00:00  ',
            'digest   : ' + Reference.TEMPLATE_DIGEST_MKDN + '  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : comma,separated,tags  ',
            'updated  : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid     : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            ''
        )
        edited = template
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '--reference', '--editor'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(None)


    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_reference_007(self, snippy):
        """Try to create reference from CLI.

        Try to create new reference by from command line with --no-editor
        option when the mandatory links is not defined.
        """

        cause = snippy.run(['snippy', 'create', '--reference', '--brief', 'Short brief', '--no-editor'])
        assert cause == 'NOK: content was not stored because mandatory content field links is empty'
        Content.assert_storage(None)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
