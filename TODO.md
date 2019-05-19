## WORKING
   - [ ] Fix updating content without updates changes the updated timestamp. There is no need to store the content either.
   - [ ] Fix JSON API v1.x requires links for collection responses too. Individual resource not found or attrbute results null otherwise empty list.
   - [ ] Design and change /groups and /tags to GET groups and tags not content. Like unique tags and groups.
   - [ ] Add possibility to import from other external sources that contain cheat sheet data or snippets in structured format. Try tldr. External tool? No more dependencies would be nice.
   - [ ] Add support to find dead links. External tool? No more dependencies would be nice.
   - [ ] Fix HTTP response 201 Created in case the second resource is failing. If any of the resources fails, the HTTP request must be rejected. This applies only to empty data because that is checked after the REST API validation. See test_api_create_snippet_025
   - [ ] Fix test_logger_017. The P3 is not correct? The links in p2 are in the same elemnet separated with \n that should be the case with P3.
   - [ ] Add --help server to list server specific commands and log parameters. Maybe add --help debug/troubleshoot? Debug better because it is shorter?
   - [ ] Incorrect header does not leave logs. Test manually since this works differently that the tests? For example ab was missing '-T application/vnd.api+json' without this it did not work.
   - [ ] Make docker tests run parallel. Now the container removal is based on image name that is not good. must be based on container hash.
   - [ ] Make more tests for Docker use cases
   - [ ] Empty array values can unambiguously be represented as the empty list, []. // https://opensource.zalando.com/restful-api-guidelines/#218
   - [ ] Swagger 3.0: Why the 'additionProperties: false' field did not affect swagger 3.0?
   - [ ] Swagger 2.0: Does not support nullable and this does not work with validation: test_api_update_reference_010/117. move to OAS3.0 to solve this?
   - [ ] Check why test_api_create_snippet_004 has specific error length in Python 3.4.
   - [ ] Config.get_resource creates external UUID usage when e.g resource is updated. Get rid of this (somehow) after UUID refactoring.
   - [ ] Test export/import Mkdn snippet with partial comments. The export must have the <not documented> tag and import must remove it.
   - [ ] Fix somehow (?) the python runner search --sall 'test' --filter test -vv | grep --all?
   - [ ] Config get_resource could return empty Resource instead of None in failure. This is now related to new migrate refactoring that prevents migrating template resources.
   - [ ] Fix server silent startup failure if for example the port is reserved. How to get proper error cause for user? There are logs but not with default?
   - [ ] Test postgreSQL SSL connection manually.
   - [ ] Fix (?) updating JSON or YAML solution (only solution?) with mkdn or text data where data brief changes. This is not now updated in case of YAML/JSON solution because the dict is just read. The problem is to how to identify text or Markdown from YAML/JSON (dict)?
   - [ ] Parse new format that supports snippets with leading comment to internal format? Or remove the support? This was the case where snippet was started with # comment followed by $ snippet
   - [ ] Database.init can be moved to database __init__ because it is always called immediately after object init. This is likely historical left over or something that some test requires (mock?)?
   - [ ] It seems that that sqlite3 (and perhaps psycopg2) automatically rollbacks or commits with context manager (with block). So the explicit commit and rollback may (?) be unnecessary? It may better to leave those since working with different databases? Document in code?
   - [ ] Change name of --scat to --cat?
   - [ ] Why container --server-host command line option does not work for healthcheck? docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --log-json -vv. Because hc is triggered as separate process and it is not possible to get the command line value. --> document.
   - [ ] Remove test case files from container.

## THINKING
   - [ ] Add TODO content.
   - [ ] Add code content.
   - [ ] Add health API to send server health with statistics.
   - [ ] Add UT tests for class Debug() methods.
   - [ ] Fix Parser which assumes always UTF-8. If CLI terminal has something else, this fails.
   - [ ] Fix does the Parser really return UTF-8 encoded strings always? For example (links/keywords) is not coverted and other use decode(utf-8) which is opposite?
   - [ ] Fix (remove) the LANG in Alpine based dockerfile? Is this useless as MUSL does not support locales? https://github.com/gliderlabs/docker-alpine/issues/144
   - [ ] Fix digest computation once things are setling down. Changing this forces changes to all tests and code that rely on digest.
   - [ ] Add Debug() for all classes. Add debug() for snippy that calls all the debugs that Snippy imports.

