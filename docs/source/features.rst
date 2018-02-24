Features
========

Terminal
--------

Content managed by Snippy is divided into two categories called snippets and
solutions. Snippets are short command examples and solutions are longer
solution descriptions. You can add metadata like links and tags to help to
search content.

You can operate snippet or solution content with six basic operations: create,
search, update, delete, import and export. These operations manage the content
in persistent file storage installed into the same place as the tool. 

Server
------

You can run the Snippy as a server. The server can create, search, update and
delete snippets and solutions. The server operates through RESTish API that
follows a subset of JSON API v1.0 specification.

The server starts by default in localhost port 8080. You can change the IP
address and port from the command line. You can also define the log format
between string and JSON and verbosity level of logs.

The API is experimental and changes can be expected. The API is documented in
Swagger Hub `OpenAPI definitions`_.

The JSON REST API server is available only when the tool is installed from
Docker Hub or directly from the source code.

.. code-block:: none

   # Start server by sharing host network and enable JSON logs with limited
   # message length. Always remove previosly started container before running
   # container with new options set.
   docker rm -f snippy
   sudo docker run -d --net="host" --name snippy heilaaks/snippy --server --json-logs -vv
   curl -s -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?limit=2" -H "accept: application/vnd.api+json" | python -m json.tool
   curl -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool

   # Start the server and define the port and IP address when the network is
   # shared between the container and host. Generate full length logs with
   # the --debug option.
   docker rm -f snippy
   sudo docker run -d --net="host" --name snippy heilaaks/snippy --server --port 8080 --ip 127.0.0.1 --json-logs --debug
   curl -s -X GET "http://127.0.0.1:8080/snippy/api/v1/snippets?sall=docker&limit=2" -H "accept: application/vnd.api+json" | python -m json.tool

   # Run the server with string logs.
   docker rm -f snippy
   sudo docker run -d --net="host" --name snippy heilaaks/snippy --server --port 8080 --ip 127.0.0.1 -vv

You can query the server logs with the Docker log command.

.. code-block:: none

   docker logs snippy

You can remove the server with the rm command.

.. code-block:: none

   docker rm -f snippy

Note that Docker container is immutable and it does not share volume from the
host. If you want to run a server that allows content modification, you must
install the server from code repository.

.. code-block:: none

   git clone https://github.com/heilaaks/snippy.git
   cd snippy
   make server

With a local server, you can change to location of the storage from the default.
If the default content is needed, you need to import it into the new location
before starting the server.

.. code-block:: none

   snippy import --defaults --storage-path ${HOME}/devel/temp
   snippy import --defaults --solution --storage-path ${HOME}/devel/temp
   snippy --server --storage-path ${HOME}/devel/temp --port 8080 --ip 127.0.0.1 -vv

.. _OpenAPI definitions: https://app.swaggerhub.com/apis/heilaaks/snippy/1.0
