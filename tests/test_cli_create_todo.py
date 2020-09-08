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

"""test_cli_create_todo: Test workflows for creating todos."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.todo import Todo


class TestCliCreateTodo(object):
    """Test workflows for creating todos."""

    @staticmethod
    @pytest.mark.usefixtures('create-defmkd-utc')
    def test_cli_create_todo_001(snippy, editor_data):
        """Create todo with editor.

        Create a new todo by using the prefilled default Markdown template
        in editor. In this case the none of the default data is changed. The
        example values in the gived default template attributes must not be
        used when the content is tried to be stored.
        """

        content = {
            'data': [
                Content.deepcopy(Todo.DEFMKD)
            ]
        }
        editor_data.return_value = Const.NEWLINE.join(Todo.TEMPLATE_MKDN)
        cause = snippy.run(['snippy', 'create', '--scat', 'todo'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with(Const.NEWLINE.join(Todo.TEMPLATE_MKDN))
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
