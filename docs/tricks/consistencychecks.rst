Consistency Checks vs. Speed
============================

Anytree can run some *costly* internal consistency checks.
With version 2.9.1 these got disabled by default.
To enable these checks, set the environment variable ``ANYTREE_ASSERTIONS=1``
before importing ``anytree`` for the first time. For example, in a POSIX shell:

.. code-block:: console

    $ ANYTREE_ASSERTIONS=1 python your_script.py

Alternatively, set the environment variable at the start of your Python program,
before importing ``anytree`` or any other module that imports it:

.. code-block:: python

    import os

    os.environ["ANYTREE_ASSERTIONS"] = "1"

    import anytree

The assertion setting is read during import. Changing
``anytree.config.ASSERTIONS`` or the environment variable after importing
``anytree`` does not enable checks in modules that have already been imported.
