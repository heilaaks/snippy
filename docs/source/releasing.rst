Releasing
---------

The are two make targets for release. The ``prepare-release`` runs all tests
and compiles the release packages. The ``release-upload`` will upload the new
release.

The release steps that are automated in Makefile are documented here.

This is a semi automated release process that is not completed. Some of the
steps must be executed manually as instructed below.

Preparations
~~~~~~~~~~~~

.. code-block:: text

    # Remove existing virtual environments.
    deactivate > /dev/null 2>&1
    for VENV in $(lsvirtualenv -b | grep snippy-py)
    do
        printf "delete snippy venv ${VENV}\033[37G: "
        rmvirtualenv ${VENV} > /dev/null 2>&1
        printf "\033[32mOK\033[0m\n"
    done

    # Upgrade CPython and PyPy versions.
    sudo dnf upgrade -y \
        python27 \
        python34 \
        python35 \
        python36 \
        python37 \
        python38 \
        python3-devel \
        python2-devel
    sudo dnf upgrade -y \
        pypy2 \
        pypy3 \
        pypy2-devel \
        pypy3-devel \
        postgresql-devel

    # Upgrade Python virtual environments.
    pip3 install --user --upgrade \
        pipenv \
        virtualenv \
        virtualenvwrapper

    # Create virtual environments.
    for PYTHON in python2.7 \
                  python3.4 \
                  python3.5 \
                  python3.6 \
                  python3.7 \
                  python3.8 \
                  pypy \
                  pypy3
    do
        if which ${PYTHON} > /dev/null 2>&1; then
            printf "create snippy venv for ${PYTHON}\033[37G: "
            mkvirtualenv --python $(which ${PYTHON}) snippy-${PYTHON} > /dev/null 2>&1
            if [[ -n "${VIRTUAL_ENV}" ]]; then
                printf "\033[32mOK\033[0m\n"
            else
                printf "\e[31mNOK\033[0m\n"
            fi
            deactivate > /dev/null 2>&1
        fi
    done

    # Install virtual environments.
    for VENV in $(lsvirtualenv -b | grep snippy-py)
    do
        workon ${VENV}
        printf "deploy snippy venv ${VENV}\033[37G: "
        if [[ ${VIRTUAL_ENV} == *${VENV}* ]]; then
            make upgrade-wheel PIP_CACHE=--no-cache-dir
            make install-devel PIP_CACHE=--no-cache-dir
            printf "\033[32mOK\033[0m\n"
        else
            printf "\e[31mNOK\033[0m\n"
        fi
        deactivate > /dev/null 2>&1
    done

    # Prune Docker containers.
    sudo docker rm $(docker ps --all -q -f status=exited)
    sudo docker rm $(docker ps --all -q -f status=exited)

    # Start PostgreSQL.
    sudo docker stop postgres
    sudo docker rm postgres
    sudo docker run -d --name postgres -e POSTGRES_PASSWORD= -p 5432:5432 -d postgres  # Wait untill the database is up!

    # workon with the Python3.7 virtual environment
    workon snippy-python3.7

    # Set the current development version and the new tagged versions in Makefile.
    DEV_VERSION := 0.11a0
    TAG_VERSION := 0.12.0

    # Run release preparations.
    make prepare-release

    # Update Python setuptools, wheels and Twine.
    make upgrade-wheel V=1 QUIET=

    # Update version numbers in project. This target fails if
    # there are development versions found.
    make upgrade-tool-version V=1 QUIET=

    # Manually grep versions to make sure that the script worked.
    grep -rn -e 0.11.0 ./

Run tests with PyPy
~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # Example installation for Fedora 28.
      make clean
      make clean-db
      dnf install pypy3
      dnf install pypy3-devel
      dnf install postgresql-devel
      make upgrade-wheel PYTHON=pypy3
      make install-devel PYTHON=pypy3
      pypy3 -m ensurepip
      pypy3 -m pip install --upgrade pip setuptools wheel
      pypy3 -m pip install --editable .[devel]
      pypy3 -m pytest -x ./tests/test_*.py --cov snippy -m "server"
      pypy3 runner --help
      pypy3 runner import --defaults --scat all
      pypy3 runner --server-host 127.0.0.1:8080 --defaults -vv
      curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?limit=4" -H "accept: application/vnd.api+json"

