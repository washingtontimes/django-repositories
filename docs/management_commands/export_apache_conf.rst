.. _management_commands__export_apache_conf.rst:

.. _export_apache_conf:

======================
``export_apache_conf``
======================

called as::

	./manage.py export_apache_conf [subversion|git|mercurial|bazaar]

Print to ``stdout`` an apache httpd configuration for the given version control types (separated by spaces).

The template ``repositories/apache2_<vc_type>.conf`` is used to render the configuration. 

Common use is to export it to a directory in your project (ideally under version control) and then symbolically link it into a place where Apache httpd can find it. For example Ubuntu stores site configurations in ``/etc/init.d/apache2/sites-available`` and then symbolically links those to ``/etc/init.d/apache2/sites-enabled`` when you enable the site with the ``a2ensite`` command.

By using the symbolic link, you get the ability to version control your configuration and keep everything in one place. The commands to do this::

	./manage.py export_apache_conf subversion > conf/apache_svn.conf
	sudo ln -s `pwd`/conf/apache_svn.conf /etc/init.d/apache2/sites-available/svn
	sudo a2ensite svn


