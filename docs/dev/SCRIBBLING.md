# Development Scibbling

# Cli refactoring

- If Snippy() is created without args, the args are taken from pytest args.
--> Must go with the /1/. Change all Snippy() to SNippy('export', etc)
/1/ Get idea from : https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module/37343818
- nargs=? from https://stackoverflow.com/questions/7484044/argparse-ignore-multiple-positional-arguments-when-optional-argument-is-specifi

Random notes and scribling during development.


   ```
   # Installing with Python virtual environment wrapper.
   $ mkdir -p ${HOME}/devel/python-virtualenvs
   $ sudo pip3 install virtualenvwrapper
   $ virtualenv --version
   $ export WORKON_HOME=${HOME}/devel/python-virtualenvs # Add to ~/.bashrc
   $ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3    # Add to ~/.bashrc
   $ source /usr/local/bin/virtualenvwrapper.sh          # Add to ~/.bashrc
   $ mkvirtualenv snippy
   ```

   ```
   # Installing for Python 3
   $ mkvirtualenv snippy
   $ pip3 install .
   $ pip3 install -e .[dev] # Development packages.
   ```

   ```
   # Installing for Python 2.7
   $ pip2 install virtualenvwrapper
   $ virtualenv --python=/usr/bin/python2 snippy-python27
   #$ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2    # Add to ~/.bashrc
   #$ mkvirtualenv snippy-python27
   #$ workon snippy-python27
   #$ pip install -e .[dev]
   #$ sudo dnf install redhat-rpm-config
   ```

   ```
   # Installing for Python 3.4
   # http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html
   $ sudo dnf install python34
   $ curl -O https://bootstrap.pypa.io/get-pip.py
   $ sudo python3.4 get-pip.py --user
   $ pip3 install virtualenvwrapper
   $ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python34    # Add to ~/.bashrc
   $ mkvirtualenv snippy-python34
   $ workon snippy-python34
   $ pip install -e .[dev]
   $ sudo dnf install redhat-rpm-config
   ```

   ```
   # Install Python3.4 virtual environment (does not work)
   $ cd /opt
   $ sudo curl -O https://www.python.org/ftp/python/3.4.7/Python-3.4.7.tgz
   $ sudo tar xzvf Python-3.4.7.tgz
   $ cd Python-3.4.7
   $ sudo ./configure --enable-shared --prefix=/usr/local LDFLAGS="-Wl,--rpath=/usr/local/lib"
   $ sudo make altinstall
   $ python3.4 -m venv myvirtualenv
   $ . myvirtualenv/bin/activate
   $ python --version
   ```

   ```
   # Install PyPy and run tests.
   $ sudo dnf install pypu
   $ export PYTHONPATH=/usr/lib64/python2.7/site-packages/
   $ wget https://bootstrap.pypa.io/get-pip.py
   $ sudo pypy get-pip.py
   $ sudo pypy -m pip install mock
   $ pypy -m pytest tests/test_cli_performance.py
   $ pypy -m pytest tests/test_api_performance.py
   $ sudo pypy -m pip install gunicorn
   $ sudo pypy -m pip install jsonschema
   $ sudo pypy -m pip install falcon
   $ pypy runner --help
   $ pypy runner --server -vv
   $ pypy -m pytest -x ./tests/test_*.py --cov snipp
   $ unset PYTHONPATH
   ```

   ```
   # Upgrade pip tools.
   $ pip install pip setuptools wheel twine --upgrade
   ```

   ```
   # Install pipenv development environment
   $ pipenv install

   # install pipenv
   $ pip install --user pipenv
   $ pipenv lock

   # Updated packages
   $ pipenv install logging_tree==1.8 --dev
   $ pipenv install sphinx_rtd_theme==0.4.1 --dev
   $ pipenv install tox==3.1.3 --dev
   $ pipenv install pytest==3.6.4 --dev
   $ pipenv install pylint==2.0.1 --dev
   $ pipenv lock -r  > requirements.txt

   # Pipenv for Python 3.6
   $ pipenv --python 3.6
   $ pipenv install pyyaml==3.12
   $ pipenv install falcon==1.4.1
   $ pipenv install gunicorn==19.9.0
   $ pipenv install jsonschema==2.6.0

   $ pipenv install codecov==2.0.15 --dev
   $ pipenv install flake8==3.5.0 --dev
   $ pipenv install logging_tree==1.7 --dev
   $ pipenv install mock==2.0.0 --dev
   $ pipenv install openapi2jsonschema==0.7.1 --dev
   $ pipenv install pprintpp==0.4.0 --dev
   $ pipenv install pyflakes --dev
   $ pipenv install pylint==2.0.0 --dev
   $ pipenv install pytest==3.6.3 --dev
   $ pipenv install pytest-cov==2.5.1 --dev
   $ pipenv install pytest-mock==1.10.0 --dev
   $ pipenv install sphinx==1.7.5 --dev
   $ pipenv install sphinx-autobuild==0.7.1 --dev
   $ pipenv install sphinxcontrib-openapi==0.3.2 --dev
   $ pipenv install sphinx_rtd_theme==0.4.0 --dev
   $ pipenv install tox==3.1.2 --dev

   # Pipenv for Python 2.7
   $ pipenv --python 2.7.14
   ```

   ```
   .. |badge-health| image:: https://landscape.io/github/heilaaks/snippy/master/landscape.svg?style=flat
      :target: https://landscape.io/github/heilaaks/snippy/master

   .. |badge-codacy| image:: https://api.codacy.com/project/badge/Grade/170f2ea74ead4f23b574478000ef578a
      :target: https://www.codacy.com/app/heilaaks/snippy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=heilaaks/snippy&amp;utm_campaign=Badge_Grade
   ```

   ```
   # Running container tests. These containers try to mimic
   # Travis CI test environment.
   $ sudo docker build -f tests/docker/Dockerfile-Python34-jessie -t snippy/python34-jessie .
   $ sudo docker build -f tests/docker/Dockerfile-Python34-trusty -t snippy/python34-trusty .
   $ sudo docker run -d snippy/python34-jessie
   $ sudo docker run -d snippy/python34-trusty
   $ sudo docker run -td snippy/python34-jessie tail -f /dev/null
   $ sudo docker run -td snippy/python34-trusty tail -f /dev/null
   $ sudo docker exec -it $(sudo docker ps | egrep -m 1 'snippy/python34-jessie' | awk '{print $1}') /bin/bash
   $ sudo docker exec -it $(sudo docker ps | egrep -m 1 'snippy/python34-trusty' | awk '{print $1}') /bin/bash
   ```

   ```
   # Docker run lingering container
   ENTRYPOINT ["tail", "-f","/dev/null"]
   ```

   ```
   # Test Docker container locale for Python.
   > https://stackoverflow.com/a/46181663
   $ docker run snippy python -c 'import sys; print(sys.stdout.encoding)'
   ```

   ```
   # Example commands for the Python virtualenvwrapper.
   $ lssitepackages
   $ lsvirtualenv
   $ deactivate
   $ rmvirtualenv snippy-python27
   $ workon snippy
   $ rmvirtualenv snippy
   ```

   ```
   # Using Pylint for the first time.
   #    - Modified test line from 100 to 125 characters.
   $ pylint --generate-rcfile > tests/pylint/pylint-snippy.rc
   ```

   ```
   # Running Pylint.
   $ pylint --rcfile tests/pylint/pylint-snippy.rc ./snippy
   $ pylint --rcfile tests/pylint/pylint-snippy.rc ./snippy > tests/pylint/pylint-snippy.txt
   ```

   ```
   # Bandit - security lint for Python
   $ pip install bandit
   $ bandit -r snippy
   ```

   ```
   # For UTF-8 set below to terminal.
   $ export LC_ALL=en_US.UTF-
   $ touch Düsseldorf.txt
   $ ll
   ```

   ```
   # Running pytests tests
   $ pytest
   ```

   ```
   # Freezing project for tag (check this one)
   $ pip freeze > requirements.txt
   ```

   ```
   # Test if Pyflame will have problems with SELinux or settings. The first
   # value needs to be 'off' and second value zero.
   $ getsebool deny_ptrace
     deny_ptrace --> off
   $ sysctl kernel.yama.ptrace_scope
     kernel.yama.ptrace_scope = 0
   ```

   ```
   # Install pyflame dependencies
   $ sudo dnf install autoconf automake gcc-c++ python-devel python3-devel libtool
   $ git clone https://github.com/uber/pyflame.git
   $ cd pyflame
   $ git checkout v1.4.4
   $ ./autogen.sh
   $ ./configure
   $ make
   ```

   ```
   # Postgres with Docker
   $ pip install psycopg2-binary
   $ docker exec -it $(docker ps | egrep -m 1 'postgres' | awk '{print $1}') /bin/bash
   $ docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
   $ docker run --name postgres -e POSTGRES_PASSWORD=postgres -v postgres_data:/var/lib/postgresql/data -p 5432:5432 -d postgres
   
   # Operate postgres
   psql -d postgres -U postgres
   \l
   \dt
   drop table contents;
   \d+ contents
   
   # Changes
   1. Test sqlite.
   
        - blob to char?
        - REGEXP to ~*?
   
   1. Change database.sql
      A) Capitalize SQL syntax.
      B) test if sqlite blob can be changed to char(64)
      C) Remove default from timestamps to force them?
      D) Rename table to align snippy namespace
      E) Connect
         import psycopg2
         connection = psycopg2.connect(host="localhost", user="postgres", password="postgres")
      F) queries ? --> %s
      G) use datetime. Do conversion in sqlite(database) module.

   
   1. sql syntax
      create table if not exists contents (
          data        text not null unique,
          brief       text default '',
          description text default '',
          groups      text default '',
          tags        text default '',
          links       text default '',
          category    text default 'snippet',
          name        text default '',
          filename    text default '',
          versions    text default '',
          source      text default '',
          uuid        text not null unique,
          -- created     datetime default current_timestamp,
          -- updated     datetime default current_timestamp,
          created     timestamp,
          updated     timestamp,
          --digest      blob(64),
          digest      char(64), --> allows searching with digest and regexp.
          metadata    text default '',
          id          serial primary key
      );
   2. ? => %s
   3. ROLLBACK is own function in postgres
   4. query = 'SELECT regexp_matches(data, %s) FROM contents '
      qargs = ['.']
      
      --> SELECT * FROM contents WHERE (data ~* %s OR brief ~* %s OR description ~* %s OR groups ~* %s OR tags ~* %s OR links ~* %s) AND (category=%s) ORDER BY brief ASC LIMIT 99 OFFSET 0
      -->  #columns = ['data', 'brief', 'description', 'groups', 'tags', 'links', 'digest'] --> bytea not able to regexp
      > https://dba.stackexchange.com/questions/166509/select-rows-from-my-table-where-a-character-column-matches-a-pattern
      
      -> sqlite regexp is case insensitve but the the postgre is case sensitive. how to change postgre? --> use ~*
      -> does sqlite support ~* syntax?

        - sqlitehelper store()
        
            content.get('created', ''), --Z must use timestamp
            content.get('updated', ''),
            -->
            content.get('created', '2018-02-02T02:02:02.000001+0000'),
            content.get('updated', '2018-02-02T02:02:02.000001+0000'),
      
   5. Table name to snippy_*?
   6. timetsamp formats?
        postgr: 2018-05-07 11:11:55.000001
        sqlite: 2017-10-16T19:42:19.000001+0000
        
        -> convert to datetime?

        self.created = row[Resource.CREATED].strftime('%Y-%m-%dT%H:%M:%S.%f+0000')
        self.updated = row[Resource.UPDATED].strftime('%Y-%m-%dT%H:%M:%S.%f+0000')

    7. Create delete table content for postgres after each test.
    8. assert storage changes to read from postgre
        change _connect in db helper

    --> test_api_create_snippet_015 (update) was failing due to updates
    
                        --> fix typo: snippet. All fields are tried to be updated but only __the that__ can be
    
                     test_api_create_reference_008 (sqlite expcetion)
                     
    --> api performance does not work since it does not use external DB
    
        - This works by manyally starting the server
        - peformance with manually started server with 1000 loop was  73.5 seconds.
    
    --> test_debug_option_001
            internal database key random (table not dropped so this increments all the time?)

    --> test_cli_update_reference_001 updates from cli are in different order in dict list which causes problems.
        - update #assert result_dictionary == expect_dictionary in assert storage.

        --> snippy mock to use Database.delete_all_contents() to clean the database instead of Database.delete_storage().

    9. performance is with cli_performance 4 times slower with postgres. from ~1s to ~4s.
    
    10. Parallel execution does not work.
    
    11. import all results python runner search --all --sall . --> 37. Was this correct?

   # Embedded postgres function that was not used after all because the Python support is not in by default.
   create language plpythonu;
   CREATE FUNCTION REGEXP (a integer, b integer)
   RETURNS integer
   AS $$
   return re.search(expr, item, re.IGNORECASE) is not None
   $$ LANGUAGE plpythonu;

   ```
      
   ```
   # cockroachDB
   docker run -d --name=roach2 --hostname=roach2 -p 26257:26257 -p 8080:8080 cockroachdb/cockroach:v2.1.2 start --insecure
   docker run -d --name=roach1 --hostname=roach1 -p 26257:26257 -p 8080:8080 -v "${PWD}/cockroach-data/roach1:/cockroach/cockroach-data" cockroachdb/cockroach:v2.1.2 start --insecure
   > http://localhost:8080
   $ docker exec -it $(docker ps | egrep -m 1 'roach' | awk '{print $1}') /bin/bash
   $ ./cockroach sql --insecure
   $ ./cockroach sql --insecure -e "SHOW USERS;
   
   > https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb.html
   ./cockroach sql --insecure
   CREATE USER IF NOT EXISTS maxroach;
   CREATE DATABASE snippy;
   GRANT ALL ON DATABASE snippy TO maxroach;
   
   show tables;
   
   # Python changes
   1. connection = psycopg2.connect(database='snippy', user='root', sslmode='disable', port=26257, host='localhost')
   2. return utc.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00') with TIMESTAMPZ
      --> same to resource load_dict and dict.pm (is resource load_dict used anymore?)
      --> this works with timestamp but there must be 00:00

   3. python  runner search --all  --sall . results 38. check this
             
   4. sql defs
      create table if not exists contents (
          data        text not null unique,
          brief       text default '',
          description text default '',
          groups      text default '',
          tags        text default '',
          links       text default '',
          category    text default 'snippet',
          name        text default '',
          filename    text default '',
          versions    text default '',
          source      text default '',
          uuid        text not null unique,
          -- created     datetime default current_timestamp,
          -- updated     datetime default current_timestamp,
          created     TIMESTAMPTZ,
          updated     TIMESTAMPTZ,
          --digest      blob(64),
          digest      char(64),
          metadata    text default '',
          id          SERIAL primary key
      );
      
   ```


   ```
   $ make docker
   $
   $ sudo docker run heilaaks/snippy search --sall .
   $ vi ~/.bashrc
     alias snippy-d='sudo docker run heilaaks/snippy'
   $ source ~/.bashrc
   $ snippy-d search --sall .
   ```

   ```
   # Print tree
   $ dnf install tree
   $ tree snippy | grep -Ev '*.pyc|*.json|*.txt|*.yml|*.yaml|*.db|*.md'
   ```

   ```
   ## Programming style guide.
   # Commit log
   > http://keepachangelog.com/en/1.0.0/
   ```

   ```
   # Signing Git commits
   > https://help.github.com/articles/generating-a-new-gpg-key/
   > https://help.github.com/articles/telling-git-about-your-gpg-key/
   > https://stackoverflow.com/a/42265848
   $ sudo dnf update gnupg2
   $ sudo dnf update libgcrypt
   $ sudo dnf update libassuan
   $ gpg2 --list-secret-keys --keyid-format LONG
   $ gpg2 --default-new-key-algo rsa4096 --gen-key
   $ gpg2 --list-secret-keys --keyid-format LONG
   $ gpg2 --armor --export <key>
   $ git config commit.gpgsign true
   $ git config --global gpg.program gpg2
   $ git commit -S -s
   $ export GPG_TTY=$(tty)
   $ git log --show-signature -1

   # GPG errors: update libgcrypt and libassuan
   $ /usr/bin/gpg-agent -v --daemon
   /usr/bin/gpg-agent: relocation error: /usr/bin/gpg-agent: symbol gcry_get_config, version GCRYPT_1.6 not defined in file libgcrypt.so.20 with link time reference
   /usr/bin/gpg-agent: relocation error: /usr/bin/gpg-agent: symbol assuan_sock_set_system_hooks, version LIBASSUAN_1.0 not defined in file libassuan.so.0 with link time reference
   ```

   ```
   # Move GPG keys. The removal from GIT causes all previous commits to be unverified.
   > https://stackoverflow.com/a/3176373
   > https://www.liquidweb.com/kb/how-to-add-a-user-and-grant-root-privileges-on-fedora-23/

   # Move keys
   $ scp -rp ~/.gnupg user@10.101.102.103:
   $ cp -rp /home_local/heilaaks/.gnupg/* .gnupg/
   $ gpg2 --list-secret-keys --keyid-format LONG

   # Delete old keys. TEST BEFORE DELETE!
   $ gpg2 --delete-secret-keys <key>
   $ gpg2 --delete-keys <key>
   ```

   ```
   # Why this slows down and starts to consume huge amount of cpu and stalls all cases=
   # The problem is the order of sys.argv that was after the Snippy object was created.
   import sys
   import unittest
   import mock
   import pytest
   from snippy.snip import Snippy
   from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


   class TestApiFramework(unittest.TestCase):
       """Test Snippy API framework."""

       #@pytest.mark.skip(reason="mocking sys.exit in here stalls all tests with pytest with high cpu load. Why?")
       #@mock.patch('sys.exit')
       #def test_resets(self, mock_exit):
       def test_resets(self):
           """Test Snippy reset."""

           #with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
           #with self.assertRaises(SystemExit): ## Blocks all logging?
           with mock.patch('snippy.config.arguments.sys.exit'):
               snippy = Snippy()
               sys.argv = ['snippy', 'search']
               cause = snippy.run_cli()
               print(cause)
               print("HERE")
               print(snippy.config.is_operation_search)
               print(snippy.config.source.get_operation())
               print(snippy.config.is_operation_search)
               print(snippy.config.source.get_operation())
               print(snippy.config)
               print("HERE-TAIL")
               snippy.release()
               snippy = None
               Database.delete_storage()

           #assert 0

       # pylint: disable=duplicate-code
       def tearDown(self):
           """Teardown each test."""

           Database.delete_all_contents()
           Database.delete_storage()
   ```

