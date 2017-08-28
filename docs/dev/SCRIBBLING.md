# Development Scibbling

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
   # Installing
   $ mkvirtualenv snippy
   $ pip3 install .
   $ pip3 install -e .[dev] # Development packages.
   ```

   ```
   # Example commands for the Python virtualenvwrapper.
   $ lssitepackages
   $ lsvirtualenv
   $ deactivate
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

## Bling

http://tjelvarolsson.com/blog/five-steps-to-add-the-bling-factor-to-your-python-package/

## Travis CI and tooling

Add '[ci skip]' to commitlog in order to prevent the CI build.

https://landscape.io/dashboard
https://travis-ci.org/heilaaks/snippy
https://codecov.io/gh/heilaaks/snippy
https://landscape.io/github/heilaaks/snippy
http://snippy.readthedocs.io/en/latest/

## Documents

Good set on loggers: https://books.google.fi/books?id=7U1CIoOs5AkC&pg=PA357&lpg=PA357&dq=Should+I+use+root+or+logger+or+module+name+logger&source=bl&ots=eNYyAjE-IP&sig=MPee2BYjTYu4epc2NlESCG0x3so&hl=en&sa=X&ved=0ahUKEwiylOaLhunVAhXDK5oKHWSaCn04ChDoAQhGMAY#v=onepage&q=Should%20I%20use%20root%20or%20logger%20or%20module%20name%20logger&f=false

## Devel

cd devel/snippy
workon snippy
make doc
make lint
make test
time python snip.py -i 'docker rm' -b 'Remove all docker containers' -c 'docker' -t docker,container,cleanup --debug
python snip.py -s docker

python snip.py -i 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -c 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py -i 'docker rmi $(docker images -f dangling=true -q)' -b 'Remove all dangling image layers' -c 'docker' -t docker,images,dangling,cleanup -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py -i 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -c 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py -i 'docker rm --force redis' -b 'Remove docker image with force' -c 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py -s docker
python snip.py -j delete -r snippet --id 1
python snip.py -j export -r snippet --file snippets.yaml
python snip.py -j export -r snippet --file snippets.json
python snip.py -j export -r snippet --file snippets.txt
python snip.py -j import -r snippet --file snippets.yaml
python snip.py -j import -r snippet --file snippets.json
python snip.py -j import -r snippet --file snippets.txt
python snip.py -r snippet -j update -id 6b8705255016268c
python snip.py -r snippet -j create


###### Command line desing
https://softwareengineering.stackexchange.com/questions/307467/what-are-good-habits-for-designing-command-line-arguments
subparsers https://stackoverflow.com/questions/23304740/optional-python-arguments-without-dashes-but-with-additional-parameters
==================================================================
usage: snippy [--version] [--help] [--debug] [-v] [-vv]
       <command> [<options>] [<arguments>]

COMMANDS: create, search, update, delete, export, import

OPTIONS:
    -e, --editor            use default editor for editing
    -d, --digest DIGEST     message digest to identify
    -f, --file FILE         file input for command
    -c, --content           optional snippet content
    -b, --brief             optional snippet description
    -c, --category          single optional category for snippet
    -t, --tags              optional comma separated tags
    -l, --links             optioanl links separated by '>'
    --stag                  search only from tags
    --scat                  search only from categories

ARGUMENTS:
    snippet, resolve

SYMBOLS:
    $   command
    >   url
    #   tags
    @   category

EXAMPLES:
    Create new snippet with default editor.
      $ python snip.py create snippet

    Search snippet with keyword list.
      $ python snip.py search docker,moby

    Delete snippet with message digest.
      $ python snip.py delete -d 2dcbecd10330ac4d

==================================================================

# Basic options
python snip.py --version
python snip.py --help
python snip.py -v
python snip.py -vv
python snip.py --debug

python snip.py create [--] <snippet>                             # Defaults to snippet and starts editor
python snip.py create [--] <resolve>                             # Starts editor
python snip.py create -e|--editor [--] <snippet>                 # Defaults to snippet
python snip.py create -e|--editor [--] <resolve>                 # Defaults to snippet
python snip.py create -f|--file FILE <snippet>
python snip.py create -f|--file FILE <resolve>
python snip.py create -c|--content CONTENT -b|--brief BRIEF -c|--category CATEGORY -t|--tags [TAGS] -l|--links [LINKS] [--] <snippet> # Only for snippet
python snip.py update -d|--digest DIGEST                         # Starts editor. Does not need type since trust digest always different.
python snip.py update -d|--digest DIGEST -e|--editor
python snip.py update -d|--digest DIGEST -f|--file FILE
python snip.py delete -d|--digest DIGEST
python snip.py search KEYWORDS [<snippet>] [<resolve>]
python snip.py search --stag [--] <keywords> [<snippet>] [<resolve>]
python snip.py search --scat [--] <keywords> [<snippet>] [<resolve>]
python snip.py export -f|--file FILE
python snip.py export -d|--digest DIGEST
python snip.py import -f|--file FILE
=====================================================

pylint --rcfile tests/pylint/pylint-snippy.rc ./snippy
pylint --rcfile tests/pylint/pylint-snippy-tests.rc ./tests
pytest --cov=snippy tests/
pytest --cov=snippy --cov-report html tests/
make -C docs html
python snip.py -i 'docker rm $(docker ps -a -q)' -b 'Remove all docker containers' -c 'docker' -t docker,container,cleanup
python snip.py -i 'docker rm $(docker ps -a -q)' -b 'Remove all docker containers' -c 'docker' -t docker, container, cleanup
pytest

   > file:///home/heilaaks/devel/snippy/htmlcov/index.html
   > file:///home/heilaaks/devel/snippy/docs/build/html/index.html

# Run single test
pytest tests/test_arguments_add_new_snippet.py -k test_tags_with_quotes_and_separated_by_comma_and_space

### Editor input
# Commented lines will be ignored.
#
# Add mandatory snippet below.
docker rm --force redis
docker rmi redis
docker rmi zookeeper

# Add optional brief description below.
Remove docker image with force

# Add optional single category below.
docker

# Add optional comma separated list of tags below.
docker,images,remove

# Add optional links below one link per line.
https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes
https://docs.docker.com/engine/reference/commandline/rm/
