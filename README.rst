gemstone_admin - easy managment for microservices
=================================================

A tool for easily managing gemstone microservices.


Installing a service
--------------------

::

    gemstone_admin install --pip mymicroservice
    # uses pip install mymicroservice then searches inside the package for the management information

    gemstone_admin install --sdist mymicroservice-0.1.0.tar.gz
    # installs the microservice by using bundled source distribution

    gemstone_admin install --git https://github.com/myuser/mymicroservice
    # clones from github and then installs it via pip.

    gemstone_admin install --git https://github.com/myuser/mymicroservice
    # clones from github and then installs it via pip.

    gemstone install ... ... --name=custom_name
    # uses a custom name for the microservice

Listing available installed microservices
-----------------------------------------

::

    gemstone_admin list installed
    # mymicroservice,0.1.0
    # mymicroservice,0.2.0

Uninstalling microservices
--------------------------

::

    gemstone_admin uninstall mymicroservice

    gemstone_admin uninstall mymicroservice


Setting global configuration
----------------------------

::

    gemstone_admin write_config registry http://myregistry:8000/api

    gemstone_admin write_config available_at http://behind_proxy/

Starting microservices
----------------------

::

    gemstone_admin start mymicroservice

    gemstone_admin start_batch mymicroservice=3 mymicroservice2=4 myotherservice=5


Listing running microservices
-----------------------------

::

    gemstone_admin list running
    # mymicroservice;<id>;0.0.0.0;9992
    # mymicroservice;<id>;0.0.0.0;6413
    # mymicroservice;<id>;0.0.0.0;6164
    # ...

Killing microservices
---------------------

::

    gemstone_admin stop <id>
