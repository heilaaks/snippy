Releasing
---------

Preparations
~~~~~~~~~~~~

   #. Update Python setuptools, wheels and Twine.
   #. Update version number in meta.py.
   #. Update version numbers in default content.
   #. Update the CHANGELOG.rst.
   #. Updated README.rst and documentation.

   .. code-block:: text

      export DEVEL_VERSION="0\.9\.d"
      export RELEASE_VERSION="0\.9\.0"

      # Update Python setuptools, wheels and Twine.
      pip install pip setuptools wheel twine --upgrade

      # Update version numbers in default content.
      make clean
      make clean-db
      python runner import --defaults --all
      python runner export --defaults --all

      # Test that version numbers were updated.
      grep -rn ./ -e ${DEVEL_VERSION}

Run tests with CPython
~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      make clean
      make clean-db
      make test
      make lint
      make docs
      tox
      python setup.py check --restructuredtext

Run tests with PyPy
~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # Example installation for Fedora 28. Comment psycopg2 out from setup.py because
      # psycopg2 replacement psycopg2cffi has not been so far to get installed with PyPy.
      make clean
      make clean-db
      dnf install pypy
      pypy -m ensurepip
      pypy -m pip install --upgrade pip wheel
      pypy -m pip install --editable .[dev]
      pypy -m pytest -x ./tests/test_*.py --cov snippy -m "not serial"
      pypy runner --help
      pypy runner import --defaults --all
      pypy runner --server-host 127.0.0.1:8080 -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=4" -H "accept: application/vnd.api+json"

Run tests with PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # The test-all target runs test with Sqlite and PostgreSQL.
      docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
      make clean
      make clean-db
      make test-all
      make test-postgresql

Test local installation
~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      make clean
      make clean-db
      pip uninstall snippy -y
      pip install . --user
      snippy --help
      snippy import --defaults
      snippy import --defaults --solutions
      snippy import --defaults --references
      snippy search --sall docker
      rm -f ${HOME}/devel/temp/snippy.db
      snippy import --defaults --storage-path ${HOME}/devel/temp
      snippy import --defaults --solutions --storage-path ${HOME}/devel/temp
      snippy import --defaults --references --storage-path ${HOME}/devel/temp
      snippy --server-host 127.0.0.1:8080 --storage-path ${HOME}/devel/temp &
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?limit=4" -H "accept: application/vnd.api+json"
      pkill snippy

Test docker installation
~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

      # Compile docker image.
      su
      make clean
      make clean-db
      make docker
      docker rm $(docker ps --all -q -f status=exited)
      docker images -q --filter dangling=true | xargs docker rmi
      docker images
      docker rmi heilaaks/snippy:v0.8.0
      docker rmi docker.io/heilaaks/snippy:latest
      docker rmi docker.io/heilaaks/snippy:v0.8.0

      # Run CLI commands with docker image.
      docker run heilaaks/snippy --help
      docker run heilaaks/snippy search --sall docker

      # Run server with Sqlite database.
      docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker logs snippy
      docker stop snippy
      docker rm snippy
      docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --log-json -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker logs snippy
      docker stop snippy
      docker rm snippy

      # Login into Docker image.
      docker exec -it snippy /bin/sh
      cd /
      du -ah | sort -n -r | head -n 50
      find / -name '*pycache*'

      # Run server with PostgreSQL database.
      docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --storage-type postgresql --storage-host localhost:5432 --storage-database postgres --storage-user postgres --storage-password postgres --log-json -vv
      curl -s -X POST "http://127.0.0.1:8080/snippy/api/app/v1/snippets" -H "accept: application/vnd.api+json; charset=UTF-8" -H "Content-Type: application/vnd.api+json; charset=UTF-8" -d '{"data":[{"type": "snippet", "attributes": {"data": ["docker ps"]}}]}'
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"

Test PyPI installation
~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

    # Test PyPI installation before official release into PyPI.
    > https://testpypi.python.org/pypi
    python setup.py sdist bdist_wheel
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    pip uninstall snippy -y
    pip3 uninstall snippy -y
    pip install --index-url https://test.pypi.org/simple/ snippy
    pip3 install --index-url https://test.pypi.org/simple/ snippy
    pip3 install --user --index-url https://test.pypi.org/simple/ snippy
    pip3 uninstall snippy -y

Release
~~~~~~~

#. Verify data in CHANGELOG.rst

   1. Update the CHANGELOG.rst release date if needed.

#. Make tag

   .. code-block:: text

      git tag -a v0.9.0 -m "Add new release 0.9.0"
      git push -u origin v0.9.0

#. Release in PyPI

   .. code-block:: text

      python setup.py sdist bdist_wheel
      twine upload dist/*

#. Test PyPI release

   .. code-block:: text

      sudo pip uninstall snippy -y
      pip install snippy --user
      snippy --help
      snippy import --defaults
      snippy import --defaults --solutions
      snippy search --sall docker

#. Release in Docker Hub

   .. code-block:: text

      su
      docker login docker.io
      docker images
      sudo docker tag 57cad43b2095 docker.io/heilaaks/snippy:v0.9.0
      sudo docker tag 57cad43b2095 docker.io/heilaaks/snippy:latest
      sudo docker push docker.io/heilaaks/snippy:v0.9.0
      sudo docker push docker.io/heilaaks/snippy:latest

#. Test Docker release

   .. code-block:: text

      su
      docker rm $(docker ps --all -q -f status=exited)
      docker images -q --filter dangling=true | xargs docker rmi
      docker images
      docker rmi heilaaks/snippy:v0.9.0
      docker rmi heilaaks/snippy:latest
      docker rmi docker.io/heilaaks/snippy:latest
      docker rmi docker.io/heilaaks/snippy:v0.9.0
      docker pull heilaaks/snippy
      docker run heilaaks/snippy:latest --help
      docker run heilaaks/snippy:latest search --sall docker
      docker run -d --net="host" --name snippy heilaaks/snippy:latest --server-host 127.0.0.1:8080 -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker run -d --net="host" --name snippy heilaaks/snippy:latest --server-host 127.0.0.1:8080 --log-json -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"

#. Release news

   1. Make new release in Github.

