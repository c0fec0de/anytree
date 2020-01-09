Multidimensional Trees
======================

**Application**: Tree nodes should be hooked-up in multiple trees.

An anytree node is only able to be part of **one** tree, not multiple.
The following example shows how to handle this.

**Example**: 4 objects `A`, `B`, `C` and `D` shall be part of the
trees `X` and `Y`.

The objects `A`, `B`, `C` and `D` are instances of a class `Item`.
It is *not* a tree node. It just contains references `x` and `y` to the node
representations in the corresponding trees.

>>> class Item:
...     def __init__(self, name):
...         self.name = name
...         self.x = None
...         self.y = None
...     def __repr__(self):
...         return "Item(%r)" % self.name
>>> a = Item('A')
>>> b = Item('B')
>>> c = Item('C')
>>> d = Item('D')

The tree nodes just contain the reference to `item` and take care of the
proper reference, by using the attach/detach protocol.

>>> from anytree import NodeMixin, RenderTree
>>> class NodeX(NodeMixin):
...     def __init__(self, item, parent=None):
...         self.item = item
...         self.parent = parent
...     def _pre_detach(self, parent):
...         self.item.x = None
...     def _pre_attach(self, parent):
...         self.item.x = self
>>> class NodeY(NodeMixin):
...     def __init__(self, item, parent=None):
...         self.item = item
...         self.parent = parent
...     def _pre_detach(self, parent):
...         self.item.y = None
...     def _pre_attach(self, parent):
...         self.item.y = self

Tree generation is simple:

>>> # X
>>> xa = NodeX(a)
>>> xb = NodeX(b, parent=xa)
>>> xc = NodeX(c, parent=xa)
>>> xd = NodeX(d, parent=xc)
>>> # Y
>>> yd = NodeY(d)
>>> yc = NodeY(c, parent=yd)
>>> yb = NodeY(b, parent=yd)
>>> ya = NodeY(a, parent=yb)

All tree functions as rendering and exporting can be used as usual:

>>> for row in RenderTree(xa):
...     print("%s%s" % (row.pre, row.node.item))
Item('A')
├── Item('B')
└── Item('C')
    └── Item('D')

>>> for row in RenderTree(yd):
...     print("%s%s" % (row.pre, row.node.item))
Item('D')
├── Item('C')
└── Item('B')
    └── Item('A')
