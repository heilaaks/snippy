Usage
=====

Terminal
--------

Snippy command line commands always must include content operation and category. Content
operation is one of the six basic operations and the category can be snippet or solution.
The content category is snippet by default. Metadata attached to the content allows
adding brief description of the content, single group to which the content belongs, list
of tags to assist search operations and a list of links for more information about the
content.

Snippy tool outputs always OK after successful operation and NOK with a failure string in
case of failure. You can use debug option with the command to investigate possible problems.
For more detailed troubleshooting instructions, please refer to the development section.

The workflow section below contains use cases.

.. note::

   The tool is used by the author in Linux environment. There is an edit functionality
   with editor that always assumes vi editor. This limitation can be circumvented by
   using text based templates to import content or command line options in case of snippets.

.. note::

   The default content is provided "as is" basis without warranties of any kind.

Server
------

Snippy can be run as a server. In this case you must access the content through a REST
API with same principles as from command line.
