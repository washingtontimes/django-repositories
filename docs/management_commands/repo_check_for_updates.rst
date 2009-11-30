.. _repo_check_for_updates.rst:

.. _repo_check_for_updates:

==========================
``repo_check_for_updates``
==========================

Loops through all repositories for a change in the known revision. Sends up a :ref:`repository_changed` signal. Designed to be used in a cron job for periodic checking.

Many Linux distributions have a ``cron`` directory for generic ``crontab``\ s like ``/etc/cron.d/``\ . You could create a file named ``repo_check`` with the following contents to check every 5 minutes::

	# projectmgr crontab to execute regular checks for repository changes
	# This should run as the web process user

	# m h dom mon dow user      command
	*/5 *  *   *   *  www-data  python /var/code/myproject/manage.py repo_check_for_updates > /dev/null

.. note:: **Why not just use repository hooks?**
   
   Some version control systems, like git, don't support hooks over http.