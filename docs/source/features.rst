Features
========

Terminal
--------

Content managed by Snippy is divided into two categories called snippets and solutions.
Snippets are short command examples and solutions are longer solution descriptions.
You can combine metadata like links and tags with the content to help searching and
tracking the content.

You can operate snippet or solution content with six basic operations: create, search,
update, delete, import and export. These operations manage the content in persistent
file storage installed into the same place as the tool. 

Server
------

You can run the Snippy as a server. The server can create, search, update and delete
snippets and solutions. The server operates through RESTish API that follows a subset
of JSON API v1.0 specification.

The command below opens starts the server on localhost port 8080.

.. code:: bash

    snippy --server
