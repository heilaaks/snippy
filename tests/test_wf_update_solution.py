#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
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

"""test_wf_update_solution.py: Test workflows for updating solutions."""

import sys
import unittest
import mock
from snippy.config.config import Config
from snippy.config.source.editor import Editor
from snippy.snip import Snippy
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfUpdateSolution(unittest.TestCase):
    """Test workflows for updating solutions."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_update_solution_with_digest(self, mock_isfile, mock_storage_file, mock_call_editor):
        """Update solution with digest."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Update solution based on short message digest. Only the content data is updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', 'a96accc25dd23ac0'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'f8ded660166ebeef': Solution.get_dictionary(template),
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update solution based on very short message digest. This must match to a single
        ##        solution that must be updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '--solution', '--digest', 'a96ac'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'f8ded660166ebeef': Solution.get_dictionary(template),
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update solution based on long message digest. Only the content data is updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'f8ded660166ebeef': Solution.get_dictionary(template),
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update solution based on message digest and accidentally define snippet
        ##        category explicitly from command line. In this case the solution is updated
        ##        properly regardless of incorrect category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '--snippet', '-d', 'a96accc25dd23ac0'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'f8ded660166ebeef': Solution.get_dictionary(template),
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Update solution based on message digest and accidentally implicitly use
        ##        snippet category by not using content category option that defaults to
        ##        snippet category. In this case the solution is updated properly regardless
        ##        of incorrect category.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '-d', 'a96accc25dd23ac0'])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'f8ded660166ebeef': Solution.get_dictionary(template),
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update solution with message digest that cannot be found. No changes must
        ##        be made to stored content.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', '123456789abcdef0'])  ## workflow
            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS],
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update solution with empty message digest. Nothing should be updated
        ##        in this case because the empty digest matches to more than one solution. Only
        ##        one content can be updated at the time.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', ''])  ## workflow
            assert cause == 'NOK: cannot use empty message digest to update content'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS],
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_update_solution_with_data(self, mock_isfile, mock_storage_file, mock_call_editor):
        """Update solution with data."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Update solution based on content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            data = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            cause = snippy.run_cli(['snippy', 'update', '--solution', '-c', data])  ## workflow
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'f8ded660166ebeef': Solution.get_dictionary(template),
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update solution based on content data that is not found.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '--solution', '--content', 'solution not existing'])  ## workflow
            assert cause == 'NOK: cannot find content with content data \'solution not existing\''
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS],
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to update solution with empty content data. Nothing must be updated
        ##        in this case because there is more than one content stored.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            template = template.replace('## description', '## updated content description')
            mock_call_editor.return_value = template
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'update', '--solution', '-c', ''])  ## workflow
            assert cause == 'NOK: cannot use empty content data to update content'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS],
                                                      '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
