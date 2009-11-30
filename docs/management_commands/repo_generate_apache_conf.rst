.. _management_commands__export_apache_conf.rst:

.. _repo_generate_apache_conf:

=============================
``repo_generate_apache_conf``
=============================

Print to ``stdout`` an apache httpd configuration for all the configured version control types.

Called as::

	./manage.py repo_generate_apache_conf

The template ``repositories/apache2_auth.conf`` is used once to render the authentication settings and then ``repositories/apache2_<vc_type>.conf`` is used for each configured version control system to render its configuration. 

Common use is to export it to a directory in your project (ideally under version control) and then symbolically link it into a place where Apache httpd can find it. For example Ubuntu stores site configurations in ``/etc/init.d/apache2/sites-available`` and then symbolically links those to ``/etc/init.d/apache2/sites-enabled`` when you enable the site with the ``a2ensite`` command.

By using the symbolic link, you get the ability to version control your configuration and keep everything in one place. The commands to do this::

	./manage.py export_apache_conf > conf/apache_vcs.conf
	sudo ln -s `pwd`/conf/apache_vcs.conf /etc/init.d/apache2/sites-available/vcs
	sudo a2ensite vcs


