.. _installing.rst:

=========================
Installing *Repositories*
=========================

There are really two parts to this: installing and configuring the Django application and configuring the Apache httpd server to serve the repositories.


Installing the Django Application
=================================

1. From a command line, type::

	sudo pip install django-repositories

   or ::

	sudo easy_install django-repositories

2. Install each version control system you want to serve.
   
   In Ubuntu:
   
   * **Subversion:** ``sudo install subversion``
   * **git:** ``sudo install git-core``
   * **Mercurial:** ``sudo install mercurial``
   * **Bazaar:** ``sudo install bzr``



Configuring the Django Application
==================================

*Repositories* has several configurable :ref:`settings` with good defaults. 

At a minimum, set :ref:`REPO_BASE_REPO_PATH` to where all the repositories are stored. :ref:`WSGI_SCRIPT` should be set if you aren't going to override the apache httpd configuration templates.


Installing Apache httpd Server Dependencies
===========================================

1. Install Apache httpd version 2.x. In Ubuntu, ``sudo apt-get install apache2``.

2. Enable the mod_dav module. In Ubuntu, ``sudo a2enmod dav``.

3. Enable the authn_alias module ``sudo a2enmod authn_alias``

4. Install mod_wsgi or mod_python, in Ubuntu: ``sudo apt-get install libapache2-mod-wsgi`` or ``sudo apt-get install libapache2-mod-python``.

5. If you are serving Subversion repositories, install the mod_dav_svn module. In Ubuntu, ``sudo apt-get install libapache2-svn``.


Configuring Apache httpd
========================

Use the :ref:`export_apache_conf` management command to output the Apache configuration for a given version control system. It uses the current configuration to fill in a template. The docs give more info.

