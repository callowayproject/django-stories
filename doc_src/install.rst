============
Installation
============

Using PIP

.. code-block:: bash

    $ pip install django-stories

or download the app `here <http://pypi.python.org/pypi/django-stories/>`_

.. code-block:: bash

    $ python setup.py install


Add **stories** to your settings **INSTALLED_APPS**

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'stories',
        ...
    )

Run syncdb

.. code-block:: bash

    $ ./manage.py syncdb
