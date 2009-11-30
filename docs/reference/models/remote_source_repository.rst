======================
RemoteSourceRepository
======================

.. module:: repositories.models

.. autoclass:: RemoteSourceRepository

   :data:`repo`
      **ForeignKey** *Required* The :class:`SourceRepository` to which this metadata is linked
   
   :data:`name`
      **SlugField** *Required* A name to refer to this remote repository. Must contain letters, numbers, underscores or dashes only.
   
   :data:`branch`
      **CharField** *Required* The name of the branch to which this remote repository is linked.
   
   :data:`url`
      **CharField** *Required* The URL to the remote repository.
   
   :data:`notes`
      **TextField** *Optional* Any notes about this remote repository
   
   :data:`active`
      **BooleanField** *Required* Indicates that this remote repository should receive updates.

