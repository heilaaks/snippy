.. :changelog:

Release history
===============

0.10.0 (development)
--------------------

Breaking changes
~~~~~~~~~~~~~~~~

New features
~~~~~~~~~~~~

* Add option to import all default content when server is started.
* Add environment variable support for server, storage and support options.

Bugfixes
~~~~~~~~

* Fix exporting and importing content template.
* Fix error when content matching to a text template is saved.
* Fix duplicated content field values when updating content.
* All commits in `0.10.0`_.

Security
~~~~~~~~

0.9.0 (2019-02-02)
------------------

Breaking changes
~~~~~~~~~~~~~~~~

* Change Markdown as default format `[1]`_.
* Change content field ``group`` to ``groups`` `[2]`_.
* Change content field ``versions`` from string to array `[3]`_.
* Change UTC offset format from +0000 to +00:00 `[4]`_.
* Change server command line options `[5]`_.
* Change ``filter`` option behaviour `[6]`_.
* Change ``editor`` option and add ``no-editor`` option `[7]`_.
* Add new content field ``description`` `[8]`_.

New features
~~~~~~~~~~~~

* Add REST API routes for: keywords, groups, tags, uuid and digest `[9]`_.
* Add experimental support for PostgreSQL database `[10]`_.
* Add support for Markdown formatted content.
* Add support to output search results also in Markdown format.
* Add one command to export and import all default content.
* Add comment auto-alignment for snippets when printed to terminal.
* Add ``description`` field in text content templates.
* Add ``uuid`` field for CLI and REST API operations.
* Add ``limit`` option for CLI operations.
* Add search category ``scat`` option for CLI operations.

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

.. _0.10.0: https://github.com/heilaaks/snippy/compare/v0.9.0...master
.. _0.9.0: https://github.com/heilaaks/snippy/compare/v0.8.0...heilaaks:v0.9.0
.. _0.8.0: https://github.com/heilaaks/snippy/compare/v0.7.0...heilaaks:v0.8.0
.. _0.7.0: https://github.com/heilaaks/snippy/compare/v0.6.0...heilaaks:v0.7.0
.. _0.6.0: https://github.com/heilaaks/snippy/compare/v0.5.0...heilaaks:v0.6.0
.. _0.5.0: https://github.com/heilaaks/snippy/compare/v0.1.0...heilaaks:v0.5.0
.. _0.1.0: https://github.com/heilaaks/snippy/compare/ce6395137b...heilaaks:v0.1.0
.. _`[1]`: https://github.com/heilaaks/snippy/commit/83aa4bb3072fe0fbb5a1c0477ba99c477fc0a3a2
.. _`[2]`: https://github.com/heilaaks/snippy/commit/08394b6acaf8d1e0c7971e5fe4de95c04c54790b
.. _`[3]`: https://github.com/heilaaks/snippy/commit/f9fadb04d26d3fbc75d12c198d9b1fff1d10cf90
.. _`[4]`: https://github.com/heilaaks/snippy/commit/1b00a4d9179bf67ada56f7ee624e851e884c7f6a
.. _`[5]`: https://github.com/heilaaks/snippy/commit/6f878407320fa1eb8834df5402db977943c55c87
.. _`[6]`: https://github.com/heilaaks/snippy/commit/4be86cff53ea4d9cdb358ed487420a67d9f5bcbe
.. _`[7]`: https://github.com/heilaaks/snippy/commit/6a289657e22952ad8276b0bb6062ca8e909ded77
.. _`[8]`: https://github.com/heilaaks/snippy/commit/8d9b0558809e56ce40798f61c8636e04307743ed
.. _`[9]`: https://app.swaggerhub.com/apis/heilaaks/snippy/1.0
.. _`[10]`: https://github.com/heilaaks/snippy/commit/6e60886d5f78d49952cd6b977db3a9b6f803f092
