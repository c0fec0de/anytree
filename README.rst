***************
Getting started
***************

.. _getting_started:

Usage is simple.

Construction
~~~~~~~~~~~~

>>> from anytree import Node, RenderTree
>>> udo = Node("Udo")
>>> marc = Node("Marc", parent=udo)
>>> lian = Node("Lian", parent=marc)
>>> dan = Node("Dan", parent=udo)
>>> jet = Node("Jet", parent=dan)
>>> jan = Node("Jan", parent=dan)
>>> joe = Node("Joe", parent=dan)

Node
~~~~

>>> print(udo)
Node('Udo')
>>> print(joe)
Node('Udo/Dan/Joe')

Tree
~~~~

>>> for pre, node in RenderTree(udo):
...     print("%s%s" % (pre, node.name))
Udo
├── Marc
│   └── Lian
└── Dan
    ├── Jet
    ├── Jan
    └── Joe

Manipulation
~~~~~~~~~~~~

A second tree:

>>> mary = Node("Mary")
>>> urs = Node("Urs", parent=mary)
>>> chris = Node("Chris", parent=mary)
>>> marta = Node("Marta", parent=mary)
>>> print(RenderTree(mary))
Node('Mary')
├── Node('Mary/Urs')
├── Node('Mary/Chris')
└── Node('Mary/Marta')

Append:

>>> udo.parent = mary
>>> print(RenderTree(mary))
Node('Mary')
├── Node('Mary/Urs')
├── Node('Mary/Chris')
├── Node('Mary/Marta')
└── Node('Mary/Udo')
    ├── Node('Mary/Udo/Marc')
    │   └── Node('Mary/Udo/Marc/Lian')
    └── Node('Mary/Udo/Dan')
        ├── Node('Mary/Udo/Dan/Jet')
        ├── Node('Mary/Udo/Dan/Jan')
        └── Node('Mary/Udo/Dan/Joe')

Subtree rendering:

>>> print(RenderTree(marc))
Node('Mary/Udo/Marc')
└── Node('Mary/Udo/Marc/Lian')

Cut:

>>> dan.parent = None
>>> print(RenderTree(dan))
Node('Dan')
├── Node('Dan/Jet')
├── Node('Dan/Jan')
└── Node('Dan/Joe')

.. _Tree: https://en.wikipedia.org/wiki/Tree_(data_structure)

************
Installation
************

To install the `anytree` module run:

    pip install anytree

If you do not have write-permissions to the python installation, try:

    pip install anytree --user
