from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

try:
    long_description = open('README').read()
except IOError:
    long_description = ''

setup(name='django-repositories',
      version='0.1.1',
      description='Version Control system management',
      long_description=long_description,
      license='Apache Software License',
      author='Corey Oordt',
      author_email='coordt@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/django-repositories/',
      packages=['repositories',],
      include_package_data=True,
      classifiers=['Development Status :: 3 - Alpha',
          'Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          ],
      )