===============
RepositoryGroup
===============
.. module:: repositories.models

.. autoclass:: RepositoryGroup

   :data:`source_repository`
      **ForeignKey** *Required* The :class:`SourceRepository` to which this group is linked
   
   :data:`group`
      **ForeignKey** *Required* The :class:`django.contrib.auth.models.Group` to which this source repository is linked
   
   :data:`permission`
      **IntegerField** *Required* One of ``PERM_CHOICES`` giving every user in this group read, read/write, or ownership privileges on this source repository.