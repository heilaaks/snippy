Plugins
=======

Introduction
------------

Snippy implements a plugin framework to import data from external tools.
This allows users to format any data source to be compatible with Snippy
without modifying the code in the Snippy tool.

Installation
------------

In order for Snippy to find the plugins, they must be installed under the
same location where the Snippy was installed. For example if the Snippy was
installed under the Python user script directory, plugins must be installed
there as well.

.. code:: bash

   # Install Snippy and tldr plugin under Python user script directory.
   pip install snippy --user
   pip install snippy-tldr --user
   snippy import --plugin <plugin>
   snippy import --plugin <plugin> --file https://github.com/tldr-pages/tldr/tree/master/pages/linux

Usage
-----

The design is to allow different plugins for each operation. For example the
import operation accepts plugin with the ``--plugin`` option. It is possible
to give also the ``--file`` option which value is passed to the plugin.

.. code:: bash

   snippy import --plugin <plugin>
   snippy import --plugin <plugin> --file https://github.com/tldr-pages/tldr/tree/master/pages/linux

Development
-----------

Discovery
~~~~~~~~~

Snippy plugins are discovered based on `package namespace`_ implementation.
Plugin entrypoint must be ``snippyplugin`` to locate the plugins. The value
of the entrypoint must be in form of ``snippy_tldr.plugin``. The ``snippy_``
is the prefix for the application and the main module is called ``plugin``.

.. code:: bash

   entry_points={
       'snippyplugin': [
           'snippy = snippy_tldr.plugin'
       ]
   }

Hooks
~~~~~

Following hooks are proveded.

**snippy_import_hook**

This hook must return iterable to iterate notes parsed from external source.


.. _package namespace: https://packaging.python.org/guides/creating-and-discovering-plugins/#using-namespace-packages
