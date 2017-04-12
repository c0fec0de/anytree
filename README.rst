.. image:: https://badge.fury.io/py/anytree.svg
    :target: https://badge.fury.io/py/anytree

.. image:: https://travis-ci.org/c0fec0de/anytree.svg?branch=master
    :target: https://travis-ci.org/c0fec0de/anytree

.. image:: https://coveralls.io/repos/github/c0fec0de/anytree/badge.svg
    :target: https://coveralls.io/github/c0fec0de/anytree

.. image:: https://readthedocs.org/projects/anytree/badge/?version=2.1.3
    :target: http://anytree.readthedocs.io/en/2.1.3/?badge=2.1.3

.. image:: https://codeclimate.com/github/c0fec0de/anytree.png
    :target: https://codeclimate.com/github/c0fec0de/anytree

Documentation
=============

The Documentation_ is hosted on http://anytree.readthedocs.io/en/2.1.3/

.. _Documentation: http://anytree.readthedocs.io/en/2.1.3/

Getting started
===============

.. _getting_started:

Usage is simple.

**Construction**

>>> from anytree import Node, RenderTree
>>> udo = Node("Udo")
>>> marc = Node("Marc", parent=udo)
>>> lian = Node("Lian", parent=marc)
>>> dan = Node("Dan", parent=udo)
>>> jet = Node("Jet", parent=dan)
>>> jan = Node("Jan", parent=dan)
>>> joe = Node("Joe", parent=dan)

**Node**

>>> print(udo)
Node('/Udo')
>>> print(joe)
Node('/Udo/Dan/Joe')

**Tree**

>>> for pre, fill, node in RenderTree(udo):
...     print("%s%s" % (pre, node.name))
Udo
├── Marc
│   └── Lian
└── Dan
    ├── Jet
    ├── Jan
    └── Joe

>>> from anytree.dotexport import RenderTreeGraph
>>> # graphviz needs to be installed for the next line!
>>> RenderTreeGraph(root).to_picture("tree.png")

.. image:: http://anytree.readthedocs.io/en/latest/_images/tree.png

**Manipulation**

A second tree:

>>> mary = Node("Mary")
>>> urs = Node("Urs", parent=mary)
>>> chris = Node("Chris", parent=mary)
>>> marta = Node("Marta", parent=mary)
>>> print(RenderTree(mary))
Node('/Mary')
├── Node('/Mary/Urs')
├── Node('/Mary/Chris')
└── Node('/Mary/Marta')

Append:

>>> udo.parent = mary
>>> print(RenderTree(mary))
Node('/Mary')
├── Node('/Mary/Urs')
├── Node('/Mary/Chris')
├── Node('/Mary/Marta')
└── Node('/Mary/Udo')
    ├── Node('/Mary/Udo/Marc')
    │   └── Node('/Mary/Udo/Marc/Lian')
    └── Node('/Mary/Udo/Dan')
        ├── Node('/Mary/Udo/Dan/Jet')
        ├── Node('/Mary/Udo/Dan/Jan')
        └── Node('/Mary/Udo/Dan/Joe')

Subtree rendering:

>>> print(RenderTree(marc))
Node('/Mary/Udo/Marc')
└── Node('/Mary/Udo/Marc/Lian')

Cut:

>>> dan.parent = None
>>> print(RenderTree(dan))
Node('/Dan')
├── Node('/Dan/Jet')
├── Node('/Dan/Jan')
└── Node('/Dan/Joe')


Installation
============

To install the `anytree` module run::

    pip install anytree

If you do not have write-permissions to the python installation, try::

    pip install anytree --user