Run tests with PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # The test-all target runs test with Sqlite and PostgreSQL.
      docker run -d --name postgres -e POSTGRES_PASSWORD= -p 5432:5432 -d postgres  # Wait untill the database is up!
      make clean
      make clean-db
      make test-all
      make test-postgresql

Run tests with HTTP server
~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # Generate TLS sertificates for server.
      openssl req -x509 -newkey rsa:4096 -nodes -keyout server.key -out server.crt -days 356 -subj "/C=US/O=Snippy/CN=127.0.0.1"
      python runner server --server-host 127.0.0.1:8080 --defaults -vv --server-ssl-cert ./server.crt --server-ssl-key ./server.key
      curl -k -s -X GET "https://127.0.0.1:8080/api/snippy/rest/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"

Test local installation
~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      make clean
      make clean-db
      pip uninstall snippy -y
      pip install .
      snippy --help
      snippy search --sall .
      snippy import --defaults
      snippy import --defaults --scat solution
      snippy import --defaults --scat reference
      snippy search --sall docker
      rm -f ${HOME}/devel/temp/snippy.db
      snippy import --defaults --storage-path ${HOME}/devel/temp
      snippy import --defaults --scat solution --storage-path ${HOME}/devel/temp
      snippy import --defaults --scat reference --storage-path ${HOME}/devel/temp
      snippy --server-host 127.0.0.1:8080 --storage-path ${HOME}/devel/temp &
      curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?limit=4" -H "accept: application/vnd.api+json"
      pkill snippy

Test docker installation
~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # Compile docker image.
      su
      make clean
      make clean-db
      docker rmi --force $(docker images --filter=reference="*/snippy*:*" -q)
      docker rm $(docker ps --scat all -q -f status=exited)
      docker images -q --filter dangling=true | xargs docker rmi
      docker images
      make docker

      # Run CLI commands with docker image.
      docker run --rm --env SNIPPY_LOG_JSON=0 heilaaks/snippy --help
      docker run --rm --env SNIPPY_LOG_JSON=0 heilaaks/snippy search --sall docker

      # Run server with Sqlite database.
      docker run -d --publish=127.0.0.1:8080:32768/tcp --name snippy heilaaks/snippy --defaults -vv
      curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker logs snippy
      docker stop snippy
      docker rm snippy
      docker run --env SNIPPY_SERVER_HOST=127.0.0.1:8080 --net=host --name snippy --detach heilaaks/snippy --debug
      curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker logs snippy
      docker stop snippy
      docker rm snippy

      # Login into Docker image (requires change to Dockerfile).
      docker run -d --publish=127.0.0.1:8080:32768/tcp --name snippy heilaaks/snippy --defaults -vv
      docker exec -it snippy /bin/sh
      cd /
      du -ah | sort -n -r | head -n 50
      find / -name '*pycache*'
      exit
      docker stop snippy
      docker rm snippy

      # Run server with PostgreSQL database.
      docker run -d --net="host" --env SNIPPY_SERVER_HOST=127.0.0.1:8080 --name snippy heilaaks/snippy --storage-type postgresql --storage-host localhost:5432 --storage-database postgres --storage-user postgres --storage-password postgres --defaults -vv
      curl -s -X POST "http://127.0.0.1:8080/api/snippy/rest/snippets" -H "accept: application/vnd.api+json; charset=UTF-8" -H "Content-Type: application/vnd.api+json; charset=UTF-8" -d '{"data":[{"type": "snippet", "attributes": {"data": ["docker ps"]}}]}'
      curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker logs snippy
      docker stop snippy
      docker rm snippy

      # Login to container to see security hardening and size.
      docker run -d --publish=127.0.0.1:8080:32768/tcp --name snippy heilaaks/snippy --defaults -vv
      docker exec -it snippy /bin/sh
      find / -perm +6000 -type f -exec ls -ld {} \;
      find / -perm +6000 -type f -exec chmod a-s {} \; || true # Check defang -> Should return zero files.
      du -a -h / | sort -n -r | head -n 20
      exit

