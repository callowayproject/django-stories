.. _tinymce_integration:

===============================
Integrating with Django TinyMCE
===============================

Install django-tinymce
======================

Django-tinymce makes it very easy to include a GUI text editor for any textarea.

1. Install `django-tinymce`

    .. code-block:: bash

        $ pip install `django-tinymce`

#. Add ``tinymce`` to your ``INSTALLED_APPS`` setting.

    .. code-block:: python

        INSTALLED_APPS = (
            ...
            'tinymce',
            ...
        )

#. Add ``(r'^tinymce/', include('tinymce.urls')),`` to your ``urls.py``.

    .. code-block:: python

        urlpatterns = patterns('',
            ...
            (r'^tinymce/', include('tinymce.urls')),
            ...
        )

#. Add the ``WIDGET`` setting

    .. code-block:: python

        STORY_SETTINGS = {
            'WIDGET': 'tinymce.widgets.TinyMCEWidget',
        }

#. Finally run `./manage.py collectstatic`
