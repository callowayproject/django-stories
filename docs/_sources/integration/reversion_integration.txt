.. _reversion_integration:

=================================
Integrating with Django Reversion
=================================

1. Install `django-reversion <http://code.google.com/p/django-reversion/>`_ ::
   
   	pip install django-reversion

2. Add ``reversion`` to your ``INSTALLED_APPS`` setting.

3. ``./manage.py syncdb``

All the hooks are there to notice when reversion is installed. Versions are tracked from when reversion is first installed. 