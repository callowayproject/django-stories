.. _tinymce_integration:

===============================
Integrating with Django TinyMCE
===============================

Install django-tinymce
======================

Django-tinymce makes it very easy to include a GUI text editor for any textarea.

1. Install a special fork of `django-tinymce <http://code.google.com/p/django-tinymce/>`_  from `github <http://github.com/justquick/django-tinymce>`_ ::
   
	pip install git+http://github.com/justquick/django-tinymce.git#egg=tinymce
   
#. Download `TinyMCE <http://tinymce.moxiecode.com/download.php>`_ and copy the contents of the ``jscript`` directory into a ``js`` directory within your ``MEDIA_ROOT`` directory. ::

	/myproject
	    /apps
	    /static
	        /css
	        /img
	        /js
	-------->   /tinymce
   
#. Add ``tinymce`` to your ``INSTALLED_APPS`` setting. ::

	INSTALLED_APPS = (
	    ...
	    'tinymce',
	)
   
#. Add ``(r'^tinymce/', include('tinymce.urls')),`` to your ``urls.py``. ::

	urlpatterns = patterns('',
	    ...
	    (r'^tinymce/', include('tinymce.urls')),
	    ...
	)
   
#. Add the settings for tinymce. The configuration of plugins and tools shown here is just an example. See the `django-tinymce docs <http://github.com/justquick/django-tinymce/blob/master/docs/installation.rst>`_ and `TinyMCE Manual <http://wiki.moxiecode.com/index.php/TinyMCE:Configuration>`_ for more information. For example::

	TINYMCE_DEFAULT_CONFIG = {
	    'theme': "advanced",
	    'relative_urls': False,
	    'plugins': "safari,paste,advimage,preview",
	    'theme_advanced_toolbar_location' : "top",
	    'theme_advanced_toolbar_align' : "left",
	    'theme_advanced_buttons1' : "formatselect,bold,italic,underline,separator,bullist,numlist,separator,undo,separator,link,unlink,separator,charmap,image,paste,pasteword,separator,code,preview",
	    'theme_advanced_buttons2' : "",
	    'theme_advanced_buttons3' : "",
	    #'skin': 'thebigreason',
		'theme_advanced_statusbar_location' : "bottom",
		'width': "600",
		'height': "600",
	}

#. Add the ``TINYMCE_ADMIN_FIELDS`` setting::

	TINYMCE_ADMIN_FIELDS = {
	    'stories.story': ('body',),
	}

   You can add other fields for other models in here as well, for example::

	TINYMCE_ADMIN_FIELDS = {
	    'stories.story': ('body',),
	    'flatpages.flatpage': ('content',),
	}

