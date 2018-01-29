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

"""test_wf_import_solution.py: Test workflows for importing solutions."""

import sys
import unittest
import json
import yaml
import mock
import pkg_resources
from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfImportSolution(unittest.TestCase):
    """Test workflows for importing solutions."""

    @mock.patch.object(json, 'load')
    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_all_solutions(self, mock_isfile, mock_storage_file, mock_yaml_load, mock_json_load):
        """Import all solutions."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [Solution.DEFAULTS[Solution.BEATS], Solution.DEFAULTS[Solution.KAFKA]]}
        mock_yaml_load.return_value = import_dict
        mock_json_load.return_value = import_dict
        compare_content = {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS],
                           'eeef5ca3ec9cd364': Solution.DEFAULTS[Solution.KAFKA]}

        ## Brief: Import all solutions. File name is not defined in commmand line. This should
        ##        result tool internal default file name ./solutions.yaml being used by default.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./solutions.yaml', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from yaml file. File name and format are extracted from
        ##        command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', './all-solutions.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from yaml file without specifying the solution category.
        ##        File name and format are extracted from command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '-f', './all-solutions.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from json file. File name and format are extracted from
        ##        command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', './all-solutions.json'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.json', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from json file without specifying the solution category.
        ##        File name and format are extracted from command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '-f', './all-solutions.json'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./all-solutions.json', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from txt file. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.txt' in this case.
        mocked_open = mock.mock_open(read_data=Solution.get_template(Solution.DEFAULTS[Solution.BEATS]) +
                                     Solution.get_template(Solution.DEFAULTS[Solution.KAFKA]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', './all-solutions.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from txt file without specifying the solution category.
        ##        File name and format are extracted from command line option -f|--file. File
        ##        extension is '*.txt' in this case.
        mocked_open = mock.mock_open(read_data=Solution.get_template(Solution.DEFAULTS[Solution.BEATS]) +
                                     Solution.get_template(Solution.DEFAULTS[Solution.KAFKA]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '-f', './all-solutions.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from txt file. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.text' in this case.
        mocked_open = mock.mock_open(read_data=Solution.get_template(Solution.DEFAULTS[Solution.BEATS]) +
                                     Const.NEWLINE +
                                     Solution.get_template(Solution.DEFAULTS[Solution.KAFKA]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', './all-solutions.text'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.text', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from txt file without specifying the solution category.
        ##        File name and format are extracted from command line option -f|--file. File
        ##        extension is '*.text' in this case.
        mocked_open = mock.mock_open(read_data=Solution.get_template(Solution.DEFAULTS[Solution.BEATS]) +
                                     Const.NEWLINE +
                                     Solution.get_template(Solution.DEFAULTS[Solution.KAFKA]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '-f', './all-solutions.text'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./all-solutions.text', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import solutions from yaml file when all but one of the solutions in the file
        ##        is already stored. Because one solution was stored successfully, the return
        ##        cause is OK.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.BEATS)
            assert len(Database.get_solutions()) == 1
            cause = snippy.run_cli(['snippy', 'import', '--solution', '--file', './all-solutions.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import empty solution template. The operation will fail because
        ##        content templates without any modifications cannot be imported.
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.TEMPLATE))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', './solution-template.txt'])  ## workflow
            assert cause == 'NOK: no content was stored because it matched to empty template'
            assert not Database.get_contents()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import solution from file which file format is not supported. This
        ##        should result error text for end user and no files should be read.
        mocked_open = mock.mock_open(read_data=Solution.get_template(Solution.DEFAULTS[Solution.BEATS]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', './foo.bar'])  ## workflow
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            assert not Database.get_contents()
            mock_file.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(json, 'load')
    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_defined_solution(self, mock_isfile, mock_storage_file, mock_yaml_load, mock_json_load):
        """Import defined solution."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
        updated_solution = Solution.get_template(Solution.DEFAULTS[Solution.NGINX])
        updated_solution = updated_solution.replace('# Instructions how to debug nginx', '# Changed instruction set')
        import_dict = {'content': [{'data': tuple(updated_solution.split(Const.NEWLINE)),
                                    'brief': 'Debugging nginx',
                                    'group': 'nginx',
                                    'tags': ('nginx', 'debug', 'logging', 'howto'),
                                    'links': ('https://www.nginx.com/resources/admin-guide/debug/',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-nginx.txt',
                                    'runalias': '',
                                    'versions': '',
                                    'utc': None,
                                    'digest': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe'}]}
        mock_yaml_load.return_value = import_dict
        mock_json_load.return_value = import_dict

        ## Brief: Import defined solution based on message digest. File name is defined from command line as
        ##        yaml file which contain one solution. One line in the content data was updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.yaml', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': Snippet.get_dictionary(updated_solution)})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined solution based on message digest without specifying the content
        ##        category explicitly.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            cause = snippy.run_cli(['snippy', 'import', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('one-solution.yaml', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': Snippet.get_dictionary(updated_solution)})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined solution based on message digest. File name is defined from command line as
        ##        json file which contain one solution. One line in the content data was updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.json'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.json', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': Snippet.get_dictionary(updated_solution)})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined solution based on message digest. File name is defined from command line as
        ##        text file which contain one solution. One line in the content data was updated. The file
        ##        extension is '*.txt' in this case.
        mocked_open = mock.mock_open(read_data=updated_solution)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': Snippet.get_dictionary(updated_solution)})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined solution based on message digest. File name is defined from command line as
        ##        text file which contain one solution. One line in the content data was updated. The file
        ##        extension is '*.text' in this case.
        mocked_open = mock.mock_open(read_data=updated_solution)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.text'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': Snippet.get_dictionary(updated_solution)})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined solution based on message digest. In this case the content category is
        ##        accidentally specified as 'snippet'. This should still import the content in solution.
        ##        category
        mocked_open = mock.mock_open(read_data=updated_solution)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            cause = snippy.run_cli(['snippy', 'import', '--snippet', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.text'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': Snippet.get_dictionary(updated_solution)})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import defined solution with message digest that cannot be found. In this
        ##        case there is one solution stored.
        mocked_open = mock.mock_open(read_data=updated_solution)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-d', '123456789abcdef0', '-f', 'one-solution.text'])  ## workflow
            assert cause == 'NOK: cannot find solution identified with digest 123456789abcdef0'
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_not_called()
            Solution.test_content(snippy, mock_file, {'61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(json, 'load')
    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_solution(self, mock_isfile, mock_storage_file, mock_yaml_load, mock_json_load):
        """Import solution."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [Solution.DEFAULTS[Solution.NGINX]]}
        mock_yaml_load.return_value = import_dict
        mock_json_load.return_value = import_dict

        ## Brief: Import new solution from yaml file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', 'one-solution.yaml'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.yaml', 'r')
            Solution.test_content(snippy, mock_file, {'61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import new solution from json file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', 'one-solution.json'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.json', 'r')
            Solution.test_content(snippy, mock_file, {'61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import new solution from text file. In this case the file extension is '*.txt'.
        mocked_open = mock.mock_open(read_data=Solution.get_template(Solution.DEFAULTS[Solution.NGINX]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', 'one-solution.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Solution.test_content(snippy, mock_file, {'61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import new solution from text file without specifying the content category
        ##        explicitly. In this case the file extension is '*.txt'.
        mocked_open = mock.mock_open(read_data=Solution.get_template(Solution.DEFAULTS[Solution.NGINX]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '-f', 'one-solution.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Solution.test_content(snippy, mock_file, {'61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import new solution from text file. In this case the file extension is '*.text'.
        mocked_open = mock.mock_open(read_data=Solution.get_template(Solution.DEFAULTS[Solution.NGINX]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '-f', 'one-solution.text'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Solution.test_content(snippy, mock_file, {'61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_solution_defaults(self, mock_isfile, mock_storage_file, mock_yaml_load):
        """Import solutions defaults."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [Solution.DEFAULTS[Solution.BEATS], Solution.DEFAULTS[Solution.NGINX]]}
        mock_yaml_load.return_value = import_dict
        compare_content = {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS],
                           '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]}

        ## Brief: Import solution defaults. All solutions should be imported from predefined file
        ##        location under tool data folder from yaml format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '--defaults'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/default/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import solution defaults again. The second import should fail with an error
        ##        because the content already exist. The error text must be the same for all content
        ##        categories.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults(Snippy())
            cause = snippy.run_cli(['snippy', 'import', '--solution', '--defaults'])  ## workflow
            assert cause == 'NOK: no content was inserted because content data already existed'
            assert len(Database.get_solutions()) == 2
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/default/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_solution_template(self, mock_isfile, mock_storage_file):
        """Import solutions from text template."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
        template = Const.NEWLINE.join(Solution.TEMPLATE)

        ## Brief: Import solution template that does not have any changes to file header
        ##        located at the top of content data. This tests a scenario where user
        ##        does not bother to do any changes to header which has the solution
        ##        metadata. Because the content was changed the import operation must
        ##        work.
        edited_template = template.replace('## description', '## description changed')
        mocked_open = mock.mock_open(read_data=edited_template)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '-f', './solution-template.txt'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./solution-template.txt', 'r')
            Solution.test_content(snippy, mock_file, {'63f2007703d70c8f': Solution.get_dictionary(edited_template)})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import solution template without any changes. This should result error
        ##        text for end user and no files should be read. The error text must be the same
        ##        for all content types.
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'import', '--solution', '--template'])  ## workflow
            assert cause == 'NOK: no content was stored because it matched to empty template'
            assert not Database.get_solutions()
            mock_file.assert_called_once_with('./solution-template.txt', 'r')
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
