Plugins
=======

Introduction
------------

Snippy implements a plugin framework to import data from external tools.
This allows users to format any data source to be compatible with Snippy
without modifying the code in Snippy.

Installation
------------

In order for Snippy to find the plugins, the must be installed under the
same location where the Snippy was installed. If the Snippy was installed
under the Python user script directory, plugins must be installed there
as well.

.. code:: bash

   # Install Snippy and tldr plugin under Python user script directory.
   pip install snippy --user
   pip install snippy-tldr --user
   snippy import --plugin <plugin>

Development
-----------
