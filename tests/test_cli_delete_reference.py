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

"""test_cli_delete_reference: Test workflows for deleting references."""

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliDeleteReference(object):
    """Test workflows for deleting references."""

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_001(self, snippy, mocker):
        """Delete reference with digest.

        Delete reference with short 16 byte version of message digest.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG]
        }
        cause = snippy.run(['snippy', 'delete', '-d', 'cb9225a81eab8ced'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-remove')
    def test_cli_delete_reference_002(self, snippy):
        """Delete reference with digest.

        Delete reference with empty message digest when there is only one
        content stored. In this case the last content can be deleted with
        empty digest.
        """

        cause = snippy.run(['snippy', 'delete', '-d', ''])
        assert cause == Cause.ALL_OK
        assert not Database.get_references().size()

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_003(self, snippy, mocker):
        """Delete reference with digest.

        Try to delete reference with message digest that cannot be found.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        assert Database.get_references().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_004(self, snippy, mocker):
        """Delete reference with uuid.

        Delete reference with short content uuid.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG]
        }
        cause = snippy.run(['snippy', 'delete', '-u', '16cd5827'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_005(self, snippy, mocker):
        """Delete reference with uuid.

        Try to delete content with empty uuid string.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '-u', ''])
        assert cause == 'NOK: cannot use empty content uuid for: delete :operation'
        assert Database.get_references().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_006(self, snippy, mocker):
        """Delete reference with uuid.

        Try to delete content with uuid that does not match to any content.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '-u', '1234567'])
        assert cause == 'NOK: cannot find content with content uuid: 1234567'
        assert Database.get_references().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_007(self, snippy, mocker):
        """Delete reference with uuid.

        Try to delete content with uuid that matches to more than one content.
        In this case nothing should get deleted because the operatione permits
        only one content to be deleted in one operation.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '-u', '1'])
        assert cause == 'NOK: content uuid: 1 :matched more than once: 2 :preventing: delete :operation'
        assert Database.get_references().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_008(self, snippy, mocker):
        """Delete reference with data.

        Delete reference based on content data.
        """

        content_read = {
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '--content', 'https://chris.beams.io/posts/git-commit/'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_009(self, snippy, mocker):
        """Delete reference with data.

        Try to delete reference with content data that does not exist. In this
        case the content data is not truncated.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '--content', 'not found content'])
        assert cause == 'NOK: cannot find content with content data: not found content'
        assert Database.get_references().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.skip(reason='not supported yet')
    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_010(self, snippy, mocker):
        """Delete reference with link.

        Delete reference based on content link.
        """

        content_read = {
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '--links', 'https://chris.beams.io/posts/git-commit/'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_011(self, snippy, mocker):
        """Delete reference with data.

        Try to delete reference with empty content data. Nothing should be
        deleted in this case because there is more than one content left.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '--content', ''])
        assert cause == 'NOK: cannot use empty content data for: delete :operation'
        assert Database.get_references().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_012(self, snippy, mocker):
        """Delete reference with search.

        Delete reference based on search keyword that results one hit. In this
        case the content is deleted.
        """

        content_read = {
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '--sall', 'chris', '--references'])
        assert cause == Cause.ALL_OK
        assert Database.get_references().size() == 1
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_delete_reference_013(self, snippy, mocker):
        """Try to delete reference with search.

        Try to delete reference based on search keyword so that the category
        is left out. In this case the search keyword matches but the default
        category is snippet and not content is deleted.
        """

        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        cause = snippy.run(['snippy', 'delete', '--sall', 'chris'])
        assert cause == 'NOK: cannot find content with given search criteria'
        assert Database.get_references().size() == 2
        Content.verified(mocker, snippy, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