Create new asciinema
~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # pip uninstall snippy --yes
      deactivate
      pip uninstall snippy --yes
      make clean-all
      make install

      # Clear existing resources.
      mkdir ~/snippy
      cd ~/snippy
      cp ~/devel/snippy/docs/release/record-asciinema.sh ../
      chmod 755 ../record-asciinema.sh
      rm -f ../snippy.cast
      sudo docker stop snippy
      sudo docker rm snippy
      rm ./*
      clear

      # Disable and enable terminal linewrap
      printf '\033[?7l'
      clear
      #printf '\033[?7h'

      # Start recording.
      asciinema rec ../snippy.cast -c ../record-asciinema.sh

      # Play recording.
      asciinema play ../snippy.cast

      # Upload recording and connect to recording to user. Use the link at
      # the end of upload command after logged into asciinema.
      asciinema upload ../snippy.cast

      # Change the README file to link to new asciinema cast.

      # In case of failure.
      make uninstall
      make install
      rm -f ../snippy.cast
      sudo docker stop snippy
      sudo docker rm snippy
      clear
      asciinema rec ../snippy.cast -c ../record-asciinema.sh

      # Increase sudo time
      sudo visudo
      Defaults:heilaaks timestamp_timeout=30


Test PyPI installation
~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # Test PyPI installation before official release into PyPI.
      > https://testpypi.python.org/pypi
      make clean-all
      python setup.py sdist bdist_wheel
      twine upload --repository-url https://test.pypi.org/legacy/ dist/*
      pip uninstall snippy -y
      pip3 uninstall snippy -y
      pip install --index-url https://test.pypi.org/simple/ snippy
      snippy --help
      snippy import --defaults --scat all
      snippy search --sall docker
      pip uninstall snippy -y
      pip3 install --index-url https://test.pypi.org/simple/ snippy
      snippy --help
      snippy import --defaults --scat all
      snippy search --sall docker
      pip3 uninstall snippy -y
      pip3 install --user --index-url https://test.pypi.org/simple/ snippy
      pip uninstall snippy -y
      pip install --user --index-url https://test.pypi.org/simple/ snippy
      which snippy
      snippy --help
      snippy import --defaults --scat all
      snippy search --sall docker
      pip3 uninstall snippy -y
      pip uninstall snippy -y

Pre-release
~~~~~~~~~~~

#. Verify data in CHANGELOG.rst

   1. Update the CHANGELOG.rst release date if needed.

   2. Push changes to master.

Release
~~~~~~~

#. Make tag

   .. code-block:: text

      git tag -a 0.12.0 -m "Add new release 0.12.0"
      git push -u origin 0.12.0

#. Release in PyPI

   .. code-block:: text

      make clean-all
      python setup.py sdist bdist_wheel
      twine upload dist/*

#. Test PyPI release

   .. code-block:: text

      sudo pip uninstall snippy -y
      pip install snippy --user
      snippy --help
      snippy import --defaults
      snippy import --defaults --scat solution
      snippy search --sall docker

#. Release in Docker Hub

   .. code-block:: text

      su
      docker stop snippy
      docker rm snippy
      docker rmi --force $(docker images --filter=reference="*/snippy*:*" -q)
      docker rm $(docker ps --scat all -q -f status=exited)
      docker images -q --filter dangling=true | xargs docker rmi
      docker images
      make docker
      docker login docker.io
      docker tag 2e988be6fc03 docker.io/heilaaks/snippy:0.11.0
      docker tag 2e988be6fc03 docker.io/heilaaks/snippy:latest
      docker images
      docker push docker.io/heilaaks/snippy:0.11.0
      docker push docker.io/heilaaks/snippy:latest

#. Test Docker release

   .. code-block:: text

      su
      docker rmi --force $(docker images --filter=reference="*/snippy*:*" -q)
      docker rm $(docker ps --scat all -q -f status=exited)
      docker images -q --filter dangling=true | xargs docker rmi
      docker images
      docker pull heilaaks/snippy
      docker run heilaaks/snippy:latest --help
      docker run heilaaks/snippy:latest search --sall docker
      docker run -d --publish=127.0.0.1:8080:32768/tcp --name snippy heilaaks/snippy -vv
      curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker stop snippy
      docker rm snippy
      docker run --env SNIPPY_SERVER_HOST=127.0.0.1:8080 --net=host --name snippy --detach heilaaks/snippy --debug
      curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker stop snippy
      docker rm snippy

#. Release news

   1. Make new release in Github.

