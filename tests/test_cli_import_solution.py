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

"""test_cli_import_solution: Test workflows for importing solutions."""

import json
import pkg_resources

import mock
import pytest
import yaml

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliImportSolution(object):  # pylint: disable=too-many-public-methods
    """Test workflows for importing solutions."""

    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_solution_001(self, snippy, mocker):
        """Import all solutions.

        Import all solutions. File name is not defined in command line. This
        should result tool internal default file name and format being used.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./solutions.yaml', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_solution_002(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from yaml file. File name and format are extracted
        from command line option -f|--file.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.yaml'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_solution_003(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from yaml file without specifying the solution
        category. File name and format are extracted from command line
        option -f|--file.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.yaml'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true', 'json')
    def test_cli_import_solution_004(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from json file. File name and format are extracted
        from command line option -f|--file.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.json'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.json', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true', 'json')
    def test_cli_import_solution_005(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from json file without specifying the solution
        category. File name and format are extracted from command line
        option -f|--file.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.json'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./all-solutions.json', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_006(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from txt file. File name and format are extracted
        from command line option -f|--file. File extension is '*.txt' in this
        case.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_007(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from txt file without specifying the solution
        category. File name and format are extracted from command line
        option -f|--file. File extension is '*.txt' in this case.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_008(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from txt file. File name and format are extracted
        from command line option -f|--file. File extension is '*.text' in this
        case.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.text', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_009(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from txt file without specifying the solution
        category. File name and format are extracted from command line option
        -f|--file. File extension is '*.text' in this case.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.text', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true', 'yaml', 'import-beats', 'import-beats-utc', 'import-kafka-utc')
    def test_cli_import_solution_010(self, snippy, mocker):
        """Import all solutions.

        Import solutions from yaml file when all but one of the solutions in
        the file is already stored. Because one solution was stored
        successfully, the return cause is OK.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            assert len(Database.get_solutions()) == 1
            cause = snippy.run(['snippy', 'import', '--solution', '--file', './all-solutions.yaml'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_011(self, snippy):
        """Import all solutions.

        Try to import empty solution template. The operation will fail because
        content templates without any modifications cannot be imported.
        """

        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.TEMPLATE))
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './solution-template.txt'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            assert not Database.get_collection()
            mock_file.assert_called_once_with('./solution-template.txt', 'r')

    def test_cli_import_solution_012(self, snippy):
        """Import all solutions.

        Try to import solution from file which file format is not supported.
        This should result error text for end user and no files should be read.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file: ./foo.bar'
            assert not Database.get_collection()
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('yaml', 'import-nginx', 'import-nginx-utc', 'isfile_true')
    def test_cli_import_solution_013(self, snippy, mocker):
        """Import solution based on message digest.

        Import defined solution based on message digest. File name is defined
        from command line as yaml file which contain one solution. One line in
        the solution data was updated.
        """

        content = Content.updated_nginx()
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '7c226ee33a088381', '-f', 'one-solution.yaml'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.yaml', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('yaml', 'import-nginx', 'import-nginx-utc', 'isfile_true')
    def test_cli_import_solution_014(self, snippy, mocker):
        """Import solution based on message digest.

        Import defined solution based on message digest without specifying the
        content category explicitly. One line in the solution data was updated.
        """

        content = Content.updated_nginx()
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '-d', '7c226ee33a088381', '-f', 'one-solution.yaml'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('one-solution.yaml', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('json', 'import-nginx', 'import-nginx-utc', 'isfile_true')
    def test_cli_import_solution_015(self, snippy, mocker):
        """Import solution based on message digest.

        Import defined solution based on message digest. File name is defined
        from command line as json file which contain one solution. One line in
        the content data was updated.
        """

        content = Content.updated_nginx()
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '7c226ee33a088381', '-f', 'one-solution.json'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.json', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('import-nginx', 'update-nginx-utc', 'isfile_true')
    def test_cli_import_solution_016(self, snippy, mocker):
        """Import solution based on message digest.

        Import defined solution based on message digest. File name is defined
        from command line as text file which contain one solution. One line
        in the content data was updated. The file extension is '*.txt' in
        this case.
        """

        content = Content.updated_nginx()
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '7c226ee33a088381', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('import-nginx', 'update-nginx-utc', 'isfile_true')
    def test_cli_import_solution_017(self, snippy, mocker):
        """Import solution based on message digest.

        Import defined solution based on message digest. File name is defined
        from command line as text file which contain one solution. One line
        in the content data was updated. The file extension is '*.text' in
        this case.
        """

        content = Content.updated_nginx()
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '7c226ee33a088381', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('import-nginx', 'update-nginx-utc', 'isfile_true')
    def test_cli_import_solution_018(self, snippy, mocker):
        """Import solution based on message digest.

        Import defined solution based on message digest. In this case the
        content category is accidentally specified as 'snippet'. This
        should still import the content in solution category.
        """

        content = Content.updated_nginx()
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--snippet', '-d', '7c226ee33a088381', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_019(self, snippy, mocker):
        """Import solution based on message digest.

        Try to import defined solution with message digest that cannot be
        found. In this case there is one solution stored.
        """

        content = Content.updated_nginx()
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '123456789abcdef0', '-f', 'one-solution.text'])
            assert cause == 'NOK: cannot find content with message digest: 123456789abcdef0'
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_not_called()
            Content.verified(mocker, snippy, {Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]})

    @pytest.mark.usefixtures('isfile_true', 'yaml')
    def test_cli_import_solution_020(self, snippy, mocker):
        """Import solution.

        Import new solution from yaml file.
        """

        content = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.yaml'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.yaml', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true', 'json')
    def test_cli_import_solution_021(self, snippy, mocker):
        """Import solution.

        Import new solution from json file.
        """

        content = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            json.load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.json'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.json', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_022(self, snippy, mocker):
        """Import solution.

        Import new solution from text file. In this case the file extension
        is '*.txt'.
        """

        content = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_023(self, snippy, mocker):
        """Import solution.

        Import new solution from text file without specifying the content
        category explicitly. In this case the file extension is '*.txt'.
        """

        content = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_024(self, snippy, mocker):
        """Import solution.

        Import new solution from text file. In this case the file extension
        is '*.text'.
        """

        content = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        mocked_open = Content.mocked_open(content)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('yaml')
    def test_cli_import_solution_025(self, snippy, mocker):
        """Import solutions defaults.

        Import solution defaults. All solutions should be imported from
        predefined file location under tool data folder from yaml format.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution', '--defaults'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('yaml', 'default-solutions', 'import-beats-utc', 'import-nginx-utc')
    def test_cli_import_solution_026(self, snippy, mocker):
        """Import solutions defaults.

        Try to import solution defaults again. The second import should fail
        with an error because the content already exist. The error text must
        be the same for all content categories. Because of random order
        dictionary in the code, the reported digest can vary when there are
        multiple failures to import each content.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--solution', '--defaults'])
            assert cause in ('NOK: content data already exist with digest: 7c226ee33a088381',
                             'NOK: content data already exist with digest: db712a82662d6932')
            assert len(Database.get_solutions()) == 2
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_027(self, snippy, mocker):
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
            'c6a215c5348a5b57': Solution.get_dictionary(template)
        }
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './solution-template.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./solution-template.txt', 'r')
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_028(self, snippy):
        """Import solutions from text template.

        Try to import solution template without any changes. This should result
        error text for end user and no files should be read. The error text must
        be the same for all content types.
        """

        template = Const.NEWLINE.join(Solution.TEMPLATE)
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '--template'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            assert not Database.get_collection()
            mock_file.assert_called_once_with('./solution-template.txt', 'r')

    @pytest.mark.usefixtures('yaml')
    def test_cli_import_solution_029(self, snippy, mocker):
        """Import all content defaults.

        Import snippet, solution and reference defaults.
        """

        content = {
            Reference.GITLOG_DIGEST: Reference.DEFAULTS[Reference.GITLOG],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX],
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]
        }
        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            yaml.safe_load.return_value = Content.imported_dict(content)
            cause = snippy.run(['snippy', 'import', '--all', '--defaults'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            assert len(Database.get_solutions()) == 1
            assert len(Database.get_references()) == 1
            defaults = []
            defaults.append(mock.call(pkg_resources.resource_filename('snippy', 'data/defaults/snippets.yaml'), 'r'))
            defaults.append(mock.call(pkg_resources.resource_filename('snippy', 'data/defaults/solutions.yaml'), 'r'))
            defaults.append(mock.call(pkg_resources.resource_filename('snippy', 'data/defaults/references.yaml'), 'r'))
            mock_file.assert_has_calls(defaults, any_order=True)
            Content.verified(mocker, snippy, content)

    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_030(self, snippy):
        """Import all solutions.

        Try to import content with option --all. This is not supported for
        import operation.
        """

        with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--all', '-f', './foo.yaml'])
            assert cause == 'NOK: import operation for content category \'all\' is supported only with default content'
            assert not Database.get_collection()
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
            assert not Database.get_collection()
            mock_file.assert_not_called()

    @pytest.mark.skip(reason="NOK: metadata cumulates in each export and import.")
    @pytest.mark.usefixtures('isfile_true')
    def test_cli_import_solution_032(self, snippy, mocker):
        """Import all solutions.

        Import all solutions from Markdown formatted file.
        """

        content = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_file(content, Content.MKDN)
        with mock.patch('snippy.content.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.md'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.md', 'r')
            Content.verified(mocker, snippy, content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
