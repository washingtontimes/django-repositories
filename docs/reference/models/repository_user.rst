===============
RepositoryUser
===============
.. module:: repositories.models

.. autoclass:: RepositoryUser

   :data:`source_repository`
      **ForeignKey** *Required* The :class:`SourceRepository` to which this user is linked
   
   :data:`user`
      **ForeignKey** *Required* The :class:`django.contrib.auth.models.User` to which this source repository is linked
   
   :data:`permission`
      **IntegerField** *Required* One of ``PERM_CHOICES`` giving this user read, read/write, or ownership privileges on this source repository.