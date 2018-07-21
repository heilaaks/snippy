Releasing
---------

#. Preparations

   1. Update version number in meta.py.
   1. Update the CHANGELOG.rst.
   1. Updated README.rst and documentation.

#. Run tests

   .. code-block:: text

      make test
      make lint
      make docs
      tox
      python setup.py check --restructuredtext

#. Test installation

   .. code-block:: text

      make clean
      make clean-db
      pip uninstall snippy
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
      snippy --server --storage-path ${HOME}/devel/temp --port 8080 --ip 127.0.0.1 &
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool
      pkill snippy

#. Test with PyPI

   .. code-block:: text

      # Install the tool into test PyPI.
      make clean
      make clean-db
      python setup.py sdist bdist_wheel upload -r testpypi # repository: https://test.pypi.org/legacy/ in ~/.pypirc
      sudo pip uninstall snippy -y
      pip uninstall snippy -y

      # Set path to local user bin and install the tool from test PyPI.
      PATH=$HOME/.local/bin:$PATH
      pip install --user --index-url https://test.pypi.org/simple/ snippy
      snippy --help
      snippy import --defaults
      snippy import --defaults --solutions
      snippy search --sall docker
      
      # Run all example commands from top down from:
      snippy --help
      snippy --help examples
      
      # Uninstall
      pip uninstall snippy -y

#. Test with Docker

   .. code-block:: text

      su
      make docker
      docker rm $(docker ps --all -q -f status=exited)
      docker images -q --filter dangling=true | xargs docker rmi
      docker images
      docker rmi heilaaks/snippy:v0.7.0
      docker rmi docker.io/heilaaks/snippy:latest
      docker rmi docker.io/heilaaks/snippy:v0.7.0
      docker run heilaaks/snippy --help
      docker run heilaaks/snippy search --sall docker
      docker run -d --net="host" --name snippy heilaaks/snippy --server --port 8080 --ip 127.0.0.1 -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker logs 632e97aa83fe
      docker stop 632e97aa83fe
      docker rm $(docker ps --all -q -f status=exited)
      docker run -d --net="host" --name snippy heilaaks/snippy --server --log-json -vv &
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json"
      docker logs f72b3902dd4b

#. Test with PyPy

   .. code-block:: text

      # Default test box install PyPy 2.7 from dnf.
      sudo dnf install pypy
      export PYTHONPATH=/usr/lib64/python2.7/site-packages/
      wget https://bootstrap.pypa.io/get-pip.py
      sudo pypy get-pip.py
      sudo pypy -m pip install codecov
      sudo pypy -m pip install logging_tree
      sudo pypy -m pip install mock
      sudo pypy -m pip install pytest
      sudo pypy -m pip install pytest-cov
      sudo pypy -m pip install pytest-mock
      sudo pypy -m pip install falcon
      sudo pypy -m pip install gunicorn
      sudo pypy -m pip install jsonschema
      pypy runner --help
      pypy runner --server -vv
      pypy -m pytest -x ./tests/test_*.py --cov snipp
      unset PYTHONPATH

#. Verify data in CHANGELOG.rst

   1. Update the CHANGELOG.rst release date if needed.

#. Make tag

   .. code-block:: text

      git tag -a v0.8.0 -m "Add new content category resources"
      git push -u origin v0.8.0

#. Releas in PyPI

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
      sudo docker tag 5dc22d1d3380 docker.io/heilaaks/snippy:v0.7.0
      sudo docker tag 5dc22d1d3380 docker.io/heilaaks/snippy:latest
      sudo docker push docker.io/heilaaks/snippy:v0.7.0
      sudo docker push docker.io/heilaaks/snippy:latest

#. Test Docker release

   .. code-block:: text

      su
      docker rm $(docker ps --all -q -f status=exited)
      docker images -q --filter dangling=true | xargs docker rmi
      docker images
      docker rmi heilaaks/snippy:v0.7.0
      docker rmi heilaaks/snippy:latest
      docker rmi docker.io/heilaaks/snippy:latest
      docker rmi docker.io/heilaaks/snippy:v0.7.0
      docker run snippy --help
      docker run snippy search --sall docker
      docker run -d --net="host" --name snippy heilaaks/snippy --server --port 8080 --ip 127.0.0.1 -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool
      docker run -d --net="host" --name snippy heilaaks/snippy --server --log-json -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool

#. Release news

   1. Make new release in Github.