## OPTIMIZATIONS
   - [ ] Fix (optimize) PyPy is 2x faster with HTTP than CPython but PyPy is 10% slower than CPython with HTTPS. Is there a problem with HTTPS certs in Snippy?
   - [ ] Fix (optimize) Import all and the storage reads and returns all imported data that is not actually used in any way.
   - [ ] Fix (optimize) migrate and dump. The dump_dict is not needed in case of text and mkdn because those methods do not need the dict format but produce string directly.
   - [x] Fix (optimize) digest computation for Resource.
   - [ ] Fix (optimize) POST API with multiple contents. Now each content in collection is *.run with own resources. The create supports collection so this should work. This is hard due to how Api/Cli is made. Maybe not worth of it.
   - [ ] Fix (optimize) the order of SQL columns. Fixed length columns first. This should ? allow database to optimize the length of data. Is this the case? Now the order is "logical". Maybe unnecessary optimization. Measure first.
   - [ ] Fix (optimize) the Mkdn and Text parsing. The parsers and Resource() do the input data formatting. Parsers when data read and Resource() when set. This is good now to avoid data format problems.
   - [ ] Fix (optimize) Why GET with limit=20 is much slower than limit=1? Even POST with one resource is much faster than GET with limit=20 (Sqlite in tests). The test produced 409 from trying to POST the same content in loop.

## RELEASING
   - [ ] Automate PostgreSQL startup.
   - [ ] Remove possibly running snippy container before testing. This will fail the test which will remove the container anyways.
   - [ ] Snippy asciinema semi faked prompt fails with rest api responses. The prompt is in the same line as the last curly bracket from rest api response.

## PACKAGING
   - [ ] Change Pytest, Pylint, Flake8, Pyflake and Bandit to use pyproject when the support comes. This merges the configuration files to one place.
   - [ ] Add delete for wheel build directory for automation. If the folder exist this is a problem (at least used to be) see how to fail python release/building/something.

## FEATURES
   - [ ] Add CORS https://stackoverflow.com/a/45183343. This is needed to make the server usable at all?
   - [ ] Add decsription, name, versions and source to CLI? Or does this make the CLI too bloated? These can be updated via editor or REST API.
   - [ ] Add support for CockroachDB.
   - [ ] Add support to store any content in YAML files when server starts. Give path to folder that contains yaml files and import all?
   - [ ] Add combine on top of migrate and merge. The combine would allow adding for example a tag to an existing list of tags. This would be nice for CLI and could be used with RFC 6902 (JSON Patch) (if implemented).
   - [ ] Add support to search phrases like has 'active end'. This should return one result with default set but it returns two since each word is searched separately.
   - [ ] Add test client to measure performance of the server.
   - [ ] Add user management with a new user table that lins to contents table.
   - [ ] Add limit to multilevel sort fields to two fields to avoid complex scenarios.
   - [ ] Add limits to all parameters: column array size, sort array size, etc.
   - [ ] Add support to print only selected fields, like brief and digest for CLI text output. Hard to generalize since layout e.g. contains header with three fields.
   - [ ] Add statistics object which tracks peak and percentile latencies with memory and CPU usage.
   - [ ] Add support for REST API YAML responses --> YAML likely not needed. JSON It is that rules.
   - [ ] How to add custom Falcon error codes? Now e.g. 500 is HTML string and it is different than normal Snippy server error code.
   - [ ] How to add custom Falcon exception handling through snippy logger?

## SECURITY
   - [ ] Remove server name and version from HTTP responses. This would require overriding Gunicorn https://stackoverflow.com/a/21294524.