## Bling

```
http://tjelvarolsson.com/blog/five-steps-to-add-the-bling-factor-to-your-python-package/

    # Recoding
    > http://linuxbrew.sh/
    > https://asciinema.org/
    $ alias docker="sudo /usr/bin/docker"

    $ dnf install asciinema
    $ export PYTHONPATH=/usr/lib64/python2.7/site-packages/
    $ pip install . --user

    clear
asciinema rec ../snippy.cast
snippy --help
snippy search --sall .
snippy import --snippet --defaults
snippy import --solution --defaults
snippy import --reference --defaults
snippy search --sall security
snippy search --solution --sall kafka | grep -Ev '[^\s]+:'
ll
snippy export -d fd4c0adffa232083
ll
snippy import -d fd4c0adffa232083 -f kubernetes-docker-log-driver-kafka.txt
snippy search --solution --sall docker | grep -Ev '[^\s]+:'
sudo docker run -d --net="host" --name snippy heilaaks/snippy --server --port 8080 --ip 127.0.0.1 --log-json -vv
snippy search --sall prune
sudo docker run -d --net="host" --name snippy heilaaks/snippy --server --port 8080 --ip 127.0.0.1 --log-json -vv
curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/" | python -m json.tool
curl -v -X OPTIONS "http://127.0.0.1:8080/snippy/api/app/v1/snippets"
curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=0" -H "accept: application/vnd.api+json"
curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=security&limit=1" -H "accept: application/vnd.api+json"
docker logs snippy
docker stop snippy
ctrl-d
```

   # server

   ```
   https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO
   ```

## Travis CI and tooling

```
Add '[ci skip]' to commitlog in order to prevent the CI build.

https://landscape.io/dashboard
https://travis-ci.org/heilaaks/snippy
https://codecov.io/gh/heilaaks/snippy
https://landscape.io/github/heilaaks/snippy
http://snippy.readthedocs.io/en/latest/

## Documents

Good set on loggers: https://books.google.fi/books?id=7U1CIoOs5AkC&pg=PA357&lpg=PA357&dq=Should+I+use+root+or+logger+or+module+name+logger&source=bl&ots=eNYyAjE-IP&sig=MPee2BYjTYu4epc2NlESCG0x3so&hl=en&sa=X&ved=0ahUKEwiylOaLhunVAhXDK5oKHWSaCn04ChDoAQhGMAY#v=onepage&q=Should%20I%20use%20root%20or%20logger%20or%20module%20name%20logger&f=false
```

#######################################
## Server
#######################################

    ```
    $ pip install gunicorn
    $ pip install falcon
    $ python runner --server
    $ curl 127.0.0.1:8080/api/hello
    $ curl 127.0.0.1:8080/api/v1/hello

    # Swagger
    > https://app.swaggerhub.com/apis/heilaaks1/snippy-rest_api/1.0.0

    # Swagger to Sphinx
    $ .. swaggerv2doc:: ../dev/swagger-2.0.json
    $ .. openapi:: ../dev/swagger-2.0.yml

    # Swagger to github pages
    > https://community.smartbear.com/t5/SwaggerHub/Host-swagger-API-documentation-on-my-own-server/td-p/141523
    $ sudo docker pull swaggerapi/swagger-ui
    $ sudo docker run -p 80:8080 -e "SWAGGER_JSON=/api.json" -v /actual/path/to/api.json:/api.json swaggerapi/swagger-ui
    $ sudo docker run -p 80:8080 -e API_URL="https://api.swaggerhub.com/apis/heilaaks1/snippy/1.0.0" swaggerapi/swagger-ui
    $ http://localhost/

    # No good generators?
    # Use *.rst and example like
    > http://docs.readthedocs.io/en/latest/api.html#api-endpoints

    # 30 API docs
    > https://nordicapis.com/ultimate-guide-to-30-api-documentation-solutions/

    # Good examples from API Docs
    > https://stripe.com/docs/api

    # REST API design
    > http://www.kennethlange.com/posts/The-Ultimate-Checklist-for-REST-APIs.html
    > https://raw.githubusercontent.com/for-GET/http-decision-diagram/master/httpdd.png

    # REST API from user perspective
    > https://github.com/wearehive/project-guidelines

    # jsonschema examples
    > https://medium.com/grammofy/handling-complex-json-schemas-in-python-9eacc04a60cf

    # Open API to JSON schema
    $ openapi2jsonschema docs/dev/swagger-2.0.yml -o snippy/data/schema/
    $ openapi2jsonschema --stand-alone docs/dev/swagger-2.0.yml -o snippy/data/schema/
    #$ openapi2jsonschema https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json
    #$ openapi2jsonschema docs/dev/swagger.yml --stand-alone
    #$ openapi2jsonschema https://github.com/heilaaks/snippy/blob/master/docs/dev/swagger-2.0.yml
    #$ openapi2jsonschema https://github.com/heilaaks/snippy/blob/master/docs/dev/swagger-2.0.yml --stand-alone

    # Swagger API
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/app/v1/"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/app/v1/hello"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=20" -H "accept: application/json"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker,filebeat&limit=20" -H "accept: application/json"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets/a516e2d6f8aa5c6f" -H "accept: application/json"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets/a516e2d6f8aa5c6f" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker,filebeat&limit=2" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker,filebeat&limit=20" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker,filebeat&limit=20&sort=-created" -H "accept: application/json"
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker,filebeat&limit=10&sort=brief&sort=-created" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker,filebeat&limit=20&sort=brief&fields=brief,group" -H  "accept: application/json" | python -m json.tool
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/security?limit=1" -H "accept: application/vnd.api+json"

    # Server OPTIONS
    $ curl -i -X OPTIONS http://127.0.0.1:8080
    $ curl -v -X OPTIONS "http://127.0.0.1:8080/"
    $ curl -v -X OPTIONS "http://127.0.0.1:8080/snippy/api/app/v1/snippets"
    $ curl -v -X OPTIONS "http://127.0.0.1:8080/snippy/api/app/v1/snippets/1234"
    $ curl -v -X OPTIONS "http://127.0.0.1:8080/snippy/api/app/v1/snippets/1234/brief"

    # Fix multiple fields
    $ curl -X GET "https://app.swaggerhub.com/api/v1/snippets?sall=docker&sall=filebeat&sort=data&fields=data&fields=brief&fields=group" -H  "accept: application/json"

    # Testing with Dredd
    > http://dredd.org/en/latest/quickstart.html
    $ sudo yum install nodejs
    $ sudo npm install -g dredd
    $ dredd snippy/data/server/openapi/swagger-2.0.yml http://127.0.0.1:8080
    $ dredd snippy/data/server/openapi/swagger-2.0.yml http://127.0.0.1:8080 --dry-run
    $ dredd snippy/data/server/openapi/swagger.yml http://127.0.0.1:8080 --dry-run

    $ curl -X POST "http://127.0.0.1:8080/snippy/api/app/v1/snippets" -H "Content-Type: application/json" -d '{}'
    $ curl -X POST "http://127.0.0.1:8080/snippy/api/app/v1/snippets" -H "Content-Type: application/json" -d '{"data":["row1","row2"]}'
    $ curl -X POST "http://127.0.0.1:8080/snippy/api/app/v1/snippets" -H "accept: application/vnd.api+json; charset=UTF-8" -H "Content-Type: application/vnd.api+json; charset=UTF-8" -d '{"data":[{"type": "snippet", "attributes": {"data": ["row1", "row2"]}}]}'
    $ curl -X POST "http://127.0.0.1:8080/snippy/api/app/v1/snippets" -H "accept: application/vnd.api+json; charset=UTF-8" -H  "Content-Type: application/vnd.api+json; charset=UTF-8" -d "{  \"data\": [    {      \"type\": \"snippet\",      \"attributes\": {        \"data\": [          \"string\"        ],        \"brief\": \"string\",        \"group\": \"string\",        \"tags\": [          \"string\"        ],        \"links\": [          \"string\"        ],        \"category\": \"snippet\",        \"filename\": \"string\",        \"name\": \"string\",        \"versions\": \"string\",        \"created\": \"string\",        \"updated\": \"string\",        \"digest\": \"string\"      }    }  ]}"
    $ curl -X POST "http://127.0.0.1:8080/snippy/api/app/v1/snippets" -H "Content-Type: application/json" -d '{"data":"occaecat veniam aliqua","links":["et dolore ipsum reprehenderit","cupidatat","Lorem aliquip quis dolor cillum","non quis adipisicing sunt esse","in"],"versions":"irure nulla laborum Duis"}'
    $ curl -X POST "http://127.0.0.1:8080/snippy/api/app/v1/snippets" -H "Content-Type: application/vnd.api+json" -d '{"data":"occaecat veniam aliqua","links":["et dolore ipsum reprehenderit","cupidatat","Lorem aliquip quis dolor cillum","non quis adipisicing sunt esse","in"],"versions":"irure nulla laborum Duis"}'
    ```

