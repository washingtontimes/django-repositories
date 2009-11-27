.. _installing.rst

=========================
Installing *Repositories*
=========================

There are really two parts to this: installing and configuring the Django application and configuring the Apache httpd server to serve the repositories.


Installing the Django Application
=================================

From a command line, type::

	sudo pip install django-repositories

or ::

	sudo easy_install django-repositories


Configuring the Django Application
==================================

*Repositories* has several configurable settings with good defaults.

Installing Server Dependencies
==============================

1. Install Apache httpd version 2.x. In Ubuntu, ``sudo apt-get install apache2``.

2. Enable the mod_dav module. In Ubuntu, ``sudo a2enmod dav``.

Enable the authn_alias module ``sudo a2enmod authn_alias``

3. Install mod_wsgi or mod_python, in Ubuntu: ``sudo apt-get install libapache2-mod-wsgi`` or ``sudo apt-get install libapache2-mod-python``.

4. If you are serving Subversion repositories, install the mod_dav_svn module. In Ubuntu, ``sudo apt-get install libapache2-svn``.

5. Install each version control system you want to serve.
   
   In Ubuntu:
   
   * **Subversion:** ``sudo install subversion``
   * **git:** ``sudo install git-core``
   * **Mercurial:** ``sudo install mercurial``
   * **Bazaar:** ``sudo install bzr``


Server Paths
============

Each type of version control system will needs two paths to store its repositories; one for the publicly readable and one for the private. Some things to keep in mind:

* **Don't put them in a subdirectory of a shared directory.** For example, if you were serving some static content from ``/var/www/`` you wouldn't want to use ``/var/www/repositories/svn/``.

* **Configure both public and private paths.** Even if you don't think you will ever make a repository publicly readable, configure the path "just in case."

* **Consider a simple hierarchy.** I like something similar to::
  
   	/var
   	    /repositories
   	        /svn
   	            /public
   	            /private
   	        /git
   	            /public
   	            /private


Server URLs
===========

Each type of version control system will also need two urls to map to the public and private paths, for example::

	http://code.example.com/svn/public/
	http://code.example.com/svn/private/
	http://code.example.com/git/public/
	http://code.example.com/git/private/


Authentication Notes
====================

mod_wsgi & authn/authz: http://code.google.com/p/modwsgi/issues/detail?id=48&can=1#c2
http://code.google.com/p/modwsgi/wiki/AccessControlMechanisms


Serve Subversion
================

In the following steps, these assumptions are made:

* The Django project is located at ``/home/projects/myproject/``.

* The Subversion repositories are located in ``/home/sourcecontrol/svn/``, and then within ``public/`` or ``private/`` depending on their public read status.

* Access to the repositories will be from ``http://code.example.com/repos/svn/`` and then ``public/`` or ``private/`` depending on their public read access.

Substitute your information where appropriate.

1. Add redirectors for requests without a trailing slash. If you want the URL to your Subversion respositories to be ``http://code.example.com/repos/svn/``, you would have these two lines::

	RedirectMatch ^(/repos/svn/public)$ $1/
	RedirectMatch ^(/repos/svn/private)$ $1/

   Note that the server name is unimportant here.

2. Handle public readable repositories ::

	<Location /repos/svn/public/>
	    # Enable Subversion
	    DAV svn
	    # System path to the public repositories
	    SVNParentPath /home/sourcecontrol/svn/public/
	    
	    SVNListParentPath On
	    SVNAutoversioning On
	    SVNReposName "Open Source Repositories"

   We haven't closed the ``<Location>`` tag yet because we have to set up mod_wsgi/mod_python and authentication and authorization.
   
   Key pieces of information required are:
   
   * the path to the public subversion repositories for ``SVNParentPath``.
   
   * a name like "My Subversion Repositories" for ``SVNReposName``.

3. Add support for mod_python *(if using mod_wsgi, skip this step):* ::
   
	<Location /repos/svn/public/>
	    ...
	    AuthType Basic
	    AuthUserFile /dev/null
	    AuthBasicAuthoritative Off
	    AuthName "My Subversion Repositories"

	    # Require authentication for commits and such
	    <LimitExcept GET PROPFIND OPTIONS REPORT>
	      Require valid-user
	    </LimitExcept>
	    
	    # Tell it which settings file to use
	    SetEnv DJANGO_SETTINGS_MODULE myproject.settings
	    
	    # Extend the Python path to locate your callable object
	    PythonPath "sys.path+['/home/projects', '/home/projects/myproject/apps']"
	    
	    # Make Apache aware that we want to use mod_python
	    AddHandler mod_python .py
	    
	    # Use mod_python for Authen/Authz
	    PythonAuthenHandler repoman.bin.apache-django-auth
	    PythonAuthzHandler repoman.bin.apache-django-auth
	</Location>
   
   Note: extend your python path to include *at least* the directory containing your project so it can import your settings, and the directory contianing the repoman app, so it can use the authentication script.

4. Add support for mod_wsgi *(if using mod_python, skip this step):* ::
   
	<Location /repos/svn/public/>
	    ...
    	AuthType Basic
		AuthName "My Subversion Repositories"
		AuthBasicProvider wsgi
		WSGIAuthUserScript /home/projects/myproject/apps/repoman/bin/apache_django_auth_wsgi.py
		WSGIAuthGroupScript /home/projects/myproject/apps/repoman/bin/apache_django_auth_wsgi.py

		Require valid-user

		<Limit GET HEAD OPTIONS CONNECT PROPFIND>
		Require group read
		</Limit>

		<Limit GET HEAD OPTIONS CONNECT POST PUT DELETE PROPFIND \
		 PROPPATCH MKCOL COPY MOVE LOCK UNLOCK>
		Require group write
		</Limit>


Link for info regarding Apache httpd and Subversion: http://svnbook.red-bean.com/en/1.5/svn.serverconfig.httpd.html
