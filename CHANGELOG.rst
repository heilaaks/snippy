.. :changelog:

Release history
===============

0.12.0 (development)
--------------------

Breaking changes
~~~~~~~~~~~~~~~~

* none

New features
~~~~~~~~~~~~

* Add support to import multiple content files with one operation.

Bugfixes
~~~~~~~~

* All commits in `0.12.0`_.

Security
~~~~~~~~

* none

Documentation
~~~~~~~~~~~~~

* none

0.11.0 (2020-03-29)
-------------------

Breaking changes
~~~~~~~~~~~~~~~~

* Change content category command line options `[2019.05.04]`_.
* Change content text templates metadata section `[2019.05.19]`_.
* Add content attribute ``languages`` `[2019.06.05]`_.

New features
~~~~~~~~~~~~

* Add import plugin architecture with `tldr plugin`_.
* Add new REST API endpoints to query distinct values of attributes.
* Add Bash completion support for command line interface.
* Add ``--sort`` command line option to sort search results.
* Add ``--headers`` command line option to print only content headers.

Bugfixes
~~~~~~~~

* Fix REST API server response if the HTTP request fails.
* Fix updating Markdown native content in text format.
* Fix ``--format`` option with the export operation.
* Fix parsing of text formatted solution.
* Fix update operation when content does not change.
* Fix ``--sall`` option did not search all attributes.
* Fix reading one line attributes like ``brief`` from multiple lines.
* Fix terminal colors on Windows.
* Fix parsing Markdown metadata from solution.
* Fix parsing Markdown solution data with '---' string.
* Fix parsing Markdown solution ``brief`` attribute.
* Fix Python 2 update and export operations with non ASCII characters.
* All commits in `0.11.0`_.

Security
~~~~~~~~

* none

Documentation
~~~~~~~~~~~~~

* none

0.10.0 (2019-05-01)
-------------------

Breaking changes
~~~~~~~~~~~~~~~~

* Change REST API endpoints `[2019.03.24]`_.
* Change REST API base path default `[2019.04.20]`_.
* Change REST API JSON schema validation `[2019.04.14]`_.
* Change REST API id attribute and queries with UUID `[2019.04.06]`_.
* Change server base path command line option name `[2019.04.21]`_.

New features
~~~~~~~~~~~~

* Add search shortcut for command line interface.
* Add support for ``name``, ``source`` and ``versions`` content attributes.
* Add ``gzip`` compression support for REST API responses.
* Add option to import all default content when server is started.
* Add environment variable support for server, storage and support options.

Bugfixes
~~~~~~~~

* Fix install requirement for PyYAML version.
* Fix multiple server startup problems in Docker container.
* Fix POST HTTP response when multiple POST requests were processed.
* Fix creating new content with prefilled templates.
* Fix exporting and importing content template.
* Fix error when content matching to a text template is saved.
* Fix duplicated content attribute values when updating content.
* Fix default value setting to ``groups`` attribute if no value was given.
* Fix error message from duplicated content when defaults imported again.
* All commits in `0.10.0`_.

Security
~~~~~~~~

* Remove setuid/setgid bit from binaries in Docker image.
* Remove unnecessary file permissions in Docker image.
* Change IP address where server binds in Docker container.

Documentation
~~~~~~~~~~~~~

* Add containerized server example usage in Dockerfile.

0.9.0 (2019-02-02)
------------------

Breaking changes
~~~~~~~~~~~~~~~~

* Change Markdown as default format `[2019.01.27]`_.
* Change content attributes ``group`` to ``groups`` `[2018.08.12]`_.
* Change content attribute ``versions`` from string to array `[2019.01.26]`_.
* Change UTC offset format from +0000 to +00:00 `[2018.12.16]`_.
* Change server command line options `[2019.01.04]`_.
* Change ``--filter`` option behaviour `[2018.09.02]`_.
* Change ``--editor`` option and add ``no-editor`` option `[2019.01.06]`_.
* Add new content attribute ``description`` `[2018.09.08]`_.

New features
~~~~~~~~~~~~

* Add REST API routes for: keywords, groups, tags, uuid and digest `[2018.08.09]`_.
* Add experimental support for PostgreSQL database `[2019.01.29]`_.
* Add support for Markdown formatted content.
* Add support to output search results also in Markdown format.
* Add one command to export and import all default content.
* Add comment auto-alignment for snippets when printed to terminal.
* Add ``description`` attribute in text content templates.
* Add ``uuid`` attribute for CLI and REST API operations.
* Add ``--limit`` option for CLI operations.
* Add search category ``--scat`` option for CLI operations.

Bugfixes
~~~~~~~~