## FIX
   - [ ] Check good rules from https://opensource.zalando.com/restful-api-guidelines/#218
   - [ ] Refactor rest.generate that now updates also headers. Body, content type and status are set in the main level but header are set in Generate which may be confusing.
   - [ ] Fix reading data from cli that does not parse description and filename from CLI --content data test_cli_create_solution_001.
   - [ ] Fix why new mkdn log driver kafka solution does not have description in quotations in defaults?  This is normal YAML behaviour?
   - [ ] Fix timestamp usage to be Datetime native? Now the created and updated times are strings. It may be usefull in future (no use case now) to have Datetime objects instead of strings.
   - [ ] Fix the internal primary key UUID. It has MAC address which is same for multiple containers? //https://docs.docker.com/engine/reference/run/#network-settings
   - [ ] Fix long description in Markdown format does not support keeping paragraph. The description supports only one paragraph that is wrapped for Markdown. Fix or ok? Read only one paragrap. This is good for example for solution which may have longer Description chapter as own header.
   - [ ] Fix Fields class. It may not have to be inherited like now. The operation ID refresh and logs are problematic now because the Fields logs would refresh OID to be different than with the base class logs. How?
   - [ ] Fix (by using OAS3.0?) swagger yaml since it uses 3.0. Componentst and etc should be under defintions // https://stackoverflow.com/questions/47293855/swagger-schema-error-should-not-have-additional-properties
   - [ ] Fix it seems that python can do like Config.parameternewparameter which adds new parameter in case of typo. Can this be prevented?
   - [ ] Fix test cases hiding that cls.source was _not_ set in init when the Config.init called storage method that used cls.source. How this can be not noticed?
   - [ ] Fix print resource it does not print data in debug part because it is empty tuple.
   - [ ] Fix failure to process request like SSL error does not refresh OID. Is there a hook for this?
   - [ ] Fix few failing tests like api perf test in Docker Trusty. Reason unknown. See 'WSGIWarning: Unknown REQUEST_METHOD: 'PATCH''.
   - [ ] Fix 'WSGIWarning: Unknown REQUEST_METHOD: 'PATCH'' It seems Python 2.7 does not support PATCH somewhere? This is coming in docker snippy/python34-trusty when running tests.
   - [ ] Fix schema check in case of error that returns different lenght result depending on Python version? Maybe ok. Maybe not fix. Just to remind.
   - [ ] Fix terminal encodings other than utf-8. Something like this may be needed https://stackoverflow.com/a/33812744.
   - [ ] Fix the Generate() does not need 'json.loads('{"links": {"self": "' + uri + '"}, "data": null}'))' because code is not called with emty collection.
   - [ ] Fix error string that complains about snippet content matching to empty template when the data is empty. See test_api_create_snippet_017.
   - [ ] Fix test reference to match to main(['snippy', 'search', '--sall', '.', '--profile']) and new document stuff
   - [ ] Fix updating cls.server = cls.source.server does not make sense after start. But this was propably fix to some other problem.
   - [ ] Fix insert_content and digest check is probably unnecessary. Remove it after content refactor.
   - [ ] Fix all post responses to have link to created resource. Why this is not always included? Only in updates but not in create?
   - [ ] Fix failing tests print the help. Something was broken. This applies only (rare?) some cases? This comes from UT sqlite cases at least.
   - [ ] Fix help tests since it is not reading new _cli_ tests. What I was thinking?
   - [ ] Fix make test if pytest cover leaves hanging files like .coverage.localhost.localdomain.4727.176219. Add --cover-erase in commmand? // https://bitbucket.org/ned/coveragepy/issues/476/coverageexception-cant-add-arcs-to
   - [ ] Fix when server parameters are erronous, error text from argparse is misleading since it complains about the content operations. Custom errors for --server-host?
   - [ ] Fix OpenAPI specs. The ResponseData and the attributes contain mandatory 'dhttps://stackoverflow.com/a/33812744ata' field. This is not true if resouce field like brief is requirested.
   - [ ] Fix export the original which contains additional whitespace before the exported template in the DATE field. Was this some test?
   - [ ] Fix indention in snippy: error: argument   {create,search,update,delete,export,import}. This indention is actually "must" in --help
   - [ ] Fix the REST API self link is not always present. It is set only in case of resources and if the digest field is not dropped from response.
   - [ ] Fix if the sys._getframe migth not exist in all Python implementations. Rerring to CPython. There is small performance advance using this. Fix?
   - [ ] Fix the example string from travifor templates and s.yml to debug cores. Tee problem is not visible anymore so this requires more investigation.
   - [ ] Why falcon.API fails but the falcon import seems not to produce ImportError when the falcon is not imported?
   - [ ] Why enabling debug logs in pytest fixture for server does not show the logs from mocked REST API call? It only shows fixture imports.
   - [ ] Why 'I/O operation on closed file' is generated as in SCRIBLING.md
   - [ ] Why Logger() UT tests produce out to capsys when the logger Pytest fixture is not used? The logger fixture hides something?
   - [ ] How to use double hyphen with Snippy search queries? Like in: search --sall '--all'
   - [ ] Why changing self._data = data in data setter in line 160 to self.data = data in config base seems to cause core. This can be used to set the Travis gdb parameters.
   - [ ] Should _add_date in Content() be based on updated when DATE already set? The reason would be that this sets the text template DATE and it should be always latest which is updated?
   - [ ] Fix tox and Python 3.4. Tox -e py34 // http://notes.webutvikling.org/darn-installation-of-python-3-4/. This was broken with Fedora 26. With Fedora 30 this works. This is heere because complication instructions are not complete in tox.ini.

