Django command interface
========================

A reusable Django app that allows to list manage.py commands and lauch them 
with one click.

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

This app uses the Django messages framework, so you need to add
``django.contrib.messages.middleware.MessageMiddleware`` to your
``MIDDLEWARE_CLASSES`` setting.

You HAVE to have `DJANGO_PROJECT_ROOT` in your settings pointing towards the
directory of your `manage.py` file.



Usage
-----

Just visit the command interface main panel at view name
``command_interface_main`` and see listed all the commands, that you can
execute just by clicking "Run command".

That's it.


Passing arguments to the commands is still WIP.


Settings
--------

COMMAND_INTERFACE_DISPLAYED_APPS
++++++++++++++++++++++++++++++++

You can limit the displayed apps by setting
``COMMAND_INTERFACE_DISPLAYED_APPS``. The syntax is the same as it is in the
``INSTALLED_APPS`` setting. It defaults to showing absolutely all apps.

.. code-block:: python

    # would list all commands of the awesome_app
    COMMAND_INTERFACE_DISPLAYED_APPS = ['awesome_app']

COMMAND_INTERFACE_DISPLAYED_COMMANDS
++++++++++++++++++++++++++++++++++++

Further you can also provide a list of commands, that should explicitly be
displayed. Defaults to all as well.

.. code-block:: python

    # would on its own only show the mycommand command
    COMMAND_INTERFACE_DISPLAYED_COMMANDS = ['mycommand']


The settings don't exclude each other. So displaying any full app and just one
or two specific commands from somewhere else is no problem at all.

COMMAND_INTERFACE_LOGFILE_PATH
++++++++++++++++++++++++++++++

For logging, you can specify a logfile path, where logfiles for each command
can be created. The logfiles will always be prefixed with
``command_interface_log-``.

..code-block:: python

    COMMAND_INTERFACE_LOGFILE_PATH = '/home/myname/tmp/logs/'

This value defaults to ``None``, which means, that no logs are created.

The log of the last run is then displayed on the command interface main view
under each respective command.

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
