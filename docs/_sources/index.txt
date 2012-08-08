.. Django Stories documentation master file, created by
   sphinx-quickstart on Thu Dec 17 11:52:22 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Stories's documentation!
==========================================

This app is designed to be flexible to configure, but still simple to
the writers and editors.

Design Goals
============

* Reduced dependencies: Checks for optional packages and only creates the
  fields if they are there.

* Rich content embedding from GUI: For embedded content, the markup language's
  GUI can do everything it needs.

* Flexible dependencies: Can pick from several applications that provide
  similar service, for example django-staff vs. User, massmedia vs. photologue


Features
========

* **Revision tracking:** Keeps track of saved versions and allows a user to
  revert to a previous version.

* **Related items:** Can set any configured item to be related to the story.
  These are for Photos, Videos, other stories, etc.

* **Quick Edit:** Several fields can be changed in the list view including
  Headline, Subheadline, Teaser, Kicker and Published Status. A form is used
  and can be overridden by your project to include what ever fields you want.

* **Optional 404 supressing:** Sometimes you may have to take down content.
  You can now return a page with an explanation instead of returning a 404 error.


Contents:
---------

.. toctree::
   :maxdepth: 2

   install
   settings
   pagination
   integration/index

   reference/index

Helping Out
===========

* `Source <https://github.com/callowayproject/django-stories>`_
* `Issues <https://github.com/callowayproject/django-stories/issues>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

