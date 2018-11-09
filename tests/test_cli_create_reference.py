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

"""test_cli_create_reference: Test workflows for creating references."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliCreateReferece(object):
    """Test workflows for creating references."""

    def test_cli_create_reference_001(self, snippy, mocker):
        """Create reference from CLI.

        Create new reference by defining all content parameters from command
        line. Content data is not used at all in case of references.
        """

        content_read = {Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG]}
        data = 'must not be used'
        brief = Reference.DEFAULTS[Reference.GITLOG]['brief']
        groups = Reference.DEFAULTS[Reference.GITLOG]['groups']
        tags = Const.DELIMITER_TAGS.join(Reference.DEFAULTS[Reference.GITLOG]['tags'])
        links = Const.DELIMITER_LINKS.join(Reference.DEFAULTS[Reference.GITLOG]['links'])
        cause = snippy.run(['snippy', 'create', '--references', '--links', links, '-b', brief, '-g', groups, '-t', tags, '-c', data])
        assert cause == Cause.ALL_OK
        assert len(Database.get_references()) == 1
        Content.verified(mocker, snippy, content_read)

    def test_cli_create_reference_002(self, snippy):
        """Try to create reference from CLI.

        Try to create new reference without defining mandatory content link.
        """

        data = 'must not be used'
        brief = Reference.DEFAULTS[Reference.GITLOG]['brief']
        groups = Reference.DEFAULTS[Reference.GITLOG]['groups']
        tags = Const.DELIMITER_TAGS.join(Reference.DEFAULTS[Reference.GITLOG]['tags'])
        cause = snippy.run(['snippy', 'create', '--references', '--brief', brief, '--groups', groups, '--tags', tags, '-c', data])
        assert cause == 'NOK: content was not stored because mandatory content field links is empty'
        assert not Database.get_references()

    @pytest.mark.usefixtures('edit-reference-template')
    def test_cli_create_reference_003(self, snippy):
        """Try to create reference from CLI.

        Try to create new reference without any changes to reference template.
        """

        cause = snippy.run(['snippy', 'create', '--editor'])
        assert cause == 'NOK: content was not stored because mandatory content field links is empty'
        assert not Database.get_references()

    @pytest.mark.usefixtures('edit-empty')
    def test_cli_create_reference_004(self, snippy):
        """Try to create reference from CLI.

        Try to create new reference with empty data. In this case the whole
        template is deleted and the edited reference is an empty string.
        """

        cause = snippy.run(['snippy', 'create', '--editor'])
        assert cause == 'NOK: could not identify edited content category - please keep tags in place'
        assert not Database.get_references()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
