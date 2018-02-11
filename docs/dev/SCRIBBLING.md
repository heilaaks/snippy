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
   $ source /usr/bin/virtualenvwrapper.sh                # Add to ~/.bashrc
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
   $ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2    # Add to ~/.bashrc
   $ mkvirtualenv snippy-python27
   $ workon snippy-python27
   $ pip install -e .[dev]
   $ sudo dnf install redhat-rpm-config
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
   # Running container tests. These containers try to mimic
   # Travis CI test environment.
   $ sudo docker build -f tests/docker/Dockerfile-Python34-jessie -t snippy/python34-jessie .
   $ sudo docker build -f tests/docker/Dockerfile-Python34-trusty -t snippy/python34-trusty .
   $ sudo docker run -d snippy/python34-jessie
   $ sudo docker run -d snippy/python34-trusty
   $ sudo docker exec -it $(sudo docker ps | egrep -m 1 'snippy/python34-jessie' | awk '{print $1}') /bin/bash
   $ sudo docker exec -it $(sudo docker ps | egrep -m 1 'snippy/python34-trusty' | awk '{print $1}') /bin/bash
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
   $ make docker
   $
   $ sudo docker run heilaaks/snippy search --sall .
   $ vi ~/.bashrc
     alias snippy-d='sudo docker run heilaaks/snippy'
   $ source ~/.bashrc
   $ snippy-d search --sall .
   ```

   ```
   ## Programming style guide.
   # Commit log
   > http://keepachangelog.com/en/1.0.0/
   ```

   ```
   # Why this slows down and starts to consume huge amount of cpu and stalls all cases=
   # The problem is the order of sys.argv that was after the Snippy object was created.
   import sys
   import unittest
   import mock
   import pytest
   from snippy.snip import Snippy
   from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


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

http://tjelvarolsson.com/blog/five-steps-to-add-the-bling-factor-to-your-python-package/

    # Recoding
    > http://linuxbrew.sh/
    > https://asciinema.org/
    $ sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
    $ /home/linuxbrew/.linuxbrew/bin/brew install asciinema
    $ export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin

    asciinema rec snippy.json
    snippy --help
    snippy search --sall .
    snippy import --defaults
    snippy import --solution --defaults
    snippy search --sall elastic
    snippy search --solution --sall kafka | grep -Ev '[^\s]+:'
    snippy export -d ec11663bee073799
    ll
    snippy import -d ec11663bee073799 -f kubernetes-docker-log-driver-kafka.txt
    snippy search --solution --sall . | grep -Ev '[^\s]+:'
    ctrl-d
    https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO

## Travis CI and tooling

Add '[ci skip]' to commitlog in order to prevent the CI build.

https://landscape.io/dashboard
https://travis-ci.org/heilaaks/snippy
https://codecov.io/gh/heilaaks/snippy
https://landscape.io/github/heilaaks/snippy
http://snippy.readthedocs.io/en/latest/

## Documents

Good set on loggers: https://books.google.fi/books?id=7U1CIoOs5AkC&pg=PA357&lpg=PA357&dq=Should+I+use+root+or+logger+or+module+name+logger&source=bl&ots=eNYyAjE-IP&sig=MPee2BYjTYu4epc2NlESCG0x3so&hl=en&sa=X&ved=0ahUKEwiylOaLhunVAhXDK5oKHWSaCn04ChDoAQhGMAY#v=onepage&q=Should%20I%20use%20root%20or%20logger%20or%20module%20name%20logger&f=false

#######################################
## Server
#######################################

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
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/v1/"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/v1/hello"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker&limit=20" -H "accept: application/json"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker,filebeat&limit=20" -H "accept: application/json"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets/a516e2d6f8aa5c6f" -H "accept: application/json"
    $ curl -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets/a516e2d6f8aa5c6f" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker,filebeat&limit=2" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker,filebeat&limit=20" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker,filebeat&limit=10&sort=brief&sort=-utc" -H "accept: application/json" | python -m json.tool
    $ curl -s -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker,filebeat&limit=20&sort=brief&fields=brief,group" -H  "accept: application/json" | python -m json.tool

    # Fix multiple fields
    $ curl -X GET "https://app.swaggerhub.com/api/v1/snippets?sall=docker&sall=filebeat&sort=data&fields=data&fields=brief&fields=group" -H  "accept: application/json"

    # Testing with Dredd
    > http://dredd.org/en/latest/quickstart.html
    $ sudo yum install nodejs
    $ sudo npm install -g dredd
    $ dredd snippy/data/openapi/swagger-2.0.yml http://127.0.0.1:8080
    $ dredd snippy/data/openapi/swagger-2.0.yml http://127.0.0.1:8080 --dry-run
    $ dredd snippy/data/openapi/swagger.yml http://127.0.0.1:8080 --dry-run

    $ curl -X POST "http://127.0.0.1:8080/snippy/api/v1/snippets" -H "Content-Type: application/json" -d '{}'
    $ curl -X POST "http://127.0.0.1:8080/snippy/api/v1/snippets" -H "Content-Type: application/json" -d '{"data":"occaecat veniam aliqua","links":["et dolore ipsum reprehenderit","cupidatat","Lorem aliquip quis dolor cillum","non quis adipisicing sunt esse","in"],"versions":"irure nulla laborum Duis"}'
    $ curl -X POST "http://127.0.0.1:8080/snippy/api/v1/snippets" -H "Content-Type: application/vnd.api+json" -d '{"data":"occaecat veniam aliqua","links":["et dolore ipsum reprehenderit","cupidatat","Lorem aliquip quis dolor cillum","non quis adipisicing sunt esse","in"],"versions":"irure nulla laborum Duis"}'

