from distutils.core import setup

import stories
version = stories.__version__

try:
    f = open('README')
    long_desc = f.read()
    f.close()
except:
    long_desc = ""

setup(name='django-stories',
      version=version,
      description='An application for handling newspaper-like stories on a web site',
      long_description=long_desc,
      author='Corey Oordt',
      author_email='coordt@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/django-stories/',
      packages=['stories'],
      classifiers=['Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          ],
      )
