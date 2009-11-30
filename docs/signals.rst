.. _signals.rst:

=======
Signals
=======

.. _repository_changed:

``repository_changed``
======================

Arguments Provided

``current_rev``
   The latest revision found

``previous_rev``
   The previous revision it knew about. The interval between ``current_rev`` and ``previous_rev`` depends on how often the :ref:`repo_check_for_updates` management command is run.