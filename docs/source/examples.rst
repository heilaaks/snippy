Examples
========

Add snippet with brief description and tags.

.. code:: bash

    snippy create --content 'docker rm $(docker ps -a -q)' --brief 'Remove all docker containers' --tags docker,image,cleanup
    snippy create --content 'docker rm --volumes $(docker ps --all --quiet)' --brief 'Remove all docker containers with volumes' --group docker --tags docker-ce,docker,moby,container,cleanup --links 'https://docs.docker.com/engine/reference/commandline/rm/'

Find snippet with keyword list.

.. code:: bash

    snippy search --sall docker,containers

Delete snippet with index.

.. code:: bash

    snippy delete --digest f6062e09e2c11b47
