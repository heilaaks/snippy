#!/usr/bin/env python3

"""test_wf_create_new_snippet.py: Test workflows for creating new snippets."""

import os
import sys
import mock
from snippy.storage import Storage
from snippy.snippet import Snippet
from snippy.config import Config
from tests.testlib.snippet_helper import SnippetHelper
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper


class TestWorkflowCreateNewSnippet(object): # pylint: skip-file
    """Test workflows for creating new snippets."""

    @mock.patch.object(Config, 'is_storage_in_memory')
    @mock.patch.object(Config, 'get_storage_schema')
    def test_creating_new_snippet_from_command_line(self, mock_get_storage_schema, mock_is_storage_in_memory):
        """Create snippet from command line with all parameters.

        Workflow:
            @ creating snippet
        Execution:
            $ python snip.py create --content 'docker rm -v $(docker ps -a -q)' --brief 'Remove all docker containers' --group 'docker' --tags docker,container,cleanup --links 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
        Expected results:
            1 Long versions from command line options work.
            2 One entry is read from storage.
            3 Content, brief, group, tags and links are read correctly.
            4 Tags are presented in a list and they are sorted.
            5 Links are presented in a list.
            6 Message digest is constantly same.
        """

        mock_is_storage_in_memory.return_value = True
        mock_get_storage_schema.return_value = 'snippy/storage/database/database.sql'

        snippet = SnippetHelper().get_snippet(SnippetHelper.SNIPPET_1)
        sys.argv = ['snippy', 'create', '-c', snippet['content']]
        #config = Config()
        #storage = Storage().init()
        #Snippet(storage).run()
        #rows = storage.search(None, None, snippet['content'])
        #rows = Sqlite3DbHelper().select_all_snippets()
        #print("rows %s" % rows)
        
        
        #obj = Snippy().run()

        #args = ('python snip.py create --content \'%s\'' % (snippet['content']))
        #print("args %s" % args)
        
        #result = os.system(args)
        #print("result %s" % result)
        #assert 0
