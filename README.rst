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

**New in 0.6**

* A refactoring of the settings to be dictionary-based.

* Added ability to limit choices in the author model

* Added new settings: ``AUTHOR_MODEL``\ , ``USE_CATEGORIES``\ , ``USE_REVERSION``

**New in 0.5**

In 0.5 a new field was added: comment_status. Comment status deprecates the comments flag as it allows for a third state of comments: Frozen (show old comments but don't allow new comments).

There is a SQL script to add the new field and migrate the appropriate values from the old field. The old field is not removed from the table, but all references to it within the app are gone.
