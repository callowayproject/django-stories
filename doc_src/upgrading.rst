.. _upgrading:

================
Upgrading to 1.0
================

Version ``1.0`` includes of bunch of changes, some of which are not backwards
compatible. This migration guide will try to help you upgrade your stories
to ``1.0``.

Before we install the new version of ``stories``, we need to determine which
parts will need your attention. While there are no schema changes to ``stories``
and ``relations`` in ``1.0``, there are, however, some steps that need to be taken
to ensure everything stays the same.

Ensureing story models are correctly configured
===============================================

If you using django-categories
------------------------------

The setting ``USE_CATEGORIES`` has been removed, instead you will need
to use the ``categories`` to register the fields you once had. These fields
were hard coded into stories as ``primary_category`` and ``categories``. Here is
an example of what you can do

.. code-block:: python

    CATEGORIES_SETTINGS = {
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
       }

If you using story relations
----------------------------

``relations`` are now a seperate app within ``stories``, you must add
``stories.relations`` to your ``INSTALLED_APPS``

.. code-block:: python

   INSTALLED_APPS = (
        ...
        'stories',
        'stories.relations',
        ...
    )

.. _upgrading_with_south:

If you using django-south
-------------------------

``stories`` is now ``south`` enabled, however, there are some things you will
need to know about how the initial migration runs. While you will be
faking the initial migration, since your upgrading, these points are good
to know.

1. In order to sync the configurable ``authors`` model, the initial migration
   contains some custom bits. Bascially, the db columns that are created, need
   to be what ``django`` expects them to be. By default, ``auth.User`` model is
   used, which makes a table with fields ``user_id`` and ``story_id``. If we use
   a custom model called ``BasicUser``, for example, django expects the db
   columns to be ``basicuser_id`` and ``story_id``.

#. It is now the responsability of ``django-categories`` to sync the category
   fields and not ``stories``. There is nothing special you have to do to get
   the fields to sync, ``categories`` includes a ``post_syncdb`` signal to sync
   the fields for you. *Note: this signal is only run when using south*.

#. ``Relations`` have there own migrations. The models for ``relations`` set the
   ``db_table`` meta attribute to ``stories_storyrelation`` and not what it
   would normally (because of the location of the app being inside stories).


Ensuring functionality
======================

The only requirement now is BeautifullSoup, all the others were removed.
If you expect ``reversion``, ``tinymce`` or ``categories`` to be installed via
``stories`` requirements, please update any site specific requirements file
to include these packages.

If you using TinyMCE
--------------------

``django-tinymce`` was removed as a dependance of ``stories`` and
therefore removed as the default widget for the ``body`` field. In order
to get ``TinyMCE`` to render the ``body`` field you will need to supply
``WIDGET`` setting.

.. code-block:: python

    STORY_SETTINGS = {
        ...
        'WIDGET': 'path.to.TinyMCEWIdget',
        ...
    }

If your using Relations
-----------------------

The relation template tags have moved into the ``relations`` app within ``stories``.
Any instance of ``{% load stories %}`` needs to be replaced with
``{% load story_relation_tags %}``. The tag names are still the same and function
the same

If your using STORY_ORDERING setting
------------------------------------

The setting ``STORY_ORDERING`` was renamed to simply ``ORDERING``

If your using the author property of the story model
----------------------------------------------------

While the property stil exists and functions the same, it was rather dumb
in the way it worked. There is a new property called ``author_display`` which
renders out a template you can use. This will be if you want to use a custom
author model
