Introduction
============

Overview
--------

`anytree` is split into the following parts:

**Node Classes**

* :any:`Node`: a simple tree node with at least a name attribute and any number of additional attributes.
* :any:`AnyNode`: a generic tree node and any number of additional attributes.
* :any:`NodeMixin`: extends any python class to a tree node.

**Node Resolution**

* :any:`Resolver`: retrieve node via absolute or relative path.
* :any:`Walker`: walk from one node to an other.

**Tree Iteration Strategies**

* :any:`PreOrderIter`: iterate over tree using pre-order strategy
* :any:`PostOrderIter`: iterate over tree using post-order strategy
* :any:`LevelOrderIter`: iterate over tree using level-order strategy
* :any:`LevelOrderGroupIter`: iterate over tree using level-order strategy returning group for every level
* :any:`ZigZagGroupIter`: iterate over tree using level-order strategy returning group for every level

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

>>> from anytree import Node, RenderTree
>>> udo = Node("Udo")
>>> marc = Node("Marc")
>>> lian = Node("Lian", parent=marc)
>>> print(RenderTree(udo))
Node('/Udo')
>>> print(RenderTree(marc))
Node('/Marc')
└── Node('/Marc/Lian')

Every node has a :any:`children` attribute with a tuple of all children:

>>> udo.children
()
>>> marc.children
(Node('/Marc/Lian'),)
>>> lian.children
()

**Add: Single Node Attach**

Just set the parent attribute and the node becomes a child node:

>>> marc.parent = udo
>>> print(RenderTree(udo))
Node('/Udo')
└── Node('/Udo/Marc')
    └── Node('/Udo/Marc/Lian')

**Delete: Single Node Detach**

A node becomes a root node, if you set the parent attribute to `None`:

>>> lian.is_root
False
>>> lian.parent = None
>>> lian.is_root
True

The node is deleted from the tree:

>>> print(RenderTree(udo))
Node('/Udo')
└── Node('/Udo/Marc')

**Modify Multiple Child Nodes**

Assume the following tree:

>>> n = Node("n")
>>> a = Node("a", parent=n)
>>> b = Node("b", parent=n)
>>> c = Node("c", parent=n)
>>> d = Node("d")
>>> n.children
(Node('/n/a'), Node('/n/b'), Node('/n/c'))

Modifying the children attribute modifies multiple child nodes.
It can be set to any iterable.

>>> n.children = [a, b]
>>> n.children
(Node('/n/a'), Node('/n/b'))

Node `c` is removed from the tree.
In case of an existing reference, the node `c` does not vanish and is the root of its own tree.

>>> c
Node('/c')

Adding works likewise.

>>> d
Node('/d')
>>> n.children = [a, b, d]
>>> n.children
(Node('/n/a'), Node('/n/b'), Node('/n/d'))
>>> d
Node('/n/d')


Detach/Attach Protocol
----------------------

A node class implementation might implement the notification slots
``_pre_detach(parent)``, ``_post_detach(parent)``,
``_pre_attach(parent)``, ``_post_attach(parent)``.

These methods are *protected* methods,
intended to be overwritten by child classes of :any:`NodeMixin`/:any:`Node`.
They are called on modifications of a nodes `parent` attribute.
Never call them directly from API.
This will corrupt the logic behind these methods.

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


.. important::
    An exception raised by ``_pre_detach(parent)`` and ``_pre_attach(parent)`` will **prevent** the tree structure to be updated.
    The node keeps the old state.
    An exception raised by ``_post_detach(parent)`` and ``_post_attach(parent)`` does **not rollback** the tree structure modification.


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

>>> from anytree import Resolver
>>> r = Resolver()
>>> r.glob(udo, "|Udo|*")
[MyNode('|Udo|Dan'), MyNode('|Udo|Marc')]
