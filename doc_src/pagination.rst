.. _story_pagination:

==========
Pagination
==========

Many sites wish to paginate long stories over multiple pages. Paginating text is a bit different from paginating a list of objects. Django Stories has a :class:`Paginator` subclass that takes an HTML-formatted string instead of a :class:`QuerySet`\ .

The simplest way to use pagination with stories is to set :ref:`PAGINATE` to ``True``\ , which changes the view that handles the story rendering.

PAGINATION settings
===================

:ref:`PAGINATE`
	Enables or disables pagination altogether. It is disabled by default.

:ref:`P_PER_PAGE`
	The number of paragraphs to show on each page. It shows 20 paragraphs by default, but only if story pagination is enabled.

:ref:`ORPHANS`
	The minimum number of paragraphs allowed allowed on the last page. It is set to 4 by default (meaning a minimum of 5 paragraphs on a page), but only if story pagination is enabled.

Using pagination in templates
=============================

The default name of the story template is ``stories/pag_story.html``\ . Within the context there are two variables:

story
	The :class:`Story` object.

story_content
	The :class:`ParagraphPaginator` class. It contains all the paragraphs of the :class:`Story` that should be on this page. A detailed reference of all the methods is in the `Django Paginator docs <http://docs.djangoproject.com/en/dev/topics/pagination/#paginator-objects>`_\ .

Different heading on first page
*******************************

.. code-block:: django

	{% if story_content.has_previous %}
	    <h3>{{ story.headline }}</h3>
	    <p><em>continued from page {{ story_content.previous_page_number }}</em></p>
	{% else %}
	    <h1>{{ story.headline }}</h1>
	    <h2>{{ story.subheadline }}</h2>
	{% endif %}

The above template snippet checks to see if this is a page other than 1 (meaning it has a previous page) and displays a small headline with a "continued from page x" below it.

If it is the first page, it displays the headline and subheadline in all their glory.

Looping through the paragraphs
******************************

.. code-block:: django

	{% load add_attribute %}
	{% for paragraph in story_content.object_list %}
	    {% ifequal story_content.number 1 %}
	        {% if forloop.first %}
	            {{ paragraph|add_attribute:"class=dropcap"|safe }}
	        {% else %}
	            {{ paragraph|safe }}
	        {% endif %}
	    {% endifequal %}
	{% endfor %}

``add_attribute`` is a filter that is included in Django Stories. It adds any attribute to the paragraph. In this example, it checks if it is the first paragraph and adds the attribute ``class`` with a value of ``dropcap`` to the ``<p>`` tag. That part is unnecessary, but allows you some artistic freedom.

Don't forget the ``|safe`` filter at the end. Django will automatically escape all the tags otherwise.

Leading them to the next page
*****************************

.. code-block:: django

	{% if story_content.has_next %}
		<p><a href="?page={{ story_content.next_page_number }}"><em>Story Continues &rarr;</em></a>
	{% endif %}

Before we hit the typical pagination anchors, it can be nice to add a simple link to the next page, so the reader doesn't have to think about which button to click.

The pagination widget
*********************

Django stories includes a template to show a list of pages with previous and next buttons. The template is in ``stories/pagination_widget.html`` and you can override it should you wish or simple include some styles in your CSS. Add the following line in your template:

.. code-block:: django

	{% include "stories/pagination_widget.html" %}

and it will generate some HTML similar to:

.. code-block:: html

	<div class="pagination">
	    <a href="?page=1" class="previous">&larr; Previous</a>
	    <a href="?page=1" class="page">1</a>
	    <span class="current">2</span>
	    <a href="?page=3" class="page">3</a>
	    <a href="?page=3" class="next">Next &rarr;</a>
	</div>

Pagination widget CSS styles
****************************

``div.pagination``
	The wrapper around the entire widget

``div.pagination a.previous``
	The anchor for the "previous" link

``div.pagination a.page``
	The anchor for each page link

``div.pagination span.current``
	The wrapper for the current page number

``div.pagination a.next``
	The anchor for the "next" link