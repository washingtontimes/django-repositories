from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(name='django-repositories',
      version='0.1.1',
      description='Version Control system management',
      long_description='',
      license='Apache Software License',
      author='Corey Oordt',
      author_email='coordt@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/django-repositories/',
      packages=['repositories',],
      package_data={
          'repositories': ['repositories/templates/repositories/*.conf'] #['bin/*.sh', 'management/*', 'repo-templates/*', 'templates/repositories/*.conf']
      },
      classifiers=['Development Status :: 3 - Alpha',
          'Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          ],
      )