## REFACTOR
   - [ ] Storage update() supports only one resource and this is not in line with others. Change to collection?
   - [ ] Offset based pagination is slow with large data sets (how large?). Measure with test. This was improved in laest sqlite 3.24.0 https://www.sqlite.org/changes.html
   - [ ] Refactor internal class level variables and methods to start with _ prefix.
   - [ ] Read storage schema directly to config() like the content templates.

## TESTS
   - [ ] How to get TypeError for --filter in try re.compile? This is not tested.
   - [ ] Refactor test case helper functions to export to yaml file instead of text. Yaml allows checking all params and text missed e.g. timestamps and uuid.
   - [ ] Refactor UT tests for single sqlite DB module. Refactor sqlite tests to single test_ut_sqlitedb.py like with the logger and parser.
   - [ ] Add test to verify that only TLS1.2 and selected ciphers are active. How and is it fast enough?
   - [ ] Add test that verifies that OID is not changing duringn one operation. Run two operations and check two OIDs in dict. Add this also for Field API tests because they inherit the base. If Field is printing log, it will cause the OID to refreshed twice.
   - [ ] Test Collection()/Resource() ne - probably UT tests.
   - [ ] Add tests that tries to sort based on non existent field. Is there already such case - migth be?
   - [ ] Refactor API tests based on update tests.
   - [ ] How to test case where required Python module is missing? Tests can be skipped when module is missing but how to simulate this? Try with Logger and gunicorn.
   - [ ] Is tested? import first content that already exist but second is new? Should result OK. Check test_cli_import_snippet_018-> Is the order this?
   - [ ] Add unit test for Cause.debug().
   - [ ] Add test to verify --help without server depdencies. This is the PyPI case.
   - [ ] Add custom parameter to pytest to enable debug logs in snippy fixture easily. Read https://docs.pytest.org/en/latest/example/simple.html?highlight=pytest_addoption
   - [ ] Add tests for 3 scenarios that exit with log in the startup.
   - [ ] Observe if Content.mocked_open and Content.imported_dict has sorting problems because of the hash. This could already sorted because the comparison sorts always the output.
   - [ ] Why test_cli_import_snippet_009 requires import-remove-utc but the 001 does not?
   - [ ] Why delete_storage requires not try/catch block for file remove when the existence is tested? This was with after server/snippy.run refactoring.
   - [ ] Test URL encoded REST API queries. The same problem that was with %2C may be with other formats.
   - [ ] Test manually the exception cases for example with file with Python3 and 2.7. Some exceptions may not be in Python2.7.
   - [ ] Fix patching in specific module. E.g snippy.migrate.migrate.os.path.isfile does not patch only specified module. Find 'side_effect' in import snippet.
   - [ ] Fix one failing API test fails all the WF cases? The cleanup does not work?
   - [ ] Why API performance test is so slow? Changed to http.client with 20% perf gain but still slow. Profile code next.
   - [ ] Why tests are failing if falcon is not installed? There is something strange when falcon is uninstalled. After uninstall import still works but variables not there?

