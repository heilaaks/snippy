Releasing
---------

#. Preparations

   1. Update release notes

#. Run tests

   .. code-block:: text

      make test
      make lint
      make docs
      tox
      python setup.py check --restructuredtext

#. Test installation

   .. code-block:: text

      make uninstall
      make install
      snippy --help
      snippy import --defaults
      snippy import --defaults --solutions
      snippy search --sall docker
      rm -f ${HOME}/devel/temp/snippy.db
      snippy import --defaults --storage-path ${HOME}/devel/temp
      snippy import --defaults --solution --storage-path ${HOME}/devel/temp
      snippy --server --storage-path ${HOME}/devel/temp --port 8080 --ip 127.0.0.1 -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool

#. Test with PyPI

   .. code-block:: text

      make clean
      make clean-db
      python setup.py sdist upload -r testpypi
      sudo pip uninstall snippy -y
      pip install --user --index-url https://test.pypi.org/simple/ snippy
      snippy --help
      snippy import --defaults
      snippy import --defaults --solutions
      snippy search --sall docker
      pip uninstall snippy -y

#. Test with Docker

   .. code-block:: text

      su
      make docker
      docker rm $(docker ps --all -q -f status=exited)
      docker images -q --filter dangling=true | xargs docker rmi
      docker images
      docker rmi heilaaks/snippy:v0.7.0
      docker rmi heilaaks/snippy:latest
      docker rmi docker.io/heilaaks/snippy:latest
      docker rmi docker.io/heilaaks/snippy:v0.7.0
      docker build -t heilaaks/snippy .
      docker run snippy --help
      docker run snippy search --sall docker
      docker run -d --net="host" --name snippy heilaaks/snippy --server --port 8080 --ip 127.0.0.1 -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool
      docker run -d --net="host" --name snippy heilaaks/snippy --server --log-json -vv
      curl -s -X GET "http://127.0.0.1:8080/snippy/api/app/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool

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

#. Make tag

   .. code-block:: text

      git tag -a v0.7.0 -m "Experimental RESTish JSON API"
      git push -u origin v0.7.0

#. Releas in PyPI

   .. code-block:: text

      python setup.py sdist # Build source distribution
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
