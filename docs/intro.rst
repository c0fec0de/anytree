Introduction
============

Overview
--------

`anytree` is splitted into the following parts:

**Node Classes**

* :any:`Node`: a simple tree node
* :any:`NodeMixin`: extends any python class to a tree node.

**Node Resolution**

* :any:`Resolver`: retrieve node via absolute or relative path.
* :any:`Walker`: walk from one node to an other.

**Tree Iteration Strategies**

* :any:`PreOrderIter`: iterate over tree using pre-order strategy
* :any:`PostOrderIter`: iterate over tree using post-order strategy
* :any:`LevelOrderIter`: iterate over tree using level-order strategy
* :any:`LevelGroupOrderIter`: iterate over tree using level-order strategy returning group for every level

**Tree Rendering**

* :any:`RenderTree` using the following styles:
    * :any:`AsciiStyle`
    * :any:`ContStyle`
    * :any:`ContRoundStyle`
    * :any:`DoubleStyle`

Basics
------

The only tree relevant information is the `parent` attribute.
If `None` the node is root node.
If set to another node, the node becomes the child of it.

>>> udo = Node("Udo")
>>> marc = Node("Marc")
>>> lian = Node("Lian", parent=marc)
>>> print(RenderTree(udo))
Node('/Udo')
>>> print(RenderTree(marc))
Node('/Marc')
└── Node('/Marc/Lian')

Every node has an :any:`children` attribute with a tuple of all children:

>>> udo.children
()
>>> marc.children
(Node('/Marc/Lian'),)
>>> lian.children
()

**Attach**

>>> marc.parent = udo
>>> print(RenderTree(udo))
Node('/Udo')
└── Node('/Udo/Marc')
    └── Node('/Udo/Marc/Lian')

**Detach**

To make a node to a root node, just set this attribute to `None`.

>>> marc.is_root
False
>>> marc.parent = None
>>> marc.is_root
True

Detach/Attach Protocol
----------------------

A node class implementation might implement the notification slots
:any:`_pre_detach(parent)`, :any:`_post_detach(parent)`,
:any:`_pre_attach(parent)`, :any:`_post_attach(parent)`.

>>> class NotifiedNode(Node):
...     def _pre_detach(self, parent):
...         print("_pre_detach", parent)
...     def _post_detach(self, parent):
...         print("_post_detach", parent)
...     def _pre_attach(self, parent):
...         print("_pre_attach", parent)
...     def _post_attach(self, parent):
...         print("_post_attach", parent)

Notification on attach:

>>> a = NotifiedNode("a")
>>> b = NotifiedNode("b")
>>> c = NotifiedNode("c")
>>> c.parent = a
_pre_attach NotifiedNode('/a')
_post_attach NotifiedNode('/a')

Notification on change:

>>> c.parent = b
_pre_detach NotifiedNode('/a')
_post_detach NotifiedNode('/a')
_pre_attach NotifiedNode('/b')
_post_attach NotifiedNode('/b')

If the parent equals the old value, the notification is not triggered:

>>> c.parent = b

Notification on detach:

>>> c.parent = None
_pre_detach NotifiedNode('/b')
_post_detach NotifiedNode('/b')

Custom Separator
----------------

By default a slash character (`/`) separates nodes.
This separator can be overwritten:

>>> class MyNode(Node):
...     separator = "|"

>>> udo = MyNode("Udo")
>>> dan = MyNode("Dan", parent=udo)
>>> marc = MyNode("Marc", parent=udo)
>>> print(RenderTree(udo))
MyNode('|Udo')
├── MyNode('|Udo|Dan')
└── MyNode('|Udo|Marc')

The resolver takes the custom separator also into account:

>>> r = Resolver()
>>> r.glob(udo, "|Udo|*")
[MyNode('|Udo|Dan'), MyNode('|Udo|Marc')]
