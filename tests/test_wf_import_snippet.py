#!/usr/bin/env python3

"""test_wf_import_snippet.py: Test workflows for importing snippets."""

import re
import sys
import copy
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
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfImportSnippet(unittest.TestCase):
    """Test workflows for importing snippets."""

    @mock.patch.object(json, 'load')
    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_all_snippets(self, mock_isfile, mock_storage_file, mock_yaml_load, mock_json_load):
        """Import all snippets."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()
        import_dict = {'content': [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.NETCAT]]}
        mock_yaml_load.return_value = import_dict
        mock_json_load.return_value = import_dict
        compare_content = {'54e41e9b52a02b63': import_dict['content'][0],
                           'f3fd167c64b6f97e': import_dict['content'][1]}

        ## Brief: Import all snippets. File name is not defined in commmand line. This should
        ##        result tool internal default file name ./snippets.yaml being used by default.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./snippets.yaml', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all snippets from yaml file. File name and format are extracted from
        ##        command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.yaml']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./all-snippets.yaml', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all snippets from json file. File name and format are extracted from
        ##        command line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.json']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./all-snippets.json', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all snippets from txt file. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.txt' in this case.
        mocked_open = mock.mock_open(read_data=Snippet.get_template(import_dict['content'][0]) +
                                     Const.NEWLINE +
                                     Snippet.get_template(import_dict['content'][1]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.txt']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./all-snippets.txt', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import all snippets from text file. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.text' in this case.
        mocked_open = mock.mock_open(read_data=Snippet.get_template(import_dict['content'][0]) +
                                     Const.NEWLINE +
                                     Snippet.get_template(import_dict['content'][1]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.text']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            mock_file.assert_called_once_with('./all-snippets.text', 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import snippet from file which file format is not supported. This
        ##        should result error text for end user and no files should be read.
        mocked_open = mock.mock_open(read_data=Snippet.get_template(import_dict['content'][0]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './foo.bar']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            assert not Database.get_contents()
            mock_file.assert_not_called()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import snippet from file that is not existing. The file extension
        ##        is one of supported formats..
        mocked_open = mock.mock_open(read_data=Snippet.get_template(import_dict['content'][0]))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            # The last call for mock_isfile is unnecessary. It is here because of Python2 way of
            # iteration that seems to require one element after the last call. This is not the
            # case with Python3.
            mock_isfile.side_effect = [True, False, None]
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './foo.yaml']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot read file ./foo.yaml'
            assert not Database.get_contents()
            mock_file.assert_not_called()
            mock_isfile.side_effect = None
            mock_isfile.return_value = True
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import snippet from text file that is empty.
        mocked_open = mock.mock_open(read_data=Const.EMPTY)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '-f', './all-snippets.txt']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: could not identify text template content category'
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./all-snippets.txt', 'r')
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(json, 'load')
    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_defined_snippet(self, mock_isfile, mock_storage_file, mock_yaml_load, mock_json_load):
        """Import defined snippet."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [copy.deepcopy(Snippet.DEFAULTS[Snippet.REMOVE])]}
        import_dict_orig = copy.deepcopy(import_dict)
        import_text = Snippet.get_template(import_dict['content'][0]) + Const.NEWLINE
        mock_yaml_load.return_value = import_dict
        mock_json_load.return_value = import_dict

        ## Brief: Import defined snippet based on message digest. File name is defined from command line as
        ##        yaml file which contain one snippet. Content was not updated in this case.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            mock_yaml_load.return_value = import_dict
            snippy = Snippet.add_one(Snippy(), Snippet.REMOVE)
            sys.argv = ['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.yaml']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            mock_file.assert_called_once_with('one-snippet.yaml', 'r')
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': import_dict['content'][0]})
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined snippet based on message digest. File name is defined from command line as
        ##        yaml file which contain one snippet. Content tags were updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            import_dict['content'][0]['tags'] = ('new', 'tags', 'set')
            mock_yaml_load.return_value = import_dict
            snippy = Snippet.add_one(Snippy(), Snippet.REMOVE)
            sys.argv = ['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.yaml']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            mock_file.assert_called_once_with('one-snippet.yaml', 'r')
            Snippet.test_content(snippy, mock_file, {'4525613eaecd5297': import_dict['content'][0]})
            import_dict = copy.deepcopy(import_dict_orig)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined snippet based on message digest. File name is defined from command line as
        ##        json file which contain one snippet. Content brief were updated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            import_dict['content'][0]['brief'] = 'Updated brief description'
            mock_json_load.return_value = import_dict
            snippy = Snippet.add_one(Snippy(), Snippet.REMOVE)
            sys.argv = ['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.json']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            mock_file.assert_called_once_with('one-snippet.json', 'r')
            Snippet.test_content(snippy, mock_file, {'f07547e7c692741a': import_dict['content'][0]})
            import_dict = copy.deepcopy(import_dict_orig)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined snippet based on message digest. File name is defined from command line as
        ##        text file which contain one snippet. Content links were updated. The file extenansion is
        ##        '*.txt' in this case.
        import_text = re.sub(r'https://docs.*', 'https://new.link', import_text)
        mocked_open = mock.mock_open(read_data=import_text)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            import_dict['content'][0]['links'] = ('https://new.link', )
            snippy = Snippet.add_one(Snippy(), Snippet.REMOVE)
            sys.argv = ['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.txt']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            mock_file.assert_called_once_with('one-snippet.txt', 'r')
            Snippet.test_content(snippy, mock_file, {'7681559ca5c001e2': import_dict['content'][0]})
            import_dict = copy.deepcopy(import_dict_orig)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Import defined snippet based on message digest. File name is defined from command line as
        ##        text file which contain one snippet. Content links were updated. The file extenansion is
        ##        '*.text' in this case.
        import_text = re.sub(r'https://docs.*', 'https://new.link', import_text)
        mocked_open = mock.mock_open(read_data=import_text)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            import_dict['content'][0]['links'] = ('https://new.link', )
            snippy = Snippet.add_one(Snippy(), Snippet.REMOVE)
            sys.argv = ['snippy', 'import', '-d', '54e41e9b52a02b63', '-f', 'one-snippet.text']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 1
            mock_file.assert_called_once_with('one-snippet.text', 'r')
            Snippet.test_content(snippy, mock_file, {'7681559ca5c001e2': import_dict['content'][0]})
            import_dict = copy.deepcopy(import_dict_orig)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import defined snippet with message digest that cannot be found. In this
        ##        case there is one snippet stored.
        mocked_open = mock.mock_open(read_data=import_text)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippet.add_one(Snippy(), Snippet.REMOVE)
            sys.argv = ['snippy', 'import', '-d', '123456789abcdef0', '-f', 'one-snippet.text']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find snippet identified with digest 123456789abcdef0'
            assert len(Database.get_snippets()) == 1
            mock_file.assert_not_called()
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': import_dict['content'][0]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_snippet_defaults(self, mock_isfile, mock_storage_file, mock_yaml_load):
        """Import snippet defaults."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]}
        mock_yaml_load.return_value = import_dict
        compare_content = {'54e41e9b52a02b63': import_dict['content'][0],
                           '53908d68425c61dc': import_dict['content'][1]}

        ## Brief: Import snippet defaults. All snippets should be imported from predefined file
        ##        location under tool data folder from yaml format.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--defaults']  ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_snippets()) == 2
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/default/snippets.yaml')
            mock_file.assert_called_once_with(defaults_snippets, 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to import snippet defaults again. The second import should fail with an error
        ##        because the content already exist.  The error text must be the same for all content
        ##        categories.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'import', '--defaults']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: no content was inserted because content data already existed'
            assert len(Database.get_snippets()) == 2
            defaults_snippets = pkg_resources.resource_filename('snippy', 'data/default/snippets.yaml')
            mock_file.assert_called_once_with(defaults_snippets, 'r')
            Snippet.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_snippet_template(self, mock_isfile, mock_storage_file):
        """Import snippets from text template."""

        mock_storage_file.return_value = Database.get_storage()
        mock_isfile.return_value = True
        template = Const.NEWLINE.join(Snippet.TEMPLATE)

        ## Brief: Try to import snippet template without any changes. This should result error
        ##        text for end user and no files should be read. The error text must be the same
        ##        for all content types.
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            snippy = Snippy()
            sys.argv = ['snippy', 'import', '--template']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: content was stored because it matched to empty template'
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./snippet-template.txt', 'r')
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_existing_snippets(self, mock_isfile, mock_storage_file, mock_yaml_load):
        """Import snippets already existing."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()
        import_dict = {'content': [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.NETCAT]]}
        mock_yaml_load.return_value = import_dict

        ## Brief: Import snippets from yaml file that is defined from command line. In this case
        ##        one of the two snippets is already existing. Because the content existing is
        ##        not considered as an error and another snippet is imported successfully, the
        ##        result cause is OK.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippet.add_defaults(Snippy())
            sys.argv = ['snippy', 'import', '-f', './snippets.yaml']   ## workflow
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./snippets.yaml', 'r')
            assert len(Database.get_contents()) == 3
            Snippet.test_content(snippy, mock_file, {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE],
                                                     '53908d68425c61dc': Snippet.DEFAULTS[Snippet.FORCED],
                                                     'f3fd167c64b6f97e': Snippet.DEFAULTS[Snippet.NETCAT]})
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
