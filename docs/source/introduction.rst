Introduction
============

Manage command snippets and solution examples from command line or through a RESTish API
that follows subset of JSON API specification v1.0.

The Snippy tool is intended to support software development and troubleshooting workflows
by collecting command examples and troubleshooting solutions into one manager. The tool
may be helpful for example when working with different open source components that all
have different configuration settings and troubleshooting methods. You can share the
best examples through REST API server or by exporting and importing the data with common
data serialization languages YAML or JSON.

.. code:: bash

    $ pip install snippy
    $ snippy import --defaults
    $ snippy search --sall docker

    1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]
       $ docker rm --volumes $(docker ps --all --quiet)

       # cleanup,container,docker,docker-ce,moby
       > https://docs.docker.com/engine/reference/commandline/rm/

    OK

.. raw:: html

   <a href="https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO"><img src="https://asciinema.org/a/wc6jSncHMWpD5RbODxQHtqElO.png"/></a>
