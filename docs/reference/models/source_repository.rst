================
SourceRepository
================
.. module:: repositories.models

.. autoclass:: SourceRepository
   
   :data:`name`
      **SlugField** *Required* The name of the repository with only characters, numbers, underscores and dashes
   :data:`summary`
      **CharField** *Optional* A short description of what the repository contains
   :data:`description`
      **TextField** *Optional* A long description of what the repository contains
   :data:`vc_system`
      **IntegerField** *Required* The type of version control system used. Changing this value after initial creation does nothing.
   :data:`repo_template`
      **CharField** *Optional* Primarily used for Subversion repositories, it will populate the repository with a directory structure in the ``repo-templates`` directory.
   :data:`repo_path`
      **CharField** *Non-editable* The absolute path to the repository on the file system.
   :data:`repo_url`
      **CharField** *Non-editable* The URL to this repository, not including the domain.
   :data:`current_rev`
      **CharField** *Non-editable* The last known revision of this repository, populated by the :ref:`repo_check_for_updates` management command.
   :data:`previous_rev`
      **CharField** *Non-editable* The previously known revision of this repository populated by the :ref:`repo_check_for_updates` management command. The interval between this field and ``current_rev`` will depend on how often the management command is run and commit frequency.

   .. cssclass:: method-group
   
   Default methods
      .. automethod:: __init__
      
      .. automethod:: save
      
      .. automethod:: delete

   .. cssclass:: method-group
   
   User Permision methods
      .. automethod:: owners
      
      .. automethod:: members
      
      .. automethod:: user_is_owner
      
      .. automethod:: user_can_write
      
      .. automethod:: user_can_read
      
      .. automethod:: members

   .. cssclass:: method-group

   Utility methods
      .. automethod:: move_to_public
      
      .. automethod:: move_to_private

