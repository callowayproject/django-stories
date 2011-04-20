.. _reversion_integration:

=================================
Integrating with Django Reversion
=================================

1. Install `django-reversion <http://code.google.com/p/django-reversion/>`_ ::
   
   	pip install django-reversion

2. Add ``reversion`` to your ``INSTALLED_APPS`` setting.

3. ``./manage.py syncdb``

4. Set ``STORY_SETTINGS['USE_REVERSION'] = True``

Versions are tracked from when reversion is first installed. 