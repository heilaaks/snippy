Contributing to Snippy
======================

Author is happy to receive bug reports, feature requests and feedback. I cannot guarantee
immediate actions and responding to issues may take time.

The project is a learning project for author and the default content reflects to areas
what author sees important. Currently the project can be considered as a beta release.

Bug reports
-----------

Please report the tool version, export content to yaml file and run the failing command
with debug option. Please mention also operaring system, test if vi editor is installed
and what is the value of EDITOR environment variable.

Modify the failing command below to match the failed command and attach the compressed
result file to the github issue report with the failure report template below.

.. code-block:: none

    ## Actual behavior
    
    ## Expected behavior
    
    ## Steps to reproduce

    ## Commands to excecute

    snippy export --snippets --debug >> snippy-$(snippy --version).log 2>&1
    snippy export --solutions --debug >> snippy-$(snippy --version).log 2>&1
    snippy --help --debug >> snippy-$(snippy --version).log 2>&1
    snippy <failing command> --debug >> snippy-$(snippy --version).log 2>&1
    uname -a >> snippy-$(snippy --version).log 2>&1
    which vi >> snippy-$(snippy --version).log 2>&1
    env | grep EDITOR >> snippy-$(snippy --version).log 2>&1
    tar -czvf snippy-$(snippy --version).tar.gz snippy-$(snippy --version).log solutions.yaml snippets.yaml

.. _issue: https://github.com/heilaaks/snippy/issues
