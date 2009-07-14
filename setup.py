from distutils.core import setup

setup(name='django-stories',
      version='0.1',
      description='An application for handling newspaper-like stories on a web site',
      long_description='This app is designed to be flexible to configure, but still simple to the writers and editors. It has revisions, related items, configurable markup and pluggable GUI.',
      author='Corey Oordt',
      author_email='coordt@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/django-stories/',
      packages=['django-stories'],
      classifiers=['Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          ],
      )
