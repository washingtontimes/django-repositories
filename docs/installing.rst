.. _installing.rst:

=========================
Installing *Repositories*
=========================

There are really two parts to this: installing and configuring the Django application and configuring the Apache httpd server to serve the repositories.

.. _installing-the-django-application:

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


.. _configuring-the-django-application:

Configuring the Django Application
==================================

*Repositories* has several configurable :ref:`settings` with good defaults. 

At a minimum, set :ref:`REPO_BASE_REPO_PATH` to where all the repositories are stored and set :ref:`REPO_WSGI_AUTH_SCRIPT` to where you will store the authentication script. *(You will generate the authentication script* :ref:`below <Generating-the-Authentication-Script>` *)*

:ref:`WSGI_SCRIPT` should also be set if you aren't going to override the apache httpd configuration templates.


.. _installing-apache-httpd-server-dependencies:

Installing Apache httpd Server Dependencies
===========================================

1. Install Apache httpd version 2.x.

2. Enable the WebDAV module.

3. Enable the WebDAV filesystem module.

4. Enable the ``authn_alias`` module.

5. Install ``mod_wsgi``.

6. If you are serving Subversion repositories, install the WebDAV Subversion module.

In Ubuntu::

	sudo apt-get install apache2 libapache2-mod-wsgi libapache2-svn
	sudo a2enmod dav
	sudo a2enmod dav_fs
	sudo a2enmod authn_alias


.. _configuring-apache-httpd:

Configuring Apache httpd
========================

Use the :ref:`repo_generate_apache_conf` management command to output the Apache configuration for all configured version control systems. It uses the current configuration to fill in multiple templates. 

To create an configuration file and store it in a directory named ``conf``::

	./manage.py repo_generate_apache_conf > conf/apache_vcs.py

To create a symbolic link to the Apache httpd configuration and enable it (in Ubuntu)::

	sudo ln -s `pwd`/conf/apache_vcs.conf /etc/init.d/apache2/sites-available/vcs
	sudo a2ensite vcs


.. _generating-the-authentication-script:

Generating the Authentication Script
====================================

Use the :ref:`repo_generate_auth` management command to output the authentication script. It requires the path to the project folder as an argument to alter the system path in the script.

To create an authentication script and store it in a directory named ``conf``::

	./manage.py repo_generate_auth > conf/auth.wsgi

.. note:: Make sure the path in which you save the authentication script is the same place you configured in :ref:`REPO_WSGI_AUTH_SCRIPT`.