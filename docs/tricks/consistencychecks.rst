Consistency Checks vs. Speed
============================

Anytree can run some *costly* internal consistency checks.
With version 2.9.1 these got disabled by default.
In case of any concerns about the internal data consistency or just for safety, either

* set the environment variable ``ANYTREE_ASSERTIONS=1``, or
* add the following lines to your code:

>>> import anytree
>>> anytree.config.ASSERTIONS = True
