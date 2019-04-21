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
from tests.lib.content import Content
from tests.lib.reference import Reference


class TestCliCreateReferece(object):
    """Test workflows for creating references."""

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_cli_create_reference_001(snippy):
        """Create reference from CLI.

        Create new reference by defining all content parameters from command
        line. Content data is must not be used at all in case of reference
        content.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
        data = 'must not be used'
        brief = content['data'][0]['brief']
        groups = content['data'][0]['groups']
        tags = content['data'][0]['tags']
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links'])
        cause = snippy.run(['snippy', 'create', '--references', '--links', links, '-b', brief, '-g', groups, '-t', tags, '-c', data])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    def test_cli_create_reference_002(snippy):
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

    @staticmethod
    @pytest.mark.usefixtures('edit-reference-template')
    def test_cli_create_reference_003(snippy):
        """Try to create reference from CLI.

        Try to create new reference without any changes to reference template.
        """

        cause = snippy.run(['snippy', 'create', '--editor', '--format', 'text'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('edit-empty')
    def test_cli_create_reference_004(snippy):
        """Try to create reference from CLI.

        Try to create new reference with empty data. In this case the whole
        template is deleted and the edited reference is an empty string.
        """

        cause = snippy.run(['snippy', 'create', '--editor', '--format', 'text'])
        assert cause == 'NOK: could not identify content category - please keep template tags in place'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_cli_create_reference_005(snippy, editor_data):
        """Create reference with editor.

        Create a new reference by using the prefilled default Markdown template
        in editor. The template presented in editor is manually defined in this
        test case on purpose. This tries to verity that the testing framework
        does not hide problems compared to situation where the template would
        be generated automatically by the testing framework.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['uuid'] = Content.UUID1
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
            'digest   : bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d  ',
            'filename : example-content.md  ',
            'name     : example content handle  ',
            'source   : https://www.example.com/source.md  ',
            'tags     : example,tags  ',
            'updated  : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : example=3.9.0,python>=3  ',
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
            'digest   : bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d  ',
            'filename :  ',
            'name     :  ',
            'source   :  ',
            'tags     : commit,git,howto  ',
            'updated  : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            '')
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '--reference', '--editor'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_cli_create_reference_006(snippy, editor_data):
        """Try to create reference with editor.

        Try to create a new reference by using the prefilled default Markdown
        template in editor. In this case there are no any changes made in
        editor on top of the displayed template.
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
            'digest   : bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d  ',
            'filename : example-content.md  ',
            'name     : example content handle  ',
            'source   : https://www.example.com/source.md  ',
            'tags     : example,tags  ',
            'updated  : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : example=3.9.0,python>=3  ',
            ''
        )
        edited = template
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '--reference', '--editor'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_reference_007(snippy):
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
