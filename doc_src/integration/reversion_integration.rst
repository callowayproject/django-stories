.. _reversion_integration:

=================================
Integrating with Django Reversion
=================================

1. Install `django-reversion`

    .. code-block:: bash

        $ pip install django-reversion

2. Add ``reversion`` to your ``INSTALLED_APPS`` setting.

    .. code-block:: python

        INSTALLED_APPS = (
            ...
            'reversion',
            ...
        )

3. ``./manage.py syncdb``

4. Set story settings

    .. code-block:: python

        STORY_SETTINGS['USE_REVERSION'] = True

Versions are tracked from when reversion is first installed.
