from setuptools import setup

import stories
version = stories.__version__

try:
    f = open('README.rst')
    long_desc = f.read()
    f.close()
except:
    long_desc = ""

try:
    reqs = open('requirements.txt').read()
except:
    reqs = ''

setup(name='django-stories',
      version=version,
      description='An application for handling newspaper-like stories on a web site',
      long_description=long_desc,
      author='Corey Oordt',
      author_email='webmaster@callowayproject.com',
      url='http://github.com/callowayproject/django-stories/',
      packages=['stories'],
      install_requires=reqs,
      dependency_links=[
        'http://opensource.washingtontimes.com/simple/',
        'http://opensource.washingtontimes.com/simple/django-tinymce/',
        'http://opensource.washingtontimes.com/simple/django-categories/',
      ],
      include_package_data=True,
      classifiers=['Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          ],
      )
