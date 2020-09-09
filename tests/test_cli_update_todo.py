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

"""test_cli_update_todo: Test workflows for updating todos."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.todo import Todo


class TestCliUpdateTodo(object):
    """Test workflows for updating todos."""

    @staticmethod
    @pytest.mark.usefixtures('import-deploy', 'update-deploy-utc')
    def test_cli_update_todo_001(snippy, editor_data, capsys):
        """Update todo with editor in Markdown format.

        Update a todo without doing any changes. The updated todo must not be
        changed in the process. In this case the Markdown format was used.
        """

        output = (
            '1. Test deploy @snippy [f3fa4d98677f1171]',
            '',
            '   ! [ ] Add testing  # No Timeline [94c789]',
            '   ! [ ] Add testing  # No Timeline [94c789]',
            '   ! [ ] Add testing  # Today [259876]',
            '   ! [ ] Add testing  # Today [259876]',
            '   ! [x] Add tests  # 2020-06-30 [3038c4]',
            '   ! [ ] Add tests  # 2020-06-30 [c8f811]',
            '   ! [ ] Add tests  # 2020-06-30 [c8f811]',
            '   ! [ ] Add tests  # 2020-06-30 [c8f811]',
            '   ! [x] Add tests 9  # 2020-06-30T11:04:55Z [202a96]',
            '   ! [x] Add tests 10  # 2020-07-30T11:04:55+00:00 [f40c77]',
            '   ! [x] Add tests 11  # 2020-07-30T11:04:55+00:00 [38f409]',
            '',
            '   # deploy,testing,todo',
            '   >',
            '',
            'OK',
            ''
        )
        content = {
            'data': [
                Content.deepcopy(Todo.DEPLOY)
            ]
        }
        editor_data.return_value = Content.dump_mkdn(content['data'][0])
        cause = snippy.run(['snippy', 'update', '-d', 'f3fa4d98677f1171', '--scat', 'todo'])
        out, err = capsys.readouterr()  # Clear old capture.
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)
        cause = snippy.run(['snippy', 'search', '-d', 'f3fa4d98677f1171', '--no-ansi'])
        out, err = capsys.readouterr()
        assert out == Const.NEWLINE.join(output)
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
