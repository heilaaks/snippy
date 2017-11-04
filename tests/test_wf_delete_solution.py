#!/usr/bin/env python3

"""test_wf_delete_solution.py: Test workflows for deleting solutions."""

import sys
import unittest
import mock
from snippy.snip import Snippy
from snippy.config.constants import Constants as Const
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfDeleteSolution(unittest.TestCase):
    """Test workflows for deleting solutions."""

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_delete_solution_with_digest(self, mock_isfile, mock_get_db_location):
        """Delete solution with digest."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Delete solution with short 16 byte version of message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--solution', '-d', '61a24a156f5e9d2d']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Delete solution with wihtout explicitly specifying solution category..
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '-d', '61a24a156f5e9d2d']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Delete solution with very short version of digest that matches to one solution.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--solution', '-d', '61a24']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Delete solution with long 16 byte version of message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--solution', '-d', '61a24a156f5e9d2d448915eb68ce44b383c8c00e8deadbf27050c6f18cd86afe']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete solution with message digest that cannot be found.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--solution', '-d', '123456789abcdef0']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
            assert len(Database.get_solutions()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete solution with empty message digest. Nothing should be deleted
        ##        in this case because there is more than one content stored.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--solution', '-d', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot use empty message digest to delete content'
            assert len(Database.get_solutions()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Delete solution with empty message digest when there is only one content
        ##        stored. In this case the last content can be deleted with empty digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_one(Snippy(), Solution.NGINX)
            sys.argv = ['snippy', 'delete', '--solution', '-d', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert not Database.get_solutions()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete solution with short version of digest that does not match
        ##        to any existing message digest.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--solution', '-d', '123456']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with message digest 123456'
            assert len(Database.get_solutions()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_delete_solution_with_data(self, mock_isfile, mock_get_db_location):
        """Delete solution with data."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Delete solution based on content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            data = Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[Solution.NGINX])
            sys.argv = ['snippy', 'delete', '--solution', '--content', data]  ## workflow
            cause = snippy.run_cli()
            assert cause == 'OK'
            assert len(Database.get_solutions()) == 1
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete solution with content data that does not exist. In this case the
        ##        content data is not truncated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--solution', '--content', 'not-exists']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with content data \'not-exists\''
            assert len(Database.get_solutions()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete solution with content data that does not exist. In this case the
        ##        content data is truncated.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            data = Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[Solution.KAFKA])
            sys.argv = ['snippy', 'delete', '--solution', '--content', data]  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot find content with content data \'##############################...\''
            assert len(Database.get_solutions()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to delete solution with empty content data. Nothing should be deleted
        ##        in this case because there is more than one content left.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True):
            snippy = Solution.add_defaults(Snippy())
            sys.argv = ['snippy', 'delete', '--solution', '--content', '']  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: cannot use empty content data to delete content'
            assert len(Database.get_solutions()) == 2
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
