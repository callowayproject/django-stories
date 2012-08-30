.. _categories_integration:

==================================
Integrating with Django Categories
==================================

Install django-categories
=========================

1. Install ``django-categories``

    .. code-block:: bash

        $ pip install django-categories

#. Add ``categories`` to your ``INSTALLED_APPS`` setting.

    .. code-block:: python

        INSTALLED_APPS = (
            ...
            'categories',
            ...
        )

#. Supply the fields you want to be added to the ``Story`` model.

    .. code-block:: python

        CATEGORIES_SETTINGS = {
            ...
            'FK_REGISTRY': {
                'stories.story': {
                'name': 'primary_category', 'related_name': 'primary_category'
                }
            },
            'M2M_REGISTRY': {
                'stories.story': {
                'name': 'categories', 'related_name': 'categories'
                }
            }
            ...
        }

    In this case, 2 fields are setup, one ``ForeignKey`` field called
    **primary_category** and one ``ManyToMany`` field called **categories**

#. Sync your database

    .. code-block:: bash

        $ ./manage.py syncdb

    or if your using ``South``

    .. code-block:: bash

        $ ./manage.py syncdb --migrate


