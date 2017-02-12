gemstone_admin - easy managment for microservices
=================================================

A tool for easily managing gemstone microservices.

For a service to be manageable through this tool, it must:

- be packaged as a python module (let's assume its name is A)
- must have a A.service module that when is executed, uses the `gemstone.MicroService.get_cli()` to start the service


Installing a service
--------------------

::

    gemstone_admin install myservice
    gemstone_admin install myservice --module_name=importable_name

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
