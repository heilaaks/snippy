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
   # Installing for Python 3
   $ mkvirtualenv snippy
   $ pip3 install .
   $ pip3 install -e .[dev] # Development packages.
   ```

   ```
   # Installing for Python 2.7
   $ pip2 install virtualenvwrapper
   $ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2    # Add to ~/.bashrc
   $ mkvirtualenv snippy-python27
   $ workon snippy-python27
   $ pip install -e .[dev]
   $ sudo dnf install redhat-rpm-config
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
## Security
#######################################

    # File security
    > https://security.openstack.org/guidelines/dg_using-temporary-files-securely.html

    # Codeclimate
    > https://codeclimate.com

#######################################
## PyPI
#######################################


    # Testing
    python setup.py register -r testpypi
    python setup.py sdist upload -r testpypi
    sudo pip install --index-url https://test.pypi.org/simple/ snippy
    sudo pip uninstall snippy
    pip3 install --user --index-url https://test.pypi.org/simple/ snippy
    pip3 uninstall snippy

    # Release
    $ git tag -a v0.1.0 -m "Experimental alpha release"
    $ git push -u origin master
    $ python setup.py sdist # Build
    $ twine register dist/snippy-0.1.0.tar.gz
    $ twine upload dist/*
    $ python setup.py sdist upload -r pypi
    $ python setup.py sdist

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
    $ docker login docker.io
    $ docker tag <image-hash> docker.io/<docker-hub-user-id>/<name>
    $ docker push docker.io/<docker-hub-user-id>/<name>
    
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
        A) Arguments()
        B) Editor()

    6. Only Storage(), Snippet() and Solution() can import Content()
    
    7. Only Storage() can import Sqlite3db()
    
    8. Content() is designed to be used by Snippet() and Solution(). It is not designed to abstract
       or hide Snippet() or Solution() classes.


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

6. Update snippet with unknown digest
python snip.py update --digest 111111111111111

7. Update snippet with unknown content
python snip.py update -c '111111111111111'

8. Update snippet by defining solution category in command line (DONE)
python snip.py update --solution -d 22c0ca5bbc9797b

9. Update solution by leaving the category out (defaults snippet) from command line
python snip.py update -d 22c0ca5bbc9797b

####################
## Deleting snippets
####################

1. Delete snippet with digest (DONE)
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py delete --digest 22c0ca5bbc9797b

2. Delete snippet with unknown digest
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py delete --digest 111111111111111

3. Test deleting snippets with content that is found

4. Test deleting snippets with content that is not found

5. Test that empty digest does not delete snippet when there is only one snippet

6. Test that deleting snippet requires at least 16 character hash to make sure that user does not accidentally use e.g. '2' that would delete all snippets which hash is starting with '2'.

#####################
## Searching snippets
#####################

1. Search snippets from all fields
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
## Importing content
######################

1. Import snippets from yaml file (DONE)
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py export --file ./snippets.yaml
python snip.py import --file ./snippets.yaml

2. Import snippets from json file
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py export --file ./snippets.json
python snip.py import --file ./snippets.json

3. Import same snippet yaml file again

4. Import snippet defaults: 1) python runner import -f defaults 2) python runner import --snippet -f defaults

5. Import solution defaults: python runner import --solution -f defaults

6. Import content from invalid file
python runner import -f foo.yaml

7. Import content from unidentified file format
python runner import -f foo.bar

8. Import content from text file (not supported)
python runner import -f foo.txt

9. Import content without specifying the file (that defaults to snippets.yaml or solutions.yaml)
python runner import
python runner import --solution

10. Import text template with on solution
python runner import -f solution.txt

11. Import text template with on snippet
python runner import -f snippet.txt

12. Import template
python runner import --template
python runner import --solution --template
python runner import --snippet --template

13. Import defaults
python import --defaults

14. Import templates without any changes
python import -f solution-template.txt
python import -f snippet-template.txt

15. Importing yaml file that contains snippet that is already stored. (DONE)

16. Import (update) specific content from file. The content category must be read automatically
python import -d e95e9092c92e3440 -f howto-debug-elastic-beats.txt # import content with category defaulting to snippet
python import --solution -d e95e9092c92e3440 -f howto-debug-elastic-beats.txt
python import --snippet -d e95e9092c92e3440 -f howto-debug-elastic-beats.txt

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
