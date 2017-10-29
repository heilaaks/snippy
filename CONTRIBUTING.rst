Contributing to Snippy
======================

Author is happy to receive bug reports, feature requests and feedback. I cannot guarantee
immediate actions and responding to issues may take time.

The project is a learning project for author and and the default content reflects to items
what author sees important. Currently the project can be considered a beta release.

Bug reports
-----------

Please report tool version, export content to yaml file and run the failing command with
debug option. Please mention also operaring system and test if vi editor is installed and
what is the EDITOR environment variable value.

Modify the failing command below to match the failed command and attach the compressed
result file to bug report with bug report template below::

    Problem description
    
    Expected behavior
    
    Snippet from failure log

.. code:: bash

    snippy --help --debug >> snippy-$(snippy --version).log 2>&1
    snippy export --snippet --debug >> snippy-$(snippy --version).log 2>&1
    snippy export --solution --debug >> snippy-$(snippy --version).log 2>&1
    snippy <failing command> --debug >> snippy-$(snippy --version).log 2>&1
    uname -a >> snippy-$(snippy --version).log 2>&1
    which vi >> snippy-$(snippy --version).log 2>&1
    env | grep EDITOR >> snippy-$(snippy --version).log 2>&1
    tar -czvf snippy-$(snippy --version).tar.gz snippy-$(snippy --version).log solutions.yaml snippets.yaml