#######################################
## Devel
#######################################

```
cd devel/snippy
workon snippy
make docs
make lint
make test
make clean
time python runner create -c 'docker rm' -b 'Remove all docker containers' -g 'moby' -t docker,container,cleanup --debug
python runner search --sall docker

cd devel/snippy
workon snippy-python27


make clean-db
python runner create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python runner create -c 'docker rmi $(docker images -f dangling=true -q)' -b 'Remove all dangling image layers' -g 'docker' -t docker,images,dangling,cleanup -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python runner create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python runner create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python runner search --sall docker
python runner delete --digest 6b8705255016268c
python runner export --file snippets.yaml
python runner export --file snippets.json
python runner export --file snippets.txt
python runner import --file snippets.yaml
python runner import --file snippets.json
python runner import --file snippets.txt
python runner update -d 6b8705255016268c

python runner create --content 'docker rm --volumes $(docker ps --all --quiet)' --brief 'Remove all docker containers with volumes' --group docker --tags docker-ce,docker,moby,container,cleanup --links 'https://docs.docker.com/engine/reference/commandline/rm/'
python runner create --brief 'Find pattern from files' --group linux --tags linux,search --links 'https://stackoverflow.com/questions/16956810/how-do-i-find-all-files-containing-specific-text-on-linux' --editor
grep -rin './' -e 'pattern'
grep -rin './' -e 'pattern' --include=\*.{ini,xml,cfg,conf,yaml}

# Multiline snippet from command line interface
$ python runner create -c $'docker rm $(docker ps --all -q -f status=exited)\ndocker images -q --filter dangling=true | xargs docker rmi' -b 'Remove all exited containers and dangling images' -g 'docker' -t docker-ce,docker,moby,container,cleanup,image -l 'https://docs.docker.com/engine/reference/commandline/rm/ https://docs.docker.com/engine/reference/commandline/images/ https://docs.docker.com/engine/reference/commandline/rmi/'
> https://stackoverflow.com/questions/26517674/passing-newline-within-string-into-a-python-script-from-the-command-line

# REFERENCES
python runner create --reference -l 'https://stackoverflow.com/a/33812744' -b 'Command line input encoding'
python runner create --reference -l 'https://stackoverflow.com/a/33812744' -b 'Command line input encoding' -t cli,coding,utf-8


python runner create --reference -l 'https://writingfordevelopers.substack.com/p/how-to-write-commit-messages|https://chris.beams.io/posts/git-commit/' -b 'How to write commit messages' -t git,commit,message,howto,scm -g git
python runner search --sall . --reference
python runner export --defaults --reference
python runner import --defaults --reference
```

#######################################
## Logging
#######################################

    > https://www.relaxdiego.com/2014/07/logging-in-python.html

#######################################
## Logging
#######################################

    # Documens - generated document for MT
    > https://stackoverflow.com/questions/7250659/python-code-to-generate-part-of-sphinx-documentation-is-it-possible

    # Sphinx API docs
    > https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/
    $ sphinx-apidoc -f -o docs/source/snippy snippy
    $ sphinx-apidoc -fMeET -o docs/source/snippy snippy

#######################################
## Formatting
#######################################

    # Colors
    > https://github.com/shiena/ansicolor/blob/master/README.md

