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

"""conftest: Fixtures for pytest."""

import json

import pytest
import yaml

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.editor import Editor
from snippy.snip import Snippy
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database

# Snippet importing and get_utc_time():
#
#   1) Create empty content.
#   2) Comparing content against template calls implicitly empty content creation in Parser.
#   3) Comparing content against template calls implicitly empty content creation in Storage.
#
# Snippet creation and get_utc_time():
#
#   1) Creating empty content.
#
# Solution creation and get_utc_time():
#
#   1) Creating empty content.
#   2) Comparing against content template (create empty).
#   3) Comparing against content template (make timestamp).
#
# Editing solution and get_utc_time():
#
#   1) Creating empty content.
#   2) converting text in Editor()
#   3) Comparing against content template (create empty).
#   4) Comparing against content template (make timestamp).
#
# Snippet or solution exporting and get_utc_time():
#
#   1) Creating metadata with export timestamp.

# Snippets
REMOVE_CREATED = '2017-10-14 19:56:31'
FORCED_CREATED = '2017-10-14 19:56:31'
EXITED_CREATED = '2017-10-20 07:08:45'
NETCAT_CREATED = '2017-10-20 07:08:45'
CREATE_REMOVE = (REMOVE_CREATED,)*1
CREATE_FORCED = (FORCED_CREATED,)*1
CREATE_EXITED = (EXITED_CREATED,)*1
CREATE_NETCAT = (NETCAT_CREATED,)*1
IMPORT_REMOVE = (REMOVE_CREATED,)*3
IMPORT_FORCED = (FORCED_CREATED,)*3
IMPORT_EXITED = (EXITED_CREATED,)*3
IMPORT_NETCAT = (NETCAT_CREATED,)*3
EDITED_REMOVE = (REMOVE_CREATED,)*1

# Solutions
BEATS_CREATED = '2017-10-20 11:11:19'
NGINX_CREATED = '2017-10-20 06:16:27'
KAFKA_CREATED = '2017-10-20 06:16:27'
CREATE_BEATS = (BEATS_CREATED,)*3
CREATE_NGINX = (NGINX_CREATED,)*3
CREATE_KAFKA = (KAFKA_CREATED,)*3
IMPORT_BEATS = (BEATS_CREATED,)*5
IMPORT_NGINX = (NGINX_CREATED,)*5
IMPORT_KAFKA = (KAFKA_CREATED,)*5
EDITED_BEATS = (BEATS_CREATED,)*4

# Templates
EXPORT_TEMPLATE = '2017-10-14 19:56:31'

# Export
EXPORT_TIME = '2018-02-02 02:02:02'

IMPORT_DEFAULT_SNIPPETS = (IMPORT_REMOVE + IMPORT_FORCED)
IMPORT_DEFAULT_SOLUTIONS = (IMPORT_BEATS + IMPORT_NGINX)

# Snippy
@pytest.fixture(scope='function', name='snippy')
def mocked_snippy(mocker, request):
    """Create mocked instance from snippy."""

    params = []
    if hasattr(request, 'param'):
        params = request.param

    params.insert(0, 'snippy')  # Add the tool name here to args list.
    snippy = _create_snippy(mocker, params)
    def fin():
        """Clear the resources at the end."""

        snippy.release()
        Database.delete_storage()
    request.addfinalizer(fin)

    return snippy

@pytest.fixture(scope='function', name='server')
def server(mocker):
    """Run mocked server for testing purposes."""

    mocker.patch('snippy.server.server.SnippyServer')

@pytest.fixture(scope='function', name='caller')
def caller(mocker):
    """Mock _caller() used to mark code module and line in logs."""

    mocker.patch.object(Cause, '_caller', return_value='snippy.testing.testing:123')

## Snippets

@pytest.fixture(scope='function', name='default-snippets')
def import_default_snippets(mocker, snippy):
    """Import default snippets for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]
    _import_content(snippy, mocker, contents, IMPORT_DEFAULT_SNIPPETS)

@pytest.fixture(scope='function', name='exited')
def import_exited_snippet(mocker, snippy):
    """Import 'exited' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.EXITED]]
    _import_content(snippy, mocker, contents, IMPORT_EXITED)

@pytest.fixture(scope='function', name='remove')
def import_remove_snippet(mocker, snippy):
    """Import 'remove' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.REMOVE]]
    _import_content(snippy, mocker, contents, IMPORT_REMOVE)

@pytest.fixture(scope='function', name='remove-utc')
def create_remove_time_mock(mocker):
    """Mock timestamps to create 'remove' snippet."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_REMOVE)

