.. _management_commands__repo_generate_auth.rst:

.. _repo_generate_auth:

======================
``repo_generate_auth``
======================

Prints to ``stdout`` the authentication script, rendered from the  ``repositories/auth.wsgi`` template.

Called as::

	./manage.py repo_generate_auth [/path/to/project/]

or::

	./manage.py repo_generate_auth [key=val] [key=val]

If there is only one argument, the command assumes that you are calling it with the path to the project. However, if you want to override the template and add additional variables, you can call it with the second option. Each ``key=val`` pair is split and passed to the template context.

Assuming that you are calling the ``manage.py`` script from the project directory, you can call it as::

	./manage.py repo_generate_auth `pwd`

To save the file automatically as ``auth.wsgi`` in the ``conf`` directory::

	./manage.py repo_generate_auth `pwd` > conf/auth.wsgi

This management command renders the template ``repositories/auth.wsgi``. Your project can override this if you require additional settings and .