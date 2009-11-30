========
Metadata
========
.. module:: repositories.models

.. autoclass:: Metadata

   :data:`source_repository`
      **ForeignKey** *Required* The :class:`SourceRepository` to which this metadata is linked
   
   :data:`key`
      **CharField** *Required* The metadata key. Choices are populated from the :ref:`REPO_METADATA_KEYS` setting.
   
   :data:`value`
      **CharField** *Optional* A value to along with the key, if necessary. A key such as "License::BSD" may not need a value while "Version" would.