* Fix solution creation from empty template.
* Fix content update when parsing user input fails.
* Fix content import from invalid source file.
* Fix search from all categories with ``all`` option.
* Fix resource validation for POST method.
* Fix resource validation for PUT and PATCH methods.
* Fix REST API HTTP OPTIONS responses.
* Fix reading timestamps without quotes from YAML.
* All commits in `0.9.0`_.

Security
~~~~~~~~

* Remove Alpine (apk) and Python (pip) installers from Docker image.
* Remove all log messages that may reveal secrets.

0.8.0 (2018-21-07)
------------------

* Add new content category for references.
* Add experimental beta release from RESTish API server.
* All commits in `0.8.0`_.

0.7.0 (2018-24-02)
------------------

* Add experimental RESTish JSON API.
* All commits in `0.7.0`_.

0.6.0 (2017-11-15)
------------------

* Add bug fixes and tests.
* All commits in `0.6.0`_.

0.5.0 (2017-10-29)
------------------

* Experimental beta release.
* All commits in `0.5.0`_.

0.1.0 (2017-10-15)
------------------

* Experimental alpha release.
* All commits in `0.1.0`_.

.. _0.12.0: https://github.com/heilaaks/snippy/compare/v0.11.0...master
.. _0.11.0: https://github.com/heilaaks/snippy/compare/v0.10.0...master
.. _0.10.0: https://github.com/heilaaks/snippy/compare/v0.9.0...master
.. _0.9.0: https://github.com/heilaaks/snippy/compare/v0.8.0...heilaaks:v0.9.0
.. _0.8.0: https://github.com/heilaaks/snippy/compare/v0.7.0...heilaaks:v0.8.0
.. _0.7.0: https://github.com/heilaaks/snippy/compare/v0.6.0...heilaaks:v0.7.0
.. _0.6.0: https://github.com/heilaaks/snippy/compare/v0.5.0...heilaaks:v0.6.0
.. _0.5.0: https://github.com/heilaaks/snippy/compare/v0.1.0...heilaaks:v0.5.0
.. _0.1.0: https://github.com/heilaaks/snippy/compare/ce6395137b...heilaaks:v0.1.0
.. _`[2019.01.27]`: https://github.com/heilaaks/snippy/commit/83aa4bb3072fe0fbb5a1c0477ba99c477fc0a3a2
.. _`[2018.08.12]`: https://github.com/heilaaks/snippy/commit/08394b6acaf8d1e0c7971e5fe4de95c04c54790b
.. _`[2019.01.26]`: https://github.com/heilaaks/snippy/commit/f9fadb04d26d3fbc75d12c198d9b1fff1d10cf90
.. _`[2018.12.16]`: https://github.com/heilaaks/snippy/commit/1b00a4d9179bf67ada56f7ee624e851e884c7f6a
.. _`[2019.01.04]`: https://github.com/heilaaks/snippy/commit/6f878407320fa1eb8834df5402db977943c55c87
.. _`[2018.09.02]`: https://github.com/heilaaks/snippy/commit/4be86cff53ea4d9cdb358ed487420a67d9f5bcbe
.. _`[2019.01.06]`: https://github.com/heilaaks/snippy/commit/6a289657e22952ad8276b0bb6062ca8e909ded77
.. _`[2018.09.08]`: https://github.com/heilaaks/snippy/commit/8d9b0558809e56ce40798f61c8636e04307743ed
.. _`[2018.08.09]`: https://github.com/heilaaks/snippy/commit/9e7e9f90e5df54f9930371617114d34e791be2ac
.. _`[2019.01.29]`: https://github.com/heilaaks/snippy/commit/6e60886d5f78d49952cd6b977db3a9b6f803f092
.. _`[2019.03.24]`: https://github.com/heilaaks/snippy/commit/063426d8c7bee05b620fa85cbf6ca81b1e96f45b
.. _`[2019.04.06]`: https://github.com/heilaaks/snippy/commit/c9f2efda31294deb149014232780952f64bc3e9c
.. _`[2019.04.14]`: https://github.com/heilaaks/snippy/commit/cd720fc4252abf68f61c080dd39143b6436067f4
.. _`[2019.04.20]`: https://github.com/heilaaks/snippy/commit/3479f27e298cd09e37dd1e1bd58c6f67fc0b2f34
.. _`[2019.04.21]`: https://github.com/heilaaks/snippy/commit/5203f6060e8f6d394befb210ce707944f9494d49
.. _`[2019.05.04]`: https://github.com/heilaaks/snippy/commit/f2344cca2307d848a7d726892bec4b0872e0f566
.. _`[2019.05.19]`: https://github.com/heilaaks/snippy/commit/b5ca1d025ec091d0572c24808744785415f61ca1
.. _`[2019.06.05]`: https://github.com/heilaaks/snippy/commit/b56ad73244e6eb01601dc1da8ca8f27300fd15a9
.. _`tldr plugin`: https://github.com/heilaaks/snippy-tldr
