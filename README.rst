Django command interface
============

A reusable Django app that allows to list manage.py commands and lauch them with one click

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-command-interface

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-command-interface.git#egg=command_interface

TODO: Describe further installation steps (edit / remove the examples below):

Add ``command_interface`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'command_interface',
    )

Add the ``command_interface`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^command-interface/', include('command_interface.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load command_interface_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate command_interface


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-command-interface
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
