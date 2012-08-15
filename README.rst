
|BUILD|_

.. |BUILD| image::
   https://secure.travis-ci.org/callowayproject/django-stories.png?branch=1.0
.. _BUILD: http://travis-ci.org/#!/callowayproject/django-stories

==============
Django Stories
==============



This app is designed to be flexible to configure, but still simple to the writers and editors.

Design Goals
============

* Reduced dependencies: Checks for optional packages and only creates the fields if they are there.

* Rich content embedding from GUI: For embedded content, the markup language's GUI can do everything it needs.

* Flexible dependencies: Can pick from several applications that provide similar service, for example django-staff vs. User, massmedia vs. photologue


Features
========

* **Revision tracking:** Keeps track of saved versions and allows a user to revert to a previous version.

* **Related items:** Can set any configured item to be related to the story. These are for Photos, Videos, other stories, etc.

* **Quick Edit:** Several fields can be changed in the list view including Headline, Subheadline, Teaser, Kicker and Published Status. A form is used and can be overridden by your project to include what ever fields you want.

* **Optional 404 supressing:** Sometimes you may have to take down content. You can now return a page with an explanation instead of returning a 404 error.

Change Log
==========

-**New in 1.0**

* Code refactor

* Tests

* New ``author_display`` property to replace te current ``author`` property

* Removed most requirements as they are not really "Required". ``BeautifulSoup`` remains a requirement.

* New settings: ``WIDGET``, ``WIDGET_ATTRS``. Since TinyMCE was removed as a requirement, these we settings will be used to supply the widget for the ``story.body`` field.

* Setting ``STORY_ORDERING`` was renamed to ``ORDERING``. Using ``STORY_ORDERING`` is still possible, but a warning will be displayed.

* Fixed issues with Quick Edit functionality on the stories changelist

* Fixes to the Quick Edit functionality

    * QuickEdit now works =)
    * Removed external jQuery references for Quick Edit. Now uses ``django.jQuery`
    * Removed inline css/js, these are now in seperate files
    * The js was rewritten in coffeescript


**New in 0.6**

* A refactoring of the settings to be dictionary-based.

* Added ability to limit choices in the author model

* Added new settings: ``AUTHOR_MODEL``\ , ``USE_CATEGORIES``\ , ``USE_REVERSION``

**New in 0.5**

In 0.5 a new field was added: comment_status. Comment status deprecates the comments flag as it allows for a third state of comments: Frozen (show old comments but don't allow new comments).

There is a SQL script to add the new field and migrate the appropriate values from the old field. The old field is not removed from the table, but all references to it within the app are gone.
