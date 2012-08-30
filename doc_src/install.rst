
.. _install:

============
Installation
============

Using PIP
=========

.. code-block:: bash

    $ pip install django-stories


Download
========

Download the app `here <http://pypi.python.org/pypi/django-stories/>`_
and run...

.. code-block:: bash

    $ python setup.py install


Install
=======

Add **stories** to your settings **INSTALLED_APPS**,

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'stories',
        ...
    )

If you want to use :ref:`story_relations`, add the app to
**INSTALLED_APPS** as well.

.. versionadded:: 1.0

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'stories',
        'stories.relations',
        ...
    )



Requirements
============

.. versionchanged:: 1.0
   The only requirement is `BeautifulSoup` for pagination

.. code-block:: bash

    $ pip install BeautifulSoup


Other Requirements
------------------

`Stories` may also require a couple `django` apps to be installed.

* **sites**
* **contenttypes** *(required if you use story relations)*
* **auth** *(required, unless you specify a custom author model)*


Run syncdb
==========

.. code-block:: bash

    $ ./manage.py syncdb

If your using ``South`` run

.. versionadded:: 1.0

.. code-block:: bash

    $ ./manage.py syncdb --migrate

.. note::

    The initial migration for `stories` is a little special, if you plan
    to use a custom author model, please consult :ref:`author_guide`