@pytest.fixture(scope='function', name='import-remove-utc')
def import_remove_time_mock(mocker):
    """Mock timestamps to import 'remove' snippet."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=IMPORT_REMOVE)

@pytest.fixture(scope='function', name='edit-remove')
def edit_remove_snippet(mocker):
    """Edited 'remove' snippet."""

    template = Snippet.get_template(Snippet.DEFAULTS[Snippet.REMOVE])
    mocker.patch.object(Editor, 'call_editor', return_value=template)
    mocker.patch.object(Config, 'get_utc_time', side_effect=EDITED_REMOVE)

@pytest.fixture(scope='function', name='edited_remove')
def edited_remove(mocker):
    """Mock edited remove snippet."""

    return _editor(mocker, EDITED_REMOVE)

@pytest.fixture(scope='function', name='forced')
def import_forced_snippet(mocker, snippy):
    """Import 'forced' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.FORCED]]
    _import_content(snippy, mocker, contents, IMPORT_FORCED)

@pytest.fixture(scope='function', name='forced-utc')
def create_forced_time_mock(mocker):
    """Mock timestamps to create 'forced' snippet."""

    side_effects = ()
    try:
        side_effects = Config.get_utc_time.side_effect
    except AttributeError:
        pass
    mocker.patch.object(Config, 'get_utc_time', side_effect=tuple(side_effects) + CREATE_FORCED)

@pytest.fixture(scope='function', name='import-forced-utc')
def import_forced_time_mock(mocker):
    """Mock timestamps to import 'forced' snippet."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=IMPORT_FORCED)

@pytest.fixture(scope='function', name='exited-utc')
def create_exited_time_mock(mocker):
    """Mock timestamps to create 'exited' solution."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_EXITED)

@pytest.fixture(scope='function', name='netcat')
def import_netcat_snippet(mocker, snippy):
    """Import 'netcat' snippet for testing purposes."""

    contents = [Snippet.DEFAULTS[Snippet.NETCAT]]
    _import_content(snippy, mocker, contents, IMPORT_NETCAT)

@pytest.fixture(scope='function', name='netcat-utc')
def create_netcat_time_mock(mocker):
    """Mock timestamps to create 'netcat' snippet."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=CREATE_NETCAT)

@pytest.fixture(scope='function', name='import-netcat-utc')
def import_netcat_time_mock(mocker):
    """Mock timestamps to import 'netcat' snippet."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=IMPORT_NETCAT)

## Solutions

@pytest.fixture(scope='function', name='default-solutions')
def import_default_solutions(mocker, snippy):
    """Import default soutions for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.BEATS], Solution.DEFAULTS[Solution.NGINX]]
    _import_content(snippy, mocker, contents, IMPORT_DEFAULT_SOLUTIONS)

@pytest.fixture(scope='function', name='beats')
def import_beats_solution(mocker, snippy):
    """Import 'beats' solution for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.BEATS]]
    _import_content(snippy, mocker, contents, IMPORT_BEATS)

@pytest.fixture(scope='function', name='nginx')
def import_nginx_solution(mocker, snippy):
    """Import 'nginx' solution for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.NGINX]]
    _import_content(snippy, mocker, contents, IMPORT_NGINX)

@pytest.fixture(scope='function', name='kafka')
def import_kafka_solution(mocker, snippy):
    """Import 'kafka' solution for testing purposes."""

    contents = [Solution.DEFAULTS[Solution.KAFKA]]
    _import_content(snippy, mocker, contents, IMPORT_KAFKA)

@pytest.fixture(scope='function', name='beats-utc')
def create_beats_time_mock(mocker):
    """Mock timestamps to create 'beats' solution."""

    side_effects = ()
    try:
        side_effects = Config.get_utc_time.side_effect
    except AttributeError:
        pass
    mocker.patch.object(Config, 'get_utc_time', side_effect=tuple(side_effects) + CREATE_BEATS)

@pytest.fixture(scope='function', name='import-beats-utc')
def import_beats_time_mock(mocker):
    """Mock timestamps to import 'beats' solution."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=IMPORT_BEATS)

@pytest.fixture(scope='function', name='edit-beats')
def edit_beats_solution(mocker):
    """Edited 'beats' solution."""

    template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
    mocker.patch.object(Editor, 'call_editor', return_value=template)

    side_effects = ()
    try:
        side_effects = Config.get_utc_time.side_effect
    except AttributeError:
        pass
    mocker.patch.object(Config, 'get_utc_time', side_effect=tuple(side_effects) + EDITED_BEATS)

@pytest.fixture(scope='function', name='edited_beats')
def edited_beats(mocker):
    """Mock edited beats solution."""

    return _editor(mocker, EDITED_BEATS)