#######################################
## Devel
#######################################

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

#######################################
## Logging
#######################################

    > https://www.relaxdiego.com/2014/07/logging-in-python.html


#######################################
## Logging
#######################################

    # Documens - generated document for MT
    > https://stackoverflow.com/questions/7250659/python-code-to-generate-part-of-sphinx-documentation-is-it-possible


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

    # Release Wheels instead of Egg next time. Try the below:
    > https://packaging.python.org/discussions/wheel-vs-egg/
    > https://packaging.python.org/tutorials/distributing-packages/
    $ python setup.py sdist
    $ python setup.py bdist_wheel --universal
    $ twine upload dist/*

    # Release PyPI (deprecated use universal wheel)
    > https://pypi.org/project/snippy/
    $ git tag -a v0.6.0 -m "Bug fixes and testing"
    $ git push -u origin v0.6.0
    $ python setup.py sdist # Build source distribution
    $ twine register dist/snippy-0.6.0.tar.gz
    $ twine upload dist/*

    # Push docker hub with Fedora
    $ su
    $ docker rm $(docker ps --all -q -f status=exited)
    $ docker rmi 0b4881af2b2d
    $ sudo docker login docker.io
    $ docker tag <image-hash> docker.io/<docker-hub-user-id>/<name>
    $ docker push docker.io/<docker-hub-user-id>/<name>
    $ sudo docker tag 0b4881af2b2d docker.io/heilaaks/snippy:v0.6.0
    $ sudo docker tag 0b4881af2b2d docker.io/heilaaks/snippy:latest
    $ sudo docker push docker.io/heilaaks/snippy:v0.6.0
    $ sudo docker push docker.io/heilaaks/snippy:latest

    # Pull
    $ docker pull heilaaks/snippy:v0.6.0
    $ docker pull heilaaks/snippy:latest

#######################################
## PyPI
#######################################


    # Testing
    $ python setup.py sdist # Build source distribution
    $ python setup.py sdist upload -r testpypi
    sudo pip install --index-url https://test.pypi.org/simple/ snippy
    sudo pip uninstall snippy
    pip3 install --user --index-url https://test.pypi.org/simple/ snippy
    pip3 uninstall snippy

    # Release
    $ git tag -a v0.5.0 -m "Experimental beta release"
    $ git push -u origin v0.5.0
    $ python setup.py sdist # Build source distribution
    $ twine register dist/snippy-0.5.0.tar.gz
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


    # Class hierarchy design notes

    1. Any class can import Constants()

    2. Any class can import Logger()

    3. Any class can import Cause()

    4. Migrate() should be kept in state where anyone can import it.

    5. Only the Config() can import and imported classes must not import outside config sub-package.
        A) Cli()
        B) Editor()

    6. Only Storage(), Snippet() and Solution() can import Content()

    7. Only Storage() can import Sqlite3db()

    8. Content() is designed to be used by Snippet() and Solution(). It is not designed to abstract
       or hide Snippet() or Solution() classes.

#######################################
## Design decisions
#######################################

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

    4. Logs from exceptions are printed in INFO level all other logs in DEBUG

       Controlled logs from exception must be printed with INFO level. All other
       logs must be printed in DEBUG level.

    5. Variables printed in logs are seprated with colon

       When variables are printed in logs, they must be separated with colon
       like in the example output below:

         > ... config source category: snippet

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
       of change types from /2/.
       
       The explicit change types in commit log header are from /2/:
       
         1. 'Add' for new features.
         2. 'Change' for changes in existing functionality.
         3. 'Deprecat' for soon-to-be removed features.
         4. 'Remove' for now removed features.
         5. 'Fix' for any bug fixes.
         6. 'Security' in case of vulnerabilities.

       The rule must be applied so that the logs are written for humans. This means
       that the commit log must tell the reasons and design decisions behind the
       change.

       This rule tries to force common look and feel for the commit logs.

       /1/ https://chris.beams.io/posts/git-commit/
       /2/ http://keepachangelog.com/en/1.0.0/

    CONTENT

    1. The tool must know if specific parameters were given

       The tool must be aware if specific parameters were give at all. These
       parameters are:

         - data
         - digest
         - sall
         - stag
         - sgrp

       The default value for these parameters must be None or the must not
       exist in the parameter set that is give for set_conf in class inherited
       from ConfigSourceBase().

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
    
       /1/ http://jsonapi.org/

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
python snip.py export --snippet  # Creates snippets.yaml
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
