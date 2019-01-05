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

"""test_cli_import_solution: Test workflows for importing solutions."""

import json
import pkg_resources

import mock
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference import Reference
from tests.testlib.snippet import Snippet
from tests.testlib.solution import Solution


class TestCliImportSolution(object):  # pylint: disable=too-many-public-methods
    """Test workflows for importing solutions."""

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_001(self, snippy):
        """Import all solutions.

        Import all solutions. File name is not defined in command line. This
        should result tool internal default file name and format being used.
        """

        content = {
            'data': [
                Solution.KAFKA,
                Solution.BEATS
            ]
        }
        file_content = Content.get_file_content(Content.MKDN, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./solutions.mkdn', 'r')

    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_solution_002(self, snippy):
        """Import all solutions.

        Import all solutions from yaml file. File name and format are extracted
        from command line option -f|--file.
        """

        content = {
            'data': [
                Solution.KAFKA,
                Solution.BEATS
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')

    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_solution_003(self, snippy):
        """Import all solutions.

        Import all solutions from yaml file without specifying the solution
        category. File name and format are extracted from command line
        option -f|--file.
        """

        content = {
            'data': [
                Solution.KAFKA,
                Solution.BEATS
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')

    @pytest.mark.usefixtures('isfile_true', 'json')
    def test_cli_import_solution_004(self, snippy):
        """Import all solutions.

        Import all solutions from json file. File name and format are extracted
        from command line option -f|--file.
        """

        content = {
            'data': [
                Solution.KAFKA,
                Solution.BEATS
            ]
        }
        file_content = Content.get_file_content(Content.JSON, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.json'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.json', 'r')

    @pytest.mark.usefixtures('isfile_true', 'json')
    def test_cli_import_solution_005(self, snippy):
        """Import all solutions.

        Import all solutions from json file without specifying the solution
        category. File name and format are extracted from command line
        option -f|--file.
        """

        content = {
            'data': [
                Solution.KAFKA,
                Solution.BEATS
            ]
        }
        file_content = Content.get_file_content(Content.JSON, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.json'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.json', 'r')

    @pytest.mark.usefixtures('isfile_true', 'default-solutions-utc')
    def test_cli_import_solution_006(self, snippy):
        """Import all solutions.

        Import all solutions from txt file. File name and format are extracted
        from command line option -f|--file. File extension is '*.txt' in this
        case.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')

    @pytest.mark.usefixtures('isfile_true', 'default-solutions-utc')
    def test_cli_import_solution_007(self, snippy):
        """Import all solutions.

        Import all solutions from txt file without specifying the solution
        category. File name and format are extracted from command line
        option -f|--file. File extension is '*.txt' in this case.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')

    @pytest.mark.usefixtures('isfile_true', 'default-solutions-utc')
    def test_cli_import_solution_008(self, snippy):
        """Import all solutions.

        Import all solutions from txt file. File name and format are extracted
        from command line option -f|--file. File extension is '*.text' in this
        case.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.text', 'r')

    @pytest.mark.usefixtures('isfile_true', 'default-solutions-utc')
    def test_cli_import_solution_009(self, snippy):
        """Import all solutions.

        Import all solutions from txt file without specifying the solution
        category. File name and format are extracted from command line option
        -f|--file. File extension is '*.text' in this case.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.text', 'r')

    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-beats', 'import-kafka-utc')
    def test_cli_import_solution_010(self, snippy):
        """Import all solutions.

        Import solutions from yaml file when all but one of the solutions in
        the file is already stored. Because one solution was stored
        successfully, the return cause is OK.
        """

        content = {
            'data': [
                Solution.KAFKA,
                Solution.BEATS
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '--file', './all-solutions.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_011(self, snippy):
        """Import all solutions.

        Try to import empty solution template. The operation will fail because
        content templates without any modifications cannot be imported.
        """

        file_content = mock.mock_open(read_data=Const.NEWLINE.join(Solution.TEMPLATE))
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './solution-template.txt'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            Content.assert_storage(None)
            mock_file.assert_called_once_with('./solution-template.txt', 'r')

    def test_cli_import_solution_012(self, snippy):
        """Import all solutions.

        Try to import solution from file which file format is not supported.
        This should result error text for end user and no files should be read.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file: ./foo.bar'
            Content.assert_storage(None)
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-nginx', 'update-kafka-utc')
    def test_cli_import_solution_013(self, snippy):
        """Import solution based on message digest.

        Import defined solution based on message digest. File name is defined
        from command line as yaml file which contain one solution. One line in
        the solution data was updated.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['data'] = content['data'][0]['data'][:13] + ('    # Changed.',) + content['data'][0]['data'][14:]
        content['data'][0]['digest'] = 'f7c59ea7da22f408d4ba71d4c4ac477b83549d29e1bfcb4d721ccda0b1fedfe2'
        content['data'][0]['updated'] = Content.KAFKA_TIME
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '5dee85bedb7f4d3a', '-f', 'one-solution.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.yaml', 'r')

    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-nginx', 'update-kafka-utc')
    def test_cli_import_solution_014(self, snippy):
        """Import solution based on message digest.

        Import defined solution based on message digest without specifying the
        content category explicitly. One line in the solution data was updated.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['data'] = content['data'][0]['data'][:13] + ('    # Changed.',) + content['data'][0]['data'][14:]
        content['data'][0]['digest'] = 'f7c59ea7da22f408d4ba71d4c4ac477b83549d29e1bfcb4d721ccda0b1fedfe2'
        content['data'][0]['updated'] = Content.KAFKA_TIME
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '-d', '5dee85bedb7f4d3a', '-f', 'one-solution.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.yaml', 'r')

    @pytest.mark.usefixtures('isfile_true', 'json', 'import-nginx', 'update-kafka-utc')
    def test_cli_import_solution_015(self, snippy):
        """Import solution based on message digest.

        Import defined solution based on message digest. File name is defined
        from command line as json file which contain one solution. One line in
        the content data was updated.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['data'] = content['data'][0]['data'][:13] + ('    # Changed.',) + content['data'][0]['data'][14:]
        content['data'][0]['digest'] = 'f7c59ea7da22f408d4ba71d4c4ac477b83549d29e1bfcb4d721ccda0b1fedfe2'
        content['data'][0]['updated'] = Content.KAFKA_TIME
        file_content = Content.get_file_content(Content.JSON, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '5dee85bedb7f4d3a', '-f', 'one-solution.json'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.json', 'r')

    @pytest.mark.usefixtures('isfile_true', 'import-nginx', 'update-kafka-utc')
    def test_cli_import_solution_016(self, snippy):
        """Import solution based on message digest.

        Import defined solution based on message digest. File name is defined
        from command line as text file which contain one solution. One line
        in the content data was updated. The file extension is '*.txt' in
        this case.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['data'] = content['data'][0]['data'][:13] + ('    # Changed.',) + content['data'][0]['data'][14:]
        content['data'][0]['description'] = 'Changed.'
        content['data'][0]['digest'] = '44a84d31fd5d4ca67aecf2dd1f92290114cbd64bd33b4f1811761c82f645458a'
        content['data'][0]['updated'] = Content.KAFKA_TIME
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '5dee85bedb7f4d3a', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.txt', 'r')

    @pytest.mark.usefixtures('isfile_true', 'import-nginx', 'update-kafka-utc')
    def test_cli_import_solution_017(self, snippy):
        """Import solution based on message digest.

        Import defined solution based on message digest. File name is defined
        from command line as text file which contain one solution. One line
        in the content data was updated. The file extension is '*.text' in
        this case.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['data'] = content['data'][0]['data'][:13] + ('    # Changed.',) + content['data'][0]['data'][14:]
        content['data'][0]['description'] = 'Changed.'
        content['data'][0]['digest'] = '44a84d31fd5d4ca67aecf2dd1f92290114cbd64bd33b4f1811761c82f645458a'
        content['data'][0]['updated'] = Content.KAFKA_TIME
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '5dee85bedb7f4d3a', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.text', 'r')

    @pytest.mark.usefixtures('isfile_true', 'import-nginx', 'update-kafka-utc')
    def test_cli_import_solution_018(self, snippy):
        """Import solution based on message digest.

        Import defined solution based on message digest. In this case the
        content category is accidentally specified as 'snippet'. This
        should still import the content in solution category.
        """

        content = {
            'data': [
                Content.deepcopy(Solution.NGINX)
            ]
        }
        content['data'][0]['data'] = content['data'][0]['data'][:13] + ('    # Changed.',) + content['data'][0]['data'][14:]
        content['data'][0]['description'] = 'Changed.'
        content['data'][0]['digest'] = '44a84d31fd5d4ca67aecf2dd1f92290114cbd64bd33b4f1811761c82f645458a'
        content['data'][0]['updated'] = Content.KAFKA_TIME
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--snippet', '-d', '5dee85bedb7f4d3a', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.text', 'r')

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_019(self, snippy):
        """Import solution based on message digest.

        Try to import defined solution with message digest that cannot be
        found. In this case there is one solution already stored.
        """

        content = {
            'data': [
                Solution.NGINX
            ]
        }
        updates = {
            'data': [
                Content.deepcopy(Solution.NGINX)
            ]
        }
        updates['data'][0]['data'] = content['data'][0]['data'][:13] + ('    # Changed.',) + content['data'][0]['data'][14:]
        updates['data'][0]['description'] = 'Changed.'
        updates['data'][0]['digest'] = '44a84d31fd5d4ca67aecf2dd1f92290114cbd64bd33b4f1811761c82f645458a'
        updates['data'][0]['updated'] = Content.KAFKA_TIME
        file_content = Content.get_file_content(Content.TEXT, updates)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '123456789abcdef0', '-f', 'one-solution.text'])
            assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
            Content.assert_storage(content)
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_solution_020(self, snippy):
        """Import solution.

        Import new solution from yaml file.
        """

        content = {
            'data': [
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.yaml'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.yaml', 'r')

    @pytest.mark.usefixtures('isfile_true', 'json')
    def test_cli_import_solution_021(self, snippy):
        """Import solution.

        Import new solution from json file.
        """

        content = {
            'data': [
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.JSON, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.json'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.json', 'r')

    @pytest.mark.usefixtures('isfile_true', 'import-nginx-utc')
    def test_cli_import_solution_022(self, snippy):
        """Import solution.

        Import new solution from text file. In this case the file extension
        is '*.txt'.
        """

        content = {
            'data': [
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.txt', 'r')

    @pytest.mark.usefixtures('isfile_true', 'import-nginx-utc')
    def test_cli_import_solution_023(self, snippy):
        """Import solution.

        Import new solution from text file without specifying the content
        category explicitly. In this case the file extension is '*.txt'.
        """

        content = {
            'data': [
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.txt', 'r')

    @pytest.mark.usefixtures('isfile_true', 'import-nginx-utc')
    def test_cli_import_solution_024(self, snippy):
        """Import solution.

        Import new solution from text file. In this case the file extension
        is '*.text'.
        """

        content = {
            'data': [
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('one-solution.text', 'r')

    @pytest.mark.usefixtures('yaml')
    def test_cli_import_solution_025(self, snippy):
        """Import solutions defaults.

        Import solution defaults. All solutions should be imported from
        predefined file location under tool data folder from yaml format.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '--defaults'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'r')

    @pytest.mark.usefixtures('yaml', 'default-solutions', 'default-solutions-utc')
    def test_cli_import_solution_026(self, snippy):
        """Import solutions defaults.

        Try to import solution defaults again. The second import should fail
        with an error because the content already exist. The error text must
        be the same for all content categories. Because of random order
        dictionary in the code, the reported digest can vary when there are
        multiple failures to import each content.
        """

        content = {
            'data': [
                Solution.BEATS,
                Solution.NGINX
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--solution', '--defaults'])
            assert cause in ('NOK: content: data :already exist with digest: 5dee85bedb7f4d3a',
                             'NOK: content: data :already exist with digest: db712a82662d6932')
            Content.assert_storage(content)
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'r')

    @pytest.mark.usefixtures('isfile_true', 'import-content-utc')
    def test_cli_import_solution_027(self, snippy):
        """Import solutions from text template.

        Import solution template that does not have any changes to file header
        located at the top of content data. This tests a scenario where user
        does not bother to do any changes to header which has the solution
        metadata. Because the content was changed the import operation must
        work.
        """

        template = Const.NEWLINE.join(Solution.TEMPLATE)
        template = template.replace('## description', '## description changed')
        content = {
            'data': [
                Content.dump_dict(template)
            ]
        }
        file_content = Content.get_file_content(Content.TEXT, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './solution-template.txt'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./solution-template.txt', 'r')

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_028(self, snippy):
        """Import solutions from text template.

        Try to import solution template without any changes. This should result
        error text for end user and no files should be read. The error text must
        be the same for all content types.
        """

        file_content = mock.mock_open(read_data=Const.NEWLINE.join(Solution.TEMPLATE))
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '--template'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            Content.assert_storage(None)
            mock_file.assert_called_once_with('./solution-template.txt', 'r')

    @pytest.mark.usefixtures('yaml')
    def test_cli_import_solution_029(self, snippy):
        """Import all content defaults.

        Import snippet, solution and reference defaults.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Solution.NGINX,
                Reference.GITLOG
            ]
        }
        file_content = Content.get_file_content(Content.YAML, content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = file_content
            cause = snippy.run(['snippy', 'import', '--all', '--defaults'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            defaults = []
            defaults.append(mock.call(pkg_resources.resource_filename('snippy', 'data/defaults/snippets.yaml'), 'r'))
            defaults.append(mock.call(pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml'), 'r'))
            defaults.append(mock.call(pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml'), 'r'))
            mock_file.assert_has_calls(defaults, any_order=True)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_030(self, snippy):
        """Import all solutions.

        Try to import content with option --all. This is not supported for
        import operation.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--all', '-f', './foo.yaml'])
            assert cause == 'NOK: import operation for content category \'all\' is supported only with default content'
            Content.assert_storage(None)
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_031(self, snippy):
        """Import all solutions.

        Try to import content with option --all. This is not supported for
        import operation.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'create', '--all', '-f', './foo.yaml'])
            assert cause == 'NOK: content category \'all\' is supported only with search, import or export operations'
            Content.assert_storage(None)
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_032(self, snippy):
        """Import all solutions.

        Import all solutions from Markdown formatted file.
        """

        content = {
            'data': [
                Solution.KAFKA,
                Solution.BEATS
            ]
        }
        file_content = Content.get_file_content(Content.MKDN, content)
        with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.md'])
            assert cause == Cause.ALL_OK
            Content.assert_storage(content)
            mock_file.assert_called_once_with('./all-solutions.md', 'r')

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
