#!/usr/bin/env python3

"""test_wf_import_solution.py: Test workflows for importing solutions."""

import sys
import unittest
import json
import yaml
import mock
import pkg_resources
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.content.content import Content
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfImportSolution(unittest.TestCase):
    """Test workflows for importing solutions."""

    @mock.patch.object(json, 'load')
    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_all_solutions(self, mock_isfile, mock_get_db_location, mock_yaml_load, mock_json_load):
        """Import all solutions."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [{'data': tuple(Solution.SOLUTIONS_TEXT[0]),
                                    'brief': 'Debugging Elastic Beats',
                                    'group': 'beats',
                                    'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                                    'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-elastic-beats.txt',
                                    'utc': None,
                                    'digest': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'},
                                   {'data': tuple(Solution.SOLUTIONS_TEXT[2]),
                                    'brief': 'Testing docker log drivers',
                                    'group': 'docker',
                                    'tags': ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin'),
                                    'links': ('https://github.com/MickayG/moby-kafka-logdriver',
                                              'https://github.com/garo/logs2kafka',
                                              'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'),
                                    'category': 'solution',
                                    'filename': 'kubernetes-docker-log-driver-kafka.txt',
                                    'utc': '2017-10-12 11:53:17',
                                    'digest': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57'}]}
        mock_yaml_load.return_value = import_dict
        mock_json_load.return_value = import_dict
        compare_content = {'a96accc25dd23ac0': Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[Solution.BEATS]),
                           'eeef5ca3ec9cd364': Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[Solution.KAFKA])}

        ## Brief: Import all solutions. File name is not defined in commmand line. This should
        ##        result tool internal default file name ./solutions.yaml being used by default.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--solution']  ## workflow
            cause = snippy.run_cli()
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
            sys.argv = ['snippy', 'import', '--solution', '-f', './all-solutions.yaml']  ## workflow
            cause = snippy.run_cli()
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
            sys.argv = ['snippy', 'import', '-f', './all-solutions.yaml']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.yaml', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from json file. File name and format are extracted from
        ##        command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--solution', '-f', './all-solutions.json']  ## workflow
            cause = snippy.run_cli()
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
            sys.argv = ['snippy', 'import', '-f', './all-solutions.json']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.json', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from txt file. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.txt' in this case.
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0]) +
                                     Const.NEWLINE+Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--solution', '-f', './all-solutions.txt']  ## workflow
            cause = snippy.run_cli()
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
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0]) +
                                     Const.NEWLINE+Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-solutions.txt']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all solutions from txt file. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.text' in this case.
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0]) +
                                     Const.NEWLINE +
                                     Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--solution', '-f', './all-solutions.text']  ## workflow
            cause = snippy.run_cli()
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
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[0]) +
                                     Const.NEWLINE +
                                     Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-solutions.text']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.text', 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import empty solution template. The operation will fail because
        ##        content templates without any modifications cannot be imported.
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.TEMPLATE))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--solution', '-f', './solution-template.txt']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: content data is not valid - content template cannot be inserted'
            assert not Database.get_contents()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import solution from file which file format is not supported. This
        ##        should result error text for end user and no files should be read.
        mocked_open = mock.mock_open(read_data=Solution.SOLUTIONS_TEXT[0])
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--solution', '-f', './foo.bar']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            assert not Database.get_contents()
            mock_file.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(json, 'load')
    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_defined_solution(self, mock_isfile, mock_get_db_location, mock_yaml_load, mock_json_load):
        """Import defined solution."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        updated_solution = Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[Solution.NGINX])
        updated_solution = updated_solution.replace('# Instructions how to debug nginx', '# Changed instruction set')
        import_dict = {'content': [{'data': tuple(updated_solution.split(Const.NEWLINE)),
                                    'brief': 'Debugging nginx',
                                    'group': 'nginx',
                                    'tags': ('nginx', 'debug', 'logging', 'howto'),
                                    'links': ('https://www.nginx.com/resources/admin-guide/debug/',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-nginx.txt',
                                    'utc': None,
                                    'digest': '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe'}]}
        mock_yaml_load.return_value = import_dict
        mock_json_load.return_value = import_dict

        ## Brief: Import defined solution based on message digest. File name is defined from command line as
        ##        yaml file which contain one solution. One line in the content data was updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            sys.argv = ['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.yaml']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.yaml', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': updated_solution})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined solution based on message digest. File name is defined from command line as
        ##        json file which contain one solution. One line in the content data was updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            sys.argv = ['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.json']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.json', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': updated_solution})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined solution based on message digest. File name is defined from command line as
        ##        text file which contain one solution. One line in the content data was updated. The file
        ##        extension is '*.txt' in this case.
        mocked_open = mock.mock_open(read_data=updated_solution)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            sys.argv = ['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.txt']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': updated_solution})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined solution based on message digest. File name is defined from command line as
        ##        text file which contain one solution. One line in the content data was updated. The file
        ##        extension is '*.text' in this case.
        mocked_open = mock.mock_open(read_data=updated_solution)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            sys.argv = ['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.text']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Solution.test_content(snippy, mock_file, {'8eb8eaa15d745af3': updated_solution})
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_solution_defaults(self, mock_isfile, mock_get_db_location, mock_yaml_load):
        """Import solutions defaults."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [{'data': tuple(Solution.SOLUTIONS_TEXT[0]),
                                    'brief': 'Debugging Elastic Beats',
                                    'group': 'beats',
                                    'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                                    'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-elastic-beats.txt',
                                    'utc': None,
                                    'digest': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'},
                                   {'data': tuple(Solution.SOLUTIONS_TEXT[2]),
                                    'brief': 'Testing docker log drivers',
                                    'group': 'docker',
                                    'tags': ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin'),
                                    'links': ('https://github.com/MickayG/moby-kafka-logdriver',
                                              'https://github.com/garo/logs2kafka',
                                              'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'),
                                    'category': 'solution',
                                    'filename': 'kubernetes-docker-log-driver-kafka.txt',
                                    'utc': '2017-10-12 11:53:17',
                                    'digest': 'eeef5ca3ec9cd364cb7cb0fa085dad92363b5a2ec3569ee7d2257ab5d4884a57'}]}
        mock_yaml_load.return_value = import_dict
        compare_content = {'a96accc25dd23ac0': Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[Solution.BEATS]),
                           'eeef5ca3ec9cd364': Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[Solution.KAFKA])}

        ## Brief: Import solution defaults. All solutions should be imported from predefined file
        ##        location under tool data folder from yaml format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--solution', '--defaults']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            defaults_solutions = pkg_resources.resource_filename('snippy', 'data/default/solutions.yaml')
            mock_file.assert_called_once_with(defaults_solutions, 'r')
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_solution_template(self, mock_isfile, mock_get_db_location):
        """Import solution from template without changing the header."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        template = Const.NEWLINE.join(Solution.TEMPLATE)
        template = template.replace('## description', '## description changed')
        content = Content((tuple(template.split(Const.NEWLINE)),
                           Const.EMPTY,
                           'default',
                           (Const.EMPTY,),
                           (Const.EMPTY,),
                           Const.SOLUTION,
                           Const.EMPTY,
                           None,
                           '63f2007703d70c8f211c1eed7b0b388977e02f7861f208494066e53c7311b5b7',
                           None,
                           1))

        ## Brief: Import solution template that does not have any changes to file header.
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './solution-template.txt']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_contents()) == 1
            mock_file.assert_called_once_with('./solution-template.txt', 'r')
            Snippet().compare(self, snippy.storage.search(Const.SOLUTION, digest='63f2007703d70c8f')[0], content)
            Solution.test_content(snippy, mock_file, {'63f2007703d70c8f': template})
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
