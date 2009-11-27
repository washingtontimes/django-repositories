.. _settings.rst:

.. _settings:

========
Settings
========


.. _repo_vcs_config:

``REPO_VCS_CONFIG``
===================

A dictionary containing the basic configuration of available version control systems. It is in the format ``id: { parameters }`` where ``id`` is a number.

The parameters are:

name
   Name of the version control system, e.g. Subversion.

command
   The shell command to execute the required version control commands, e.g. ``svn``. This can be a full path if the executable is not on the default path.

public_path
   The place on the filesystem to store publicly readable repositories. The path defaults to the ``BASE_REPO_PATH`` setting plus the repository type plus ``public``, e.g. ``/var/code/repositories/svn/public/`` or ``/var/code/repositories/git/public/``.

private_path
   The place on the filesystem to store private repositories. The path defaults to the ``BASE_REPO_PATH`` setting plus the repository type plus ``private``, e.g. ``/var/code/repositories/svn/private/`` or ``/var/code/repositories/git/private/``.

public_url
   The url path to access publicly readable repositories. It defaults to the repository type plus ``public``, e.g. ``/svn/public/`` or ``/git/public``.

private_url
   The url path to access private repositories. It defaults to the repository type plus ``private``, e.g. ``/svn/private/`` or ``/git/private/``.

config_dir
    For Subversion, pass this with the ``--config-dir`` option to have Subversion read user configuration files from this specific directory.

The default configuration for is::

	{
	    1:{ 'name':'Subversion',
	        'command': 'svn',
	        'public_path': os.path.join(BASE_REPO_PATH, 'svn', 'public'),
	        'private_path': os.path.join(BASE_REPO_PATH, 'svn', 'private'),
	        'public_url': '/svn/public/',
	        'private_url': '/svn/private/',
	        'config_dir': None, },
	    2:{ 'name': 'Bazaar',
	        'command': 'bzr',
	        'public_path': os.path.join(BASE_REPO_PATH, 'bzr', 'public'),
	        'private_path': os.path.join(BASE_REPO_PATH, 'bzr', 'private'),
	        'public_url': '/bzr/public/',
	        'private_url': '/bzr/private/', },
	    3:{ 'name': 'Git',
	        'command': 'git',
	        'public_path': os.path.join(BASE_REPO_PATH, 'git', 'public'),
	        'private_path': os.path.join(BASE_REPO_PATH, 'git', 'private'),
	        'public_url': '/git/public/',
	        'private_url': '/git/private/', },
	    4:{ 'name': 'Mercurial',
	        'command': 'hg',
	        'public_path': os.path.join(BASE_REPO_PATH, 'hg', 'public'),
	        'private_path': os.path.join(BASE_REPO_PATH, 'hg', 'private'),
	        'public_url': '/hg/public/',
	        'private_url': '/hg/private/', },
	}


.. _repo_base_repo_path:

``REPO_BASE_REPO_PATH``
=======================

If the default configuration for the version control systems works for you, you can just configure the base path which contains all the repositories. By default, it is a directory named ``repositories`` within the application directory.

If you set ``REPO_BASE_REPO_PATH = '/var/code/repositories/``, for example, it would store repositories in the following way::

	+var
	+--code
	+----repositories
	+------bzr
	+--------public
	+--------private
	+------git
	+--------public
	+--------private
	+------hg
	+--------public
	+--------private
	+------svn
	+--------public
	+--------private


.. _repo_metadata_keys:

``REPO_METADATA_KEYS``
======================

The :class:`SourceRepository` model supports adding metadata to repositories. ``REPO_METADATA_KEYS`` is a list of strings that a user can select and optionally enter a corresponding value.

``Version`` will always be added if the list doesn't contain it.


.. _repo_url_pattern:

``REPO_URL_PATTERN``
====================

For authentication and authorization purposes, the script requires the name of the repository the user is attempting to access. It gets this from the url. ``REPO_URL_PATTERN`` is a regular expression that contains ``(?P<repo_name>\w+)`` somewhere in it to retrieve the repository name.

The default is: ``'^/\w+/\w+/(?P<repo_name>\w+)/'`` which allows for the default URLs like ``/svn/public/myrepo/`` and ``/git/private/repo2.git/``
