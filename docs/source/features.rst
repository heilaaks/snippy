Features
========

Terminal
--------

Notes managed by the ``snippy`` are divided into three categories called
``snippet``, ``solution`` and ``reference``. Snippets are short command
examples and solutions are longer solution descriptions. The references
are collection of links. You can add metadata like links and tags to help
to search content.

You can operate snippet or solution content with six basic operations: create,
search, update, delete, import and export. These operations manage the content
in persistent file storage installed into the same place as the tool.

Command line operations
~~~~~~~~~~~~~~~~~~~~~~~

Create
^^^^^^

Search
^^^^^^

Update
^^^^^^

Delete
^^^^^^

Export
^^^^^^

When notes are exported, the filename and file format are defined with the
following logic. There can be a difference depending on how many notes are
exported.

1. The ``--file`` option always overrides any filename and format regardless
   of how many notes are exported.

2. When the ``--file`` option is not used, the ``--format`` option always
   overrides the file format. This applies regadless of how many notes are
   exported.

3. If the ``--file`` or ``--format`` options are not used, the ``filename``
   attribute will define the filename and file format if there is a single
   note to be exported.

4. If none of the above conditions are met, a default values are used.

   The default filename in case of a single note is ``[category]s.mkdn``.
   The default filename in case of multiple notes is ``contents.mkdn``.


Import
^^^^^^

Server
^^^^^^

Server
------

You can run the Snippy as a server. The server can create, search, update and
delete snippets and solutions. The server operates through RESTish API that
follows a subset of JSON API v1.0 specification.

The server does not bind to any address by default and the server-host option
must be always defined. The server-host option supports format <ip>:<port.
You can also define the log format between string and JSON and verbosity level
of logs.

The API is experimental and changes can be expected. The API is documented in
Swagger Hub `OpenAPI definitions`_.

The JSON REST API server is available only when the tool is installed from
Docker Hub or directly from the source code.

.. code-block:: text

   # Start server by sharing host network and enable JSON logs with limited
   # message length. Always remove previosly started container before running
   # container with new options set.
   docker rm -f snippy
   sudo docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --log-json -vv
   curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?limit=2" -H "accept: application/vnd.api+json" | python -m json.tool
   curl -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool

   # Start the server and define the port and IP address when the network is
   # shared between the container and host. Generate full length logs with
   # the --debug option.
   docker rm -f snippy
   sudo docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --log-json --debug
   curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool

   # Run the server with string logs.
   docker rm -f snippy
   sudo docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 -vv

You can query the server logs with the Docker log command.

.. code-block:: text

   docker logs snippy

You can remove the server with the rm command.

.. code-block:: none

   docker rm -f snippy

Note that Docker container is immutable and it does not share volume from the
host. If you want to run a server that allows content modification, you must
install the server from code repository.

.. code-block:: text

   git clone https://github.com/heilaaks/snippy.git
   cd snippy
   make server

With a local server, you can change to location of the storage from the default.
If the default content is needed, you need to import it into the new location
before starting the server.

.. code-block:: text

   snippy import --defaults --storage-path ${HOME}/devel/temp
   snippy import --defaults --scat solution --storage-path ${HOME}/devel/temp
   snippy --server-host 127.0.0.1:8080 --storage-path ${HOME}/devel/temp -vv

.. _OpenAPI definitions: https://app.swaggerhub.com/apis/heilaaks/snippy/0.11.0
