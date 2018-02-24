Installation
============

To install, run:

.. code:: bash

    pip install snippy --user

To remove, run:

.. code:: bash

    pip uninstall --yes snippy

To install from Docker Hub, run:

.. code:: bash

    docker pull heilaaks/snippy

To install from Github, run:

.. code-block:: none

    git clone https://github.com/heilaaks/snippy.git
    cd snippy
    make install

To try for the very first time, run:

.. raw:: html

    <div class="highlight-none"><div class="highlight"><pre><span></span>
    $ snippy import --defaults
    $ snippy search --sall docker

    <font color="#20b2aa">1.</font> <font color="#228B22">Remove all docker containers with volumes</font> @docker <font color="#979a9a">[54e41e9b52a02b63]</font>
       <font color="#ff0000">$</font> docker rm --volumes $(docker ps --all --quiet)

       <font color="#ff0000">#</font> <font color="#979a9a">cleanup,container,docker,docker-ce,moby</font>
       <font color="#ff0000">></font> <font color="#979a9a">https://docs.docker.com/engine/reference/commandline/rm/</font>

    OK
    </pre></div>
    </div>
