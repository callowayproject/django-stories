.. _settings:

========
Settings
========

Here are several settings that you can use to customize Stories.

.. _story_status_choices:

STORY_STATUS_CHOICES
====================

A story can be in several different states, for example draft vs. live. Your workflow might have several states that a story goes through, but there can only be one choice that is considered "Published". 

Choices are specified as a ``list`` or ``tuple`` of ``integer`` - ``string`` tuples. The ``integer`` is the code for the choice and the ``string`` is the description that the user sees.

**Defaults:** ::

	STORY_STATUS_CHOICES = (
	    (1, 'DRAFT'),
	    (2, 'READY FOR EDITING'),
	    (3, 'READY TO PUBLISH'),
	    (4, 'PUBLISHED'),
	    (5, 'REJECTED'),
	    (6, 'UN-PUBLISHED'),
	)

*Draft:* A work-in-progress.

*Ready for Editing:* The story is ready for an editor's touch.

*Ready to Publish:* The editing is finished and the story is ready to go on to the web site.

*Published:* The story is on the web site, as long as it is past the story's publish date and time.

*Rejected:* The editor didn't like something and the author needs to work on it some more.

*Un-published:* The story has been removed from the site for some reason.

.. _story_default_status:

STORY_DEFAULT_STATUS
====================

When a story is created, what should the the status default to?

**Default:** ::

	STORY_DEFAULT_STATUS = 1 # Draft

.. _story_published_status:

STORY_PUBLISHED_STATUS
======================

Which one of the possible statuses is considered "On Site." 

**Default:** ::

	STORY_PUBLISHED_STATUS = 4 # Published

.. _story_markup_choices:

STORY_MARKUP_CHOICES
====================

The Story app endeavors to have a pluggable markup system for the content of the each story. This allows a variety of ways to markup content, depending on end user or source of the content.

It is also possible to have a WYSIWYG editor in the admin that stores the resulting content in the correct format.

Choices are specified as a ``list`` or ``tuple`` of ``integer`` - ``string`` tuples. The ``integer`` is the code for the choice and the ``string`` is the description that the user sees.


**Defaults:** ::

	STORY_MARKUP_CHOICES = (
	    (0, 'None'),
	    (1, 'Creole'),
	    (2, 'reStructuredText'),
	    (3, 'Textile'),
	    (4, 'Markdown'),
	    (5, 'HTML'),
	)

.. _story_default_markup:

STORY_DEFAULT_MARKUP
====================

To make it easy on authors, you can specify which of the formats available is the default.

**Default:** ::

	STORY_DEFAULT_MARKUP = 0 # None

.. _story_origin_choices:

STORY_ORIGIN_CHOICES
====================

It is possible that stories could be coming in from several sources, such as a wire service, an editorial front end, or an FTP site. This settings allows you to mark which stories originated from which source, so you can potentially do something different depending on the source. For example, include all stories in the RSS feed, except ones that came from a wire service.

Choices are specified as a ``list`` or ``tuple`` of ``integer`` - ``string`` tuples. The ``integer`` is the code for the choice and the ``string`` is the description that the user sees.

**Default:** ::

	STORY_ORIGIN_CHOICES = (
	    (0, 'Admin'),
	)

.. _story_default_origin:

STORY_DEFAULT_ORIGIN
====================

When a story is created from the Django Admin, which choice of origin should it default to?

**Default:** ::

	STORY_DEFAULT_ORIGIN = 0 # Admin

.. _story_relation_models:

STORY_RELATION_MODELS
=====================

A story can relate to several other things, such as other stories, photographs, photo galleries, and external links. Stories links to the Django Content Types application, which would normally show all sorts of things that don't matter to the author and end users. This setting specifies which specific models are relatable to a story.

The value should be a tuple of `'appname.modelname'` strings.

If this setting is empty or ``None``\ , the story relations are not available in the admin. If at a later time you decide to set this, you must ``syncdb`` before it will work properly.

**Default:** ::

	STORY_RELATION_MODELS = None # Not enabled

.. _story_pagination:

STORY_PAGINATION
================

Django Stories has a built-in :class:`Paginator` subclass that splits HTML-formatted text into paragraphs for paginating. If ``STORY_PAGINATION`` is ``True``\ , stories will be paginated in the template. See :ref:`pagination` for more information, and the 
`Django Paginator docs <http://docs.djangoproject.com/en/dev/topics/pagination/#paginator-objects>`_ for more about pagination is general.

**Default:** ::

	STORY_PAGINATION = False

.. _story_p_per_page:

STORY_P_PER_PAGE
================

If ``STORY_PAGINATION`` is ``True``\ , then this setting sets the number of paragraphs per page for pagination.

**Default:** ::

	STORY_P_PER_PAGE = 20

.. _story_orphans:

STORY_ORPHANS
=============

If ``STORY_PAGINATION`` is ``True``\ , then this setting sets the minimum number of paragraphs allowed on the last page for pagination. This means that with ``STORY_P_PER_PAGE = 20`` and ``STORY_ORPHANS = 4`` a story with 24 paragraphs would only have one page, but a story with 25 paragraphs would have two pages.

**Default:** ::

	STORY_ORPHANS = 4