@pytest.fixture(scope='function', name='import-nginx-utc')
def import_nginx_time_mock(mocker):
    """Mock timestamps to create 'nginx' solution."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=IMPORT_NGINX)

@pytest.fixture(scope='function', name='kafka-utc')
def create_kafka_time_mock(mocker):
    """Mock timestamps to create 'kafka' solution."""

    side_effects = ()
    try:
        side_effects = Config.get_utc_time.side_effect
    except AttributeError:
        pass
    mocker.patch.object(Config, 'get_utc_time', side_effect=tuple(side_effects) + CREATE_KAFKA)

@pytest.fixture(scope='function', name='import-kafka-utc')
def import_kafka_time_mock(mocker):
    """Mock timestamps to create 'kafka' solution."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=IMPORT_KAFKA)

## Templates
@pytest.fixture(scope='function', name='template-utc')
def export_template_time_mock(mocker):
    """Mock timestamps to export solution template."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=(EXPORT_TEMPLATE,)*2)

## Content

@pytest.fixture(scope='function', name='export-time')
def export_time_mock(mocker):
    """Mock timestamps to export any content."""

    side_effects = ()
    try:
        side_effects = Config.get_utc_time.side_effect
    except AttributeError:
        pass
    mocker.patch.object(Config, 'get_utc_time', side_effect=tuple(side_effects) + (EXPORT_TIME,))

## Templates

@pytest.fixture(scope='function', name='edit-snippet-template')
def edit_snippet_template(mocker):
    """Edited default snippet template."""

    template = Const.NEWLINE.join(Snippet.TEMPLATE)
    mocker.patch.object(Editor, 'call_editor', return_value=template)

@pytest.fixture(scope='function', name='edit-solution-template')
def edit_solution_template(mocker):
    """Edited default solution template."""

    template = Const.NEWLINE.join(Solution.TEMPLATE)
    mocker.patch.object(Editor, 'call_editor', return_value=template)

@pytest.fixture(scope='function', name='edit-empty')
def edit_empty_template(mocker):
    """Edited empty template."""

    mocker.patch.object(Editor, 'call_editor', return_value=Const.EMPTY)

@pytest.fixture(scope='function', name='edit-unknown-template')
def edit_unidentified_template(mocker):
    """Edited unidentified template."""

    template = (
        '################################################################################',
        '## description',
        '################################################################################',
        '',
        '################################################################################',
        '## solutions',
        '################################################################################',
        '',
        '################################################################################',
        '## configurations',
        '################################################################################',
        '',
        '################################################################################',
        '## whiteboard',
        '################################################################################',
        ''
    )
    mocker.patch.object(Editor, 'call_editor', return_value=template)

## Yaml

@pytest.fixture(scope='function', name='yaml_load')
def yaml_load(mocker):
    """Mock importing from yaml file."""

    mocker.patch.object(yaml, 'safe_load')
    mocker_open = mocker.patch('snippy.migrate.migrate.open', mocker.mock_open(), create=True)

    return mocker_open

@pytest.fixture(scope='function', name='yaml_dump')
def yaml_dump(mocker):
    """Mock exporting to yaml file."""

    mocker.patch.object(yaml, 'safe_dump')
    mocker_open = mocker.patch('snippy.migrate.migrate.open', mocker.mock_open(), create=True)

    return mocker_open

## Json

@pytest.fixture(scope='function', name='json_load')
def json_load(mocker):
    """Mock importing from json file."""

    mocker.patch.object(json, 'load')
    mocker_open = mocker.patch('snippy.migrate.migrate.open', mocker.mock_open(), create=True)

    return mocker_open

@pytest.fixture(scope='function', name='json_dump')
def json_dump(mocker):
    """Mock exporting to json file."""

    mocker.patch.object(json, 'dump')
    mocker_open = mocker.patch('snippy.migrate.migrate.open', mocker.mock_open(), create=True)

    return mocker_open

## Devel

@pytest.fixture(scope='function', name='devel_file_list')
def devel_file_list(mocker):
    """Mock devel package file list for tests."""

    tests = [
        'test_ut_arguments_create.py',
        'test_wf_console_help.py',
        'test_wf_export_snippet.py'
    ]
    mocker.patch('snippy.devel.reference.pkg_resources.resource_isdir', return_value=True)
    mocker.patch('snippy.devel.reference.pkg_resources.resource_listdir', return_value=tests)

@pytest.fixture(scope='function', name='devel_file_data')
def devel_file_data(mocker):
    """Mock devel package file reading for tests."""

    testcase = (
        '#!/usr/bin/env python3',
        '',
        '"""test_wf_import_snippet.py: Test workflows for importing snippets."""',
        '',
        'import re',
        'import sys',
        'import copy',
        'import json',
        'import yaml',
        'import mock',
        'import pkg_resources',
        'from snippy.snip import Snippy',
        'from snippy.config.config import Config',
        'from snippy.config.constants import Constants as Const',
        'from snippy.cause import Cause',
        'from tests.testlib.snippet_helper import SnippetHelper as Snippet',
        'from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database',
        '',
        '',
        'class TestWfImportSnippet(object):',
        '    """Test workflows for importing snippets."""',
        '',
        '    @mock.patch.object(json, \'load\')',
        '    @mock.patch.object(yaml, \'safe_load\')',
        '    @mock.patch.object(Config, \'_storage_file\')',
        '    @mock.patch(\'snippy.migrate.migrate.os.path.isfile\')',
        '    def test_import_all_snippets(self, mock_isfile, mock_storage_file, mock_yaml_load, mock_json_load):',
        '        """Import all snippets."""',
        '',
        '        mock_isfile.return_value = True',
        '        mock_storage_file.return_value = Database.get_storage()',
        '        import_dict = {\'content\': [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.NETCAT]]}',
        '        mock_yaml_load.return_value = import_dict',
        '        mock_json_load.return_value = import_dict',
        '        compare_content = {\'54e41e9b52a02b63\': import_dict[\'content\'][0],',
        '                           \'f3fd167c64b6f97e\': import_dict[\'content\'][1]}',
        '',
        '        ## Brief: Import all snippets. File name is not defined in commmand line. This should',
        '        ##        result tool internal default file name ./snippets.yaml being used by default.',
        '        with mock.patch(\'snippy.migrate.migrate.open\', mock.mock_open(), create=True) as mock_file:',
        '            snippy = Snippy()',
        '            cause = snippy.run_cli([\'snippy\', \'import\', \'--filter\', \'.*(\\$\\s.*)\'])  ## workflow',
        '            assert cause == Cause.ALL_OK',
        '            assert len(Database.get_snippets()) == 2',
        '            mock_file.assert_called_once_with(\'./snippets.yaml\', \'r\')',
        '            Snippet.test_content(snippy, mock_file, compare_content)',
        '            snippy.release()',
        '            snippy = None',
        '            Database.delete_storage()'
    )
    mocked_open = mocker.mock_open(read_data=Const.NEWLINE.join(testcase))
    mocker.patch('snippy.devel.reference.open', mocked_open, create=True)

@pytest.fixture(scope='function', name='devel_no_tests')
def devel_no_tests(mocker):
    """Mock tests package missing exception."""

    tests = [
        'test_ut_arguments_create.py',
        'test_wf_console_help.py',
        'test_wf_export_snippet.py'
    ]
    # The exception in Python 3.6 is ModuleNotFoundError but this is not
    # available in earlier Python versions. The used ImportError is a parent
    # class of ModuleNotFoundError and it works with older Python versions.
    mocker.patch('snippy.devel.reference.pkg_resources.resource_isdir', side_effect=[ImportError("No module named 'tests'"), mocker.DEFAULT])
    mocker.patch('snippy.devel.reference.pkg_resources.resource_listdir', return_value=tests)
    mocked_open = mocker.mock_open(read_data=Const.EMPTY)
    mocker.patch('snippy.devel.reference.open', mocked_open, create=True)

## Helpers

def _create_snippy(mocker, options):
    """Create snippy with mocks."""

    mocker.patch.object(Config, '_storage_file', return_value=Database.get_storage())
    mocker.patch('snippy.migrate.migrate.os.path.isfile', return_value=True)
    snippy = Snippy(options)

    return snippy

def _import_content(snippy, mocker, contents, timestamps):
    """Import requested content."""

    mocker.patch.object(Config, 'get_utc_time', side_effect=timestamps)
    start = len(Database.get_contents()) + 1
    for idx, content in enumerate(contents, start=start):
        mocked_open = mocker.mock_open(read_data=Snippet.get_template(content))
        mocker.patch('snippy.migrate.migrate.open', mocked_open, create=True)
        cause = snippy.run_cli(['snippy', 'import', '-f', 'content.txt'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_contents()) == idx

def _editor(mocker, timestamp):
    """Mock editor."""

    editor = mocker.patch.object(Editor, 'call_editor')

    side_effects = ()
    try:
        side_effects = Config.get_utc_time.side_effect
    except AttributeError:
        pass
    mocker.patch.object(Config, 'get_utc_time', side_effect=tuple(side_effects) + timestamp*3)

    return editor
