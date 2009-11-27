.. _goals.rst

=============
Project Goals
=============

* **Easily create version control repositories on a remote server.** We wanted an easy way to create a repository for projects as they came up. Creating a shared repository was and is a bit of a hassle. If it was too much work, people wouldn't do it.

* **Serve repositories via HTTP(S).** It should be incredibly simple to checkout or clone a repository. A single ``http://`` URL seems most universally understood and still maintains all security.

* **Allow for private repositories.** It should handle individual repositories that are meant to be for specific users.

* **Allow for publicly readable repositories.** We were about to release several projects as open source, and we wanted a way to host them ourselves. If this could serve *both* public and private repositories, we could manage all our code in one place.

* **Manage the user access for read/write via Django's admin.** Managing user access typically is a pain, so let's just do it through Django!

* **Handle multiple types of version control systems simultaneously.** Initially we were using Subversion, but we knew we or others may want to use other systems.

* **Signal when a repository has been changed.** Allow for listeners to do tasks when a repository has changed.

* **Manage remote clones of local repositories.** As we moved more toward git and away from Subversion, we wanted a way to clone our open source repositories on `GitHub <http://github.com/>`_ to utilize its social features.