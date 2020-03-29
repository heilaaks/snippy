# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

        Create a new reference by defining all content attributes from command
        line. The content ``data`` attribute must not be used when creating new
        reference content.
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
        cause = snippy.run(['snippy', 'create', '--scat', 'reference', '--links', links, '-b', brief, '-g', groups, '-t', tags, '-c', data])
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @staticmethod
    def test_cli_create_reference_002(snippy):
        """Try to create reference from CLI.

        Try to create new reference without defining mandatory content the
        ``links`` attribute.
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
        cause = snippy.run(['snippy', 'create', '--scat', 'reference', '--brief', brief, '--groups', groups, '--tags', tags, '-c', data, '--no-editor'])  # pylint: disable=line-too-long
        assert cause == 'NOK: content was not stored because mandatory content field links is empty'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('edit-reference-template')
    def test_cli_create_reference_003(snippy):
        """Try to create reference from CLI.

        Try to create new reference without any changes to the reference
        template.
        """

        cause = snippy.run(['snippy', 'create', '--editor', '--format', 'text'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('edit-empty')
    def test_cli_create_reference_004(snippy):
        """Try to create reference from editor.

        Try to create new reference with empty content. In this case the whole
        template is deleted in editor and the edited content is just an empty
        string.
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
            '> category  : reference  ',
            'created   : 2018-06-22T13:11:13.678729+00:00  ',
            'digest    : bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d  ',
            'filename  : example-content.md  ',
            'languages : example-language  ',
            'name      : example content handle  ',
            'source    : https://www.example.com/source.md  ',
            'tags      : example,tags  ',
            'updated   : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid      : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  : example=3.9.0,python>=3  ',
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
            '> category  : reference  ',
            'created   : 2018-06-22T13:11:13.678729+00:00  ',
            'digest    : bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d  ',
            'filename  :  ',
            'languages :  ',
            'name      :  ',
            'source    :  ',
            'tags      : commit,git,howto  ',
            'updated   : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid      : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  :  ',
            '')
        editor_data.return_value = Const.NEWLINE.join(edited)
        cause = snippy.run(['snippy', 'create', '--scat', 'reference', '--editor'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with(Const.NEWLINE.join(template))
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_cli_create_reference_006(snippy, editor_data):
        """Try to create reference with editor.

        Try to create a new reference by using the prefilled default Markdown
        template in editor. In this case there are no changes made in editor
        on top of the displayed template. Content must not be stored because
        it is matching to a content template.
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
            '> category  : reference  ',
            'created   : 2018-06-22T13:11:13.678729+00:00  ',
            'digest    : bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d  ',
            'filename  : example-content.md  ',
            'languages : example-language  ',
            'name      : example content handle  ',
            'source    : https://www.example.com/source.md  ',
            'tags      : example,tags  ',
            'updated   : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid      : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  : example=3.9.0,python>=3  ',
            ''
        )
        edited = template
        editor_data.return_value = Const.NEWLINE.join(edited)
        cause = snippy.run(['snippy', 'create', '--scat', 'reference', '--editor'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        editor_data.assert_called_with(Const.NEWLINE.join(template))
        Content.assert_storage(None)

    @staticmethod
    def test_cli_create_reference_007(snippy):
        """Try to create reference from CLI.

        Try to create new reference by from command line with ``--no-editor``
        option when the mandatory ``links`` attribute for a reference category
        is not defined.
        """

        cause = snippy.run(['snippy', 'create', '--scat', 'reference', '--brief', 'Short brief', '--no-editor'])
        assert cause == 'NOK: content was not stored because mandatory content field links is empty'
        Content.assert_storage(None)

    @staticmethod
    def test_cli_create_reference_008(snippy):
        """Try to create reference from CLI.

        Try to create new reference by from command line when the content
        category contains two values. The ``--scat`` option must specify
        an unique content category when new content is created.
        """

        cause = snippy.run(['snippy', 'create', '--scat', 'reference,snippet', '--links', 'http://short', '--no-editor'])
        assert cause == "NOK: content category must be unique when content is created: ('reference', 'snippet')"
        Content.assert_storage(None)

    @staticmethod
    def test_cli_create_reference_009(snippy):
        """Try to create reference from CLI.

        Try to create new reference by from command line when the content
        category contains invalid and valid content category. Because of a
        failure to define the content category correctly, content creation
        must fail.
        """

        cause = snippy.run(['snippy', 'create', '--scat', 'reference,failure', '--links', 'http://short', '--no-editor'])
        assert cause == "NOK: content categories ('failure', 'reference') are not a subset of ('snippet', 'solution', 'reference')"
        Content.assert_storage(None)

    @staticmethod
    @pytest.mark.usefixtures('create-gitlog-utc')
    def test_cli_create_reference_010(snippy, editor_data):
        """Create reference with editor.

        Create a new reference by using the prefilled default Markdown template
        in editor. In this case the metadata section is not touched and there
        is the example content left. The example values for attributes must not
        be used when the content is created.
        """

        content = {
            'data': [
                Content.deepcopy(Reference.GITLOG)
            ]
        }
        content['data'][0]['tags'] = ()
        content['data'][0]['uuid'] = Content.UUID1
        content['data'][0]['digest'] = '7093775e077941bad7a707295feb6a6630458f89e18a35994179e27fc4937b02'
        template = (
            '# Add brief title for content @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> [1] https://www.example.com/add-links-here.html',
            '',
            '## Meta',
            '',
            '> category  : reference  ',
            'created   : 2018-06-22T13:11:13.678729+00:00  ',
            'digest    : bb4c2540fab3a12b051b77b6902f426812ec95f8a1fa9e07ca1b7dc3cca0cc0d  ',
            'filename  : example-content.md  ',
            'languages : example-language  ',
            'name      : example content handle  ',
            'source    : https://www.example.com/source.md  ',
            'tags      : example,tags  ',
            'updated   : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid      : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions  : example=3.9.0,python>=3  ',
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
            'digest   : 7093775e077941bad7a707295feb6a6630458f89e18a35994179e27fc4937b02  ',
            'filename : example-content.md  ',
            'languages : example-language  ',
            'name     : example content handle  ',
            'source   : https://www.example.com/source.md  ',
            'tags     : example,tags  ',
            'updated  : 2018-06-22T13:11:13.678729+00:00  ',
            'uuid     : a1cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : example=3.9.0,python>=3  ',
            '')
        editor_data.return_value = Const.NEWLINE.join(edited)
        cause = snippy.run(['snippy', 'create', '--scat', 'reference', '--editor'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with(Const.NEWLINE.join(template))
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
