|badge-pypiv| |badge-pys| |badge-pyv| |badge-cov| |badge-docs| |badge-build| |badge-docker|

Snippy
======

  I can't remember how - I just remember what.

Snippy is a software development and maintenance notes manager. It allows
organizing and sharing examples and solutions from self hosted or shared
storage through command line interface or via REST API server. Snippy may
be able to help you when working with different open source components that
all have different commands, settings and issues.

Features
========

Main features include:

- Linux command line tool or a `REST API server`_.
- Manage notes in three categories.
- Supports Markdown, YAML, JSON and text formats.
- Organize notes with metadata like groups and links.

Installation
============

To install as a tool, run:

.. code:: text

    pip install snippy --user

To install as a server, run:

.. code:: text

    docker pull docker.io/heilaaks/snippy

Usage
=====

.. image:: https://asciinema.org/a/pRd8Cf6WUGb1ioB7TPFdTq8Fb.png
    :target: https://asciinema.org/a/pRd8Cf6WUGb1ioB7TPFdTq8Fb
    :alt: Snippy in action!

Contributing
============

Author is happy to receive bug reports and feature requests.

Development
===========

See the `development`_ chapter from the documentation.

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