## DOCUMENTS
   - [ ] Add instructions how to start docker container in README and docs.
   - [ ] Move test case brief to test case document. This cannot be done untill are cases are in new format because the documentation is lost. When this is done, check the autodock before massive desc move.
   - [ ] Add link to specific OAS (swaggerhub) specficiation from homepage and docs.
   - [ ] Add document note that content type is application/vnd.api+json; charset=UTF-8 inclufing the character set.
   - [ ] It is not possible in OAS 2 to deffine single mandatory parameter from group? For example search must have at least one for GET. For OAS 3 this works?
   - [ ] Document that importing content defined with digest will be update operation internally. This allows importing the same content data again with OK cause.
   - [ ] Add to document that using double dash is interpreted as option. To use this in grep: search --sall "--all" --no-ansi | grep -- '--all'
   - [ ] Update documents.

## BUBLING UNDER
   - [ ] Try ULID https://github.com/ahawker/ulid (does this support P2.7) or https://github.com/mdomke/python-ulid as in https://opensource.zalando.com/restful-api-guidelines/#resources
   - [ ] Add 'internal server errors' from logger scribling to Sphinx docs. Check that this part is there.
   - [ ] Add optional extra fields for logging.warning('test', extra={'foo': 'bar'}) which might be good for json. What fields to add?
   - [ ] There is a pylint bug that it does not see see Python decorators being used with underscore // https://github.com/PyCQA/pylint/issues/409
   - [ ] Check security implications from using setup.py (runs code) // https://stackoverflow.com/questions/44878600/is-setup-cfg-deprecated
   - [ ] How to add upgrade procedure? Is this needed? What happens when there is content stored and pip upgrade is made?
   - [ ] How to sign PyPI code? Is this feasible? https://help.github.com/articles/signing-commits-with-gpg/)
   - [ ] Add statistics print that shows the amout of snippets and unique categories.
   - [ ] Fix case described in 'git log 11448a2e90dab3a' and somehow and make test_wf a bit nicer?
   - [ ] Fix the Python2 test database naming to be random temp file in the same folder to allow parallelism.
   - [ ] Why when in Python2 a database test fails, it leaves hanging resources and DB clean does not work? Was this fixed into sqlite3_helper already?
   - [ ] How to better prevent commits to snippy.db than git hooks or git --assume-unchanged?
   - [ ] Fix PyPy 5.5.0 (Python 3.3) that does not have sqlite uri=True and does not have server 'ssl_version': ssl.PROTOCOL_TLSv1_2. This is working with latest PyPy implementations and this is not a priority fix.

## FOLLOW EXTERNAL BUGS/ISSUES
   - [x] Misleading ValidationError from AnyOf required property list // https://github.com/Julian/jsonschema/issues/535
   - [ ] Is there an external bug with more and ANSI color codes? // 'Linux more command with ANSI colors'
   - [ ] Pytest support for PEP-518 pyproject.toml is missing // https://github.com/pytest-dev/pytest/issues/1556
   - [ ] OpenAPI does not support OPTIONS HTTP method and it cannot be defined. // https://github.com/OAI/OpenAPI-Specification/issues/325
   - [x] The openapi2jsonschema does not work with Python 3. // https://github.com/garethr/openapi2jsonschema/issues/6.
   - [x] The openapi2jsonschema does not work with OAS 3.0. // https://github.com/garethr/openapi2jsonschema/issues/6.
   - [ ] OAS3.0 to JSON schema. // https://github.com/OAI/OpenAPI-Specification/issues/1032
   - [ ] There is a pylint bug that it does not see see Python properties being used with underscore. // https://github.com/PyCQA/pylint/issues/409
   - [x] Python logging is not following ISO8601 format and it cannot have timezone. Workaround has been implemented for Snippy Logger() class.
   - [ ] Python module jsonschema has open fault that prevent splitting schema to multiple files. // https://github.com/Julian/jsonschema/issues/313