#######################################
## Pytest
#######################################

    # Pytest
    > https://media.readthedocs.org/pdf/pytest/3.0.2/pytest.pdf

    # Mocking cookbook
    > http://chase-seibert.github.io/blog/2015/06/25/python-mocking-cookbook.html

    # Mocking examples for fixture prints.
    print("")
    print("calls %s" % Config.utcnow.called)
    print("calls %s" % Config.utcnow.call_count)
    print("calls %s" % Config.utcnow.call_count)
    print("calls %s" % Config.utcnow.mock_calls)

    # List tests
    $ cat tests/test_wf_* | grep -E '[[:space:]]{12}\$' | grep -Ev SnippetHelp

    # With the latest patches the pytest -p no:logging is not needed
    # and it must not be used. There is one case the relies caplog which
    # is a pytest fixture to capture logs from Python logger. There was
    # no other way figured out this could be done.
    $ pytest tests/test_wf_console_help.py -k test_console_help_examples

    # Travis core debugging
    > http://jsteemann.github.io/blog/2014/10/30/getting-core-dumps-of-failed-travisci-builds/
    > https://wiki.python.org/moin/DebuggingWithGdb
    > http://lint.travis-ci.org/
    > http://podoliaka.org/2016/04/10/debugging-cpython-gdb/
    $ vi .travis.yaml
      language: python
      python:
        - "2.7"
        - "3.4"
        - "3.5"
        - "3.6"
      before_install:
        - "sudo apt-get install -y gdb python-dbg" # Install libsqlite3-0-dbg?
        - "pip install -e .[test]"
      install:
        - "pip install -r requirements.txt"
      before_script:
        - "ulimit -c unlimited -S"
      script:
      # - "python -m pytest ./tests/test_*.py --cov snippy -vv"
      #  - "gdb -ex r -x .travis.gdb --args python -m pytest ./tests/test_*.py --cov snippy -vv" # Should this have '-ex "set pagination 0" -batch' to prevent prompt?
      after_success:
        - codecov
      after_failure:
        - ls -al
        - gdb -c ./core example -ex "thread info" -ex "set pagination 0" -batch

       Program received signal SIGSEGV, Segmentation fault.
       0x0000000000000000 in ?? ()
       #0  0x0000000000000000 in ?? ()
       #1  0x00007ffff1846e5c in ?? () from /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
       #2  0x00007ffff1847013 in ?? () from /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
       #3  0x00007ffff185b6b9 in ?? () from /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
       #4  0x00007ffff1883a75 in ?? () from /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
       #5  0x00007ffff188bf87 in sqlite3_step ()
          from /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
       #6  0x00007ffff1addb6e in pysqlite_step (statement=0xfa2268,
           connection=<optimized out>)
           at /tmp/python-build.20170626083852.6823/Python-3.5.3/Modules/_sqlite/util.c:37
       #7  0x00007ffff1adb879 in _pysqlite_query_execute (self=0x7ffff0eded50,
           multiple=0, args=<optimized out>)
           at /tmp/python-build.20170626083852.6823/Python-3.5.3/Modules/_sqlite/cursor---Type <return> to continue, or q <return> to quit---

    # Gdb - if there is no stack trace, the bt command fails in .travis.gdb
      [Inferior 1 (process 4590) exited normally]

      .travis.gdb:1: Error in sourced command file:

      No stack.

      (gdb)

    # no interaction to promtp
    $ gdb --batch --quiet -ex "thread apply all bt full" -ex "quit" ${exe} ${corefile}

    # https://www.stev.org/post/usinggdbtodebugacorefile
    cat ./core |strings |grep -E '^_='

    $ python -c 'import sqlite3; print(sqlite3.sqlite_version)'
    3.8.2

    $ cat ./core |strings |grep -E '^_='
    _=/home/travis/virtualenv/python3.6.3/bin/python

    $ gdb --c ./core -ex "set pagination 0" -batch
    [New LWP 4577]
    Core was generated by `python -m pytest ./tests/test_performance.py ./tests/test_ut_arguments_create.p'.
    Program terminated with signal SIGSEGV, Segmentation fault.
    #0  0x00007f23fefd26b0 in ?? ()

    $ gdb -c ./core -ex "thread info" -ex "set pagination 0" -batch
    [New LWP 4577]
    Core was generated by `python -m pytest ./tests/test_performance.py ./tests/test_ut_arguments_create.p'.
    Program terminated with signal SIGSEGV, Segmentation fault.
    #0  0x00007f23fefd26b0 in ?? ()
    No symbol table is loaded.  Use the "file" command.

    $ gdb -c ./core example -ex "bt" -ex "set pagination 0" -batch
    example: No such file or directory.
    [New LWP 4577]
    Core was generated by `python -m pytest ./tests/test_performance.py ./tests/test_ut_arguments_create.p'.
    Program terminated with signal SIGSEGV, Segmentation fault.
    #0  0x00007f23fefd26b0 in ?? ()
    #0  0x00007f23fefd26b0 in ?? ()
    #1  0x00007f23feff02a4 in ?? ()
    #2  0x000000000110dd98 in ?? ()
    #3  0x000000000110dd98 in ?? ()
    #4  0x000000000103b3f8 in ?? ()
    #5  0x00007f23feff1e5c in ?? ()
    #6  0x000000000112c308 in ?? ()
    #7  0x000000000110dd98 in ?? ()
    #8  0x00007fff9f4667b4 in ?? ()
    #9  0x0000000000000001 in ?? ()
    #10 0x0000060200001116 in ?? ()
    #11 0x0000000000000000 in ?? ()



#######################################
## Mocks
#######################################

    # Mock only specific builtin.
    > http://www.voidspace.org.uk/python/weblog/arch_d7_2010_10_02.shtml#e1188

#######################################
## Tox
#######################################

    # Tox
    > https://blog.ionelmc.ro/2015/04/14/tox-tricks-and-patterns/

#######################################
## Packaging
#######################################

    # Packaging
    > https://stackoverflow.com/questions/779495/python-access-data-in-package-subdirectory
    > http://peterdowns.com/posts/first-time-with-pypi.html
    > https://testpypi.python.org/pypi?%3Aaction=register_form

#######################################
## Linting
#######################################

    # Codacy
    > https://www.codacy.com/wizard/projects

#######################################
## Security
#######################################

    # File security
    > https://security.openstack.org/guidelines/dg_using-temporary-files-securely.html

    # Codeclimate
    > https://codeclimate.com

#######################################
## Releasing
#######################################

    # Check long description
    $ python setup.py check --restructuredtext
    $ pip install collective.checkdocs
    $ python setup.py checkdocs
    $ st2html.py README.rst  > /tmp/test.html
    $ python setup.py check --restructuredtext

    # Test PyPI
    > https://testpypi.python.org/pypi
    > https://pypi.python.org/pypi/snippy
    > https://pypi.python.org/pypi/html2text
    $ python setup.py sdist bdist_wheel
    $ python setup.py sdist upload -r testpypi

    # Testing in test PyPI.
    $ make clean
    $ make clean-db
    $ python setup.py sdist # Build source distribution
    $ python setup.py sdist bdist_wheel
    $ python setup.py sdist upload -r testpypi
    $ sudo pip uninstall snippy -y
    $ sudo pip3 uninstall snippy -y
    $ sudo pip install --index-url https://test.pypi.org/simple/ snippy
    $ sudo pip3 install --index-url https://test.pypi.org/simple/ snippy
    $ pip3 install --user --index-url https://test.pypi.org/simple/ snippy
    $ pip3 uninstall snippy -y

    # Release Wheels instead of Egg next time. Try the below:
    > https://packaging.python.org/discussions/wheel-vs-egg/
    > https://packaging.python.org/tutorials/distributing-packages/
    $ python setup.py sdist
    $ python setup.py bdist_wheel --universal
    $ twine upload dist/*

    # Release PyPI (deprecated use universal wheel)
    > https://pypi.org/project/snippy/
    $ git tag -a v0.7.0 -m "Experimental RESTish JSON API"
    $ git push -u origin v0.7.0
    $ python setup.py sdist # Build source distribution
    $ twine register dist/snippy-0.7.0.tar.gz
    $ twine upload dist/*

    # Push docker hub with Fedora
    $ su
    $ make docker
    $ docker rm $(docker ps --all -q -f status=exited)
    $ docker images -q --filter dangling=true | xargs docker rmi
    $ docker images
    $ docker rmi heilaaks/snippy:v0.6.0
    $ docker rmi heilaaks/snippy:latest
    $ docker rmi docker.io/heilaaks/snippy
    $ docker images
    $ docker login docker.io
    $ docker tag <image-hash> docker.io/<docker-hub-user-id>/<name>
    $ docker push docker.io/<docker-hub-user-id>/<name>
    $ sudo docker tag 5dc22d1d3380 docker.io/heilaaks/snippy:v0.7.0
    $ sudo docker tag 5dc22d1d3380 docker.io/heilaaks/snippy:latest
    $ sudo docker push docker.io/heilaaks/snippy:v0.7.0
    $ sudo docker push docker.io/heilaaks/snippy:latest

    # Pull
    $ docker pull heilaaks/snippy:v0.7.0
    $ docker pull heilaaks/snippy:latest

#######################################
## PyPI
#######################################


    # Release (OLD)
    $ git tag -a v0.7.0 -m "Experimental RESTish JSON API"
    $ git push -u origin v0.7.0
    $ python setup.py sdist # Build source distribution
    $ twine register dist/snippy-0.7.0.tar.gz
    $ twine upload dist/*

    # Source dist for PyPI
    python setup.py sdist
    python setup.py sdist bdist_wheel
    tar -ztvf dist/snippy-0.1.0.tar.gz

    gpg --list-keys
    gpg --detach-sign -a dist/snippy-0.1.0.tar.gz
    twine upload dist/snippy-0.1.0.tar.gz snippy-0.1.0.tar.gz.asc

    twine register dist/snippy-0.1.0.tar.gz
    twine register dist/snippy-0.1.0-py3-none-any.whl
    twine register dist/snippy-0.1.0.tar.gz
    twine upload dist/*

    # Old (insecure)
    python setup.py register
    python setup.py sdist upload

    # Links
    https://pypi.org/simple/snippet/
    https://pypi.org/simple/snippy/

    # Service request and pypi index package names
    https://pypi.org/project/snippy/
    https://stackoverflow.com/questions/45935230/transfer-ownership-of-pypi-packages
    https://www.python.org/dev/peps/pep-0541/
    https://sourceforge.net/p/pypi/support-requests/
    https://www.python.org/dev/peps/pep-0423/

# Must be in $HOME
[distutils]
index-servers=
    pypi
    testpypi

[testpypi]
repository: https://test.pypi.org/legacy/
username: <user>
password: <password>

[pypi]
repository: https://testpypi.python.org/pypi
username: <user>
password: <password>

# Make the snippy.db not included into the git
https://stackoverflow.com/questions/9794931/keep-file-in-a-git-repo-but-dont-track-changes
git update-index --assume-unchanged FILE_NAME # no changes tracked
git update-index --assume-unchanged snippy/data/storage/snippy.db
git update-index --no-assume-unchanged FILE_NAME # change back

#######################################
## Python general
#######################################

    # Ordered dictionary also in Python 2.7
    https://stackoverflow.com/questions/31605131/dumping-a-dictionary-to-a-yaml-file-while-preserving-order

    # Ansicolor
    https://github.com/shiena/ansicolor/blob/master/README.md

#######################################
## Docker Hub
#######################################

    # Push docker hub with Fedora
    $ sudo docker login docker.io
    $ docker tag <image-hash> docker.io/<docker-hub-user-id>/<name>
    $ docker push docker.io/<docker-hub-user-id>/<name>
    $ sudo docker tag 0b4881af2b2d docker.io/heilaaks/snippy:v0.5.0
    $ sudo docker tag 0b4881af2b2d docker.io/heilaaks/snippy:latest
    $ docker push docker.io/heilaaks/snippy:v0.5.0
    $ docker push docker.io/heilaaks/snippy:latest

    # Pull
    $ docker pull heilaaks/snippy:v0.1.0

#######################################
## Class design
#######################################


    # Use absolute imports
    > https://stackoverflow.com/questions/4209641/absolute-vs-explicit-relative-import-of-python-module

    # How to include
    > https://www.reddit.com/r/Python/comments/1bbbwk/whats_your_opinion_on_what_to_include_in_init_py/

#######################################
## Design notes and decisions
#######################################

    TERMS

    category           : Content category which can be: 'snippet', 'solution' or 'reference'.
    operation          : Refers to one operation that can be either:
                         A) Command line operation: 'create', 'delete', 'search', 'update', 'export' or 'import'.
                       : B) HTTP methods like: POST, PUT, GET, DELETE, PATCH or OPTION.
    operation category : Referers to 'category' defined for
                         A) command line operation with: --snippet(s), --solution(s), --reference(s) or --all
                         B) REST API operation defined with data.type: ['snippet', 'solution' or 'reference']
    search category    : Refers to categories which are searched when operation or request is executed.
    operation ID (OID) : Unique identifier allocated for all log messages generation from a single operation.
    HTTP method        : Same as operation when referring to REST API implementation.

    content            : Content object: Snippet, Solution or Reference that is stored inside Resource.
    field              : Field that is part of a content definition, same as attribute.
    attribute          : Field that is part of a content definition, same as field.
    resource           : A Resource object that can hold any of the content objects.
    collection         : A collection of resources.

    parameter          : Parameter in URL that defines for search criteria like sall, scat or sgrp for HTTP request.

    STRANGER THINGS

    1. 'I/O operation on closed file'

       If test 'test_debug_option_001' removes the caplog, there is error about
       I/O operation on closed file. Why? The case seems to work so this is
       caplog or capsys issue? Investigate more.

    ERROR HANDLING

    1. Fail opereration from the first failure

       The operations will flow from the beginning to end and there are no
       intermediate exists or shortcust. But the error handling must be made
       simple in order to keep the implementation size in control. The target
       is not to try to recover all possible errors but to fail operation as
       soon as the first failure is detected by setting an error cause.

       For example if the search category (scat) parameter is failty for one
       category, it will fail setting of scat configuration and no search
       is made from any existing category. This example results no search
       hits at all and it minimizes the search results.

    TIME STAMPS

    1. Rules to update time stamps

       A) When content is created, the created and updated time stamps are the
          same.

       B) When content is updated, the created time stamps remains same.

       C) When content is updated, the updated time stamps is always updated
          automatically. That is, the updated timestamp is never read from the
          user input like the Solution text template.

       D) When content is imported from JSON or YAML file, the created and
          updated times will remain as defined in the source file.

       E) When content is imported from TEXT file, the updated and created times
          are lost. In this case the time stamps are sert automatically based
          on the time of import.

       F) All time stamps are in UTC/GMT time.

    CONFIGURATION

    1. The tool configuration is global and shared with all instances of Snippy()

       If the Snippy() instance is created into the same process multiple times,
       the configuration is shared between all instances. This is a result of the
       Config() class being implemented with static class variables that hold the
       configuration /1/.

       Each module in the tool is accessing the data from Config class with class
       methods. This avoids passing the configuration into every instance.

       This is an accident and result of not realizing this behaviour before.

       The code could be changed to pass the Config() instance everywhere and
       re-design the Config() not to use class level static variables. This was
       tried but the decision was not to change this. The main reason is that test
       case helpers  are using few methods from Content(). This would have required
       creating and passing the Config() for each helper method in every test and
       subtest. Also the passing of 'self.config' everywhere was not so nice to
       authors eye.

       The confgiration is always updated with new source like CLI command or API
       request. But the pattern cannot be creating two instances from Snippy()
       into the same process like below and expect different configuration:

         from snippy.snip import Snippy

         snippy1 = Snippy()
         snippy2 = Snippy()
         print(snippy1.config.storage_in_memory) # Results False
         snippy2.config.storage_in_memory = True
         print(snippy1.config.storage_in_memory) # Results True

       The proper pattern is to create one instance and release it when it is
       not needed anymore.

         # Example results: NOK: cannot find content with given search criteria
         import sys
         from snippy.snip import Snippy

         sys.argv = ['snippy', 'search', '--sall', '.']
         snippy = Snippy()
         snippy.run()
         snippy.release()

       /1/ https://stackoverflow.com/questions/68645/static-class-variables-in-python

    CAUSE CODE

    1. The tool cause code is global and shared with all instances of Snippy()

       The same explanation applies for the tool exist cause from Cause() class
       than for the 'The tool configuration is global and shared with all instances
       of Snippy()'.

    2. Variables printed in causes are seprated with colon

       When variables are printed in cause, they must be separated with colon
       like in the example output below:

         > ... cannot find resource field: not-exist

       This follows the same rule as printing variables in logs.

    LOGGING

    1. There are no logs printed to user

       There is only the tool exit cause that must produce OK or NOK with a cause
       text in case of failure. In case more information is needed from the failure,
       the debug logs can be enabled with -vv or --debug option.

       This rule tries to reduce glutter printed for the end user.

    2. There are no exceptions printed to user

       Exceptions are not printed as is to the user. See reasoning from rule 'There
       are no logs printed to user'.

       This rule tries to reduce glutter printed for the end user.

    3. All logs are printed to stdout

       Because of rules 'There are no logs printed to user' and 'There are no
       exceptions printed to user', it is more suitable to use always the stdout.
       This is also considered more predictable for the end user who is debugging.
       the logs.

       The exception is that the argument parser prints parse failures to stderr.

    4. Logs from exceptions are printed in INFO level all other logs in DEBUG

       Controlled logs from exception must be printed with INFO level. All other
       logs must be printed in DEBUG level.

    5. Variables printed in logs are seprated with colon

       When variables are printed in logs, they must be separated with colon
       like in the examples below.

       When there is a variable being printed in the middle of the text string,
       it must be separated with colons and space before and after the printed
       variable.

       These rules intent to improve parsing of the text strings by providing
       tags than be used to exract variable values inside log strings.

         > ... config source category: snippet
         > content data: docker :matched more than once: 2 :preventing update operation

    6. All other than error logs are always printed in lower case

       All logs strings other than ERROR and CRITICAL are always printed with all
       lower case characters. This applies also also the log level name that is
       usually in capital letters.

    7. The debug option prints logs without modifications in full length

       When --debug option is applied, the logs must be printed without any
       modifications and filterings.

    8. The very verbose option prints logs always in lower case one log per line

       The -vv option prints always all logs one log per line and the whole
       log string is in lower case.

    9. Logs from internal server errors always contain 'internal server error '

       In order to find all logs related cases where the tool identified internal
       server error, the logs contain prefix of 'internal server error '.

    THREADING

    1. The tool is single threaded

       The tool was originally built for command line usage and it end up being
       single threaded. For example the configuration and cause code related
       objects are global and shared. To change this, would require largish
       refactoring effort which likely does not make sense. The performance is
       pretty ok based on reference performance tests.

       If there is a need to scale the performance up, it can be done by spawning
       multiple services from the same implementation which are sharing database
       that can scale.

    COMMITS

    1. Git commit logs follows rules from Chris Beams with explicit change types

       The commit logs follow seven rules from Chris Beams /1/ with explicit list
       of change types from listed below derived from /2/ and /3/.

       The explicit change types in commit log header are from:

         1. 'Add' new external features.
         2. 'Change' external behavior in existing functionality.
         3. 'Fix' bugs. Use 'Edit' for typo and layout corrections.
         4. 'Remove' external feature.
         5. 'Deprecat' a soon-to-be removed features.
         6. 'Security' in case of vulnerabilities.
         7. 'Refactor' code without external changes.
         8. 'Edit' small fixes like typo and layout fixes.
         9. 'Test' new test cases.

       The rule must be applied so that the logs are written for humans. This means
       that the commit log must tell the reasons and design decisions behind the
       change.

       This rule tries to force common look and feel for the commit logs.

       /1/ https://chris.beams.io/posts/git-commit/
       /2/ https://writingfordevelopers.substack.com/p/how-to-write-commit-messages
       /3/ http://keepachangelog.com/en/1.0.0/

    CONTENT

    1. The tool must know if specific parameters were given from CLI

       The tool must be aware if specific parameters were give at all from
       command line interface. These parameters are:

         - data
         - digest
         - sall
         - scat
         - search_filter
         - stag
         - sgrp
         - uuid

       The default value for these parameters must be None or these must not
       exist in the parameter set that is given for set_conf in class inherited
       from ConfigSourceBase().

       This is related to special case with CLI interface only. In case user
       used any of the these search keywords with command line option(s) and
       did not give any values for the CLI option, it is considered as "match
       any". For example a CLI option and value combination '--sall ' causes
       the tool to list all content.

       For the search_filter the use of None prevents unnecessary usage of the
       search filter for database search results.

    2. All but reference content links are sorted

       It is expected that with reference content the order where user gives
       links matters. That is, the first link is expected to be more relevant
       if there are multiple links in reference content. The reference category
       and it's link field can be compared to data field with other content
       categories. User is not expected to want the data to be sorted because
       the order matters.

       With all other content categories, the links are sorted automatically.

    3. Overlapping operation and search categories

       It is possible to use search category (scat) option on top of operation
       category defined with --snippet, --solution --reference or --all. For
       search and export operation, the search category (scat) overrides the
       operation category.

       This means for example that search results re presented from all
       categories if search category is defined as: snippet,solution,reference
       even when the operation category is defined to --solution or it defaults
       to --snippet. The same logic applies when the operation category is
       defined to --all.

    4. Markdown

       The Markdown content can use either code block or solution header. This
       allows using text based solution content inside code block that renders
       nicely or totally Markdup based solution.

       Example with code block:

            # Testing docker log drivers @docker

            >

            >

            ```
            #######################
            ## BRIEF  : Testing
            ######################
            ```

            # Meta

        Example with solution header:

            # Testing docker log drivers @docker

            >

            >

            # Solution

            Descirption of the solution

            ## Commands

            Commands

            # Meta

        The first example will render the solution as:

            #######################
            ## BRIEF  : Testing
            ######################

        The later example will render the solution as.

            # Solution

            Descirption of the solution

            ## Commands

            Commands

    UPDATING CONTENT ATTRIBUTES

    1. Attributes that can be updated

       Following attributes can be freely modified by user withing the limits
       of attribute definitions:

       - data
       - brief
       - group
       - tags
       - links
       - name
       - filename
       - versions
       - source

    2. Attributes that cannot be changed by user

       A) Category

          The category is defined when the content is created. After this,
          it cannot be changed by updating it. The only way to change this
          attribute is to delete and create the content again.

       B) Created

          The created timestamp is set when the content is created and user
          cannot modify. The only way to change this attribute is to delete
          and create the content again.

       C) Updated

          The updated timestamp is set when the content is updated and user
          cannot modify.

       D) UUID

          The UUID is intended to be used in cases where multiple databases are
          merged to one. The UUID is allocated always for the content and it
          never changes. Used UUID format is uuid1 which contains the hostname
          and timestamp where it was generated. This allows separting different
          processes running for example in different containers or hosts.

       E) Digest

          The content digest field is always set by the tool based on sha256
          hash algorithm. The digest is automatically updated when content
          is changed.

    CONTENT AND TIMESTAMPS (TODO remove from content and refere to here from there)

    1. Following operations require new timestamp

       Calls to Config.utcnow()
       =======================

       Content creation:

         1) Create collection from given input.

       Content updating:

         1) Create resource from configured content.
         2) Update 'updated' timestamp.

       Content importing from file:

         1) Create collection from given input. Same timestamp
            is used for all created resources.


       Content importing (=update) based on digest:

         1) Create collection from given input.
         2) Update 'updated' timestamp.

       Content editing:

         1) Create resource from configured content.

       Content exporting:

         1) Creating metadata with export timestamp.


    FILE NAME SELECTION

    1. Common rules for selecting filename in export operation

       1. Default file format is always YAML.

       2. Command line -f|--file always overrides other parameters.

       3. Default 'content.yaml' filename is used with more than one category

          If a collection of resources contains resources from more than one
          category, default file 'content.yaml' is used. Only if the collection
          contains resources from a single category, a content category specific
          filename is used.

       4. When --defaults option is used, the -f|--file option is not allowed

          The --defaults option is intended as a shorthand to export stored
          content. The same can be done without the option and defining the
          file with -f|--file option.

       5. When --template option is used, the -f|--file option is not allowed

          Currently only a text template is available. In this case defining
          the -f|--file could be considered in the future.

    2. Exporting files

       A. Single specified content without --file option

          1. Content does not define filename field: <category>.yaml
             - python runner export -d 6d221115da7b9540
             - test_cli_export_reference_004

          2. Content defines filename field: <filename>
             - python runner export -d 15d1688c970fa336
             - test_cli_export_solution_022

       B. Single specified content with --file option

          1. Content does not define filename field: <--file>
             - python runner export -d 6d221115da7b9540 -f testing.txt
             - python runner export -d 6d221115da7b9540 -f testing.json
             - test_cli_export_reference_005

          2. Content defines filename field: <--file>
             - python runner export -d 15d1688c970fa336 -f testing.yaml
             - test_cli_export_solution_023

       C. Search option (scat, sall, stag, sgrp) without --file option resulting one content

          1. Content does not define filename field: <category>.yaml
             - python runner export --references --sall commit
             - test_cli_export_snippet_011

          2. Content defines filename field: <filename>
             - python runner export --solution --sall kubeadm reset
             - test_cli_export_solution_022

       D. Search option (scat, sall, stag, sgrp) with --file option resulting one content

          1. Content does not define filename field: <--file>
             - python runner export --references --sall commit -f testing.json
             - test_cli_export_snippet_009

          2. Content defines filename field: <--file>
             - python runner export --solution --sall kubeadm reset -f testing.yaml
             - test_cli_export_solution_023

       E. Search option (scat, sall, stag, sgrp) without --file option resulting more than one content from single category

          1. Content does not define filename field: <category>.yaml
             - python runner export --sall kube --solution
             - test_cli_export_reference_021
             - test_cli_export_solution_036
             - test_cli_export_snippet_026

          2. Content defines filename field: <category>.yaml   # Content filename fields do not have any effect.

       F. Search option (scat, sall, stag, sgrp) with --file option resulting more than one content from single category

          1. Content does not define filename field: <--file>
             - python runner export --sall kube --solution -f testing.yaml
             - test_cli_export_snippet_016

          2. Content defines filename field: <--file>   # Content filename fields do not have any effect.
             - python runner export --sall kube --solution -f testing.yaml

       G. Search option (scat, sall, stag, sgrp) without --file option resulting more than one content from more than one category

          1. Content does not define filename field: content.yaml
             - python runner export --sall kube --scat solution,snippet
             - test_cli_export_reference_022

          2. Content defines filename field: content.yaml   # Content filename fields do not have any effect.

       H. Search option (scat, sall, stag, sgrp) with --file option resulting more than one content from more than one category

          1. Content does not define filename field: <--file>
             - python runner export --sall kube --scat solution,snippet -f testing.yaml
             - test_cli_export_reference_024

          2. Content defines filename field: <--file>   # Content filename fields do not have any effect.

       I. Exporting single category without --file option

          1. Content does not define filename field: <category.yaml>
             python runner export --reference

          2. Content defines filename field: <category.yaml>   # Content filename fields do not have any effect.

       J. Exporting single category with --file option

          1. Content does not define filename field: <--file>
             - python runner export --reference -f testing.json

          2. Content defines filename field: <--file>   # Content filename fields do not have any effect.

       K. Exporting more than one category without --file option

          1. Content does not define filename field: content.yaml
          2. Content defines filename field: content.yaml

       L. Exporting more than one category with --file option

          1. Content does not define filename field: <--file>
          2. Content defines filename field: <--file>

       M. Exporting all categories without --file option

          1. Content does not define filename field: content.yaml
          2. Content defines filename field: content.yaml

       N. Exporting all categories with --file option

          1. Content does not define filename field: <--file>
          2. Content defines filename field: <--file>

       O. Exporting single category with --default option

          1. Content does not define filename field:
          2. Content defines filename field:

       P. Exporting single category with --default and --scat options

          1. Content does not define filename field: default/<scat>.yaml
                - python runner export --scat solution --default
                - test_cli_export_reference_025

          2. Content defines filename field: N/A

       Q. Exporting single category with --default and --file options

          1. Content does not define filename field: Not Allowed
          2. Content defines filename field: Not Allowed

       R. Exporting more than one category with --default option

          1. Content does not define filename field: Not allowed
                - python runner export --solution --reference --defaults

          2. Content defines filename field: Content filename field does not affect.

       S. Exporting more than one category with --default and --file options

          1. Content does not define filename field: Not Allowed
          2. Content defines filename field: Not Allowed

       T. Exporting more than one category with --default and --scat options

          1. Content does not define filename field: default/<scat>.yaml
                - python runner export --scat solution,reference --default

          2. Content defines filename field: Content filename field does not affect.

       U. Exporting all categories with --default option

          1. Content does not define filename field: default/<scat>.yaml
          2. Content defines filename field: Content filename field does not affect.

       V. Exporting all categories with --default and --file options

          1. Content does not define filename field: Not Allowed
          2. Content defines filename field: Not Allowed

    JSON API

    1. The JSON API responses must follow JSON API v1.0 specifications

       Few highlights that are currently supported:

       - Top level meta, error and data objects
       - Top level links and self pointing to resource(s)
       - Top level data as JSON object (not list) when resource requested
       - Top level data as JSON object list when collection is requested
       - Top level data set to null if resource not found.
       - Top level data type set to 'snippets' or 'solutions'.
       - Top level data id always unique ID.
       - Data attributes containing resource or collection with the requested fields.

       Notes:

       - Note that numbers are presented as strings. For example HTTP status
         code is string.
       - The JSON response fileds are in CamelCase because the expected use
         case is from Javascript that uses CamelCase.
       - If resource is requested, it always results error or an object.
       - If GET is used to request explitcit digest in query parmater or with
         any search keys, the result is always error or list.

       /1/ http://jsonapi.org/

    2. Conflicts against JSON API v1.0

       1. If unique resource is not found, an error is returned

          The JSON API v1.0 [1] defines that "null is only an appropriate response
          when the requested URL is one that might correspond to a single resource,
          but doesn’t currently". It was considered that it is better to tell end
          user why the content was not properly returned instead of providing 'null'
          with 200 OK.

          [1] http://jsonapi.org/format/1.0/

          The above is understood so that in case of multiple hits from unique
          resource request, a null should be returned. The CLI and API interfaces
          allow requesting content with partial digest or uuid. If partial digest
          or uuid is used, it may match to multiple contents in search request.
          How ever, when user issues request like:

            GET /snippy/api/app/v1/uuid/1/brief
            GET /snippy/api/app/v1/digest/1/brief

         it is considered that it is better to return error and tell the user why
         the request failed than return 200 OK with data set to 'null'.

         It is also considered that 404 Not Found in cases when there is no matches
         or multiple matches is simpler than setting different error codes. The
         other option for multiple matches could be 409 Conflict that is used in
         case of import and update operations that require unique content to be
         operated. The failure reason can be determined from the error title.

         This case is different if uuid or digest is used in query parameter like:

           GET /snippy/api/app/v1/group/docker?scat=snippet&uuid=1

         In the above case, the result can be collection of resources if there are
         resources in snippet category which uuid start with 1.

    CLASS HIERARCHY

    1. Any class can import Constants().

    2. Any class can import Logger().

    3. Any class can import Cause().

    4. Any class can import Collection().

    5. Only Collection can import Resource().

    6. With exception of config package, any class can import Migrate().

    7. Only the Config() configuration sources Cli() and Editor().

    8. Only the Storage() can import Sqlitedb().

    9. Only Collection() and configuration sources Cli() and Editor() can import Parser().

    CHARACTER ENCODING

       1. In Python 2.7, unicode defaults to decoding 'ascii'.

       2. All strings are automatically encoded to TEXT_TYPE

          In Python 2, the text type is unicode and in Python 3 it si str.

    LOCALES

       Testing

       Starting from Sphinx 1.8.0 the LC_ALL must be set [6]. This variable seems
       to overrides all other localisation settings with few exceptions [1]. With
       Python 3 setting the LC_ALL=C causes problems with Click Python module.
       This also causes problems with Python 3 itself. The reason is likely that
       the value C forces the environment character set to ASCII [3]. This has
       been improved in Python 3.7 with PEP 538 and PEP 540 [3].

       Based on above, setting LC_ALL=C is a problem in Python 3 ... 3.6.

       There are ways to set the environment variable LC_ALL for virtualenv [4]
       and pipenv [5] but these are not provided with git repository code.

       Deployment

       The Alpine based container delivery sets the LANG to C.UTF-8 which is the
       same as official Python 3 Docker distribution.

       It seems that Alpine defines C.utf-8 by default but there is proposal
       to add support for LANG [10]. But Alpine uses MUSL which does not support
       support locales LC_* and LANG [11] but defaults [12].

       Because of the above, it seems that current definition of LANG in Alpine
       container does not have any effect and thus it is unnecessary.

       Solution (testing problem)

       This should work by defining the LC_ALL=C.UTF-8. See explanation of locale
       environment variable settings [8]

       ```
       $ export LC_ALL=C.UTF-8
       ```

       Other solution alternative would be setting the value of LC_ALL as empty
       which selects implementation defined native environment [7]. An empty value
       does not override all settings like C and POSIX do. With empty value the
       LC_ALL falls back to LC_* or then LANG. How ever, the supported locales
       define what values can be defined in LC_*, LANG or LC_ALL. If the LANG is
       not defined from list of supported locales, the below will fail

       ```
       $ export LC_ALL=
       $ export LANG=C.UTF-8
       ```

       Commands

       ```
       # list locales
       $ locale

       # list supported locales
       $ locale -a
       ```

       [1] https://unix.stackexchange.com/a/87763
       [2] http://www.sphinx-doc.org/en/master/changes.html
       [3] https://bugs.python.org/issue19846
       [4] https://stackoverflow.com/a/11134336
       [5] https://github.com/pypa/pipenv/blob/master/docs/advanced.rst#-support-for-environment-variables
       [6] https://github.com/sphinx-doc/sphinx/pull/4674
       [7] http://pubs.opengroup.org/onlinepubs/009695399/functions/setlocale.html
       [8] http://pubs.opengroup.org/onlinepubs/7908799/xbd/envvar.html
       [9] https://bugs.alpinelinux.org/issues/7374
       [10] https://bugs.alpinelinux.org/issues/7374
       [11] https://github.com/gliderlabs/docker-alpine/issues/144
       [12] https://wiki.musl-libc.org/functional-differences-from-glibc.html

    SECURITY HARDENING

    1. Logger has own security log level

       All suspected security related events are printed to logs with 'security'
       level.

    2. Hard maximum on log messages

       There is a hard maximum 'Logger.SECURITY_LOG_MSG_MAX' for log messages for
       safety and security reasons. This tries to prevent extremely long log messages
       which may cause problems for the server.


    SECURITY

    1. All code commits must be signed

       Following example can be used to generate and use GPG2 keys with GitHub.

       ```
       # Signing Git commits
       > https://help.github.com/articles/generating-a-new-gpg-key/
       > https://help.github.com/articles/telling-git-about-your-gpg-key/
       > https://stackoverflow.com/a/42265848
       $ sudo dnf update gnupg2
       $ gpg2 --list-secret-keys --keyid-format LONG
       $ gpg2 --default-new-key-algo rsa4096 --gen-key
       $ gpg2 --list-secret-keys --keyid-format LONG
       $ gpg2 --armor --export <key>
       $ git config commit.gpgsign true
       $ git config --global gpg.program gpg2
       $ export GPG_TTY=$(tty)
       $ git commit -S -s
       $ git log --show-signature -1
       ```

    2. Only TLSv1.2 is allowed

       All SSL versions are considered unsecure and compromised. TLS v1.1 and
       v1.2 are both without known security issues, but only v1.2 provides
       modern cryptographic algorithms. [1]

       [1] https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices
       [2] https://wiki.mozilla.org/Security/Server_Side_TLS

    3. Only selected set of ciphers are allowed

       Only ECDHE-RSA-AES256-SHA and ECDHE-RSA-AES128-SHA ciphers are allowed
       with the TLSv1.2. This set balances compatiblity and security. Ciphers
       can be tested for example with script [1]. Cipher list and mapping can
       be read from [2].

       [1] https://superuser.com/a/224263
       [2] https://testssl.sh/openssl-rfc.mapping.html

    3. Generating self signed SSL certificates

       ```
       # Create private key and self signed SSL certificate to run
       # server in 127.0.0.1.
       $ openssl req -x509 -newkey rsa:4096 -nodes -keyout server.key -out server.crt -days 356 -subj "/C=US/O=Snippy/CN=127.0.0.1"

       # View certificate.
       $ openssl x509 -text -noout -in server.crt

       # Verify private key.
       $ openssl rsa -check -in server.key
       ```

    TESTING

    1. Mocking UUIDs

       The UUIDs must be unique as defined for the database SQL schema. Each
       content has one unique UUID. Tests must be able to create the predefined
       content in any order. This causes situation where content can have
       different UUID depending on the order how it was generated.

       In order to test predefined but random set of UUIDs, the value of the UUID
       is tested first against set of valid values and then stored as one valid
       value for assert.

       The default data for snippet, solution and reference has their own range
       of UUIDs' The snippet range starts with 1, solution with 2 and reference
       with 3.

    2. Locales for testing

       See chapter LOCALES.

    3. Using collections for asserting expected content

       Test case help module Content() uses collections to assert expected content.
       The collections are read for example from text, Markdown, Yaml or Json files
       as well as from Database content to compare to expected results.

       This approach has benefits as well as limitations.

       Benefits:

           1. Clean implementation on a high level that is easy to read.

           2. Does not require adding for example exact Markdown formatted result in
              test. This can be seen as a drawback as well. It is currently considered
              so that adding the actual text or Markdown formatted data on every test
              case causes too long tests which are hard to read on high level.

           3. Tests the both sides of collection load and dump. This makes sure that
              the load method can parse the content generated by collection dump
              method.

       Drawbacks:

           1. Does not explicitlly define e.g. Markdown formatted expected results in
              every test.

           2. Uses actual implementation to dump and load which can hide faults.

           3. Creates areas in code that are not really verified by integration tests.

       Mitigations:

       In order to mitigate the drawbacks, there must be sufficient set of unit tests
       that verify the Collection() dump and load methods (text and Markdown format
       parsers).

    4. Test case layouts and data structures

       All test cases can be divided into three main categories. All the test withing
       one category must follow the same layout. The test case layout differences are
       minimized between main categories in order to improve maintainability and test
       readability.

           1. Creating, updating and importing content => assert tool storage

           2. Exporting content                        => assert mocked file

           3. Using REST API queries                   => assert REST API response

       The rules below align test case data presentation in every test case and make
       test cases more readable and maintainable.

       Rules:

           1. Content is always stored into 'content' variable in database format in
              every test case main category.

           2. The 'content' variable has all or one of the 'data', 'meta' or 'error'
              keys. The 'data' key contain the content in database format.

           3. The 'content' variable is always first and it is used to defined the
              input for the test case as well as to test the expected results.
           
           4. Test case variables and layout must follow the layout in existing tests
              and in the examples below.

           5. Default content that is created and updated timestamps must be same
              within one content category. The reason is that when default content
              is imported or created, only one timestamp is created for the whole
              collection of imported or created content.

              This matters only with tool proprietary text format. The reason is that
              other formats have the timestamps in metadata that will override the
              allocated (or mocked) time. In order to have constant rules, the rule
              is enforced with all content categories.

       Explanations:

       The file format that tool uses to store JSON or YAML content into a file uses
       'data' and 'meta' keys in dictionary. The 'data' key contains list of contents.
       The 'meta' key is optional and it is not always used.

       It is considered better to align test cases in same manner that the data passed
       to test case helpers in Collection always use the 'data' and optinal 'meta' keys.
       This allows for example adding new kind of data on top of the existing keys.

       Test cases must pass a dictionary with 'data' and optional 'meta' keys when
       comparing expected content stored in created file, database or JSON REST API
       response. The 'data' key must contain a list of dictionaries where each
       dictionary is a content with content specific attributes as keys.

       The content format in test case must follow the format that is stored in database.
       This is, for example the data and tags fields must use tuples and the tags must
       be sorted correctly in each test case.

        # Example 1: Assert content creation, updating and importing.

        @pytest.mark.usefixtures('isfile_true', 'yaml')
        def test_cli_import_snippet_999(self, snippy):
            """Import content from mocked YAML file.

            The YAML file contains created and updated timestamps and there
            is no need to mock these. The 'yaml' fixture returns a variable
            to a mock that can be used define input for the test case as well
            as reading the test case result.

            The Python YAML module uses file handles. This requires that the
            file handle where the YAML data is going to be written must be
            mocked with the used Python YAML API.

            Same applies also to JSON content.
            """

            # Content data is always defined in database format. This means
            # for example that tuple is used for data, groups, tags and links
            # and that the groups, tags and links dedending on content are
            # sorted.
            content = {
                'data': [
                    Snippet.DEFAULTS[Snippet.REMOVE],
                    Snippet.DEFAULTS[Snippet.NETCAT]
                ]
            }
            file_content = Content.get_file_content(Content.YAML, content)
            with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
                yaml.safe_load.return_value = file_content
                cause = snippy.run(['snippy', 'import'])
                assert cause == Cause.ALL_OK
                Content.assert_storage(content)
                mock_file.assert_called_once_with('./snippets.yaml', 'r')

        @pytest.mark.usefixtures('isfile_true', 'import-content-utc')
        def test_cli_import_snippet_999(self, snippy):
            """Import content from mocked text file.

            The text file does not contain timestamp fields. Because of this,
            the timestamp must be mocked and it must match the given content.

            The same applies also to Markdown content.
            """

            # Content data is always defined in database format. This means
            # for example that tuple is used for data, groups, tags and links
            # and that the groups, tags and links dedending on content are
            # sorted.
            content = {
                'data': [
                    Snippet.DEFAULTS[Snippet.REMOVE],
                    Snippet.DEFAULTS[Snippet.NETCAT]
                ]
            }
            file_content = Content.get_file_content(Content.TEXT, content)
            with mock.patch('snippy.content.migrate.open', file_content, create=True) as mock_file:
                cause = snippy.run(['snippy', 'import', '-f', './all-snippets.txt'])
                assert cause == Cause.ALL_OK
                Content.assert_storage(content)
                mock_file.assert_called_once_with('./all-snippets.txt', 'r')

        @pytest.mark.usefixtures('isfile_true', 'yaml')
        def test_cli_import_snippet_001(self, snippy):
            """Import content from mocked YAML file
    
            YAML file contain all the fields stored into the database with the
            exception of database specific key and internal metadata fields.

            Test like this would work just by defining the YAML safe_load value
            directly as in content variable. The get_file_content is used to
            protect code changes affecting to multiple test cases.

            The same applies also to JSON file imports.
            """
    
            content = {
                'data': [
                    Snippet.DEFAULTS[Snippet.REMOVE],
                    Snippet.DEFAULTS[Snippet.NETCAT]
                ]
            }
            file_content = Content.get_file_content(Content.YAML, content)
            with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
                yaml.safe_load.return_value = file_content
                cause = snippy.run(['snippy', 'import'])
                assert cause == Cause.ALL_OK
                Content.assert_storage(content)
                mock_file.assert_called_once_with('./snippets.yaml', 'r')


        # Example 2: Assert exporting content.

        @pytest.mark.usefixtures('default-snippets', 'export-time')
        def test_cli_export_snippet_999(self, snippy):
            """Export content to Markdown format."""

            # Content data is always defined in database format. This means
            # for example that tuple is used for data, groups, tags and links
            # and that the groups, tags and links dedending on content are
            # sorted.
            content = {
                'meta': Content.get_cli_meta(),
                'data': [
                    Snippet.DEFAULTS[Snippet.REMOVE],
                    Snippet.DEFAULTS[Snippet.FORCED]
                ]
            }
            with mock.patch('snippy.content.migrate.open', mock.mock_open(), create=True) as mock_file:
                cause = snippy.run(['snippy', 'export', '-f', './snippets.mkdn'])
                assert cause == Cause.ALL_OK
                Content.assert_mkdn(mock_file, './snippets.mkdn', content)


        # Example 3: Assert REST API response.

        @pytest.mark.usefixtures('create-remove-utc', 'create-forced-utc')
        def test_api_create_snippet_999(self, server):

            # Content data is always defined in database format. This means
            # for example that tuple is used for data, groups, tags and links
            # and that the groups, tags and links dedending on content are
            # sorted.
            content = {
                'data': [
                    Snippet.DEFAULTS[Snippet.REMOVE],
                    Snippet.DEFAULTS[Snippet.FORCED]
                ]
            }
            request_body = {
                'data': [{
                    'type': 'snippet',
                    'attributes': content['data'][0]
                }, {
                    'type': 'snippet',
                    'attributes': content['data'][1]
                }]
            }
            expect_headers = {
                'content-type': 'application/vnd.api+json; charset=UTF-8',
                'content-length': '1481'
            }
            expect_body = {
                'data': [{
                    'type': 'snippet',
                    'id': Snippet.REMOVE_DIGEST,
                    'attributes': content['data'][0]
                }, {
                    'type': 'snippet',
                    'id': Snippet.FORCED_DIGEST,
                    'attributes': content['data'][0]
                }]
            }
            result = testing.TestClient(server.server.api).simulate_post(
                path='/snippy/api/app/v1/snippets',
                headers={'accept': 'application/json'},
                body=json.dumps(request_body))
            assert result.status == falcon.HTTP_201
            assert result.headers == expect_headers
            Content.assert_restapi(result.json, expect_body)
            Content.assert_storage(content)

        @pytest.mark.usefixtures('import-forced', 'update-forced-utc')
        def test_api_create_snippet_013(self, server):

            # Content data is always defined in database format. This means
            # for example that tuple is used for data, groups, tags and links
            # and that the groups, tags and links dedending on content are
            # sorted.
            #
            # Content must be copied if it is changed locally. If a copy is
            # not made, it will change the global default content which will
            # affect to all test cases.
            content = {
                'data': [
                    Content.deepcopy(Snippet.DEFAULTS[Snippet.FORCED])
                ]
            }
            content['data'][0]['data'] = Snippet.DEFAULTS[Snippet.REMOVE]['data']
            content['data'][0]['digest'] = a9e137c08aee09852797a974ef91b871c48915fecf25b2e89c5bdba4885b2bd2'
            request_body = {
                'data': {
                    'type': 'snippet',
                    'attributes': {
                        'data': Const.NEWLINE.join(content['data'][0]['data'])
                    }
                }
            }
            expect_headers = {
                'content-type': 'application/vnd.api+json; charset=UTF-8',
                'content-length': '894'
            }
            expect_body = {
                'links': {
                    'self': 'http://falconframework.org/snippy/api/app/v1/snippets/a9e137c08aee0985'
                },
                'data': {
                    'type': 'snippet',
                    'id': content['data'][0]['digest'],
                    'attributes': content['data'][0]
                }
            }
            result = testing.TestClient(server.server.api).simulate_post(
                path='/snippy/api/app/v1/snippets/53908d68425c61dc',
                headers={'accept': 'application/vnd.api+json', 'X-HTTP-Method-Override': 'PATCH'},
                body=json.dumps(request_body))
            assert result.status == falcon.HTTP_200
            assert result.headers == expect_headers
            Content.assert_storage(content)
            Content.assert_restapi(result.json, expect_body)

    DOCUMENTATION

    1. Code documentation follows Goolge docstring format

       The Google docstring format is considered shorter and more readable than
       the NumPy format. The later format has it's place when explaining complex
       algorithms and their parameters. But here the intention is that the method
       description explains the complicated parts and the method argument is a
       short explanation of the pararameters.

    === WHITEBOARD ===
    # SECURITY
    $ curl --insecure -v https://127.0.0.1:8080

    # Running in 443 requires sudo and all installs?

    # Best practises
    > https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices

    $ openssl req -x509 -newkey rsa:4096 -nodes -keyout server.key -out server.crt -days 356 -subj "/C=US/O=Snippy/CN=127.0.0.1"

    # certificates are not dependent on protocols

    $ openssl s_client -debug -connect 127.0.0.1:8080 -tls1_2  # must work
    $ openssl s_client -debug -connect 127.0.0.1:8080 -tls1    # must not work
    $ openssl s_client -debug -connect 127.0.0.1:8080 -tls1_1  # must not work
    $ openssl s_client -debug -connect 127.0.0.1:8080 -ssl3    # must not work

    # Run server
    $ python runner --server -vv --ssl-cert ./snippy/data/ssl/server.crt --ssl-key ./snippy/data/ssl/server.key
    === WHITEBOARD ===



#######################################
## Command line design
#######################################

    # Command line desing
    https://softwareengineering.stackexchange.com/questions/307467/what-are-good-habits-for-designing-command-line-arguments
    subparsers https://stackoverflow.com/questions/23304740/optional-python-arguments-without-dashes-but-with-additional-parameters
    https://www.gnu.org/prep/standards/standards.html#g_t_002d_002dhelp
    http://docopt.org/
    http://www.tldp.org/LDP/abs/html/standard-options.html

    # Customise help
    https://stackoverflow.com/questions/20094215/argparse-subparser-monolithic-help-output
    https://gist.github.com/evertrol/09d7fe69efb65bbc35d2

pylint --rcfile tests/pylint/pylint-snippy.rc ./snippy
pylint --rcfile tests/pylint/pylint-snippy-tests.rc ./tests
pytest --cov=snippy tests/
pytest --cov=snippy --cov-report html tests/
make -C docs html
python snip.py create -c 'docker rm $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup
python snip.py create -c 'docker rm $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker, container, cleanup
pytest

   > file:///home/heilaaks/devel/snippy/htmlcov/index.html
   > file:///home/heilaaks/devel/snippy/docs/build/html/index.html

# Run single test
pytest tests/test_arguments_add_new_snippet.py -k test_tags_with_quotes_and_separated_by_comma_and_space

#######################################
## Editor example
#######################################

### Editor input
# Commented lines will be ignored.
#
# Add mandatory snippet below.
docker rm --force redis
docker rmi redis
docker rmi zookeeper

# Add optional brief description below.
Remove docker image with force

# Add optional single group below.
docker

# Add optional comma separated list of tags below.
docker,images,remove

# Add optional links below one link per line.
https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes
https://docs.docker.com/engine/reference/commandline/rm/


#######################################
## Test plan new
#######################################

##########################################
## Search content
##########################################

## snippets: search all keyword
snippy search --sall KW                                     # search --sall to match from data (DONE)
snippy search --sall KW                                     # search --sall to match from brief (DONE)
snippy search --sall KW                                     # search --sall to match from group (DONE)
snippy search --sall KW                                     # search --sall to match from tags (DONE)
snippy search --sall KW                                     # search --sall to match from links (DONE)
snippy search --sall KW                                     # search --sall to match from digest (DONE)
snippy search --sall KW                                     # search --sall not to match (DONE)
snippy search --sall                                        # search --sall does not have value (DONE)
snippy search --sall ''                                     # search --sall value is empty string (DONE)
snippy search --sall .                                      # search --sall value is dot (match any) with stored content (DONE)
snippy search --sall .                                      # search --sall value is dot (match any) without content stored (DONE)
snippy search --sall KW,KW                                  # search --sall with two keywords (TODO)
snippy search --sall KW,KW,KW                               # search --sall with three keywords (TODO)

## snippets: search tags keyword
snippy search --stag KW                                     # search --stag to match from tags (DONE)
snippy search --stag KW                                     # search --stag not to match (DONE)

## snippets: search group keyword
snippy search --sgrp KW                                     # search --sgrp to match from group (DONE)
snippy search --sgrp KW                                     # search --sgrp not to match (DONE)

## snippets: search with regepx filter
snippy search --sall . --flter <regexp>                     # search --filter to match only commands (DONE)
snippy search --sall . --flter <regexp>                     # search --filter not to match (DONE)
snippy search --all --sall . --filter <regexp>              # search --filter to match only commands from category --all (DONE)

## snippets: search with content
snippy search -c <content>                                  # search --content to match content (DONE)
snippy search -c <content>                                  # search --content not to match

## snippets: search with digest
snippy search -d <digest>                                   # search --digest to match short digest (DONE)
snippy search -d <digest>                                   # search --digest to match long digest (DONE)
snippy search -d <digest>                                   # search --digest to match multiple contents (DONE)
snippy search -d <digest>                                   # search --digest not to match

##########################################
## Export content
##########################################

## export template to specific file.

## snippets: template
snippy export --template                                    # export snippet template (DONE)
snippy export --snippet --template                          # export snippet template with explicit category (DONE)

## solutions: template
snippy export --solution --template                         # export solution template without --file option (DONE)

## snippets: defaults
snippy export --defaults                                    # export snippet defaults (DONE)
snippy export --defaults                                    # export snippet defaults without stored content (DONE)

## solutions: defaults
snippy export --solution --defaults                         # export solutions defaults (DONE)
snippy export --solution --defaults                         # export solution defaults without stored content (DONE)

## snippets: all content
snippy export                                               # export all snippets to default file (DONE)
snippy export --snippet                                     # export all snippets to default file (DONE)
snippy export -f ./file.yaml                                # export all snippets to yaml file (DONE)
snippy export --file foo.bar                                # try to export all snippets to unsupported file format (DONE)

## solutions: all content
snippy export --solution                                    # export all solutions to default file (DONE)
snippy export --solution -f ./file.yaml                     # export all solutions to yaml file (DONE)
snippy export --solution -f ./file.json                     # export all solutions to json file (DONE)
snippy export --solution -f ./file.txt                      # export all solutions to text file (DONE)
snippy export --solution -f ./file.text                     # export all solutions to text file (DONE)
snippy export --solution -f ./file.foo                      # try to export all solutions to unsupported file format (DONE)

## snippets: defined content
snippy export -d <digest>                                   # export defined snippet to default file (DONE)
snippy export -d <digest> -f ./file.yaml                    # export defined snippet to yaml file (DONE)
snippy export -d <digest> -f ./file.json                    # export defined snippet to json file (DONE)
snippy export -d <digest> -f ./file.txt                     # export defined snippet to text file (DONE)

## solutions: defined content
snippy export -d <digest>                                   # export solution with digest to default file (DONE)
snippy export --solution -d <digest>                        # export solution to file defined by solution metadata (DONE)
snippy export --solution -d <digest>                        # export solution to file without solution metadata for file name(DONE)
snippy export --solution -d <digest> -f ./file.yaml         # export solution to yaml file (DONE)
snippy export -d a96accc25dd23ac0 -f ./file.yaml            # export solution to yaml file wihtout category (DONE)
snippy export --solution -d <digest> -f ./file.json         # export solution to json file (DONE)
snippy export -d a96accc25dd23ac0 -f ./file.json            # export solution to json file wihtout category (DONE)
snippy export --solution -d <digest> -f ./file.txt          # export solution to text file (DONE)
snippy export -d a96accc25dd23ac0 -f ./file.txt             # export solution to text file wihtout category (DONE)
snippy export --solution -d <digest> -f ./file.text         # export solution to text file (DONE)
snippy export -d a96accc25dd23ac0 -f ./file.text            # export solution to text file wihtout category (DONE)
snippy export --solution -d <digest> -f ./file.foo          # try to export solution to unsupported file format (DONE)
snippy export --solution -d <unknown digest> -f ./file.text # try to export solution with unknown digest (DONE)

#######################################
## Test plan
#######################################

########################
## Creating new snippets
########################
1. Create snippet from command line with all parameters (DONE)
python snip.py create --content 'docker rm -v $(docker ps -a -q)' --brief 'Remove all docker containers' --group 'docker' --tags docker,container,cleanup --links 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'

2. Create new snippet from command line with only mandatory parameter content
python snip.py create -c 'docker rm -v $(docker ps -a -q)'

3. Create new snippet from command line with content and brief
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers'

4. Create new snippet from command line with content, brief and group
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker'

5. Create new snippet from command line with content, brief, group and tags
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup

6. Create new snippet with editor without any parameters. Fill all parameters from editor
python snip.py create --editor

7. Create new snippet with editor and define content as default
python snip.py create -e -c 'docker rm -v $(docker ps -a -q)'

8. Create new snippet with editor and define content and brief for the editor
python snip.py create -e -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers'

9. Create new snippet with editor and define content, brief and group for the editr
python snip.py create -e -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker'

10. Create new snippet with editor and define content, brief, group and tags for the editr
python snip.py create -e -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup

11. Create new snippet with editor and define content, brief, group, tags and link for the editor
python snip.py create -e -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'

12. Try to Create new snippet which content already exists
python snip.py create -c 'docker rm -v $(docker ps -a -q)'
python snip.py create -c 'docker rm -v $(docker ps -a -q)'

13. Create new content in editor with three reference links
python snip.py create -e

14. Create new content without mandatory parameter
python snip.py create

15. Create new from editor. Must not show the 'default' value for the group. If user does not set group, it must be insert with 'default' value.

16. Create new from editor. Only only --group parameter to make sure the edir show this value and not default or empty.

17. Create content with quotes like 'grep -rin './' -e 'pattern'

18. Create content with that has tags, brief and group only numbers to see if the string handling takes care of numbers.

####################
## Updating snippets
####################

1. Update snippet content with only mandatory parameters with digest (DONE)
python snip.py create -c 'docker rm -v $(docker ps -a -q)'
python snip.py update --digest 22c0ca5bbc9797b

2. Update snippet with with digest when all parameters filled
python snip.py create --content 'docker rm -v $(docker ps -a -q)' --brief 'Remove all docker containers' --group 'docker' --tags docker,container,cleanup --links 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py update --digest 22c0ca5bbc9797b

3. Update snippet with digest when only mandatory parameter is set without making any changes
python snip.py create -c 'docker rm -v $(docker ps -a -q)'
python snip.py update --digest 22c0ca5bbc9797b

4. Update snippet by defining the content and updated group and tags from command line.
python snip.py create --content 'docker rm -v $(docker ps -a -q)' --brief 'Remove all docker containers' --group 'docker' --tags docker,container,cleanup --links 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py update --content 'docker rm -v $(docker ps -a -q)' --brief 'Remove all docker containers' --group 'moby' --tags moby,container,cleanup --links 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'

5. Update snippet by defining the content itself and not making any changes
python snip.py create --content 'docker rm -v $(docker ps -a -q)' --brief 'Remove all docker containers' --group 'docker' --tags docker,container,cleanup --links 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py update --content 'docker rm -v $(docker ps -a -q)' --brief 'Remove all docker containers' --group 'docker' --tags docker,container,cleanup --links 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'

6. Update snippet with unknown digest (DONE)
python snip.py update --digest 111111111111111

7. Update snippet with unknown content (DONE)
python snip.py update -c '111111111111111'

8. Update snippet by defining solution category in command line (DONE)
python snip.py update --solution -d 22c0ca5bbc9797b

9. Update solution by leaving the category out (defaults snippet) from command line (DONE)
python snip.py update -d 22c0ca5bbc9797b

####################
## Deleting snippets
####################

1. Delete snippet with digest (TESTED)
python snip.py delete --digest 22c0ca5bbc9797b

2. Delete snippet with unknown digest (TESTED)
python snip.py delete --digest 111111111111111

3. Test deleting snippets with content that is found (TESTED)

4. Test deleting snippets with content that is not found (TESTED)

5. Test that empty digest does not delete snippet when there are two snippet (TESTED)

#####################
## Searching snippets
#####################

1. --sall to match from data



python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py search --sall images # Returns one snippet
python snip.py search --sall how # Returns three snippets
python snip.py search --sall image,cleanup # Returns two snippets
python snip.py search --sall image,cleanup,moby # Returns three snippets
python snip.py search --sall notfound # Returns no snippets
python snip.py search --sall . # Returns three snippets

2. Search snippets from tag field
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py search --stag images # Returns one snippet
python snip.py search --stag how # Returns no snippets
python snip.py search --stag image,cleanup # Returns one snippets
python snip.py search --stag image,cleanup,moby # Returns two snippets
python snip.py search --stag notfound # Returns no snippets
python snip.py search --stag . # Returns three snippets

3. Search snippets from group field
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py search --sgrp images # Returns no snippets
python snip.py search --sgrp how # Returns no snippets
python snip.py search --sgrp image,docker # Returns two snippets
python snip.py search --sgrp docker,moby # Returns three snippets
python snip.py search --sgrp notfound # Returns no snippets
python snip.py search --sgrp . # Returns three snippets

4. Search with content
python snip.py search -c 'docker rm --volumes $(docker ps --all --quiet)'

5. Search content with digest

######################
## Exporting snipppets
######################

1. Export all snippets into yaml file (DONE)
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py export --file ./snippets.yaml

2. Export all snippets into json file
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py export --file ./snippets.json

3. Export all snippets into text file
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py export --file ./snippets.txt

4. Export without file to use default file
python snip.py export (DONE)
python snip.py export --snippets  # Creates snippets.yaml
python snip.py export --solution # Creates solutions.yaml (DONE)

5. Export template
python runner export --template (DONE)
python runner export --solution --template
python runner export --snippet --template (DONE)

6. Export with unsupported file format foo.bar. This must not create empty file foo.bar
python runner export --file foo.bar (DONE)

7. Export defaults
python runner export --defaults

8. Export specific content indentified by message digest into default file. This works for snippets and solutions and creates text file
python runner export -d e95e9092c92e3440 (DONE)

9. Export specific content into specified file
python runner export -d e95e9092c92e3440 -f testing.txt (DONE)

######################
## Exporting solutions
######################

1. Export solutions into yaml file. Filename is not defined in command line. (DONE)
snippet export --solution

2. Export solutions into yaml file. Filename is defined in command line. (DONE)
snippet export --solution -f ./defined-solutions.yaml

3. Export solution based on message digest. Filename is defined in command line and in solution data. (DONE)
snippet export --solution -d a96accc25dd23ac0 -f ./defined-solutions.text

4. Export solution based on message digest. Filename not defined in solution data or in command line. (DONE)
snippet export --solution -d a96accc25dd23ac0

5. Export solution based on message digest. Filename is defined in solution data but not in command line. (DONE)
snippet export --solution -d a96accc25dd23ac0

6. Export solution based on message digest. Filename is not defined in command line or in solution data. (DONE)
snippet export --solution -d a96accc25dd23ac0

7. Export solution template to default file. (DONE)
snippy export --solution --template

snippy export --solution                                      # All solutions in default file solutions.yaml. (TESTED)
snippy export --solution -f ./file-s.txt                      # All solutions in file defined file in text format. (TESTED)
snippy export --solution -f ./file-s.text                     # All solutions in file defined file in text format. (TESTED)
snippy export --solution -f ./file-s.yaml                     # All solutions in file defined file in yaml format. (TESTED)
snippy export --solution -f ./file-s.json                     # All solutions in file defined file in json format. (TESTED)
snippy export --solution -f ./file-s.foo                      # Unknown file format results error and no export is made. (TESTED)

snippy export --solution -d ce6ef2f0408ff378                  # One content in file and format defined by content metadata. (TESTED)
snippy export --solution -d ce6ef2f0408ff378                  # One content in file and format by tool default when metadata is not set. (TESTED)
snippy export --solution -d a96accc25dd23ac0 -f ./file-s.txt  # One content in file always in text format. (TESTED)
snippy export --solution -d a96accc25dd23ac0 -f ./file-s.text # One content in file always in text format. (TESTED)
snippy export --solution -d a96accc25dd23ac0 -f ./file-s.yaml # One content in file always in yaml format. (TESTED)
snippy export --solution -d a96accc25dd23ac0 -f ./file-s.json # One content in file always in json format. (TESTED)
snippy export --solution -d a96accc25dd23ac0 -f ./file-s.foo  # Unknown file format results error and no export is made. (TESTED)

snippy export -d ce6ef2f0408ff378 # Export solution without defining the content category. (TESTED)
snippy export -d a96accc25dd23ac0 -f ./file-s.txt (TESTED)
snippy export -d a96accc25dd23ac0 -f ./file-s.text (TESTED)
snippy export -d a96accc25dd23ac0 -f ./file-s.yaml (TESTED)
snippy export -d a96accc25dd23ac0 -f ./file-s.json (TESTED)
snippy export -d a96accc25dd23ac0 -f ./file-s.foo

snippy export --solution --defaults                           # All solutions in yaml format into default location that stores the defaults. (TESTED)
snippy export --solution --template                           # Always just the template to solution-template.txt. (TESTED)


######################
## Importing snippet
######################

1. Import snippets from yaml file (DONE)
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py export --file ./snippets.yaml
python snip.py import --file ./snippets.yaml

2. Import snippets from json file (DONE)
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py export --file ./snippets.json
python snip.py import --file ./snippets.json

3. Import same snippet yaml file again (DONE)

4. Import snippet defaults: 1) python runner import -f defaults 2) python runner import --snippet -f defaults (DONE)

5. Import solution defaults: python runner import --solution -f defaults (DONE)

6. Import content from invalid file
python runner import -f foo.yaml (DONE)

7. Import content from unidentified file format (DONE)
python runner import -f foo.bar

8. Import content from text file (DONE)
python runner import -f foo.txt

9. Import content without specifying the file (that defaults to snippets.yaml or solutions.yaml) (DONE)
python runner import
python runner import --solution

10. Import text template with on solution (DONE)
python runner import -f solution.txt

11. Import text template with on snippet (DONE)
python runner import -f snippet.txt

12. Import template
python runner import --template
python runner import --solution --template
python runner import --snippet --template

13. Import defaults
python import --defaults (DONE)

14. Import templates without any changes
python import -f solution-template.txt (DONE)
python import -f snippet-template.txt (DONE)

15. Importing yaml file that contains snippet that is already stored. (DONE)

16. Import (update) specific content from file. The content category must be read automatically
python import -d e95e9092c92e3440 -f howto-debug-elastic-beats.txt # import content with category defaulting to snippet (DONE)
python import --solution -d e95e9092c92e3440 -f howto-debug-elastic-beats.txt (DONE)
python import --snippet -d e95e9092c92e3440 -f howto-debug-elastic-beats.txt (DONE)

######################
## Importing solution
######################

snippy import --solution                                      # Uses default file /solutions.yaml  (TESTED)
snippy import --solution -f ./all-solutions.yaml              # Import all solutions from yaml file (TESTED)
snippy import --solution -f ./all-solutions.json              # Import all solutions from json file (TESTED)
snippy import --solution -f ./all-solutions.txt               # Import all solutions from txt file (TESTED)
snippy import --solution -f ./all-solutions.text              # Import all solutions from txt file (TESTED)
snippy import --solution -f ./all-solutions.yaml              # Import solutions that are already imported
snippy import --solution -f ./all-solutions.yaml              # Import solutions where only one is new
snippy import -f ./all-solutions.yaml                         # Import all solutions without defining content category. (TESTED)
snippy import -f ./all-solutions.json (TESTED)
snippy import -f ./all-solutions.txt (TESTED)
snippy import -f ./all-solutions.text (TESTED)

snippy import --solution -f ./solution-template.yaml          # Import one content from yaml template (TESTED)
snippy import --solution -f ./solution-template.json          # Import one content from json template (TESTED)
snippy import --solution -f ./solution-template.txt           # Import one content from text template (TESTED)
snippy import --solution -f ./solution-template.text          # Import one content from text template (TESTED)
snippy import --solution -f ./foo.bar                         # Import one content from unknown file format (TESTED)

snippy import --solution -f ./solution-template.yaml -d 12345 # Import (update) one content from yaml template (TESTED)
snippy import --solution -f ./solution-template.json -d 12345 # Import (update) one content from json template (TESTED)
snippy import --solution -f ./solution-template.txt  -d 12345 # Import (update) one content from text template (TESTED)
snippy import --solution -f ./solution-template.text -d 12345 # Import (update) one content from text template (TESTED)
snippy import --solution -f ./solution-template.text -d 00000 # Import (update) one content with digest not found

snippy import --solution -f ./solution-template.txt   # Import solution template without any changes (TESTED)

snippy import --solution --defaults                   # Import solution defaults (TESTED)

snippy import --solution --template                   # Must produce error (TESTED)

########################
## Supplementary options
########################

1. Print version
python snip.py --version
python snip.py --v

2. Print help
python snip.py --help
python snip.py --h

3. Print truncated logs with -vv option
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container' -vv

4. Print full logs with --debug option
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container' --debug

5. Suppress all output with -q option
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container' -q

6. Print profiling results with --profile option
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container' --profile

7. Suppress ANSI characters with --no-ansi (DONE)

########################
## Security TODO
########################

         - [ ] Main: Document
               - [ ] Add generate SSL cert and key
                     - [ ] openssl req -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 365 -out domain.crt
                           // -nodes (no des) if you don't want to protect your private key with a passphrase
                           // -subj "/C=FI/ST=Helsinki/L=Portland/O=Company Name/OU=Org/CN=www.snippy.com" // localhost how?
         - [ ] Main: Configure server
               - [ ] Add --jws-secret-key <secret>  // do not store in server. Do not add --secured because other params can be used to find this.
               - [ ] Add --jws-public-key <key>  // do not store in server. Do not add --secured because other params can be used to find this.
               - [ ] Add --jws-private-key <key>  // do not store in server. Do not add --secured because other params can be used to find this.
               - [ ] Add --jws-expire-secs <seconds>
               - [ ] Add check which generates security log if the request was not over HTTPS when --secured is not used. When it is used, reject request.
               - [ ] Add paths
                     /snippy/api/admin/v1/settings [server settings]
                     /snippy/api/admin/v1/users    [server users]
                     /snippy/api/auth/v1           [user authentication]
         - [ ] Main: Register new user
               - [ ] Add /snippy/api/admin/v1/users to create new user.
               - [ ] Add user table with uuid and hashed password
               - [ ] Add hash_password and verify password
         - [ ] Main: Authenticate registered user with JWT (or simple session ID?)
               - [ ] http://cryto.net/~joepie91/blog/2016/06/13/stop-using-jwt-for-sessions/ Simple is better?
               - [ ] Add /snippy/api/auth/v1 for authentication
               - [ ] Session ID
                     - [ ] sessionIdCookie_v1 = username ":" SHA256(username + global salt)
               - [ ] Add Authentication with JWT.
                     - [x] JWS is simpler https://tools.ietf.org/html/rfc7519
                           - [ ] Tokens have size limit.
                           - [ ] Tokens cannot be revoked.
                           - [ ] This requires tokens to have a short expiration --> use cookies.
                           - [ ] Authorization: Bearer <token>
                           - [ ] Use import jwt
                           - [ ] https://auth0.com/blog/ten-things-you-should-know-about-tokens-and-cookies/
                           - [x] https://www.youtube.com/watch?v=oXxbB5kv9OA
                                    header {'typ': JWT, 'alg': 'hash alg'}
                                    claims {'iss': 'Snippy', 'exp': 'expiration', 'iat': 'issued at time'} #  Do not add user name for security https://stormpath.com/blog/jwt-the-right-way
                                    s = base64encode(header) + '.' + base64encode(payload)
                                    signature = hashAlgHs256(s, 'secret')
                                    jwt = s + '.' base64encode(signature)

                                    Request token --> user/password                               Enforce HTTPS
                                                                                                  check credentials
                                                                                                  create JWT token
                                                  <-- JWT or error in cookie to expire
                           - [ ] Encrypted or not
                           - [ ] https://github.com/jhildreth/falcon-jwt-checker/tree/master/falcon_jwt_checker
                           - [ ] https://github.com/jpadilla/pyjwt
                           - [ ] https://github.com/loanzen/falcon-auth
                           - [ ] "symmetric algorithms such as HS256, you will have only a single key to be used to sign and verify the signature."
                           - [ ] "If you consider asymmetric algorithms such as RS256, you will have a private and a public key. "
                           - [ ] Add HS256
                           - [ ] RS256
                           - [ ] Add How can I extract a public / private key from a x509 certificate https://pyjwt.readthedocs.io/en/latest/faq.html
                           - [ ] JWT JTI can prevent replay attack mut it makes server stateful. It works so that user is stored and has unique JTI, When user complains, the JTI is generated again for removed user. https://security.stackexchange.com/a/106375
               - [ ] Add generate_auth_token for JSON Web tokens
         - [ ] Main: Do we need to store sessions because authentication tokens?
               - [ ] Add new table for sessions?
               - [ ] Use same table as for user?

########################
## Make container with
########################

Build language: python
Build group: stable
Build dist: trusty
Build id: 311339532
Job id: 311339534
Runtime kernel version: 4.4.0-93-generic
travis-build version: 97c4a12f8
Build image provisioning date and time
Tue Aug 29 02:48:34 UTC 2017
Operating System Details
Distributor ID:	Ubuntu
Description:	Ubuntu 14.04.5 LTS
Release:	14.04
Codename:	trusty


####
2018-05-03 10:15:51.361 snippy[11276] [d] [352ebe6a]: config source sorted fields: ('brief', '-created')
2018-05-03 10:15:51.361 snippy[11276] [d] [352ebe6a]: config source internal format for sorted fields: {'order': [1, 9], 'value': {1: False, 9: True}}

DESC --> '-'
ASC  --> ''

sort = OrderedDict()

{'brief': DESC,
 'created': ASC}


¿/defects?offset=5&limit=5	# 	Returns defects 6..10.
¿/defects?offset=10	Returns defects 11..36 (the default number of the returned defects is 25).

1. You can request ¿/defects?limit=0 to get just metadata, without defect data.
2. When the response doesn¿t contain a link to the next page of results, you know that you¿ve reached the end.

# From start
"meta": {
    "count":  5,
    "offset":10,
    "limit":  5,
    "total": 32
},

# Mixed offset and count for prev
"meta": {
    "count": 10,
    "offset": 5,
    "limit": 10,
    "total": 32
},
"data": {},
"links": {
    "self": "http://example.com/articles?limit=5&offset=10",
    "first": "http://example.com/articles?limit=5&offset=0",
    "prev": "http://example.com/articles?limit=5&offset=5",
    "next": "http://example.com/articles?limit=5&offset=15",
    "last": "http://example.com/articles?limit=5&offset=30",
}

# SQL
https://stackoverflow.com/a/5742289
ORDER BY rating DESC, name ASC
LIMIT <count> OFFSET <skip>

ORDER BY rating DESC, name ASC LIMIT <count> OFFSET <skip>

"links":{"self":"URL?limit=5&offset=10","first":"URL?limit=5&offset=0","prev":"URL?limit=5&offset=5","next":"URL?limit=5&offset=15","last":"URL?limit=5&offset=30",}

====
# Manipulate compressed tar files @linux

> This is a very long testing description that is supposed to extend to several lines in
order to test how this goes in Markdown.

>

- Compress folder excluding the tar.

    `$ tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./`

- List content of compressed tar.

    `$ tar tvf mytar.tar.gz`

- Cat file in compressed tar.

    `$ tar xfO mytar.tar.gz manifest.json`

- Extract and exclude one file.

    `$ tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"`

- Extract only one file.

    `$ tar -xf mytar.tar.gz manifest.json`

## Meta

> category : snippet
created  : 2018-05-07T11:13:17.000001+0000
digest   : b890ba7be5c03b2008aa2160d34d14f651f22eb6f319df2ac06837c01bcf68e1
filename :
name     :
source   :
tags     : howto,linux,tar,untar
updated  : 2018-11-11T10:51:33.675848+0000
uuid     : f21c8ed8-8830-11e8-a114-2c4d54508088
versions :
=====
