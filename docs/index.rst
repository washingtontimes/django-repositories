.. app documentation master file, created by
   sphinx-quickstart on Wed Oct 21 13:18:22 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

============
Repositories
============

Repositories is a simple Django-based app to manage source code repositories.

It is not meant to manage repositories that are only accessed by one person, but for a team of people.

It can:

* Create new repositories
* Manage public or private read access
* Manage user or group authentication and commit access

It can use these version control systems:

* Subversion
* Git
* Mercurial (Not Done: Need help)
* Bazaar (Not Done: Need help)
* Others could be written in to the vcs abstraction

The hosting is done through Apache httpd, as there are hooks in Apache httpd's mod_python and mod_wsgi implementations for external authentication and authorization.

Contents
========

.. toctree::
   :maxdepth: 2
   :glob:
   
   goals
   installing
   authentication
   settings
   management_commands/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

