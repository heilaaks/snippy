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
make docs
make lint
make test
time python snip.py create -c 'docker rm' -b 'Remove all docker containers' -g 'moby' -t docker,container,cleanup --debug
python snip.py search --sall docker

python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -f dangling=true -q)' -b 'Remove all dangling image layers' -g 'docker' -t docker,images,dangling,cleanup -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py search --sall docker
python snip.py delete --digest 6b8705255016268c
python snip.py export --file snippets.yaml
python snip.py export --file snippets.json
python snip.py export --file snippets.txt
python snip.py import --file snippets.yaml
python snip.py import --file snippets.json
python snip.py import --file snippets.txt
python snip.py update -d 6b8705255016268c
python snip.py create


=====================================================
## Test Plan for work flows
=====================================================

########################
## Creating new snippets
########################

1. Create snippet from command line with all parameters
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

####################
## Updating snippets
####################

1. Update snippet content with only mandatory parameters with digest
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

####################
## Deleting snippets
####################

1. Delete snippet with digest
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py delete --digest 22c0ca5bbc9797b

2. Delete snippet with unknown digest
python snip.py create -c 'docker rm -v $(docker ps -a -q)' -b 'Remove all docker containers' -g 'docker' -t docker,container,cleanup -l 'https://askubuntu.com/questions/574163/how-to-stop-and-remove-a-docker-container'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'moby' -t moby,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py delete --digest 111111111111111

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

######################
## Exporting snipppets
######################

1. Export all snippets into yaml file
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

######################
## Importing snipppets
######################

1. Import snippets from yaml file
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

================================================

python snip.py create -c 'docker rmi $(docker images -f dangling=true -q)' -b 'Remove all dangling image layers' -g 'docker' -t docker,images,dangling,cleanup -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rmi $(docker images -a -q)' -b 'Remove all docker images' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes'
python snip.py create -c 'docker rm --force redis' -b 'Remove docker image with force' -g 'docker' -t docker,images,remove -l 'https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes https://docs.docker.com/engine/reference/commandline/rm/'
python snip.py search --sall docker
python snip.py delete --digest 6b8705255016268c
python snip.py export --file snippets.yaml
python snip.py export --file snippets.json
python snip.py export --file snippets.txt
python snip.py import --file snippets.yaml
python snip.py import --file snippets.json
python snip.py import --file snippets.txt
python snip.py update -d 6b8705255016268c
python snip.py create


=====================================================

=====================================================
## Logging
https://www.relaxdiego.com/2014/07/logging-in-python.html
=====================================================

## Documens - generated document for MT
https://stackoverflow.com/questions/7250659/python-code-to-generate-part-of-sphinx-documentation-is-it-possible


=====================================================
###### Command line desing
https://softwareengineering.stackexchange.com/questions/307467/what-are-good-habits-for-designing-command-line-arguments
subparsers https://stackoverflow.com/questions/23304740/optional-python-arguments-without-dashes-but-with-additional-parameters
https://www.gnu.org/prep/standards/standards.html#g_t_002d_002dhelp
http://docopt.org/
http://www.tldp.org/LDP/abs/html/standard-options.html
=====================================================

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


