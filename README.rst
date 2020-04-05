|badge-pypiv| |badge-pys| |badge-pyv| |badge-cov| |badge-docs| |badge-build| |badge-docker|

Snippy
======

  I can't remember how - I just remember what.

Snippy is a software development and maintenance notes manager. It allows
organizing and sharing examples and solutions from self hosted or shared
storage through command line interface or via REST API server. Snippy may
be able to help you for example when working with different open source
components that all have different commands, settings and issues.

Features
========

Main features include:

- Use from Linux command line or from a `REST API server`_ as in `Heroku example`_.
- Run with a self-hosted SQLite or shared PostgreSQL database.
- Manage notes in three categories: snippets, solutions and references.
- Supports Markdown, YAML, JSON and text formats.
- Organize notes with metadata like groups, tags and links.
- Write import plugins like `snippy-tldr`_.

Installation
============

To install as a tool, run:

.. code:: text

    pip install snippy --user

To install as a server, run:

.. code:: text

    docker pull docker.io/heilaaks/snippy:latest

Usage
=====

.. image:: https://asciinema.org/a/cssisV5qtLlaxeYORblrEf7YL.png
    :target: https://asciinema.org/a/cssisV5qtLlaxeYORblrEf7YL
    :alt: Snippy in action!

Contributing
============

This is a personal hobby project to try to organize maintenance notes when
working with large software projects. Author is happy to hear if this project
has been actually used by anyone. Please post bug reports of feature requests
through GitLab issues.

This project got inspiration from the `Buku <https://github.com/jarun/Buku>`_.

Related work
============

- `tldr <https://github.com/tldr-pages/tldr>`_
- `cheat <https://github.com/cheat/cheat>`_
- `Buku <https://github.com/jarun/Buku>`_
- `CRUD in 2 minutes <https://www.youtube.com/watch?v=kMs-Tltf_Og>`_


.. |badge-pypiv| image:: https://img.shields.io/pypi/v/snippy.svg
   :target: https://pypi.python.org/pypi/snippy

.. |badge-pys| image:: https://img.shields.io/pypi/status/snippy.svg
   :target: https://pypi.python.org/pypi/snippy

.. |badge-pyv| image:: https://img.shields.io/pypi/pyversions/snippy.svg
   :target: https://pypi.python.org/pypi/snippy

.. |badge-cov| image:: https://codecov.io/gh/heilaaks/snippy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/heilaaks/snippy

.. |badge-docs| image:: https://readthedocs.org/projects/snippy/badge/?version=latest
   :target: http://snippy.readthedocs.io/en/latest/?badge=latest

.. |badge-build| image:: https://travis-ci.org/heilaaks/snippy.svg?branch=master
   :target: https://travis-ci.org/heilaaks/snippy

.. |badge-pyup| image:: https://pyup.io/repos/github/heilaaks/snippy/shield.svg
   :target: https://pyup.io/repos/github/heilaaks/snippy/

.. |badge-docker| image:: https://images.microbadger.com/badges/image/heilaaks/snippy.svg
   :target: https://hub.docker.com/r/heilaaks/snippy

.. _REST API server: https://app.swaggerhub.com/apis/heilaaks/snippy/0.11.0

.. _development: https://snippy.readthedocs.io/en/latest/development.html

.. _Heroku example: https://snippy-server.herokuapp.com/api/snippets?sall=docker&limit=5

.. _snippy-tldr: https://github.com/heilaaks/snippy-tldr
