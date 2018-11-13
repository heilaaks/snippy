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

"""test_cli_update_reference: Test workflows for updating references."""

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliUpdateReference(object):
    """Test workflows for updating references."""

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_001(self, snippy, edited_gitlog, mocker):
        """Update reference with digest.

        Update reference based on short message digest. Only content links
        are updated.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            '1fc34e79a4d2bac5': Reference.get_dictionary(template),
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '-d', '5c2071094dbfaa33'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_002(self, snippy, edited_gitlog, mocker):
        """Update reference with digest.

        Update reference based on very short message digest. This must match
        to a single reference that must be updated.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            '1fc34e79a4d2bac5': Reference.get_dictionary(template),
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '--digest', '5c2071'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_003(self, snippy, edited_gitlog, mocker):
        """Update reference with digest.

        Update reference based on message digest and accidentally define
        solution category explicitly from command line. In this case the
        reference is updated properly regardless of incorrect category.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            '1fc34e79a4d2bac5': Reference.get_dictionary(template),
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--solution', '-d', '5c2071094dbfaa33'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_004(self, snippy, edited_gitlog, mocker):
        """Update reference with digest.

        Update reference based on message digest and accidentally implicitly
        use snippet category by not using content category option that
        defaults to snippet category. In this case the reference is updated
        properly regardless of incorrect category.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            '1fc34e79a4d2bac5': Reference.get_dictionary(template),
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', '5c2071094dbfaa33'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_005(self, snippy, edited_gitlog, mocker):
        """Update reference with digest.

        Try to update reference with message digest that cannot be found. No
        changes must be made to stored content.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '-d', '123456789abcdef0'])
        assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_006(self, snippy, edited_gitlog, mocker):
        """Update reference with digest.

        Try to update reference with empty message digest. Nothing should be
        updated in this case because the empty digest matches to more than
        one reference. Only one content can be updated at the time.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '-d', ''])
        assert cause == 'NOK: cannot use empty message digest for: update :operation'
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_007(self, snippy, edited_gitlog, mocker):
        """Update reference with uuid.

        Update reference based on short uuid. Only content links are updated.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            '1fc34e79a4d2bac5': Reference.get_dictionary(template),
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '-u', '12cd5827-b6ef-4067-b5ac'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_008(self, snippy, edited_gitlog, mocker):
        """Update reference with uuid.

        Try to update reference based on uuid that cannot be found.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '-u', '9999994'])
        assert cause == 'NOK: cannot find content with content uuid: 9999994'
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.skip(reason='not supported yet')
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_009(self, snippy, edited_gitlog, mocker):
        """Update reference with data.

        Update reference based on content links.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            '1fc34e79a4d2bac5': Reference.get_dictionary(template),
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '-l', 'https://chris.beams.io/posts/git-commit/'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.skip(reason='not supported yet')
    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_010(self, snippy, edited_gitlog, mocker):
        """Update reference with data.

        Try to update reference based on content links that is not found.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', 'https://docs.docker.com')
        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '--links', 'links-not-exist'])
        assert cause == 'NOK: cannot find content with content data: reference not existing'
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-references')
    def test_cli_update_reference_011(self, snippy, edited_gitlog, mocker):
        """Update reference with data.

        Try to update reference with empty content links. Nothing must be
        updated in this case because links are mandatory item in reference
        content.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        template = template.replace('https://chris.beams.io/posts/git-commit/', '')
        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Reference.REGEXP_DIGEST: Reference.DEFAULTS[Reference.REGEXP]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '--reference', '-d', '5c2071094dbfaa33'])
        assert cause == 'NOK: content was not stored because mandatory content field links is empty'
        assert len(Database.get_references()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-regexp', 'update-gitlog-utc')
    def test_cli_update_reference_012(self, snippy, edited_gitlog, mocker):
        """Update existing reference from editor.

        Update existing reference by defining all values from editor. In this
        case the reference is existing and previously stored data must be set
        into editor on top of the default template. In this case the regexp
        reference is edited to gitlog reference. The case verifies that editor
        shows the regexp reference and not an empty reference template.
        """

        template = Reference.dump(Reference.DEFAULTS[Reference.GITLOG], Content.TEXT)
        content_read = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG]
        }
        edited_gitlog.return_value = template
        cause = snippy.run(['snippy', 'update', '-d', 'cb9225a81eab8ced', '--reference', '--editor'])
        edited_gitlog.assert_called_with(Reference.dump(Reference.DEFAULTS[Reference.REGEXP], Content.TEXT))
        assert cause == Cause.ALL_OK
        assert len(Database.get_references()) == 1
        Content.verified(mocker, snippy, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
