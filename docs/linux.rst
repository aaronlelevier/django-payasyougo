Linux (Ubuntu 14.04)
====================

Check processes
---------------

.. code-block::

    # get running processes
    ps --sort -rss -eo rss,pid,command | head

    # free memory
    free -m

Packages
--------

.. code-block::

    # completely remove a package
    apt-get purge <package>

    # update
    apt-get update

    # upgrade 
    apt-get upgrade


grep
----

.. code-block::

    # look for a string in files
    grep -rnw 'directory' -e 'pattern'


echo
----

.. code-block::

    # insert date into file
    echo Test Job ran at  `date` >> /var/log/testjob.log

    # clear file contents
    echo '' > <fillename>


ubuntu server
-------------

.. code-block::

    # reboot
    shutdown -r now


ssh
---

.. code-block::

    # generate ssh key
    ssh-keygen -t rsa -C "your_email@example.com"

    # start ssh-agent and assign
    eval "$(ssh-agent -s)"
    ssh-add <path_to_key>

    # get ssh rsa fingerprint
    ssh-keygen -lf ~/.ssh/id_rsa.pub

    # required permissions for private / public keys
    chmod 0400 <key>


ports
-----

.. code-block::

    # kill pid using port # 8000
    fuser -k 8000/tcp

    # kill using pid #
    kill -9 pid